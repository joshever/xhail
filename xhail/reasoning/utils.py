"""
xhail.reasoning.utils — shared ASP program-building helpers
============================================================

Functions shared between the Abduction and Induction phases that
build fragments of ASP program text.
"""

from __future__ import annotations


def load_examples(examples: list) -> str:
    """Return the ASP program fragment encoding all examples."""
    program = "%EXAMPLES%\n"
    for example in examples:
        program += example.createProgram() + "\n"
    return program + "\n"


def load_background(background: list) -> str:
    """Return the ASP program fragment encoding all background clauses."""
    program = "%BACKGROUND%\n" + "\n".join(str(b) for b in background) + "\n"
    return program + "\n"
