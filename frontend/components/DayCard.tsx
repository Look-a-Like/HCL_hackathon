"use client";

import { ItineraryDay } from "@/lib/types";

const PERIOD_SLOTS = [
  { key: "morning"   as const, time: "09:00", emoji: "🌅" },
  { key: "afternoon" as const, time: "14:00", emoji: "☀️" },
  { key: "evening"   as const, time: "19:00", emoji: "🌆" },
];
const MEAL_TIMES = { breakfast: "08:00", lunch: "12:30", dinner: "20:00" };

export default function DayCard({ day, index, isLast }: { day: ItineraryDay; index: number; isLast?: boolean }) {
  const slots = PERIOD_SLOTS.filter((s) => day[s.key]);
  const meals = Object.entries(day.meals ?? {}).filter(([, v]) => v) as [string, string][];

  return (
    <div
      className="slide-up"
      style={{
        display: "flex",
        gap: 16,
        paddingTop: index === 0 ? 0 : 20,
        paddingBottom: isLast ? 0 : 20,
        borderBottom: isLast ? "none" : "1px solid #F3F4F6",
        animationDelay: `${index * 0.08}s`,
      }}
    >
      {/* Day bubble */}
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", flexShrink: 0, width: 36 }}>
        <div style={{
          width: 36, height: 36, borderRadius: "50%",
          background: "linear-gradient(135deg, #7C3AED, #8B5CF6)",
          boxShadow: "0 4px 12px rgba(124,58,237,0.3)",
          display: "flex", alignItems: "center", justifyContent: "center",
          color: "white", fontSize: 13, fontWeight: 800, flexShrink: 0,
        }}>
          {day.day}
        </div>
        {!isLast && (
          <div style={{ flex: 1, width: 2, background: "linear-gradient(180deg, #DDD6FE 0%, transparent 100%)", marginTop: 6, minHeight: 20 }} />
        )}
      </div>

      {/* Content */}
      <div style={{ flex: 1, minWidth: 0, paddingTop: 4 }}>
        <div style={{ marginBottom: 12 }}>
          <h3 style={{ fontWeight: 700, fontSize: 15, color: "#1E1B4B", lineHeight: 1.3 }}>{day.theme}</h3>
          {day.date && <p style={{ fontSize: 11, color: "#9CA3AF", marginTop: 2 }}>{day.date}</p>}
          {(day.estimated_cost ?? 0) > 0 && (
            <p style={{ fontSize: 12, color: "#7C3AED", fontWeight: 600, marginTop: 3 }}>
              Est. ${day.estimated_cost.toLocaleString()} for the day
            </p>
          )}
        </div>

        {/* Slots */}
        <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          {slots.map((slot) => {
            const text = day[slot.key] as string;
            const [title, ...rest] = text.split(". ");
            const desc = rest.join(". ").trim();
            return (
              <div key={slot.key} style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
                <span style={{ fontSize: 11, color: "#9CA3AF", width: 38, flexShrink: 0, paddingTop: 2, fontFamily: "monospace", fontVariantNumeric: "tabular-nums" }}>
                  {slot.time}
                </span>
                <div style={{ width: 28, height: 28, borderRadius: 8, background: "rgba(124,58,237,0.08)", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, fontSize: 13 }}>
                  {slot.emoji}
                </div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <p style={{ fontSize: 13, fontWeight: 600, color: "#1E1B4B", lineHeight: 1.3 }}>{title}</p>
                  {desc && <p style={{ fontSize: 12, color: "#7C3AED", marginTop: 2, lineHeight: 1.5 }}>{desc}</p>}
                </div>
              </div>
            );
          })}

          {/* Meals */}
          {meals.map(([meal, val]) => (
            <div key={meal} style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
              <span style={{ fontSize: 11, color: "#9CA3AF", width: 38, flexShrink: 0, paddingTop: 2, fontFamily: "monospace" }}>
                {MEAL_TIMES[meal as keyof typeof MEAL_TIMES] ?? "—"}
              </span>
              <div style={{ width: 28, height: 28, borderRadius: 8, background: "#FFF7ED", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, fontSize: 13 }}>
                🍽
              </div>
              <div style={{ flex: 1 }}>
                <p style={{ fontSize: 10, color: "#9CA3AF", textTransform: "uppercase", letterSpacing: "0.06em", fontWeight: 600 }}>{meal}</p>
                <p style={{ fontSize: 13, color: "#1E1B4B", marginTop: 1 }}>{val}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
