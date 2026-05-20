"""
XHAIL — eXtended Hybrid Abductive Inductive Learning
======================================================

A symbolic Inductive Logic Programming (ILP) system built on Answer Set
Programming (ASP).  XHAIL learns logic-program rules from background
knowledge and examples through three phases: abduction, deduction, and
induction.

Quick start::

    from xhail import learn

    result = learn("penguins.lp")
    print(result)          # flies(V1) :- not penguin(V1).

For programmatic use see :func:`xhail.learn` and :class:`xhail.LearningResult`.
For the command-line interface run ``xhail --help``.

Original XHAIL algorithm:
    Ray, O. (2009). Nonmonotonic abductive inductive learning.
    Journal of Applied Logic, 7(3), 329–340.
"""

from .core import LearningResult, learn

__version__ = "0.1.0"
__all__ = ["learn", "LearningResult", "__version__"]
