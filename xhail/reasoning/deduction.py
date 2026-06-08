import logging
import platform
import signal
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
        # D6 fix: deduction previously hung indefinitely on certain inputs.
        # Wrap with a SIGALRM timeout on Unix/macOS; no-op on Windows.
        use_timeout = (
            self.TIMEOUT > 0
            and platform.system() != 'Windows'
            and hasattr(signal, 'SIGALRM')
        )
        if use_timeout:
            def _handle_timeout(signum, frame):
                raise DeductionTimeoutError(
                    f"Deduction phase exceeded the {self.TIMEOUT}s time limit. "
                    "Try reducing --depth or simplifying the input program."
                )
            old_handler = signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(self.TIMEOUT)
        try:
            self._runPhase()
        finally:
            if use_timeout:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)

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
