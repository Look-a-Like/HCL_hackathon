"use client";

import { AgentState, AgentStatus, AGENT_LABELS, AGENT_DESCRIPTIONS, AGENT_ORDER } from "@/lib/types";

const AGENT_ICON_PATHS: Record<string, React.ReactNode> = {
  planner: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="2" y="7" width="20" height="14" rx="2" /><path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2" />
      <line x1="12" y1="12" x2="12" y2="16" /><line x1="10" y1="14" x2="14" y2="14" />
    </svg>
  ),
  destination: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" /><line x1="2" y1="12" x2="22" y2="12" />
      <path d="M12 2a15.3 15.3 0 010 20M12 2a15.3 15.3 0 000 20" />
    </svg>
  ),
  budget: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="2" y="5" width="20" height="14" rx="2" /><line x1="2" y1="10" x2="22" y2="10" />
    </svg>
  ),
  itinerary: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="4" width="18" height="18" rx="2" /><line x1="16" y1="2" x2="16" y2="6" />
      <line x1="8" y1="2" x2="8" y2="6" /><line x1="3" y1="10" x2="21" y2="10" />
    </svg>
  ),
  booking: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z" />
    </svg>
  ),
  local_experience: (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
    </svg>
  ),
};

function AgentCard({ agentKey, status, delay }: { agentKey: string; status: AgentStatus; delay: number }) {
  const isRunning = status === "running";
  const isDone = status === "done";
  const isLead = agentKey === "planner";

  const iconBg = isRunning
    ? "linear-gradient(135deg, #7C3AED, #8B5CF6)"
    : isDone
    ? "rgba(124,58,237,0.1)"
    : "rgba(124,58,237,0.06)";

  const iconColor = isRunning ? "white" : "#7C3AED";

  const cardStyle: React.CSSProperties = {
    background: isDone
      ? "linear-gradient(135deg, #FAFAFF 0%, #FFFFFF 100%)"
      : "#FFFFFF",
    border: isRunning
      ? "1.5px solid #7C3AED"
      : isDone
      ? "1.5px solid rgba(124,58,237,0.25)"
      : "1.5px solid #E5E7EB",
    borderRadius: "16px",
    boxShadow: isRunning
      ? "0 0 0 3px rgba(124,58,237,0.1), 0 4px 16px rgba(124,58,237,0.1)"
      : "0 1px 4px rgba(109,40,217,0.06), 0 1px 2px rgba(0,0,0,0.03)",
    transition: "border-color 0.25s, box-shadow 0.25s",
    minHeight: 175,
    display: "flex",
    flexDirection: "column",
  };

  return (
    <div className="fade-in" style={{ ...cardStyle, animationDelay: `${delay}s` }}>
      <div style={{ padding: "16px 16px 12px", flex: 1, display: "flex", flexDirection: "column" }}>
        {/* Icon + badge row */}
        <div className="flex items-start justify-between mb-3">
          <div style={{ width: 40, height: 40, borderRadius: 12, background: iconBg, display: "flex", alignItems: "center", justifyContent: "center", color: iconColor, boxShadow: isRunning ? "0 4px 12px rgba(124,58,237,0.25)" : "none", flexShrink: 0 }}>
            {AGENT_ICON_PATHS[agentKey]}
          </div>

          {/* Status badge */}
          {isLead && isRunning && (
            <span style={{ fontSize: 11, fontWeight: 700, color: "#7C3AED", letterSpacing: "0.04em" }}>Lead</span>
          )}
          {isDone && (
            <div style={{ width: 22, height: 22, borderRadius: "50%", background: "rgba(16,185,129,0.12)", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#10B981" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="20 6 9 17 4 12" />
              </svg>
            </div>
          )}
          {status === "error" && (
            <div style={{ width: 22, height: 22, borderRadius: "50%", background: "rgba(239,68,68,0.12)", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#EF4444" strokeWidth="3" strokeLinecap="round">
                <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </div>
          )}
        </div>

        {/* Running: progress */}
        {isRunning && (
          <div style={{ marginBottom: 8 }}>
            <p style={{ fontSize: 11, color: "#7C3AED", fontWeight: 500, marginBottom: 6, lineHeight: 1.5 }}>
              {agentKey === "budget"
                ? "Analyzing travel costs…"
                : agentKey === "destination"
                ? "Scouting destinations…"
                : `Working on your plan…`}
            </p>
            <div className="progress-track">
              <div className="progress-indeterminate" />
            </div>
          </div>
        )}

        <div style={{ flex: 1 }} />
      </div>

      {/* Footer */}
      <div style={{ padding: "12px 16px 14px", borderTop: "1px solid #F3F4F6" }}>
        <p style={{ fontWeight: 700, fontSize: 13, color: "#1E1B4B", marginBottom: 3 }}>{AGENT_LABELS[agentKey]}</p>
        <p style={{ fontSize: 11, color: "#6B7280", lineHeight: 1.5, overflow: "hidden", display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical" }}>
          {AGENT_DESCRIPTIONS[agentKey]}
        </p>
      </div>
    </div>
  );
}

export default function AgentTimeline({ agents }: { agents: AgentState }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12 }}>
      {AGENT_ORDER.map((key, i) => (
        <AgentCard key={key} agentKey={key} status={agents[key]} delay={i * 0.07} />
      ))}
    </div>
  );
}
