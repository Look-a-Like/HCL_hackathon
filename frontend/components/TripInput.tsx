"use client";

import { useState } from "react";

const EXAMPLES = [
  "Weekend in Tokyo under $1500, love street food and temples",
  "10 days in Patagonia, adventure hiking, $3000",
];

interface Props {
  onSubmit: (query: string) => void;
  loading: boolean;
  variant?: "hero" | "bar";
  placeholder?: string;
}

export default function TripInput({ onSubmit, loading, variant = "hero", placeholder }: Props) {
  const [value, setValue] = useState("");

  function submit() {
    const q = value.trim();
    if (!q || loading) return;
    onSubmit(q);
    if (variant === "bar") setValue("");
  }

  if (variant === "bar") {
    return (
      <div style={{ display: "flex", alignItems: "center", gap: 10, background: "white", borderRadius: 14, border: "1.5px solid #E5E7EB", padding: "10px 12px", boxShadow: "0 2px 8px rgba(109,40,217,0.06)" }}>
        <button type="button" style={{ width: 32, height: 32, borderRadius: "50%", border: "2px solid #E5E7EB", display: "flex", alignItems: "center", justifyContent: "center", color: "#9CA3AF", cursor: "pointer", background: "transparent", flexShrink: 0, transition: "border-color 0.2s, color 0.2s" }}>
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
            <line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" />
          </svg>
        </button>
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && submit()}
          placeholder={placeholder ?? "Instruct the agents…"}
          disabled={loading}
          className="bar-input"
        />
        <button onClick={submit} disabled={loading || !value.trim()} className="btn-icon">
          {loading
            ? <svg className="animate-spin" width="15" height="15" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="rgba(255,255,255,0.3)" strokeWidth="4" /><path fill="white" d="M4 12a8 8 0 018-8V0C5.4 0 0 5.4 0 12h4z" /></svg>
            : <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="19" x2="12" y2="5" /><polyline points="5 12 12 5 19 12" /></svg>
          }
        </button>
      </div>
    );
  }

  return (
    <div>
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); submit(); } }}
        placeholder={placeholder ?? "Describe your journey — destination, dates, style, budget…"}
        rows={3}
        disabled={loading}
        className="hero-input"
        style={{ borderRadius: "12px 12px 0 0", borderBottom: "none", padding: "18px 20px" }}
      />
      <div style={{ background: "rgba(249,248,255,0.9)", borderRadius: "0 0 12px 12px", border: "1.5px solid", borderTop: "1px solid rgba(124,58,237,0.12)", borderColor: "#E9E8F0", padding: "10px 14px", display: "flex", alignItems: "center", justifyContent: "space-between", gap: 8 }}>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
          {EXAMPLES.map((ex) => (
            <button
              key={ex}
              type="button"
              onClick={() => setValue(ex)}
              style={{ padding: "5px 10px", borderRadius: 999, border: "1px solid #E5E7EB", fontSize: 11, color: "#6B7280", background: "white", cursor: "pointer", transition: "all 0.15s", whiteSpace: "nowrap" }}
            >
              {ex.length > 36 ? ex.slice(0, 36) + "…" : ex}
            </button>
          ))}
        </div>
        <button onClick={submit} disabled={loading || !value.trim()} className="btn-primary" style={{ fontSize: 13, padding: "10px 20px", flexShrink: 0 }}>
          {loading
            ? <><svg className="animate-spin" width="14" height="14" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="rgba(255,255,255,0.3)" strokeWidth="4" /><path fill="white" d="M4 12a8 8 0 018-8V0C5.4 0 0 5.4 0 12h4z" /></svg>Planning…</>
            : "Dispatch Agents →"
          }
        </button>
      </div>
    </div>
  );
}
