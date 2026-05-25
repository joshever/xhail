"""
xhail.core — public learning API
=================================

The primary entry point for running XHAIL programmatically.  The
:func:`learn` function drives the three-phase pipeline (abduction →
deduction → induction) and returns a :class:`LearningResult` containing
the learned hypothesis.

Example::

    from xhail import learn

    result = learn("penguins.lp", depth=10)
    if result.success:
        for rule in result.hypothesis:
            print(rule)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union

from .parser.parser import Parser
from .reasoning.abduction import Abduction
from .reasoning.deduction import Deduction
from .reasoning.induction import Induction
from .reasoning.model import Model

logger = logging.getLogger(__name__)


@dataclass
class LearningResult:
    """The output of a XHAIL learning run.

    Attributes:
        hypothesis: The learned rules as formatted strings.
        success: True if at least one rule was learned.
        source: The file or string that was used as input (for reference).
        n_examples: Number of examples supplied to the learner.
        n_background: Number of background clauses supplied.
    """

    hypothesis: list[str] = field(default_factory=list)
    success: bool = False
    source: Optional[str] = None
    n_examples: int = 0
    n_background: int = 0

    def __str__(self) -> str:
        if not self.success:
            return "No hypothesis found."
        return "\n".join(self.hypothesis)

    def __repr__(self) -> str:
        return (
            f"LearningResult(success={self.success}, "
            f"n_rules={len(self.hypothesis)}, source={self.source!r})"
        )


def learn(
    source: Union[str, Path],
    depth: int = 10,
    *,
    debug: bool = False,
    debug_output_dir: Optional[Union[str, Path]] = None,
) -> LearningResult:
    """Run the full XHAIL learning pipeline and return the learned hypothesis.

    XHAIL operates in three phases:

    1. **Abduction** — find a minimal set of atoms (Δ) that, together with
       the background knowledge, satisfies the examples.
    2. **Deduction** — build a *kernel set* of maximally-specific clauses
       that cover the abduced atoms.
    3. **Induction** — compress the kernel into a minimal hypothesis H that
       explains all examples.

    Args:
        source: Either a path to a ``.lp`` file, or a raw program string.
            A raw string is assumed if the value does not end in ``.lp``
            and does not correspond to an existing file.
        depth: Maximum search depth for the deduction phase (default: 10).
        debug: If ``True``, write intermediate ASP programs produced by
            the abduction and induction phases to *debug_output_dir*.
        debug_output_dir: Directory for intermediate ASP output when
            ``debug=True``.  Defaults to ``./xhail_debug/``.

    Returns:
        A :class:`LearningResult` containing the learned rules.

    Raises:
        ParseError: If *source* cannot be parsed.
        FileNotFoundError: If *source* is a path and the file does not exist.
        RuntimeError: If the abduction phase yields no model (UNSAT program).
        DeductionTimeoutError: If the deduction phase exceeds the time limit.
    """
    source_path = Path(source) if not isinstance(source, str) else None
    if isinstance(source, str) and not source.endswith(".lp"):
        # treat as raw program string
        raw_string = source
        source_label = "<string>"
    else:
        source_path = Path(source)
        if not source_path.exists():
            raise FileNotFoundError(f"Input file not found: {source_path}")
        raw_string = None
        source_label = str(source_path)

    # Resolve debug output directory
    output_dir: Optional[Path] = None
    if debug:
        output_dir = Path(debug_output_dir) if debug_output_dir else Path("xhail_debug")
        output_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("Debug mode: intermediate programs will be written to %s", output_dir)

    # --- Parse ---
    logger.debug("Parsing %s ...", source_label)
    parser = Parser()
    if raw_string is not None:
        parser.loadString(raw_string)
    else:
        parser.loadFile(str(source_path))
    parser.parseProgram()
    EX, MH, MB, BG = parser.separate()
    logger.debug(
        "Parsed: %d example(s), %d modeh, %d modeb, %d background clause(s)",
        len(EX), len(MH), len(MB), len(BG),
    )

    # --- Build model and run phases ---
    model = Model(EX, MH, MB, BG, depth, debug_output_dir=output_dir)

    logger.info("Phase 1: Abduction ...")
    Abduction(model).runPhase()

    logger.info("Phase 2: Deduction (depth=%d) ...", depth)
    Deduction(model).runPhase()

    logger.info("Phase 3: Induction ...")
    Induction(model).runPhase()

    hypothesis_clauses = model.getHypothesis()
    hypothesis_strs = [str(c) for c in hypothesis_clauses]

    return LearningResult(
        hypothesis=hypothesis_strs,
        success=bool(hypothesis_strs),
        source=source_label,
        n_examples=len(EX),
        n_background=len(BG),
    )
