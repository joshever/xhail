"""
Benchmark regression tests for XHAIL.

Each test runs a canonical benchmark from experiments/benchmarks/ and asserts:
  - the pipeline succeeds (success=True)
  - the expected number of examples was parsed
  - the learned hypothesis mentions the expected head predicate
  - (where deterministic) the exact rule is produced

All tests are marked @pytest.mark.integration because they invoke clingo.

Known limitations documented here:
  - Multi-head tasks (multiple #modeh) are not yet supported; only the first
    modeh predicate is used in the learned hypothesis.
  - Recursive modeb predicates (e.g. member/2) cause non-termination in the
    current deduction phase; recursive tasks are excluded from the suite.
  - Chained output variables (-type) in modeh are not supported; modeh must
    use only input (+type) placemarkers.
"""

from pathlib import Path

import pytest

from xhail import learn

BENCHMARKS = Path(__file__).parent.parent / "experiments" / "benchmarks"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _hyp(name: str):
    """Run a benchmark and return its LearningResult."""
    return learn(BENCHMARKS / f"{name}.lp")


# ---------------------------------------------------------------------------
# Penguins: negation-as-failure
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestPenguinsBenchmark:
    """flies(V1) :- not penguin(V1)."""

    def test_success(self):
        assert _hyp("penguins").success is True

    def test_n_examples(self):
        assert _hyp("penguins").n_examples == 4

    def test_hypothesis_mentions_flies(self):
        combined = " ".join(_hyp("penguins").hypothesis)
        assert "flies" in combined

    def test_hypothesis_uses_negation(self):
        combined = " ".join(_hyp("penguins").hypothesis)
        assert "not penguin" in combined

    def test_exact_rule(self):
        result = _hyp("penguins")
        assert result.hypothesis == ["flies(V1) :- not penguin(V1)."]


# ---------------------------------------------------------------------------
# Animals: feature-based classification
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestAnimalsBenchmark:
    """mammal(V1) :- has_hair(V1). OR mammal(V1) :- produces_milk(V1)."""

    def test_success(self):
        assert _hyp("animals").success is True

    def test_n_examples(self):
        # 4 positive + 2 negative = 6 examples
        assert _hyp("animals").n_examples == 6

    def test_hypothesis_mentions_mammal(self):
        combined = " ".join(_hyp("animals").hypothesis)
        assert "mammal" in combined

    def test_hypothesis_uses_defining_feature(self):
        combined = " ".join(_hyp("animals").hypothesis)
        # Either has_hair or produces_milk is a valid discriminating feature
        assert "has_hair" in combined or "produces_milk" in combined

    def test_rules_are_clauses(self):
        for rule in _hyp("animals").hypothesis:
            assert ":-" in rule


# ---------------------------------------------------------------------------
# Propositional: 0-arity (no variables)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestPropositionalBenchmark:
    """Exercises the 0-arity (propositional) code path fixed in Phase 3."""

    def test_success(self):
        assert _hyp("propositional").success is True

    def test_n_examples(self):
        assert _hyp("propositional").n_examples == 1

    def test_hypothesis_mentions_output(self):
        combined = " ".join(_hyp("propositional").hypothesis)
        assert "output" in combined

    def test_hypothesis_is_string(self):
        for rule in _hyp("propositional").hypothesis:
            assert isinstance(rule, str)
            assert len(rule) > 0


# ---------------------------------------------------------------------------
# Traffic light: simple single-head rule
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestTrafficBenchmark:
    """stop(V1) :- red(V1)."""

    def test_success(self):
        assert _hyp("traffic").success is True

    def test_n_examples(self):
        # 2 positive (stop) + 2 negative (not stop) = 4 examples
        assert _hyp("traffic").n_examples == 4

    def test_hypothesis_mentions_stop(self):
        combined = " ".join(_hyp("traffic").hypothesis)
        assert "stop" in combined

    def test_hypothesis_uses_red(self):
        combined = " ".join(_hyp("traffic").hypothesis)
        assert "red" in combined

    def test_exact_rule(self):
        result = _hyp("traffic")
        assert result.hypothesis == ["stop(V1) :- red(V1)."]


# ---------------------------------------------------------------------------
# Experiment runner smoke test (no clingo required)
# ---------------------------------------------------------------------------


class TestBenchmarkRunner:
    """Verify the experiment runner script is importable and its helpers work."""

    def test_runner_importable(self):
        import importlib.util
        from pathlib import Path

        runner_path = Path(__file__).parent.parent / "experiments" / "run_benchmarks.py"
        assert runner_path.exists(), "run_benchmarks.py not found"
        spec = importlib.util.spec_from_file_location("run_benchmarks", runner_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        assert hasattr(mod, "run_benchmark")
        assert hasattr(mod, "write_csv")
        assert hasattr(mod, "write_json")

    def test_rule_complexity_empty(self):
        import importlib.util
        from pathlib import Path

        from xhail import LearningResult

        runner_path = Path(__file__).parent.parent / "experiments" / "run_benchmarks.py"
        spec = importlib.util.spec_from_file_location("run_benchmarks", runner_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        assert mod._rule_complexity(LearningResult()) == 0.0

    def test_rule_complexity_fact(self):
        import importlib.util
        from pathlib import Path

        from xhail import LearningResult

        runner_path = Path(__file__).parent.parent / "experiments" / "run_benchmarks.py"
        spec = importlib.util.spec_from_file_location("run_benchmarks", runner_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        r = LearningResult(hypothesis=["p."], success=True)
        assert mod._rule_complexity(r) == 0.0

    def test_rule_complexity_one_body(self):
        import importlib.util
        from pathlib import Path

        from xhail import LearningResult

        runner_path = Path(__file__).parent.parent / "experiments" / "run_benchmarks.py"
        spec = importlib.util.spec_from_file_location("run_benchmarks", runner_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        r = LearningResult(hypothesis=["flies(X) :- bird(X)."], success=True)
        assert mod._rule_complexity(r) == 1.0

    def test_write_csv_creates_file(self, tmp_path):
        import importlib.util
        from pathlib import Path

        runner_path = Path(__file__).parent.parent / "experiments" / "run_benchmarks.py"
        spec = importlib.util.spec_from_file_location("run_benchmarks", runner_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        row = {
            "benchmark": "test",
            "success": True,
            "n_rules": 1,
            "n_examples": 2,
            "n_background": 3,
            "runtime_s": 0.1,
            "peak_memory_mb": 0.0,
            "rule_complexity": 1.0,
            "hypothesis": "p(X) :- q(X).",
            "error": "",
            "seed": 0,
            "depth": 10,
            "timestamp": "2024-01-01T00:00:00Z",
        }
        out = tmp_path / "out.csv"
        mod.write_csv([row], out, append=False)
        assert out.exists()
        content = out.read_text()
        assert "benchmark" in content  # header
        assert "test" in content  # data
