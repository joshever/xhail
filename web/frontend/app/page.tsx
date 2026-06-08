"use client";

import { useState, useEffect, useCallback, useRef } from "react";

// ── Types ─────────────────────────────────────────────────────────────────

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

// ── Benchmark presets ─────────────────────────────────────────────────────

const BENCHMARKS = {
  penguins: {
    label: "Penguins",
    icon: "🐧",
    tag: "Defaults",
    description: "Birds fly — unless they're penguins",
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
    icon: "🐾",
    tag: "Classification",
    description: "Learn what makes an animal a mammal",
    source: `% Background knowledge
has_hair(dog).   produces_milk(dog).
has_hair(cat).   produces_milk(cat).
has_hair(bat).   produces_milk(bat).
has_hair(whale). produces_milk(whale).
lays_eggs(eagle). lays_eggs(salmon).

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
    icon: "🚦",
    tag: "Rules",
    description: "Learn when a car should stop",
    source: `% Background knowledge
red(light1). red(light3).
green(light2). green(light4).

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
    icon: "⊕",
    tag: "Logic",
    description: "Learn a 0-arity AND from propositional facts",
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
} as const;

type BenchmarkKey = keyof typeof BENCHMARKS;

// ── Clipboard hook ────────────────────────────────────────────────────────

function useClipboard(timeout = 1500) {
  const [copied, setCopied] = useState<string | null>(null);
  const copy = useCallback(
    (text: string, id: string) => {
      navigator.clipboard.writeText(text).then(() => {
        setCopied(id);
        setTimeout(() => setCopied(null), timeout);
      });
    },
    [timeout]
  );
  return { copied, copy };
}

// ── Icons ─────────────────────────────────────────────────────────────────

function IconCopy({ size = 13 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="9" y="9" width="13" height="13" rx="2" />
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
    </svg>
  );
}

function IconCheck({ size = 13 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12" />
    </svg>
  );
}

function IconPlay({ size = 13 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <polygon points="5 3 19 12 5 21 5 3" />
    </svg>
  );
}

function IconGitHub({ size = 13 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
    </svg>
  );
}

function IconSpinner({ size = 14 }: { size?: number }) {
  return (
    <svg className="spin" width={size} height={size} viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
      <path d="M21 12a9 9 0 11-6.219-8.56" />
    </svg>
  );
}

// ── CopyButton ────────────────────────────────────────────────────────────

function CopyButton({
  text, id, copied, copy, className = "",
}: {
  text: string; id: string; copied: string | null;
  copy: (t: string, id: string) => void; className?: string;
}) {
  const done = copied === id;
  return (
    <button
      onClick={() => copy(text, id)}
      title={done ? "Copied!" : "Copy"}
      className={`transition-colors ${className}`}
      style={{ color: done ? "#34d399" : undefined }}
    >
      {done ? <IconCheck /> : <IconCopy />}
    </button>
  );
}

// ── Idle state: animated pipeline diagram ─────────────────────────────────

function PipelineIdleState() {
  return (
    <div className="flex-1 flex flex-col items-center justify-center gap-8 py-10 px-4 animate-fade-in">
      <svg viewBox="0 0 500 110" className="w-full max-w-[480px]">
        {/* ─ Node 1: Abduction ─ */}
        <rect x="2" y="18" width="126" height="68" rx="11"
          fill="rgba(139,92,246,.07)" stroke="rgba(139,92,246,.28)" strokeWidth="1.5" />
        <text x="65" y="49" textAnchor="middle" fill="#a78bfa" fontSize="11.5"
          fontFamily="JetBrains Mono, monospace" fontWeight="600" letterSpacing="1">
          ABDUCE
        </text>
        <text x="65" y="68" textAnchor="middle" fill="rgba(139,92,246,.4)" fontSize="9.5"
          fontFamily="Inter, system-ui, sans-serif">
          Generate candidates
        </text>

        {/* ─ Arrow 1 ─ */}
        <line x1="128" y1="52" x2="178" y2="52" stroke="rgba(139,92,246,.35)"
          strokeWidth="1.5" strokeDasharray="5 4">
          <animate attributeName="stroke-dashoffset" values="0;-27" dur="1s" repeatCount="indefinite" />
        </line>
        <polygon points="178,47.5 186,52 178,56.5" fill="rgba(139,92,246,.45)" />

        {/* ─ Node 2: Deduction ─ */}
        <rect x="187" y="18" width="126" height="68" rx="11"
          fill="rgba(6,182,212,.06)" stroke="rgba(6,182,212,.22)" strokeWidth="1.5" />
        <text x="250" y="49" textAnchor="middle" fill="#67e8f9" fontSize="11.5"
          fontFamily="JetBrains Mono, monospace" fontWeight="600" letterSpacing="1">
          DEDUCE
        </text>
        <text x="250" y="68" textAnchor="middle" fill="rgba(6,182,212,.38)" fontSize="9.5"
          fontFamily="Inter, system-ui, sans-serif">
          Build kernel set
        </text>

        {/* ─ Arrow 2 ─ */}
        <line x1="313" y1="52" x2="363" y2="52" stroke="rgba(6,182,212,.3)"
          strokeWidth="1.5" strokeDasharray="5 4">
          <animate attributeName="stroke-dashoffset" values="0;-27" dur="1s" begin="0.33s" repeatCount="indefinite" />
        </line>
        <polygon points="363,47.5 371,52 363,56.5" fill="rgba(6,182,212,.4)" />

        {/* ─ Node 3: Induction ─ */}
        <rect x="372" y="18" width="126" height="68" rx="11"
          fill="rgba(16,185,129,.06)" stroke="rgba(16,185,129,.22)" strokeWidth="1.5" />
        <text x="435" y="49" textAnchor="middle" fill="#6ee7b7" fontSize="11.5"
          fontFamily="JetBrains Mono, monospace" fontWeight="600" letterSpacing="1">
          INDUCE
        </text>
        <text x="435" y="68" textAnchor="middle" fill="rgba(16,185,129,.38)" fontSize="9.5"
          fontFamily="Inter, system-ui, sans-serif">
          Search hypothesis
        </text>
      </svg>

      <div className="text-center space-y-2">
        <p className="text-slate-500 text-sm">
          Load an example or write your own program, then press{" "}
          <kbd className="inline-flex items-center gap-0.5 px-1.5 py-0.5 rounded
            bg-[var(--surface-2)] border border-[var(--border-2)]
            text-[10px] font-mono text-slate-400">
            ⌘ ↵
          </kbd>{" "}
          to run.
        </p>
        <p className="text-slate-700 text-xs">
          XHAIL abduces candidate atoms, deduces a kernel set, then induces the minimal consistent hypothesis.
        </p>
      </div>
    </div>
  );
}

// ── Loading skeleton ──────────────────────────────────────────────────────

function LoadingState() {
  const phases = [
    { label: "Abduction",  color: "#8b5cf6", desc: "Generating hypothesis candidates…" },
    { label: "Deduction",  color: "#06b6d4", desc: "Constructing kernel set…"          },
    { label: "Induction",  color: "#10b981", desc: "Searching hypothesis space…"       },
  ];
  return (
    <div className="flex flex-col gap-3">
      {phases.map((ph, i) => (
        <div key={ph.label} className="phase-card p-4 flex items-start gap-3 animate-fade-in"
          style={{ animationDelay: `${i * 0.12}s` }}>
          <div
            className="ping-dot mt-1 w-2 h-2 rounded-full flex-shrink-0"
            style={{ background: ph.color, boxShadow: `0 0 7px ${ph.color}`, animationDelay: `${i * 0.35}s` }}
          />
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-2.5">
              <span className="text-xs font-mono font-semibold" style={{ color: ph.color }}>
                {ph.label}
              </span>
              <div className="skeleton h-2 w-20" />
            </div>
            <div className="space-y-1.5">
              <div className="skeleton h-2 w-full" />
              <div className="skeleton h-2 w-4/5" />
              <div className="skeleton h-2 w-2/3" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

// ── StatPill ──────────────────────────────────────────────────────────────

function StatPill({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="stat-pill flex flex-col items-center bg-[var(--surface)]
      border border-[var(--border)] rounded-lg px-3.5 py-2.5 min-w-[70px]">
      <span className="text-[9px] uppercase tracking-widest text-slate-600 mb-0.5 font-medium">
        {label}
      </span>
      <span className="text-sm font-semibold text-slate-200 font-mono leading-tight">
        {value}
      </span>
    </div>
  );
}

// ── PhaseCard ─────────────────────────────────────────────────────────────

function PhaseCard({
  title, badge, color, content, defaultOpen = false,
}: {
  title: string; badge: string; color: string;
  content: string | null; defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  const { copied, copy } = useClipboard();

  return (
    <div className="phase-card">
      <div className="phase-header" onClick={() => setOpen((o) => !o)}>
        <span
          className="text-[10px] font-mono font-semibold px-2 py-0.5 rounded-md"
          style={{ background: `${color}18`, color }}
        >
          {badge}
        </span>
        <span className="text-sm font-medium text-slate-300">{title}</span>
        <span className="ml-auto text-slate-600 text-[10px] select-none">
          {open ? "▲" : "▼"}
        </span>
      </div>

      {open && (
        <div className="border-t border-[var(--border)] animate-fade-in">
          {content ? (
            <div className="relative group">
              <pre
                className="text-xs font-mono p-4 overflow-x-auto text-slate-400 leading-relaxed"
                style={{ maxHeight: "260px", overflowY: "auto" }}
              >
                {content.trim()}
              </pre>
              <button
                onClick={() => copy(content.trim(), badge)}
                className="absolute top-3 right-3 opacity-0 group-hover:opacity-100
                  transition-all p-1.5 rounded-md
                  bg-[var(--surface-2)] border border-[var(--border-2)]
                  text-slate-500 hover:text-slate-200"
                title="Copy"
              >
                {copied === badge ? <IconCheck /> : <IconCopy />}
              </button>
            </div>
          ) : (
            <p className="text-xs text-slate-600 p-4 italic font-mono">
              No output captured for this phase.
            </p>
          )}
        </div>
      )}
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────

export default function Home() {
  const [program, setProgram]               = useState<string>(BENCHMARKS.penguins.source);
  const [depth, setDepth]                   = useState(10);
  const [activeBm, setActiveBm]             = useState<BenchmarkKey | null>("penguins");
  const [result, setResult]                 = useState<LearnResponse | null>(null);
  const [loading, setLoading]               = useState(false);
  const [error, setError]                   = useState<string | null>(null);
  const textareaRef                         = useRef<HTMLTextAreaElement>(null);
  const { copied, copy }                    = useClipboard();

  const apiUrl   = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8080";
  const lineCount = program.split("\n").length;

  // ── Run ──
  const runLearn = useCallback(async () => {
    if (loading || !program.trim()) return;
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
        throw new Error((body as { detail?: string }).detail ?? `HTTP ${res.status}`);
      }
      setResult(await res.json() as LearnResponse);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  }, [loading, program, depth, apiUrl]);

  // ── Keyboard shortcut: Cmd/Ctrl + Enter ──
  useEffect(() => {
    function handler(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
        e.preventDefault();
        runLearn();
      }
    }
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [runLearn]);

  function selectBenchmark(key: BenchmarkKey) {
    setActiveBm(key);
    setProgram(BENCHMARKS[key].source);
    setResult(null);
    setError(null);
  }

  // ── Render ──
  return (
    <>
      {/* ── Ambient background ── */}
      <div className="fixed inset-0 pointer-events-none" style={{ zIndex: 0 }}>
        {/* Dot grid */}
        <div
          className="absolute inset-0"
          style={{
            backgroundImage:
              "radial-gradient(circle at 1px 1px, rgba(139,92,246,.075) 1px, transparent 0)",
            backgroundSize: "28px 28px",
          }}
        />
        {/* Top radial glow */}
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(ellipse 80% 45% at 50% -5%, rgba(139,92,246,.13) 0%, transparent 60%)",
          }}
        />
        {/* Bottom subtle vignette */}
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(ellipse 100% 40% at 50% 110%, rgba(59,130,246,.06) 0%, transparent 60%)",
          }}
        />
      </div>

      {/* ── Shell ── */}
      <div className="relative min-h-screen flex flex-col" style={{ zIndex: 1 }}>

        {/* ══════════ HEADER ══════════ */}
        <header
          className="border-b border-[var(--border)] px-5 py-3 flex items-center gap-3"
          style={{ background: "rgba(8,11,20,.85)", backdropFilter: "blur(12px)" }}
        >
          {/* Logo */}
          <div
            className="logo-glow w-8 h-8 rounded-lg flex items-center justify-center
              text-white font-bold text-sm flex-shrink-0"
            style={{ background: "linear-gradient(135deg, #7c3aed, #2563eb)" }}
          >
            X
          </div>

          <div className="mr-1">
            <h1 className="gradient-text text-base font-bold tracking-tight leading-none">
              XHAIL
            </h1>
            <p className="text-[10px] text-slate-600 leading-none mt-[3px]">
              eXtended Hybrid Abductive Inductive Learning
            </p>
          </div>

          <div className="hidden sm:flex items-center gap-2 ml-1">
            <span className="w-px h-5 bg-[var(--border)]" />
            {["ILP", "ASP", "Symbolic AI"].map((tag) => (
              <span
                key={tag}
                className="text-[9px] font-mono px-2 py-0.5 rounded-full
                  border border-[var(--border)] text-slate-600"
              >
                {tag}
              </span>
            ))}
          </div>

          <div className="ml-auto flex items-center gap-2">
            <a
              href={`${apiUrl}/docs`}
              target="_blank"
              rel="noopener noreferrer"
              className="ghost-btn hidden sm:inline-flex"
            >
              API Docs
            </a>
            <a
              href="https://github.com/everettmakes/xhail"
              target="_blank"
              rel="noopener noreferrer"
              className="ghost-btn"
            >
              <IconGitHub size={12} />
              GitHub
            </a>
          </div>
        </header>

        {/* ══════════ BODY ══════════ */}
        <main className="flex-1 flex flex-col lg:flex-row overflow-hidden">

          {/* ─────── LEFT PANEL ─────── */}
          <div
            className="flex flex-col gap-4 p-5 lg:w-[46%] lg:border-r border-[var(--border)] overflow-y-auto"
            style={{ minHeight: 0 }}
          >

            {/* Benchmark selector */}
            <section>
              <p className="text-[10px] uppercase tracking-widest text-slate-600 font-semibold mb-2.5">
                Load example
              </p>
              <div className="grid grid-cols-2 gap-2">
                {(Object.entries(BENCHMARKS) as [BenchmarkKey, (typeof BENCHMARKS)[BenchmarkKey]][]).map(
                  ([key, bm]) => {
                    const active = activeBm === key;
                    return (
                      <button
                        key={key}
                        onClick={() => selectBenchmark(key)}
                        className={`bench-btn ${active ? "active" : ""}`}
                      >
                        <div className="flex items-start gap-2">
                          <span className="text-lg leading-none mt-0.5">{bm.icon}</span>
                          <div className="flex-1 min-w-0 text-left">
                            <div className="flex items-center gap-1.5 mb-1">
                              <span
                                className="text-xs font-semibold"
                                style={{ color: active ? "#a78bfa" : "#94a3b8" }}
                              >
                                {bm.label}
                              </span>
                              <span
                                className="text-[8px] font-mono px-1.5 py-px rounded-full border ml-auto"
                                style={{
                                  color: active ? "#8b78f0" : "#475569",
                                  borderColor: active ? "rgba(139,92,246,.3)" : "var(--border)",
                                }}
                              >
                                {bm.tag}
                              </span>
                            </div>
                            <p
                              className="text-[10px] leading-relaxed"
                              style={{ color: active ? "#7470a8" : "#3d4260" }}
                            >
                              {bm.description}
                            </p>
                          </div>
                        </div>
                      </button>
                    );
                  }
                )}
              </div>
            </section>

            {/* Editor */}
            <section className="flex flex-col flex-1">
              {/* macOS-style top bar */}
              <div
                className="flex items-center gap-2 px-3 py-2 border border-[var(--border)]
                  border-b-0 rounded-t-lg"
                style={{ background: "var(--surface-2)" }}
              >
                {/* Traffic lights */}
                <div className="flex gap-1.5 flex-shrink-0">
                  <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#ff5f57" }} />
                  <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#febc2e" }} />
                  <div className="w-2.5 h-2.5 rounded-full" style={{ background: "#28c840" }} />
                </div>
                <span className="font-mono text-[10px] text-slate-500 ml-1 flex-1">program.lp</span>
                <span className="text-[10px] text-slate-700 font-mono flex-shrink-0">
                  {lineCount} ln
                </span>
                <CopyButton
                  text={program}
                  id="editor"
                  copied={copied}
                  copy={copy}
                  className="flex items-center gap-1 text-[10px] text-slate-600 hover:text-slate-300 ml-1"
                />
              </div>

              <textarea
                ref={textareaRef}
                className="code-editor flex-1"
                style={{ minHeight: "260px" }}
                value={program}
                onChange={(e) => {
                  setProgram(e.target.value);
                  setActiveBm(null);
                }}
                spellCheck={false}
                placeholder={`% Write your XHAIL program here\n% ─────────────────────────────\nbird(tweety).\n\n#modeh flies(+bird).\n#modeb bird(+bird).\n\n#example flies(tweety).`}
              />
            </section>

            {/* Controls row */}
            <div className="flex items-end gap-4">
              {/* Depth slider */}
              <div className="flex flex-col gap-1.5 flex-1">
                <div className="flex items-center justify-between">
                  <label className="text-[10px] uppercase tracking-widest text-slate-600 font-semibold">
                    Deduction depth
                  </label>
                  <span
                    className="text-xs font-mono text-slate-300 px-2 py-px rounded
                      bg-[var(--surface-2)] border border-[var(--border)]"
                  >
                    {depth}
                  </span>
                </div>
                <input
                  type="range"
                  min={1}
                  max={50}
                  value={depth}
                  onChange={(e) => setDepth(Number(e.target.value))}
                  className="w-full accent-violet-500"
                />
              </div>

              {/* Run button */}
              <button
                onClick={runLearn}
                disabled={loading || !program.trim()}
                className="run-btn px-5 py-2.5 rounded-lg text-sm font-semibold
                  flex items-center gap-2 flex-shrink-0"
              >
                {loading ? (
                  <>
                    <IconSpinner />
                    Running…
                  </>
                ) : (
                  <>
                    <IconPlay />
                    Run
                    <kbd className="text-[9px] opacity-50 font-mono ml-0.5">⌘↵</kbd>
                  </>
                )}
              </button>
            </div>

            {/* Syntax reference (collapsible) */}
            <details className="border border-[var(--border)] rounded-lg overflow-hidden">
              <summary
                className="px-3.5 py-2.5 cursor-pointer flex items-center justify-between
                  text-[10px] uppercase tracking-widest text-slate-600 font-semibold
                  hover:bg-[var(--surface)] transition-colors"
              >
                <span>Syntax reference</span>
                <span className="text-[8px]">▼</span>
              </summary>
              <div
                className="px-4 pt-3 pb-4 border-t border-[var(--border)]"
                style={{ background: "var(--surface)" }}
              >
                <div
                  className="grid text-[11px] text-slate-500 leading-relaxed gap-y-2"
                  style={{ gridTemplateColumns: "auto 1fr", columnGap: "12px" }}
                >
                  {[
                    ["#modeh pred(+type).", "Head mode — predicate to learn"],
                    ["#modeb pred(+type).", "Body mode — available conditions"],
                    ["#example atom.",      "Positive example"],
                    ["#example not atom.",  "Negative example"],
                    ["fact(a). r(X) :- …", "Background knowledge (normal ASP)"],
                  ].map(([code, desc]) => (
                    <>
                      <code key={code} className="text-violet-400 font-mono whitespace-nowrap self-center">
                        {code}
                      </code>
                      <span key={desc} className="text-slate-600">{desc}</span>
                    </>
                  ))}
                </div>
              </div>
            </details>
          </div>

          {/* ─────── RIGHT PANEL ─────── */}
          <div
            className="flex flex-col gap-4 p-5 lg:flex-1 overflow-y-auto"
            style={{ minHeight: 0 }}
          >
            {/* Panel header */}
            <div className="flex items-center justify-between flex-shrink-0">
              <p className="text-[10px] uppercase tracking-widest text-slate-600 font-semibold">
                Pipeline output
              </p>
              {result && (
                <span
                  className="animate-fade-up text-[10px] font-mono px-2.5 py-0.5 rounded-full border"
                  style={result.success
                    ? { color: "#34d399", borderColor: "rgba(52,211,153,.3)", background: "rgba(52,211,153,.06)" }
                    : { color: "#f87171", borderColor: "rgba(248,113,113,.3)", background: "rgba(248,113,113,.06)" }
                  }
                >
                  {result.success ? "✓ Hypothesis found" : "✗ No hypothesis"}
                </span>
              )}
            </div>

            {/* ── Error ── */}
            {error && (
              <div
                className="animate-fade-up border rounded-lg p-4"
                style={{
                  borderColor: "rgba(248,113,113,.35)",
                  background: "rgba(127,29,29,.18)",
                }}
              >
                <p className="text-xs font-semibold text-red-400 mb-1.5 uppercase tracking-wide">
                  Error
                </p>
                <pre className="text-sm text-red-300 font-mono whitespace-pre-wrap leading-relaxed">
                  {error}
                </pre>
              </div>
            )}

            {/* ── Idle ── */}
            {!result && !error && !loading && <PipelineIdleState />}

            {/* ── Loading ── */}
            {loading && <LoadingState />}

            {/* ── Results ── */}
            {result && (
              <div className="flex flex-col gap-5 animate-fade-in">

                {/* Stats row */}
                <div className="flex gap-2 flex-wrap">
                  <StatPill label="Runtime"    value={`${result.runtime_ms.toFixed(0)} ms`} />
                  <StatPill label="Rules"      value={result.hypothesis.length}              />
                  <StatPill label="Examples"   value={result.n_examples}                     />
                  <StatPill label="Background" value={result.n_background}                   />
                </div>

                {/* Learned hypothesis */}
                <section>
                  <p className="text-[10px] uppercase tracking-widest text-slate-600 font-semibold mb-2.5">
                    Learned hypothesis
                  </p>
                  {result.success ? (
                    <div className="flex flex-col gap-2">
                      {result.hypothesis.map((rule, i) => (
                        <div key={i} className="hypothesis-rule" style={{ animationDelay: `${i * 0.06}s` }}>
                          <code className="flex-1 min-w-0">{rule}</code>
                          <button
                            onClick={() => copy(rule, `rule-${i}`)}
                            className="flex-shrink-0 text-emerald-700 hover:text-emerald-400 transition-colors"
                            title="Copy rule"
                          >
                            {copied === `rule-${i}` ? <IconCheck /> : <IconCopy />}
                          </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div
                      className="animate-fade-up border rounded-lg p-4 text-sm font-mono"
                      style={{
                        borderColor: "rgba(251,191,36,.25)",
                        background: "rgba(120,53,15,.15)",
                        color: "rgba(251,191,36,.75)",
                      }}
                    >
                      No hypothesis found — try loosening mode declarations or increasing depth.
                    </div>
                  )}
                </section>

                {/* Pipeline trace */}
                <section>
                  <p className="text-[10px] uppercase tracking-widest text-slate-600 font-semibold mb-2.5">
                    Pipeline trace
                  </p>
                  <div className="flex flex-col gap-2">
                    <PhaseCard
                      title="Abduction — minimal grounding"
                      badge="Phase 1"
                      color="#8b5cf6"
                      content={result.phases.abduction_program}
                      defaultOpen
                    />
                    <PhaseCard
                      title="Deduction — kernel construction"
                      badge="Phase 2"
                      color="#06b6d4"
                      content={
                        "% Deduction builds the kernel set in working memory.\n" +
                        "% The intermediate representation is not a serialisable ASP program.\n" +
                        "% See Ray (2009) §4.2 for the formal definition of the kernel set."
                      }
                    />
                    <PhaseCard
                      title="Induction — hypothesis search"
                      badge="Phase 3"
                      color="#10b981"
                      content={result.phases.induction_program}
                    />
                  </div>
                </section>
              </div>
            )}
          </div>
        </main>

        {/* ══════════ FOOTER ══════════ */}
        <footer
          className="border-t border-[var(--border)] px-5 py-2.5 flex items-center justify-between flex-shrink-0"
          style={{ background: "rgba(8,11,20,.8)", backdropFilter: "blur(8px)" }}
        >
          <span className="text-[10px] text-slate-700 font-mono">
            XHAIL · Inductive Logic Programming via Answer Set Programming
          </span>
          <a
            href="https://doi.org/10.1007/s10994-008-5083-8"
            target="_blank"
            rel="noopener noreferrer"
            className="text-[10px] text-slate-700 hover:text-slate-400 transition-colors underline underline-offset-2"
          >
            Ray (2009)
          </a>
        </footer>
      </div>
    </>
  );
}
