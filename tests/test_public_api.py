"""
Tests for the extended public API:
  - learn_from_string()
  - LearningResult.to_dict()
  - LearningResult.to_json()
  - LearningResult.to_lp()
  - LearningResult.n_rules property
  - learn(..., on_phase=callback)
  - PhaseCallback type alias export
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from xhail import LearningResult, PhaseCallback, learn, learn_from_string

BENCHMARKS = Path(__file__).parent.parent / "experiments" / "benchmarks"
PENGUINS_PROGRAM = """
    bird(a). bird(b). bird(c). penguin(d).
    bird(X) :- penguin(X).
    #modeh flies(+bird).
    #modeb not penguin(+bird).
    #example flies(a). #example flies(b). #example flies(c).
    #example not flies(d).
"""


# ---------------------------------------------------------------------------
# LearningResult — serialisation (pure unit tests, no clingo)
# ---------------------------------------------------------------------------


class TestLearningResultSerialisation:
    def _make_result(self) -> LearningResult:
        r = LearningResult(
            hypothesis=["flies(V1) :- not penguin(V1)."],
            success=True,
            source="penguins.lp",
            n_examples=4,
            n_background=3,
        )
        r._phase_times = {"abduction": 0.003, "deduction": 0.002, "induction": 0.001}
        return r

    def test_n_rules_property(self):
        r = self._make_result()
        assert r.n_rules == 1

    def test_n_rules_empty(self):
        assert LearningResult().n_rules == 0

    def test_to_dict_keys(self):
        d = self._make_result().to_dict()
        assert set(d) == {
            "success", "n_rules", "hypothesis", "source",
            "n_examples", "n_background", "phase_times_ms",
        }

    def test_to_dict_values(self):
        d = self._make_result().to_dict()
        assert d["success"] is True
        assert d["n_rules"] == 1
        assert d["hypothesis"] == ["flies(V1) :- not penguin(V1)."]
        assert d["source"] == "penguins.lp"
        assert d["n_examples"] == 4
        assert d["n_background"] == 3

    def test_to_dict_phase_times_in_ms(self):
        d = self._make_result().to_dict()
        assert d["phase_times_ms"]["abduction"] == pytest.approx(3.0, abs=0.1)
        assert d["phase_times_ms"]["deduction"] == pytest.approx(2.0, abs=0.1)
        assert d["phase_times_ms"]["induction"] == pytest.approx(1.0, abs=0.1)

    def test_to_dict_no_phase_times(self):
        r = LearningResult(hypothesis=["a :- b."], success=True)
        d = r.to_dict()
        assert d["phase_times_ms"] == {}

    def test_to_dict_is_json_serialisable(self):
        d = self._make_result().to_dict()
        serialised = json.dumps(d)
        assert isinstance(serialised, str)

    def test_to_json_default_indent(self):
        j = self._make_result().to_json()
        parsed = json.loads(j)
        assert parsed["success"] is True
        assert "flies" in parsed["hypothesis"][0]

    def test_to_json_compact(self):
        j = self._make_result().to_json(indent=None)
        assert "\n" not in j  # compact = single line

    def test_to_json_round_trips(self):
        r = self._make_result()
        parsed = json.loads(r.to_json())
        assert parsed == r.to_dict()

    def test_to_lp_contains_rules(self):
        r = self._make_result()
        lp = r.to_lp()
        assert "flies(V1) :- not penguin(V1)." in lp
        assert lp.endswith("\n")

    def test_to_lp_multiple_rules(self):
        r = LearningResult(
            hypothesis=["a(V1) :- b(V1).", "c(V1) :- d(V1)."],
            success=True,
        )
        lp = r.to_lp()
        assert "a(V1) :- b(V1)." in lp
        assert "c(V1) :- d(V1)." in lp

    def test_to_lp_no_hypothesis(self):
        r = LearningResult()
        lp = r.to_lp()
        assert "%" in lp  # comment indicating no hypothesis

    def test_unsuccessful_to_dict(self):
        r = LearningResult()
        d = r.to_dict()
        assert d["success"] is False
        assert d["n_rules"] == 0
        assert d["hypothesis"] == []


# ---------------------------------------------------------------------------
# PhaseCallback type alias is exported
# ---------------------------------------------------------------------------


class TestPhaseCallbackExport:
    def test_phase_callback_is_importable(self):
        assert PhaseCallback is not None

    def test_callable_matches_signature(self):
        # Any callable (str, dict) -> None is a valid PhaseCallback
        cb: PhaseCallback = lambda phase, info: None  # noqa: E731
        cb("abduction", {"elapsed_ms": 1.0})  # should not raise


# ---------------------------------------------------------------------------
# learn_from_string — integration tests
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestLearnFromString:
    def test_returns_learning_result(self):
        result = learn_from_string(PENGUINS_PROGRAM)
        assert isinstance(result, LearningResult)

    def test_source_label_is_string_sentinel(self):
        result = learn_from_string(PENGUINS_PROGRAM)
        assert result.source == "<string>"

    def test_success_on_valid_program(self):
        result = learn_from_string(PENGUINS_PROGRAM)
        assert result.success is True

    def test_hypothesis_contains_flies(self):
        result = learn_from_string(PENGUINS_PROGRAM)
        combined = " ".join(result.hypothesis)
        assert "flies" in combined
        assert "penguin" in combined

    def test_n_examples_populated(self):
        result = learn_from_string(PENGUINS_PROGRAM)
        assert result.n_examples == 4

    def test_n_background_populated(self):
        result = learn_from_string(PENGUINS_PROGRAM)
        assert result.n_background >= 1

    def test_to_dict_works_on_result(self):
        result = learn_from_string(PENGUINS_PROGRAM)
        d = result.to_dict()
        assert d["success"] is True
        assert d["source"] == "<string>"

    def test_to_json_works_on_result(self):
        result = learn_from_string(PENGUINS_PROGRAM)
        j = result.to_json()
        parsed = json.loads(j)
        assert parsed["success"] is True

    def test_to_lp_works_on_result(self):
        result = learn_from_string(PENGUINS_PROGRAM)
        lp = result.to_lp()
        assert "flies" in lp
        assert lp.endswith("\n")

    def test_phase_times_populated(self):
        result = learn_from_string(PENGUINS_PROGRAM)
        assert "abduction" in result._phase_times
        assert "deduction" in result._phase_times
        assert "induction" in result._phase_times
        for t in result._phase_times.values():
            assert t >= 0.0

    def test_phase_times_in_to_dict(self):
        result = learn_from_string(PENGUINS_PROGRAM)
        d = result.to_dict()
        assert "phase_times_ms" in d
        assert d["phase_times_ms"]["abduction"] >= 0.0


# ---------------------------------------------------------------------------
# learn(..., on_phase=callback) — integration
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestOnPhaseCallback:
    def test_callback_called_three_times(self):
        cb = MagicMock()
        learn(BENCHMARKS / "penguins.lp", on_phase=cb)
        assert cb.call_count == 3

    def test_callback_phase_names(self):
        phases = []
        learn(BENCHMARKS / "penguins.lp", on_phase=lambda p, i: phases.append(p))
        assert phases == ["abduction", "deduction", "induction"]

    def test_callback_info_has_elapsed_ms(self):
        infos = []
        learn(BENCHMARKS / "penguins.lp", on_phase=lambda p, i: infos.append(i))
        for info in infos:
            assert "elapsed_ms" in info
            assert info["elapsed_ms"] >= 0.0

    def test_abduction_info_has_delta_size(self):
        abduction_info = {}
        def cb(phase, info):
            if phase == "abduction":
                abduction_info.update(info)
        learn(BENCHMARKS / "penguins.lp", on_phase=cb)
        assert "delta_size" in abduction_info

    def test_deduction_info_has_kernel_size(self):
        deduction_info = {}
        def cb(phase, info):
            if phase == "deduction":
                deduction_info.update(info)
        learn(BENCHMARKS / "penguins.lp", on_phase=cb)
        assert "kernel_size" in deduction_info
        assert deduction_info["kernel_size"] >= 0

    def test_induction_info_has_n_rules(self):
        induction_info = {}
        def cb(phase, info):
            if phase == "induction":
                induction_info.update(info)
        learn(BENCHMARKS / "penguins.lp", on_phase=cb)
        assert "n_rules" in induction_info
        assert induction_info["n_rules"] >= 1

    def test_no_callback_still_works(self):
        result = learn(BENCHMARKS / "penguins.lp")
        assert result.success

    def test_callback_exception_propagates(self):
        def bad_cb(phase, info):
            raise ValueError("callback failed")
        with pytest.raises(ValueError, match="callback failed"):
            learn(BENCHMARKS / "penguins.lp", on_phase=bad_cb)

    def test_learn_from_string_accepts_on_phase(self):
        phases = []
        learn_from_string(PENGUINS_PROGRAM, on_phase=lambda p, i: phases.append(p))
        assert phases == ["abduction", "deduction", "induction"]
