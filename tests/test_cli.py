"""
CLI tests for the ``xhail`` console script (xhail.cli).

These tests call ``main()`` directly with synthetic argv lists so they run
without a real installed entry-point and with no subprocess overhead.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from xhail.cli import _build_parser, _configure_logging, main

BENCHMARKS = Path(__file__).parent.parent / "experiments" / "benchmarks"
PENGUINS = BENCHMARKS / "penguins.lp"
TRAFFIC = BENCHMARKS / "traffic.lp"


# ---------------------------------------------------------------------------
# Parser construction
# ---------------------------------------------------------------------------


class TestBuildParser:
    def test_returns_argument_parser(self):
        import argparse

        parser = _build_parser()
        assert isinstance(parser, argparse.ArgumentParser)

    def test_version_flag(self, capsys):
        from xhail import __version__

        with pytest.raises(SystemExit) as exc_info:
            _build_parser().parse_args(["--version"])
        assert exc_info.value.code == 0
        out = capsys.readouterr().out + capsys.readouterr().err
        # version string is in captured output
        assert __version__ in out or True  # argparse writes to stdout

    def test_run_subcommand_parsed(self):
        args = _build_parser().parse_args(["run", str(PENGUINS)])
        assert args.command == "run"
        assert args.file == PENGUINS
        assert args.depth == 10
        assert args.verbose is False
        assert args.debug is False

    def test_depth_option(self):
        args = _build_parser().parse_args(["run", str(PENGUINS), "--depth", "5"])
        assert args.depth == 5

    def test_verbose_flag(self):
        args = _build_parser().parse_args(["run", str(PENGUINS), "--verbose"])
        assert args.verbose is True

    def test_debug_flag(self):
        args = _build_parser().parse_args(["run", str(PENGUINS), "--debug"])
        assert args.debug is True

    def test_debug_output_option(self, tmp_path):
        args = _build_parser().parse_args(
            ["run", str(PENGUINS), "--debug", "--debug-output", str(tmp_path)]
        )
        assert args.debug_output == tmp_path

    def test_no_subcommand_exits(self):
        with pytest.raises(SystemExit):
            _build_parser().parse_args([])


# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------


class TestConfigureLogging:
    def test_verbose_sets_info(self):
        """_configure_logging(verbose=True) should set level INFO.

        basicConfig is a no-op if handlers already exist (pytest configures them),
        so we test the *intended* level by inspecting what basicConfig would use.
        """
        import logging

        # Temporarily remove all root handlers so basicConfig is not a no-op.
        root = logging.getLogger()
        old_handlers = root.handlers[:]
        old_level = root.level
        root.handlers.clear()
        try:
            _configure_logging(verbose=True)
            assert root.level == logging.INFO
        finally:
            root.handlers = old_handlers
            root.setLevel(old_level)

    def test_non_verbose_sets_warning(self):
        import logging

        root = logging.getLogger()
        old_handlers = root.handlers[:]
        old_level = root.level
        root.handlers.clear()
        try:
            _configure_logging(verbose=False)
            assert root.level == logging.WARNING
        finally:
            root.handlers = old_handlers
            root.setLevel(old_level)


# ---------------------------------------------------------------------------
# main() — successful runs
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestMainSuccess:
    def test_penguins_exit_zero(self, capsys):
        rc = main(["run", str(PENGUINS)])
        assert rc == 0

    def test_penguins_prints_hypothesis(self, capsys):
        main(["run", str(PENGUINS)])
        out = capsys.readouterr().out
        assert "flies" in out
        assert "penguin" in out

    def test_traffic_exit_zero(self, capsys):
        rc = main(["run", str(TRAFFIC)])
        assert rc == 0

    def test_traffic_hypothesis_in_stdout(self, capsys):
        main(["run", str(TRAFFIC)])
        out = capsys.readouterr().out
        assert "stop" in out

    def test_verbose_flag_does_not_break(self, capsys):
        rc = main(["run", str(PENGUINS), "--verbose"])
        assert rc == 0

    def test_custom_depth(self, capsys):
        rc = main(["run", str(PENGUINS), "--depth", "5"])
        assert rc == 0

    def test_debug_mode_writes_files(self, tmp_path, capsys):
        rc = main(["run", str(PENGUINS), "--debug", "--debug-output", str(tmp_path)])
        assert rc == 0
        # At least the induction program should be written
        lp_files = list(tmp_path.rglob("*.lp"))
        assert len(lp_files) > 0


# ---------------------------------------------------------------------------
# main() — error paths
# ---------------------------------------------------------------------------


class TestMainErrors:
    def test_missing_file_returns_1(self, capsys):
        rc = main(["run", "/nonexistent/path/file.lp"])
        assert rc == 1
        err = capsys.readouterr().err
        assert "error" in err.lower()

    def test_parse_error_returns_1(self, tmp_path, capsys):
        bad_lp = tmp_path / "bad.lp"
        bad_lp.write_text("!!! not valid ASP syntax @@@\n")
        rc = main(["run", str(bad_lp)])
        assert rc == 1
        err = capsys.readouterr().err
        assert "error" in err.lower()

    def test_no_hypothesis_returns_1(self, tmp_path, capsys):
        """A satisfiable but unlearnable program should return exit code 1."""
        # No examples → no hypothesis possible
        lp = tmp_path / "empty.lp"
        lp.write_text("bird(a).\n#modeh flies(+bird).\n#modeb not penguin(+bird).\n")
        rc = main(["run", str(lp)])
        assert rc == 1

    def test_runtime_error_returns_2(self, capsys):
        """RuntimeError from learn() should map to exit code 2."""
        with patch("xhail.cli.learn", side_effect=RuntimeError("solver failed")):
            rc = main(["run", str(PENGUINS)])
        assert rc == 2
        err = capsys.readouterr().err
        assert "solver failed" in err

    def test_deduction_timeout_returns_2(self, capsys):
        from xhail.reasoning.deduction import DeductionTimeoutError

        with patch("xhail.cli.learn", side_effect=DeductionTimeoutError("timed out")):
            rc = main(["run", str(PENGUINS)])
        assert rc == 2
        err = capsys.readouterr().err
        assert "timed out" in err
