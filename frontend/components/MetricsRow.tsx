"use client";

import { Metrics } from "@/lib/types";

export default function MetricsRow({ metrics }: { metrics: Metrics }) {
  const latency = metrics.total_latency_ms != null ? (metrics.total_latency_ms / 1000).toFixed(1) : null;
  const completeness = metrics.completeness_score != null ? Math.round(metrics.completeness_score * 100) : null;
  if (!latency && !completeness) return null;

  return (
    <div style={{ display: "flex", gap: 10, flexShrink: 0 }}>
      {latency && (
        <div style={{ background: "#FFFFFF", border: "1px solid #E5E7EB", borderRadius: 12, padding: "10px 16px", textAlign: "center", minWidth: 90, boxShadow: "0 2px 8px rgba(109,40,217,0.06)" }}>
          <p style={{ fontSize: 10, fontWeight: 700, color: "#6B7280", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: 2 }}>Latency</p>
          <p style={{ fontSize: 22, fontWeight: 800, color: "#1E1B4B", lineHeight: 1, letterSpacing: "-0.02em" }}>
            {latency}<span style={{ fontSize: 12, fontWeight: 500, color: "#6B7280", marginLeft: 2 }}>sec</span>
          </p>
        </div>
      )}
      {completeness != null && (
        <div style={{ background: "#FFFFFF", border: "1px solid #E5E7EB", borderRadius: 12, padding: "10px 16px", textAlign: "center", minWidth: 90, boxShadow: "0 2px 8px rgba(109,40,217,0.06)" }}>
          <p style={{ fontSize: 10, fontWeight: 700, color: "#7C3AED", textTransform: "uppercase", letterSpacing: "0.07em", marginBottom: 2 }}>Completeness</p>
          <p style={{ fontSize: 22, fontWeight: 800, color: "#7C3AED", lineHeight: 1, letterSpacing: "-0.02em" }}>
            {completeness}<span style={{ fontSize: 12, fontWeight: 500, marginLeft: 1 }}>%</span>
          </p>
        </div>
      )}
    </div>
  );
}
