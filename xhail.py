"""
xhail.py — DEPRECATED entry script.

This file is superseded by the `xhail` CLI installed via pyproject.toml.
Use instead:

    xhail run <file.lp>          # command line
    from xhail import learn      # Python API

This file is kept only for backwards compatibility with existing scripts
that call `python xhail.py`. It will be removed in a future release.
Run `git rm --cached xhail.py` to stop tracking it.
"""
import sys
import warnings

warnings.warn(
    "xhail.py is deprecated. Use `xhail run <file>` or `from xhail import learn` instead.",
    DeprecationWarning,
    stacklevel=1,
)

from xhail.cli import main  # noqa: E402

sys.exit(main())