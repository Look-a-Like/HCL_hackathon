"use client";

import { useEffect, useState } from "react";
import { BudgetBreakdown } from "@/lib/types";

const LINE_ITEMS: Array<{ key: keyof Omit<BudgetBreakdown, "total" | "currency">; label: string }> = [
  { key: "flights",    label: "Flights" },
  { key: "hotel",      label: "Accommodation" },
  { key: "activities", label: "Activities" },
  { key: "food",       label: "Dining & Experiences" },
  { key: "transport",  label: "Transport" },
  { key: "misc",       label: "Miscellaneous" },
];

export default function BudgetBar({ budget }: { budget: BudgetBreakdown }) {
  const [animated, setAnimated] = useState(false);
  useEffect(() => { const t = setTimeout(() => setAnimated(true), 150); return () => clearTimeout(t); }, []);

  const total = budget.total || 1;
  const items = LINE_ITEMS.filter(({ key }) => (budget[key] ?? 0) > 0);

  return (
    <div style={{ background: "#FFFFFF", border: "1px solid #E5E7EB", borderRadius: 16, boxShadow: "0 4px 16px rgba(109,40,217,0.08)", padding: "20px" }}>
      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 16 }}>
        <h3 style={{ fontWeight: 700, fontSize: 15, color: "#1E1B4B" }}>Budget Allocation</h3>
        <div style={{ width: 28, height: 28, borderRadius: 8, background: "rgba(124,58,237,0.1)", display: "flex", alignItems: "center", justifyContent: "center" }}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#7C3AED" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="18" y1="20" x2="18" y2="10" /><line x1="12" y1="20" x2="12" y2="4" /><line x1="6" y1="20" x2="6" y2="14" />
          </svg>
        </div>
      </div>

      {/* Total */}
      <div style={{ marginBottom: 18 }}>
        <p style={{ fontSize: 30, fontWeight: 800, color: "#1E1B4B", lineHeight: 1, letterSpacing: "-0.02em" }}>
          {budget.currency ?? "$"}{budget.total?.toLocaleString()}
        </p>
        <p style={{ fontSize: 12, color: "#6B7280", marginTop: 4 }}>Estimated Total</p>
      </div>

      {/* Items */}
      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {items.map(({ key, label }) => {
          const pct = (budget[key]! / total) * 100;
          return (
            <div key={key}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
                <span style={{ fontSize: 13, color: "#6B7280" }}>{label}</span>
                <span style={{ fontSize: 13, fontWeight: 600, color: "#1E1B4B" }}>
                  {budget.currency ?? "$"}{budget[key]?.toLocaleString()}
                </span>
              </div>
              <div style={{ height: 4, background: "#EDE9FE", borderRadius: 999, overflow: "hidden" }}>
                <div style={{
                  height: 4,
                  width: animated ? `${pct}%` : "0%",
                  background: "linear-gradient(90deg, #7C3AED 0%, #8B5CF6 100%)",
                  borderRadius: 999,
                  transition: "width 1.1s cubic-bezier(0.16,1,0.3,1)",
                }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
