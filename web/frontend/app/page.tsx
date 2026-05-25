"use client";

import { useState } from "react";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface PhaseOutput {
  abduction_program: string | null;
  induction_program: string | null;
}

interface LearnResponse {
  success: boolean;
  hypothesis: string[];
  n_examples: number;
  n_background: number;
  runtime_ms: number;
  phases: PhaseOutput;
}

// ---------------------------------------------------------------------------
// Benchmark presets (embedded so the UI works even before the backend loads)
// ---------------------------------------------------------------------------

const BENCHMARKS: Record<string, { label: string; description: string; source: string }> = {
  penguins: {
    label: "Penguins",
    description: "Learn that birds fly unless they are penguins",
    source: `% Background knowledge
bird(a). bird(b). bird(c).
penguin(d).
bird(X) :- penguin(X).

% Mode declarations
#modeh flies(+bird).
#modeb penguin(+bird).
#modeb not penguin(+bird).

% Examples
#example flies(a).
#example flies(b).
#example flies(c).
#example not flies(d).`,
  },
  animals: {
    label: "Animals",
    description: "Learn what makes an animal a mammal",
    source: `% Background knowledge
has_hair(dog).   produces_milk(dog).
has_hair(cat).   produces_milk(cat).
has_hair(bat).   produces_milk(bat).
has_hair(whale). produces_milk(whale).
lays_eggs(eagle). lays_eggs(salmon).

% Type declarations
animal(dog). animal(cat). animal(bat).
animal(whale). animal(eagle). animal(salmon).

% Mode declarations
#modeh mammal(+animal).
#modeb has_hair(+animal).
#modeb produces_milk(+animal).

% Examples
#example mammal(dog).
#example mammal(cat).
#example mammal(bat).
#example mammal(whale).
#example not mammal(eagle).
#example not mammal(salmon).`,
  },
  traffic: {
    label: "Traffic",
    description: "Learn when a car should stop",
    source: `% Background knowledge
red(light1). red(light3).
green(light2). green(light4).

% Type declarations
light(light1). light(light2).
light(light3). light(light4).

% Mode declarations
#modeh stop(+light).
#modeb red(+light).
#modeb green(+light).

% Examples
#example stop(light1).
#example stop(light3).
#example not stop(light2).
#example not stop(light4).`,
  },
  propositional: {
    label: "AND Gate",
    description: "Learn a propositional AND from 0-arity facts",
    source: `% Background knowledge
input_a.
input_b.

% Mode declarations (0-arity)
#modeh output.
#modeb input_a.
#modeb input_b.

% Examples
#example output.`,
  },
};

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function PhaseCard({
  title,
  badge,
  color,
  content,
  defaultOpen = false,
}: {
  title: string;
  badge: string;
  color: string;
  content: string | null;
  defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div className="phase-card">
      <div className="phase-header" onClick={() => setOpen((o) => !o)}>
        <span
          className="text-xs font-mono font-semibold px-2 py-0.5 rounded"
          style={{ background: `${color}20`, color }}
        >
          {badge}
        </span>
        <span className="text-sm font-medium text-slate-300">{title}</span>
        <span className="ml-auto text-slate-500 text-xs">{open ? "▲" : "▼"}</span>
      </div>
      {open && (
        <div className="border-t border-[var(--border)]">
          {content ? (
            <pre
              className="text-xs font-mono p-4 overflow-x-auto text-slate-400 leading-relaxed"
              style={{ maxHeight: "280px", overflowY: "auto" }}
            >
              {content.trim()}
            </pre>
          ) : (
            <p className="text-xs text-slate-600 p-4 italic">No output captured for this phase.</p>
          )}
        </div>
      )}
    </div>
  );
}

function StatPill({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex flex-col items-center bg-[var(--surface)] border border-[var(--border)] rounded-lg px-4 py-2">
      <span className="text-[10px] uppercase tracking-widest text-slate-500">{label}</span>
      <span className="text-base font-semibold text-slate-200 font-mono">{value}</span>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Main page
// ---------------------------------------------------------------------------

export default function Home() {
  const [program, setProgram] = useState(BENCHMARKS.penguins.source);
  const [depth, setDepth] = useState(10);
  const [activeBenchmark, setActiveBenchmark] = useState<string>("penguins");
  const [result, setResult] = useState<LearnResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";

  async function runLearn() {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`${apiUrl}/learn`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ program, depth }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail ?? `HTTP ${res.status}`);
      }
      const data: LearnResponse = await res.json();
      setResult(data);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  }

  function selectBenchmark(key: string) {
    setActiveBenchmark(key);
    setProgram(BENCHMARKS[key].source);
    setResult(null);
    setError(null);
  }

  return (
    <div className="min-h-screen flex flex-col" style={{ background: "var(--bg)" }}>
      {/* ── Header ── */}
      <header className="border-b border-[var(--border)] px-6 py-4 flex items-center gap-4">
        <div className="flex items-center gap-3">
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center text-white font-bold text-sm"
            style={{ background: "var(--accent)" }}
          >
            X
          </div>
          <div>
            <h1 className="text-base font-semibold text-white tracking-tight">XHAIL</h1>
            <p className="text-[11px] text-slate-500 leading-none">
              eXtended Hybrid Abductive Inductive Learning
            </p>
          </div>
        </div>
        <div className="ml-auto flex items-center gap-3">
          <a
            href={`${apiUrl}/docs`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-slate-400 hover:text-white transition-colors border border-[var(--border)] rounded px-3 py-1.5"
          >
            API Docs
          </a>
          <a
            href="https://github.com/everettmakes/xhail"
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs text-slate-400 hover:text-white transition-colors border border-[var(--border)] rounded px-3 py-1.5"
          >
            GitHub
          </a>
        </div>
      </header>

      {/* ── Body ── */}
      <main className="flex-1 flex flex-col lg:flex-row gap-0 overflow-hidden">
        {/* ── Left panel: editor ── */}
        <div
          className="flex flex-col gap-4 p-5 lg:w-[48%] lg:border-r border-[var(--border)] overflow-y-auto"
          style={{ minHeight: 0 }}
        >
          {/* Benchmark selector */}
          <div>
            <p className="text-[11px] uppercase tracking-widest text-slate-500 mb-2">
              Load benchmark
            </p>
            <div className="flex flex-wrap gap-2">
              {Object.entries(BENCHMARKS).map(([key, bm]) => (
                <button
                  key={key}
                  onClick={() => selectBenchmark(key)}
                  className="text-xs px-3 py-1.5 rounded-md border transition-all"
                  style={{
                    borderColor:
                      activeBenchmark === key ? "var(--accent)" : "var(--border)",
                    background:
                      activeBenchmark === key ? "rgba(124,106,247,0.12)" : "var(--surface)",
                    color: activeBenchmark === key ? "#a89ff7" : "#8890aa",
                  }}
                  title={bm.description}
                >
                  {bm.label}
                </button>
              ))}
            </div>
          </div>

          {/* Editor */}
          <div className="flex flex-col gap-1 flex-1">
            <p className="text-[11px] uppercase tracking-widest text-slate-500">
              Program
            </p>
            <textarea
              className="code-editor flex-1"
              style={{ minHeight: "320px" }}
              value={program}
              onChange={(e) => {
                setProgram(e.target.value);
                setActiveBenchmark("");
              }}
              spellCheck={false}
              placeholder={`% Write your XHAIL program here\n% Use #modeh, #modeb, #example\n\nbird(tweety).\n#modeh flies(+bird).\n#example flies(tweety).`}
            />
          </div>

          {/* Depth + run */}
          <div className="flex items-center gap-4">
            <div className="flex flex-col gap-1 flex-1">
              <label className="text-[11px] uppercase tracking-widest text-slate-500">
                Depth: <span className="text-slate-300 font-mono">{depth}</span>
              </label>
              <input
                type="range"
                min={1}
                max={20}
                value={depth}
                onChange={(e) => setDepth(Number(e.target.value))}
                className="w-full accent-violet-500"
              />
            </div>
            <button
              onClick={runLearn}
              disabled={loading || !program.trim()}
              className="px-6 py-2.5 rounded-lg text-sm font-semibold transition-all disabled:opacity-40 disabled:cursor-not-allowed"
              style={{
                background: loading ? "var(--accent-dim)" : "var(--accent)",
                color: "white",
                minWidth: "100px",
              }}
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <svg className="animate-spin h-3.5 w-3.5" viewBox="0 0 24 24" fill="none">
                    <circle
                      className="opacity-25"
                      cx="12" cy="12" r="10"
                      stroke="currentColor" strokeWidth="4"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8v8z"
                    />
                  </svg>
                  Running
                </span>
              ) : (
                "Run ▶"
              )}
            </button>
          </div>

          {/* Syntax hint */}
          <div className="text-[11px] text-slate-600 leading-relaxed border border-[var(--border)] rounded-lg p-3 bg-[var(--surface)]">
            <span className="text-slate-500 font-semibold">Syntax: </span>
            <span className="font-mono text-violet-400">#modeh pred(+type).</span>
            {" declares a head schema, "}
            <span className="font-mono text-violet-400">#modeb pred(+type).</span>
            {" a body schema, "}
            <span className="font-mono text-violet-400">#example atom.</span>
            {" a positive example, "}
            <span className="font-mono text-violet-400">#example not atom.</span>
            {" a negative one. Background knowledge is any normal ASP rule."}
          </div>
        </div>

        {/* ── Right panel: results ── */}
        <div className="flex flex-col gap-4 p-5 lg:flex-1 overflow-y-auto" style={{ minHeight: 0 }}>
          <p className="text-[11px] uppercase tracking-widest text-slate-500">
            Pipeline output
          </p>

          {/* Error */}
          {error && (
            <div className="border border-red-800 bg-red-950/40 rounded-lg p-4 text-sm text-red-400 font-mono">
              {error}
            </div>
          )}

          {/* Idle state */}
          {!result && !error && !loading && (
            <div className="flex-1 flex flex-col items-center justify-center gap-4 text-center py-16">
              <div className="text-5xl opacity-20">⊢</div>
              <p className="text-slate-600 text-sm max-w-xs">
                Write or load a program on the left, then hit{" "}
                <span className="text-slate-500 font-semibold">Run</span> to
                watch XHAIL induce a hypothesis.
              </p>
              <div className="flex gap-3 text-xs text-slate-700 mt-2">
                <span>Abduction</span>
                <span>→</span>
                <span>Deduction</span>
                <span>→</span>
                <span>Induction</span>
              </div>
            </div>
          )}

          {/* Loading skeleton */}
          {loading && (
            <div className="flex flex-col gap-3 animate-pulse">
              {["Phase 1: Abduction", "Phase 2: Deduction", "Phase 3: Induction"].map((ph) => (
                <div key={ph} className="phase-card p-4">
                  <div className="h-3 bg-slate-800 rounded w-40 mb-2" />
                  <div className="h-2 bg-slate-800 rounded w-full mb-1" />
                  <div className="h-2 bg-slate-800 rounded w-3/4" />
                </div>
              ))}
            </div>
          )}

          {/* Results */}
          {result && (
            <div className="flex flex-col gap-4">
              {/* Stats row */}
              <div className="flex gap-3 flex-wrap">
                <StatPill label="Status" value={result.success ? "✓ Learned" : "✗ No hyp."} />
                <StatPill label="Rules" value={result.hypothesis.length} />
                <StatPill label="Examples" value={result.n_examples} />
                <StatPill label="Background" value={result.n_background} />
                <StatPill label="Runtime" value={`${result.runtime_ms.toFixed(0)}ms`} />
              </div>

              {/* Hypothesis */}
              <div>
                <p className="text-[11px] uppercase tracking-widest text-slate-500 mb-2">
                  Learned hypothesis
                </p>
                {result.success ? (
                  <div className="flex flex-col gap-2">
                    {result.hypothesis.map((rule, i) => (
                      <div key={i} className="hypothesis-rule">
                        {rule}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="border border-yellow-800 bg-yellow-950/30 rounded-lg p-4 text-sm text-yellow-500">
                    No hypothesis found. Try adjusting mode declarations or depth.
                  </div>
                )}
              </div>

              {/* Pipeline phases */}
              <div>
                <p className="text-[11px] uppercase tracking-widest text-slate-500 mb-2">
                  Pipeline trace
                </p>
                <div className="flex flex-col gap-2">
                  <PhaseCard
                    title="Abduction — minimal grounding"
                    badge="Phase 1"
                    color="#7c6af7"
                    content={result.phases.abduction_program}
                    defaultOpen={true}
                  />
                  <PhaseCard
                    title="Deduction — kernel construction"
                    badge="Phase 2"
                    color="#38bdf8"
                    content={
                      "% Deduction builds the kernel set in memory.\n% The intermediate representation is not an ASP program."
                    }
                  />
                  <PhaseCard
                    title="Induction — hypothesis search"
                    badge="Phase 3"
                    color="#34d399"
                    content={result.phases.induction_program}
                  />
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* ── Footer ── */}
      <footer className="border-t border-[var(--border)] px-6 py-3 flex items-center justify-between">
        <span className="text-[11px] text-slate-600">
          XHAIL · Inductive Logic Programming via Answer Set Programming
        </span>
        <span className="text-[11px] text-slate-600">
          Based on{" "}
          <a
            href="https://doi.org/10.1007/s10994-008-5083-8"
            target="_blank"
            rel="noopener noreferrer"
            className="underline hover:text-slate-400"
          >
            Ray (2009)
          </a>
        </span>
      </footer>
    </div>
  );
}
