import logging
import threading
from dataclasses import dataclass, field
from typing import Optional, Set

from ..language.terms import Atom, Clause, Literal, PlaceMarker

logger = logging.getLogger(__name__)


@dataclass
class DeductionNode:
    """One node in the BFS deduction search.

    Attributes:
        fact: The ground atom matched at this level.
        priority_terms: Terms that still need to be explained (input ``+`` terms).
        all_terms: All terms seen so far (inputs + introduced outputs).
        previous: The parent node's fact (None at level 0).
    """
    fact: Atom
    priority_terms: Set[str]
    all_terms: Set[str]
    previous: Optional[Atom]


class DeductionTimeoutError(RuntimeError):
    """Raised when the deduction phase exceeds the configured time limit."""
    pass


class Deduction:
    # D6: configurable timeout in seconds for the deduction phase.
    # Uses SIGALRM (Unix/macOS only). Set to 0 to disable.
    TIMEOUT = 60

    def __init__(self, model):
        self.MH = model.MH
        self.MB = model.MB
        self.BG = model.BG
        self.DEPTH = model.DEPTH
        self.model = model

    # ---------- get marker terms given specific marker (+/-) ---------- #
    def getMarkerTerms(self, atom, mode, marker):
        n = set()
        for term1, term2 in zip(atom.terms, mode.terms):
            if isinstance(term2, Atom):
                n.update(self.getMarkerTerms(term1, term2, marker))
            elif isinstance(term2, PlaceMarker) and term2.marker == marker:
                n.add(term1.value)
            else:
                continue
        return n

    def extractTerms(self, schemas, facts, priorityTerms, allTerms, previous, mode):
        level: list[DeductionNode] = []
        for schema in schemas:
            for fact in facts:
                factPriorityTerms = priorityTerms.copy()
                factAllTerms = allTerms.copy()
                if str(fact) != str(previous) and self.model.isSubsumed(fact, schema):
                    if mode == 'head':
                        factPriorityTerms = self.getMarkerTerms(fact, schema, '+')
                        factAllTerms = factPriorityTerms
                    elif mode == 'body':
                        factPositiveTerms = self.getMarkerTerms(fact, schema, '+')
                        if factPositiveTerms.issubset(factAllTerms):
                            # D9 fix: .difference() returns a new set and was never assigned.
                            # Changed to .difference_update() which mutates in place.
                            factPriorityTerms.difference_update(factPositiveTerms)
                            factPositiveTerms.difference_update(factPriorityTerms)
                            factPositiveTerms.difference_update(factAllTerms)
                            factPriorityTerms.update(self.getMarkerTerms(fact, schema, '-'))
                            factAllTerms.update(factPriorityTerms)
                        else:
                            continue
                    else:
                        continue
                    level.append(DeductionNode(fact, factPriorityTerms, factAllTerms, previous))
        return level

    def findNext(self, atomToFind, levels, idl):
        if atomToFind is None:
            return []
        if idl < 0:
            raise RuntimeError(
                f"Deduction chain broken: exhausted all levels searching for '{atomToFind}'. "
                "This indicates a bug in the deduction search."
            )
        for node in levels[idl]:
            if str(node.fact) == str(atomToFind):
                chain = self.findNext(node.previous, levels, idl - 1)
                chain.append(node.fact)
                return chain
        raise RuntimeError(
            f"Deduction chain broken: could not find atom '{atomToFind}' "
            f"in levels[{idl}]. This indicates a bug in the deduction search."
        )






    def runPhase(self):
        """Run deduction with an optional wall-clock timeout.

        Uses a daemon thread + ``Thread.join(timeout)`` so this is safe to call
        from any thread (including FastAPI / uvicorn worker threads).  The old
        ``signal.SIGALRM`` approach raised ``ValueError`` when called outside the
        main interpreter thread.
        """
        if self.TIMEOUT <= 0:
            self._runPhase()
            return

        exc_holder: list[BaseException] = []

        def _target() -> None:
            try:
                self._runPhase()
            except Exception as exc:  # noqa: BLE001
                exc_holder.append(exc)

        thread = threading.Thread(target=_target, daemon=True)
        thread.start()
        thread.join(timeout=self.TIMEOUT)

        if thread.is_alive():
            # Thread is still running — the call exceeded the time limit.
            # The daemon thread will be reaped when the process exits.
            raise DeductionTimeoutError(
                f"Deduction phase exceeded the {self.TIMEOUT}s time limit. "
                "Try reducing --depth or simplifying the input program."
            )

        if exc_holder:
            raise exc_holder[0]

    def _runPhase(self):
        head_atoms = [mh.atom for mh in self.MH]
        body_atoms = [mb.atom for mb in self.MB if not mb.negation]
        negated_bodies = [Atom(f'not_{mb.atom.predicate}', mb.atom.terms) for mb in self.MB if mb.negation]
        body_atoms += negated_bodies
        conditions = head_atoms + body_atoms
        matches = self.model.getMatches(conditions)

        levels: list[list[DeductionNode]] = []
        levels.append(self.extractTerms(head_atoms, matches, set(), set(), None, 'head'))

        for d in range(1, self.DEPTH + 1):
            current_level: list[DeductionNode] = []
            for node in levels[d - 1]:
                if node.priority_terms is None:
                    continue
                results = self.extractTerms(
                    body_atoms, matches,
                    node.priority_terms, node.all_terms,
                    node.fact, 'body',
                )
                current_level.extend(results)
            if not current_level:
                break
            levels.append(current_level)

        top = len(levels) - 1

        if top == 0 and not levels[0]:
            logger.warning(
                "Deduction produced an empty kernel: no facts in the abduced model "
                "matched the mode declarations. Check that #modeh/#modeb schemas "
                "align with your background predicates, or try increasing --depth."
            )

        clauses = []
        for node in levels[top]:
            chain = self.findNext(node.previous, levels, top - 1)
            chain.append(node.fact)
            clauses.append(Clause(
                chain[0],
                [
                    Literal(Atom(atom.predicate[4:], atom.terms), True)
                    if atom.predicate[:4] == "not_"
                    else Literal(atom, False)
                    for atom in chain[1:]
                ],
            ))

        self.model.setKernel(clauses)
