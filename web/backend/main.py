"""
XHAIL REST API
==============
FastAPI backend exposing the XHAIL learning pipeline.
Deployed on Fly.io; consumed by the Next.js frontend on Vercel.

Endpoints:
  GET  /health                - liveness check
  GET  /benchmarks            - list available benchmark names + descriptions
  GET  /benchmarks/{name}     - return the raw .lp source for a benchmark
  POST /learn                 - run the full XHAIL pipeline on a program string
"""

from __future__ import annotations

import tempfile
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from xhail import learn
from xhail.parser.parser import ParseError

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="XHAIL API",
    description=(
        "eXtended Hybrid Abductive Inductive Learning — "
        "a symbolic ILP system built on Answer Set Programming."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Benchmark registry
# ---------------------------------------------------------------------------

_BENCHMARKS_DIR = Path(__file__).parent.parent.parent / "experiments" / "benchmarks"

BENCHMARK_META = {
    "penguins": {
        "title": "Penguins",
        "description": "Classic ILP task: learn that birds fly unless they are penguins.",
        "expected": "flies(V1) :- not penguin(V1).",
        "file": "penguins.lp",
    },
    "animals": {
        "title": "Animal Classification",
        "description": "Learn that mammals have hair and produce milk.",
        "expected": "mammal(V1) :- has_hair(V1).",
        "file": "animals.lp",
    },
    "traffic": {
        "title": "Traffic Light",
        "description": "Learn that a car must stop when the light is red.",
        "expected": "stop(V1) :- red(V1).",
        "file": "traffic.lp",
    },
    "propositional": {
        "title": "Propositional Circuit",
        "description": "Learn a 0-arity AND gate: output holds when both inputs are active.",
        "expected": "output :- input_a, input_b.",
        "file": "propositional.lp",
    },
}

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------


class LearnRequest(BaseModel):
    program: str = Field(..., description="Raw .lp program text to learn from.")
    depth: int = Field(10, ge=1, le=50, description="Max deduction depth (default 10).")


class PhaseOutput(BaseModel):
    abduction_program: Optional[str] = None
    induction_program: Optional[str] = None


class LearnResponse(BaseModel):
    success: bool
    hypothesis: list[str]
    n_examples: int
    n_background: int
    runtime_ms: float
    phases: PhaseOutput


class BenchmarkSummary(BaseModel):
    name: str
    title: str
    description: str
    expected: str


class BenchmarkDetail(BaseModel):
    name: str
    title: str
    description: str
    expected: str
    source: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/health", tags=["Meta"])
def health():
    """Liveness check."""
    return {"status": "ok"}


@app.get("/benchmarks", response_model=list[BenchmarkSummary], tags=["Benchmarks"])
def list_benchmarks():
    """List all available benchmark tasks."""
    return [
        BenchmarkSummary(name=name, **{k: v for k, v in meta.items() if k != "file"})
        for name, meta in BENCHMARK_META.items()
    ]


@app.get("/benchmarks/{name}", response_model=BenchmarkDetail, tags=["Benchmarks"])
def get_benchmark(name: str):
    """Return the raw .lp source for a named benchmark."""
    if name not in BENCHMARK_META:
        raise HTTPException(status_code=404, detail=f"Benchmark '{name}' not found.")
    meta = BENCHMARK_META[name]
    path = _BENCHMARKS_DIR / meta["file"]
    if not path.exists():
        raise HTTPException(status_code=500, detail="Benchmark file missing on server.")
    return BenchmarkDetail(
        name=name,
        title=meta["title"],
        description=meta["description"],
        expected=meta["expected"],
        source=path.read_text(encoding="utf-8"),
    )


@app.post("/learn", response_model=LearnResponse, tags=["Learning"])
def run_learn(req: LearnRequest):
    """
    Run the full XHAIL pipeline (abduction → deduction → induction)
    on the supplied program string and return the learned hypothesis.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        start = time.perf_counter()
        try:
            result = learn(
                req.program,
                depth=req.depth,
                debug=True,
                debug_output_dir=tmp_path,
            )
        except ParseError as e:
            raise HTTPException(status_code=422, detail=f"Parse error: {e}")
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except RuntimeError as e:
            raise HTTPException(status_code=400, detail=str(e))
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000

        abduction_prog = (
            (tmp_path / "abduction.lp").read_text(encoding="utf-8")
            if (tmp_path / "abduction.lp").exists()
            else None
        )
        induction_prog = (
            (tmp_path / "induction.lp").read_text(encoding="utf-8")
            if (tmp_path / "induction.lp").exists()
            else None
        )

    return LearnResponse(
        success=result.success,
        hypothesis=result.hypothesis,
        n_examples=result.n_examples,
        n_background=result.n_background,
        runtime_ms=round(elapsed_ms, 2),
        phases=PhaseOutput(
            abduction_program=abduction_prog,
            induction_program=induction_prog,
        ),
    )
