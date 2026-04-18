"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import Header from "@/components/Header";
import TripInput from "@/components/TripInput";
import AgentTimeline from "@/components/AgentTimeline";
import DayCard from "@/components/DayCard";
import BudgetBar from "@/components/BudgetBar";
import BookingList from "@/components/BookingList";
import GemsGrid from "@/components/GemsGrid";
import MetricsRow from "@/components/MetricsRow";
import { streamPlan } from "@/lib/stream";
import type { AgentState, FinalPlan, FeedMessage } from "@/lib/types";
import { AGENT_ORDER, AGENT_LABELS } from "@/lib/types";

type Phase = "idle" | "planning" | "results";

const IDLE_AGENTS: AgentState = {
  planner: "idle", destination: "idle", budget: "idle",
  itinerary: "idle", booking: "idle", local_experience: "idle",
};

function buildFeedMessage(agent: string, data: unknown): FeedMessage {
  const p = (data ?? {}) as Partial<FinalPlan>;
  const msgs: Record<string, { title: string; body: string }> = {
    planner: {
      title: "Planning Strategy Locked",
      body: `Coordinating 5 specialized agents for ${p.destination ?? "your destination"}. Style: ${p.travel_style ?? "flexible"}.`,
    },
    destination: {
      title: "Destination Analysis Complete",
      body: "Top destinations confirmed. Routes and key attractions have been mapped.",
    },
    budget: {
      title: "Budget Allocation Optimized",
      body: `Total estimated: ${p.budget_breakdown?.currency ?? "$"}${p.budget_breakdown?.total?.toLocaleString() ?? "—"} across flights, accommodation, and experiences.`,
    },
    itinerary: {
      title: "Day-by-Day Itinerary Built",
      body: `${(p.itinerary?.length ?? 0) > 0 ? `${p.itinerary!.length}-day` : "Full"} schedule crafted with curated activities and dining.`,
    },
    booking: {
      title: "Best Booking Options Secured",
      body: "Flights and accommodation found within budget. Awaiting confirmation.",
    },
    local_experience: {
      title: "Local Gems Discovered",
      body: `${p.local_gems?.length ?? 0} hidden spots and insider recommendations curated.`,
    },
  };
  const m = msgs[agent] ?? { title: `${AGENT_LABELS[agent] ?? agent} Complete`, body: "Analysis finalized." };
  return { id: `${agent}-${Date.now()}`, agent, title: m.title, body: m.body };
}

/* ─────────── Idle / Landing ─────────── */
function IdleView({ onSubmit }: { onSubmit: (q: string) => void }) {
  return (
    <div className="relative min-h-screen overflow-hidden" style={{ background: "linear-gradient(160deg, #F5F3FF 0%, #EDE9FE 40%, #F5F3FF 100%)" }}>

      {/* Background orbs */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        <div className="absolute w-[600px] h-[600px] rounded-full" style={{ top: "-200px", left: "-150px", background: "radial-gradient(circle, rgba(139,92,246,0.15) 0%, transparent 65%)", filter: "blur(60px)" }} />
        <div className="absolute w-[500px] h-[500px] rounded-full" style={{ bottom: "-100px", right: "-100px", background: "radial-gradient(circle, rgba(196,181,253,0.2) 0%, transparent 65%)", filter: "blur(60px)" }} />
        <div className="absolute w-[300px] h-[300px] rounded-full" style={{ top: "40%", right: "20%", background: "radial-gradient(circle, rgba(124,58,237,0.08) 0%, transparent 65%)", filter: "blur(40px)" }} />
        {/* Dot grid */}
        <div className="absolute inset-0 dot-grid opacity-60" />
      </div>

      {/* Minimal nav */}
      <nav className="relative z-10 flex items-center justify-between px-8 py-5">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-xl flex items-center justify-center" style={{ background: "linear-gradient(135deg, #7C3AED, #8B5CF6)", boxShadow: "0 4px 16px rgba(124,58,237,0.35)" }}>
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10" /><line x1="2" y1="12" x2="22" y2="12" />
              <path d="M12 2a15.3 15.3 0 010 20M12 2a15.3 15.3 0 000 20" />
            </svg>
          </div>
          <span className="font-bold text-[16px]" style={{ color: "#1E1B4B" }}>Cartographer AI</span>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full" style={{ background: "rgba(124,58,237,0.08)", border: "1px solid rgba(124,58,237,0.15)" }}>
            <span className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ background: "#7C3AED" }} />
            <span className="text-[11px] font-semibold tracking-wider uppercase" style={{ color: "#7C3AED" }}>6 Agents Ready</span>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <main className="relative z-10 flex flex-col items-center justify-center px-4 pt-12 pb-24">
        <div className="w-full max-w-2xl text-center">

          {/* Eyebrow */}
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full mb-8 fade-in" style={{ background: "rgba(255,255,255,0.7)", border: "1px solid rgba(124,58,237,0.2)", boxShadow: "0 2px 12px rgba(124,58,237,0.08)", backdropFilter: "blur(8px)" }}>
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
            </svg>
            <span className="text-[12px] font-semibold" style={{ color: "#7C3AED" }}>Multi-Agent AI Travel Planner</span>
          </div>

          {/* Headline */}
          <h1 className="font-extrabold leading-[1.05] mb-5 fade-in-1" style={{ fontSize: "clamp(36px, 6vw, 58px)", color: "#1E1B4B", letterSpacing: "-0.02em" }}>
            Plan your perfect journey,<br />
            <span style={{ background: "linear-gradient(135deg, #7C3AED 0%, #8B5CF6 50%, #A78BFA 100%)", WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent", backgroundClip: "text" }}>
              effortlessly.
            </span>
          </h1>

          <p className="mb-10 fade-in-2" style={{ fontSize: "17px", color: "#6B7280", lineHeight: 1.65, maxWidth: "480px", margin: "0 auto 40px" }}>
            Describe your trip in plain language. Six specialized agents handle destination research, budgeting, bookings, and local insights — all in one go.
          </p>

          {/* Input card */}
          <div className="fade-in-3 text-left" style={{ background: "rgba(255,255,255,0.85)", borderRadius: "20px", boxShadow: "0 8px 40px rgba(124,58,237,0.12), 0 2px 12px rgba(0,0,0,0.04)", backdropFilter: "blur(12px)", border: "1.5px solid rgba(124,58,237,0.12)", padding: "6px" }}>
            <TripInput onSubmit={onSubmit} loading={false} variant="hero" />
          </div>

          {/* Agent chips */}
          <div className="flex flex-wrap items-center justify-center gap-2.5 mt-8 fade-in-4">
            {[
              { icon: "◈", label: "Master Planner" },
              { icon: "⊕", label: "Destination Scout" },
              { icon: "◎", label: "Budget Optimizer" },
              { icon: "▣", label: "Itinerary Builder" },
              { icon: "◇", label: "Booking Agent" },
              { icon: "✦", label: "Local Oracle" },
            ].map(({ icon, label }) => (
              <div key={label} className="flex items-center gap-1.5 px-3 py-1.5 rounded-full" style={{ background: "rgba(255,255,255,0.7)", border: "1px solid rgba(124,58,237,0.15)", fontSize: "12px", color: "#6B7280", backdropFilter: "blur(8px)" }}>
                <span style={{ color: "#7C3AED", fontSize: "11px" }}>{icon}</span>
                {label}
              </div>
            ))}
          </div>
        </div>

        {/* Feature row */}
        <div className="w-full max-w-3xl mt-20 fade-in-5">
          <div className="grid grid-cols-3 gap-4">
            {[
              { icon: "🗺", title: "Instant Itinerary", desc: "Day-by-day schedule with times, activities, and dining" },
              { icon: "💰", title: "Budget Breakdown", desc: "Flights, hotels, food, and activities all priced out" },
              { icon: "✈", title: "Booking Options", desc: "Best-matched flights and hotels within your budget" },
            ].map(({ icon, title, desc }) => (
              <div key={title} className="p-5 rounded-2xl text-center" style={{ background: "rgba(255,255,255,0.6)", border: "1px solid rgba(124,58,237,0.12)", backdropFilter: "blur(8px)" }}>
                <span className="text-2xl block mb-2">{icon}</span>
                <p className="font-semibold text-[13px] mb-1" style={{ color: "#1E1B4B" }}>{title}</p>
                <p className="text-[12px] leading-relaxed" style={{ color: "#6B7280" }}>{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </main>

      <footer className="relative z-10 text-center py-5 text-[11px]" style={{ color: "#9CA3AF", borderTop: "1px solid rgba(124,58,237,0.08)" }}>
        Cartographer AI coordinates multiple specialized agents. Responses may take a moment.
      </footer>
    </div>
  );
}

/* ─────────── Planning View ─────────── */
function PlanningView({ query, agents, feed, onFollowUp, isLoading }: {
  query: string; agents: AgentState; feed: FeedMessage[];
  onFollowUp: (msg: string) => void; isLoading: boolean;
}) {
  const feedEndRef = useRef<HTMLDivElement>(null);
  useEffect(() => { feedEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [feed.length]);
  const allDone = AGENT_ORDER.every((k) => agents[k] === "done" || agents[k] === "error");

  return (
    <div className="min-h-screen flex flex-col" style={{ background: "linear-gradient(160deg, #F5F3FF 0%, #EDE9FE 30%, #F5F3FF 100%)" }}>
      <div className="flex-1 max-w-3xl mx-auto w-full px-4 py-8">
        {/* Badge */}
        <div className="mb-5 fade-in">
          <div className={`badge-active ${allDone ? "badge-done" : ""}`}>
            <span className="dot" style={allDone ? { background: "#10B981", animation: "none" } : {}} />
            {allDone ? "Agent Generation Complete" : "Agent Cluster Active"}
          </div>
        </div>

        {/* Title */}
        <div className="mb-7 fade-in-1">
          <h1 className="font-extrabold leading-tight mb-2" style={{ fontSize: "clamp(28px, 5vw, 42px)", color: "#1E1B4B", letterSpacing: "-0.02em" }}>
            {allDone ? "Your journey is ready" : "Crafting your itinerary"}
          </h1>
          <p style={{ fontSize: "15px", color: "#6B7280" }}>
            {allDone ? "All 6 agents completed." : `Orchestrating 6 specialized agents to optimize your trip.`}
          </p>
          {query && (
            <p className="mt-1 text-[13px] italic" style={{ color: "#9CA3AF" }}>
              "{query.length > 80 ? query.slice(0, 80) + "…" : query}"
            </p>
          )}
        </div>

        {/* Agent grid */}
        <div className="mb-8 fade-in-2">
          <AgentTimeline agents={agents} />
        </div>

        {/* Feed */}
        {feed.length > 0 && (
          <div className="space-y-4 mb-8">
            {feed.map((msg, i) => (
              <div key={msg.id} className="flex gap-3 slide-up" style={{ animationDelay: `${i * 0.05}s` }}>
                <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5" style={{ background: "linear-gradient(135deg, #7C3AED, #8B5CF6)", boxShadow: "0 2px 8px rgba(124,58,237,0.3)" }}>
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <polyline points="20 6 9 17 4 12" />
                  </svg>
                </div>
                <div className="card flex-1 p-4">
                  <p className="font-bold text-[14px] mb-1" style={{ color: "#1E1B4B" }}>{msg.title}</p>
                  <p className="text-[13px] leading-relaxed" style={{ color: "#6B7280" }}>{msg.body}</p>
                </div>
              </div>
            ))}
            <div ref={feedEndRef} />
          </div>
        )}
      </div>

      {/* Sticky input bar */}
      <div className="sticky bottom-0 z-20" style={{ background: "rgba(245,243,255,0.92)", backdropFilter: "blur(12px)", borderTop: "1px solid rgba(124,58,237,0.12)" }}>
        <div className="max-w-3xl mx-auto px-4 py-3 space-y-2">
          <TripInput onSubmit={onFollowUp} loading={isLoading} variant="bar" placeholder="Instruct the agents… (e.g. 'Find a boutique hotel near the station')" />
          <p className="text-center text-[11px]" style={{ color: "#9CA3AF" }}>
            Cartographer AI coordinates multiple specialized agents. Responses may take a moment.
          </p>
        </div>
      </div>
    </div>
  );
}

/* ─────────── Results View ─────────── */
function ResultsView({ plan, onReset }: { plan: FinalPlan; onReset: () => void }) {
  return (
    <div className="min-h-screen" style={{ background: "#F5F3FF" }}>
      <Header />

      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
        {/* Badge */}
        <div className="mb-4 fade-in">
          <div className="badge-done badge-active">
            <span className="dot" style={{ background: "#10B981", animation: "none" }} />
            Agent Generation Complete
          </div>
        </div>

        {/* Hero row */}
        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-8 fade-in-1">
          <div>
            <h1 className="font-extrabold leading-tight mb-2" style={{ fontSize: "clamp(28px, 5vw, 46px)", color: "#1E1B4B", letterSpacing: "-0.02em" }}>
              {plan.destination}
            </h1>
            <div className="flex flex-wrap items-center gap-3 text-[13px]" style={{ color: "#6B7280" }}>
              {plan.trip_duration && (
                <span className="flex items-center gap-1.5">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" /><line x1="16" y1="2" x2="16" y2="6" />
                    <line x1="8" y1="2" x2="8" y2="6" /><line x1="3" y1="10" x2="21" y2="10" />
                  </svg>
                  {plan.trip_duration}
                </span>
              )}
              {plan.travel_style && (
                <>
                  <span style={{ color: "#E5E7EB" }}>•</span>
                  <span className="capitalize">{plan.travel_style}</span>
                </>
              )}
            </div>
            {plan.summary && (
              <p className="mt-3 text-[13px] leading-relaxed max-w-xl" style={{ color: "#6B7280" }}>{plan.summary}</p>
            )}
          </div>
          {plan.metrics && <MetricsRow metrics={plan.metrics} />}
        </div>

        {/* Two-column */}
        <div className="grid lg:grid-cols-[1fr_320px] gap-6">
          {/* LEFT */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-bold text-[18px]" style={{ color: "#1E1B4B" }}>Curated Path</h2>
              <button className="flex items-center gap-1 text-[13px] font-medium transition-colors" style={{ color: "#7C3AED" }}>
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="21" y1="10" x2="3" y2="10" /><line x1="21" y1="6" x2="3" y2="6" />
                  <line x1="21" y1="14" x2="3" y2="14" /><line x1="21" y1="18" x2="3" y2="18" />
                </svg>
                Adjust Pace
              </button>
            </div>

            <div className="card p-5">
              <div className="itinerary-timeline">
                {plan.itinerary?.length > 0 ? (
                  plan.itinerary.map((day, i) => (
                    <DayCard key={day.day} day={day} index={i} isLast={i === plan.itinerary.length - 1} />
                  ))
                ) : (
                  <p className="text-[13px] py-8 text-center" style={{ color: "#9CA3AF" }}>No itinerary data available.</p>
                )}
              </div>
            </div>

            {plan.local_gems?.length > 0 && <div className="mt-5"><GemsGrid gems={plan.local_gems} /></div>}

            {(plan.packing_tips?.length ?? 0) > 0 && (
              <div className="card p-5 mt-5">
                <h3 className="font-bold text-[15px] mb-3" style={{ color: "#1E1B4B" }}>Packing Essentials</h3>
                <ul className="grid sm:grid-cols-2 gap-2">
                  {plan.packing_tips!.map((tip, i) => (
                    <li key={i} className="flex items-start gap-2 text-[13px]" style={{ color: "#6B7280" }}>
                      <span className="mt-0.5 flex-shrink-0" style={{ color: "#7C3AED" }}>—</span>{tip}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* RIGHT */}
          <div className="space-y-4">
            {plan.budget_breakdown && <BudgetBar budget={plan.budget_breakdown} />}
            {plan.booking_options && <BookingList bookings={plan.booking_options} />}
          </div>
        </div>

        <div className="mt-10 text-center pb-12">
          <button onClick={onReset} className="btn-primary text-[14px] px-6 py-3">
            Plan Another Journey
          </button>
        </div>
      </div>
    </div>
  );
}

/* ─────────── Root ─────────── */
export default function Home() {
  const [phase, setPhase] = useState<Phase>("idle");
  const [query, setQuery] = useState("");
  const [agents, setAgents] = useState<AgentState>(IDLE_AGENTS);
  const [plan, setPlan] = useState<FinalPlan | null>(null);
  const [feed, setFeed] = useState<FeedMessage[]>([]);
  const [error, setError] = useState<string | null>(null);
  const loadingRef = useRef(false);

  const runPlan = useCallback(async (q: string) => {
    if (loadingRef.current) return;
    loadingRef.current = true;
    setQuery(q);
    setError(null);
    setPlan(null);
    setFeed([]);
    setAgents(IDLE_AGENTS);
    setPhase("planning");

    try {
      for await (const event of streamPlan(q)) {
        if (event.type === "agent_start" && event.agent) {
          setAgents((p) => ({ ...p, [event.agent!]: "running" }));
        } else if (event.type === "agent_done" && event.agent) {
          setAgents((p) => ({ ...p, [event.agent!]: "done" }));
          setFeed((p) => [...p, buildFeedMessage(event.agent!, event.data)]);
        } else if (event.type === "agent_error" && event.agent) {
          setAgents((p) => ({ ...p, [event.agent!]: "error" }));
        } else if (event.type === "final_plan") {
          setPlan(event.data as FinalPlan);
          setAgents(AGENT_ORDER.reduce((a, k) => ({ ...a, [k]: "done" }), {} as AgentState));
          setPhase("results");
        } else if (event.type === "error") {
          setError(event.error ?? "An error occurred.");
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Stream interrupted.");
    } finally {
      loadingRef.current = false;
    }
  }, []);

  function reset() { setPhase("idle"); setPlan(null); setAgents(IDLE_AGENTS); setFeed([]); setError(null); }

  return (
    <>
      {error && (
        <div className="fixed top-4 right-4 z-50 card p-4 max-w-xs" style={{ borderColor: "#FCA5A5", background: "#FEF2F2" }}>
          <p className="text-[13px] font-medium" style={{ color: "#DC2626" }}>{error}</p>
          <button onClick={() => setError(null)} className="mt-2 text-[11px]" style={{ color: "#9CA3AF" }}>Dismiss</button>
        </div>
      )}
      {phase === "idle" && <IdleView onSubmit={runPlan} />}
      {phase === "planning" && (
        <PlanningView
          query={query}
          agents={agents}
          feed={feed}
          onFollowUp={(msg) => runPlan(`${query}. Also: ${msg}`)}
          isLoading={loadingRef.current}
        />
      )}
      {phase === "results" && plan && <ResultsView plan={plan} onReset={reset} />}
    </>
  );
}
