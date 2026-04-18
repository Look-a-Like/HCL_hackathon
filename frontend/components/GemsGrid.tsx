"use client";

import { LocalGem } from "@/lib/types";

const TYPE_EMOJI: Record<string, string> = {
  restaurant:"🍽",bar:"🍸",market:"🏪",temple:"⛩",museum:"🏛",
  viewpoint:"🌄",beach:"🏖",shop:"🛍",park:"🌿",cafe:"☕",street:"🚶",activity:"🎯",
};

export default function GemsGrid({ gems }: { gems: LocalGem[] }) {
  if (!gems?.length) return null;

  return (
    <div style={{ background: "#FFFFFF", border: "1px solid #E5E7EB", borderRadius: 16, boxShadow: "0 4px 16px rgba(109,40,217,0.08)", padding: "20px" }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 14 }}>
        <h3 style={{ fontWeight: 700, fontSize: 15, color: "#1E1B4B" }}>Local Gems</h3>
        <span style={{ fontSize: 12, color: "#7C3AED", fontWeight: 600 }}>{gems.length} picks</span>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
        {gems.map((gem, i) => (
          <div
            key={i}
            className="slide-up"
            style={{
              padding: "12px",
              borderRadius: 12,
              border: "1px solid #F3F4F6",
              background: "linear-gradient(135deg, #FAFAFF 0%, #FFFFFF 100%)",
              animationDelay: `${i * 0.06}s`,
              transition: "border-color 0.2s",
            }}
          >
            <div style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
              <span style={{ fontSize: 18, flexShrink: 0, marginTop: 1 }}>
                {TYPE_EMOJI[gem.type?.toLowerCase()] ?? "✨"}
              </span>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 6, marginBottom: 3 }}>
                  <p style={{ fontWeight: 700, fontSize: 12, color: "#1E1B4B", lineHeight: 1.3 }}>{gem.name}</p>
                  <span style={{
                    fontSize: 9, fontWeight: 700, color: "#7C3AED",
                    background: "#EDE9FE", padding: "1px 6px", borderRadius: 999,
                    flexShrink: 0, textTransform: "capitalize", letterSpacing: "0.03em",
                  }}>
                    {gem.type}
                  </span>
                </div>
                <p style={{ fontSize: 11, color: "#6B7280", lineHeight: 1.5 }}>{gem.description}</p>
                {gem.tip && (
                  <p style={{ marginTop: 5, fontSize: 10, color: "#7C3AED", fontStyle: "italic" }}>💡 {gem.tip}</p>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
