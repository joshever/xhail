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
        ancestors: frozenset of string keys for every atom on the path from the
            BFS root to this node (inclusive).  Used for O(1) cycle detection.
            Full ancestor tracking (not just the immediate parent) prevents
            A→B→A cycles and keeps the BFS search tree bounded to the number
            of unique atoms available per chain — far smaller than the
            exponential growth produced by the old immediate-parent-only check.
        parent_node: Direct pointer to the parent ``DeductionNode`` (or None
            at level 0).  Enables exact O(depth) chain reconstruction via
            ``_reconstruct_chain``, replacing the old ``findNext`` level-walk
            which could pick the wrong parent when the same atom appeared at the
            same depth in multiple chains.
    """

    fact: Atom
    priority_terms: Set[str]
    all_terms: Set[str]
    ancestors: frozenset = field(default_factory=frozenset)
    parent_node: Optional["DeductionNode"] = field(default=None)


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
                # term1 may be a Normal (ground constant) or a compound Atom
                # (e.g. available(glucose) filling a +fluent slot).  Use .value
                # for Normal, str() for compound atoms.
                from ..language.terms import Normal as _Normal  # local to avoid circular

                n.add(term1.value if isinstance(term1, _Normal) else str(term1))
            else:
                continue
        return n

    @staticmethod
    def _reconstruct_chain(node: "DeductionNode") -> list:
        """Walk parent_node pointers back to the root and return the atom chain.

        Returns a list [head_atom, body_atom_1, ..., body_atom_k] in root-first
        order.  This is O(depth) and uses no extra memory beyond the pointer
        chain already stored in the nodes.
        """
        chain: list = []
        current: Optional["DeductionNode"] = node
        while current is not None:
            chain.append(current.fact)
            current = current.parent_node
        chain.reverse()
        return chain

    def extractTerms(
        self,
        schemas,
        facts,
        priorityTerms,
        allTerms,
        mode,
        ancestors: frozenset = frozenset(),
        parent_node: Optional["DeductionNode"] = None,
        *,
        fact_index: dict | None = None,
    ):
        """Match ground facts against mode schemas and return new BFS nodes.

        ``ancestors`` is the frozenset of string keys for every atom on the
        path from the BFS root to the current node (inclusive of the parent).
        Full ancestor tracking prevents *any* atom from appearing twice on a
        single chain (not just the immediate parent), which bounds BFS growth
        to the number of unique matching atoms rather than allowing exponential
        oscillation (A→B→A→B→…).

        ``parent_node`` is the parent ``DeductionNode`` (or None at level 0).
        Storing a direct pointer enables exact O(depth) chain reconstruction via
        ``_reconstruct_chain``, avoiding the ambiguity of the old ``findNext``
        level-walk (where the same atom at the same depth in different chains
        could yield the wrong reconstruction).

        ``fact_index`` is an optional ``{predicate: [Atom, ...]}`` dict built
        once per phase in ``_runPhase``.  When present each schema only
        considers the facts whose predicate matches, cutting the inner loop from
        O(|schemas| × |facts|) to O(|schemas| × |facts_with_matching_predicate|).
        """
        level: list[DeductionNode] = []
        for schema in schemas:
            # Use predicate index when available — avoids scanning all facts for
            # every schema, which dominates runtime on grandfather/trains where
            # >100 facts exist but only a handful share each predicate.
            candidate_facts: list = (
                fact_index.get(schema.predicate, []) if fact_index is not None else list(facts)
            )
            for fact in candidate_facts:
                fact_key = str(fact)
                # Full ancestor cycle guard: prevent any atom from appearing
                # twice on the same chain.  This keeps BFS polynomial — trains
                # has ~5 unique matching atoms per head, so chains terminate
                # after at most 5 levels rather than oscillating exponentially.
                if fact_key in ancestors:
                    continue
                factPriorityTerms = priorityTerms.copy()
                factAllTerms = allTerms.copy()
                if self.model.isSubsumed(fact, schema):
                    if mode == "head":
                        factPriorityTerms = self.getMarkerTerms(fact, schema, "+")
                        factAllTerms = factPriorityTerms.copy()
                    elif mode == "body":
                        factPositiveTerms = self.getMarkerTerms(fact, schema, "+")
                        if factPositiveTerms.issubset(factAllTerms):
                            factPriorityTerms.difference_update(factPositiveTerms)
                            factPositiveTerms.difference_update(factPriorityTerms)
                            factPositiveTerms.difference_update(factAllTerms)
                            factPriorityTerms.update(self.getMarkerTerms(fact, schema, "-"))
                            factAllTerms.update(factPriorityTerms)
                        else:
                            continue
                    else:
                        continue
                    child_ancestors = ancestors | {fact_key}
                    level.append(
                        DeductionNode(
                            fact, factPriorityTerms, factAllTerms, child_ancestors, parent_node
                        )
                    )
        return level

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

    # BFS node budget: stop expanding when the total number of BFS nodes across
    # all levels exceeds this value.  Because the induction phase truncates the
    # abstract kernel to _MAX_KERNEL_DEFAULT (50) clauses anyway, there is no
    # benefit in generating thousands of nodes — the short clauses from the
    # first few BFS levels already provide enough diversity for induction to find
    # the minimal hypothesis.  This keeps deduction O(budget) regardless of depth.
    # Override with the XHAIL_MAX_BFS_NODES environment variable.
    import os as _os

    MAX_BFS_NODES: int = int(_os.environ.get("XHAIL_MAX_BFS_NODES", "1000"))

    def _runPhase(self):
        import os as _os

        max_nodes = int(_os.environ.get("XHAIL_MAX_BFS_NODES", str(self.MAX_BFS_NODES)))

        head_atoms = [mh.atom for mh in self.MH]
        body_atoms = [mb.atom for mb in self.MB if not mb.negation]
        negated_bodies = [
            Atom(f"not_{mb.atom.predicate}", mb.atom.terms) for mb in self.MB if mb.negation
        ]
        body_atoms += negated_bodies
        conditions = head_atoms + body_atoms
        matches = self.model.getMatches(conditions)

        # Build a predicate → [Atom] index so extractTerms can skip facts
        # that can't possibly match a schema — O(|facts|) build, then each
        # BFS call costs O(|schemas| × |facts_with_matching_predicate|)
        # instead of O(|schemas| × |all_facts|).  On grandfather (20+ parents,
        # 5+ grandparents, 2 target examples) and trains (100+ car facts) this
        # cuts the BFS cross-join by ~10×.
        fact_index: dict[str, list] = {}
        for atom in matches:
            fact_index.setdefault(atom.predicate, []).append(atom)
        logger.debug(
            "Fact index: %d predicate bucket(s) over %d total facts.",
            len(fact_index),
            len(matches),
        )

        levels: list[list[DeductionNode]] = []
        # Level 0: head atoms.  Empty ancestor set — no atoms seen yet.
        head_nodes = self.extractTerms(
            head_atoms, matches, set(), set(), "head", frozenset(), None, fact_index=fact_index
        )
        levels.append(head_nodes)
        total_nodes = len(head_nodes)

        # Track which nodes have at least one child so we can identify leaves.
        # A leaf is any non-level-0 node that generated no children — either
        # because the ancestor set blocked all further extensions, or because
        # the depth/budget limit was reached.  Collecting from leaves (rather
        # than only from levels[top]) ensures chains that terminate early are
        # included in the kernel alongside deeper chains from other head atoms.
        # Example: epidemic's "infect(bob)" rule has depth-1 chain (only
        # alice is ill at T=1) while "infect(carol)" extends to depth-2 —
        # levels[top]-only collection missed the bob rule entirely.
        has_children: set[int] = set()

        for d in range(1, self.DEPTH + 1):
            if total_nodes >= max_nodes:
                logger.debug(
                    "BFS node budget (%d) reached at depth %d — stopping expansion.",
                    max_nodes,
                    d,
                )
                break
            current_level: list[DeductionNode] = []
            for node in levels[d - 1]:
                if node.priority_terms is None:
                    continue
                # NOTE: we do NOT stop when priority_terms is empty.
                # The induction phase selects a *subset* of body literals from
                # each kernel clause, so the kernel should be as deep (specific)
                # as possible.  Stopping early would prevent multi-constraint
                # rules (e.g. trains needs has_car + short + triangle_load).
                results = self.extractTerms(
                    body_atoms,
                    matches,
                    node.priority_terms,
                    node.all_terms,
                    "body",
                    node.ancestors,  # full ancestor set for cycle prevention
                    node,  # parent_node pointer for reconstruction
                    fact_index=fact_index,
                )
                if results:
                    has_children.add(id(node))
                current_level.extend(results)
            if not current_level:
                break
            levels.append(current_level)
            total_nodes += len(current_level)

        if not any(levels):
            logger.warning(
                "Deduction produced an empty kernel: no facts in the abduced model "
                "matched the mode declarations. Check that #modeh/#modeb schemas "
                "align with your background predicates, or try increasing --depth."
            )

        # Collect kernel clauses from BFS leaf nodes — nodes at level >= 1
        # that generated no children.  This captures:
        #   • Chains that exhaust all valid body extensions early (short rules).
        #   • Chains stopped by the depth/budget limit (long, specific rules).
        # Induction then selects the *minimal* subset of body literals per clause,
        # so deeper clauses naturally subsume shorter ones — we lose nothing by
        # including both.  The key invariant: every abduced head atom contributes
        # at least one kernel clause (its deepest reachable chain), rather than
        # being silently dropped when another head atom's chain happens to be deeper.
        seen_clauses: set[str] = set()
        clauses = []
        for level_idx, level in enumerate(levels):
            if level_idx == 0:
                # Skip level-0 head-only nodes — zero-body clauses are facts,
                # not learnable rules.  (If no body atoms match a head at all,
                # we legitimately have nothing to learn for it.)
                continue
            for node in level:
                if id(node) in has_children:
                    continue  # interior node — its leaf descendants are deeper
                chain = self._reconstruct_chain(node)  # [head, body_1, ..., body_k]
                clause = Clause(
                    chain[0],
                    [
                        Literal(Atom(atom.predicate[4:], atom.terms), True)
                        if atom.predicate[:4] == "not_"
                        else Literal(atom, False)
                        for atom in chain[1:]
                    ],
                )
                key = str(clause)
                if key not in seen_clauses:
                    seen_clauses.add(key)
                    clauses.append(clause)

        logger.debug("Deduction produced %d kernel clause(s) from leaf nodes.", len(clauses))
        self.model.setKernel(clauses)
