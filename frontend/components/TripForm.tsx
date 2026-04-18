"use client";

import { useState } from "react";

/* ── Indian number formatting ── */
function formatINR(n: number): string {
  if (n >= 100000) {
    const lakh = n / 100000;
    return lakh % 1 === 0 ? `${lakh}L` : `${lakh.toFixed(1)}L`;
  }
  if (n >= 1000) {
    const k = n / 1000;
    return k % 1 === 0 ? `${k}K` : `${k.toFixed(1)}K`;
  }
  return n.toLocaleString("en-IN");
}

function fullINR(n: number): string {
  return "₹" + n.toLocaleString("en-IN");
}

/* ── Data ── */
const DOMESTIC: string[] = [
  "Rajasthan", "Kerala", "Goa", "Himachal Pradesh", "Uttarakhand",
  "Jammu & Kashmir", "Tamil Nadu", "Karnataka", "Maharashtra",
  "Andaman & Nicobar", "Sikkim", "Meghalaya", "Odisha",
  "Madhya Pradesh", "Gujarat", "Ladakh", "Arunachal Pradesh",
  "Lakshadweep", "Coorg (Karnataka)", "Spiti Valley",
];

const INTERNATIONAL: string[] = [
  "Thailand", "Dubai / UAE", "Singapore", "Malaysia", "Maldives",
  "Sri Lanka", "Nepal", "Bali / Indonesia", "Vietnam", "Japan",
  "France", "Italy", "Switzerland", "UK", "Greece", "Portugal",
  "Turkey", "Australia", "USA", "South Korea", "Germany",
  "Morocco", "Egypt", "South Africa", "New Zealand",
];

const DOMESTIC_CITIES: Record<string, string[]> = {
  "Rajasthan":          ["Jaipur", "Udaipur", "Jodhpur", "Jaisalmer", "Pushkar"],
  "Kerala":             ["Munnar", "Alleppey", "Kochi", "Wayanad", "Kovalam"],
  "Goa":                ["North Goa", "South Goa", "Panjim"],
  "Himachal Pradesh":   ["Manali", "Shimla", "Dharamshala", "Kasol", "Dalhousie"],
  "Uttarakhand":        ["Rishikesh", "Nainital", "Mussoorie", "Haridwar", "Auli"],
  "Jammu & Kashmir":    ["Srinagar", "Pahalgam", "Gulmarg", "Leh"],
  "Tamil Nadu":         ["Chennai", "Madurai", "Ooty", "Kodaikanal", "Rameswaram"],
  "Karnataka":          ["Bangalore", "Mysore", "Coorg", "Hampi", "Gokarna"],
  "Maharashtra":        ["Mumbai", "Pune", "Aurangabad", "Mahabaleshwar", "Lonavala"],
  "Andaman & Nicobar":  ["Port Blair", "Havelock Island", "Neil Island"],
  "Sikkim":             ["Gangtok", "Pelling", "Lachung"],
  "Meghalaya":          ["Shillong", "Cherrapunji", "Mawlynnong"],
  "Odisha":             ["Puri", "Bhubaneswar", "Konark"],
  "Madhya Pradesh":     ["Khajuraho", "Bhopal", "Pachmarhi", "Orchha"],
  "Gujarat":            ["Ahmedabad", "Rann of Kutch", "Gir", "Dwarka"],
  "Ladakh":             ["Leh", "Nubra Valley", "Pangong Lake"],
};

const DURATIONS = [
  { label: "Long Weekend (2–3 days)", value: "3 days" },
  { label: "Short Break (4–5 days)",  value: "5 days" },
  { label: "One Week",                value: "7 days" },
  { label: "10 Days",                 value: "10 days" },
  { label: "Two Weeks",               value: "14 days" },
  { label: "Three Weeks",             value: "21 days" },
  { label: "One Month",               value: "30 days" },
];

const STYLES = [
  { icon: "🏔", label: "Adventure" },
  { icon: "🛕", label: "Pilgrimage" },
  { icon: "🏛",  label: "Heritage & Forts" },
  { icon: "🍛",  label: "Food & Cuisine" },
  { icon: "💆", label: "Relaxation" },
  { icon: "💎", label: "Luxury" },
  { icon: "🎒", label: "Backpacking" },
  { icon: "💑", label: "Honeymoon" },
  { icon: "👨‍👩‍👧", label: "Family" },
  { icon: "🌿", label: "Nature & Wildlife" },
  { icon: "📸", label: "Photography" },
  { icon: "🏖", label: "Beach & Water" },
];

/* Budget in INR — 5K to 5L */
const BUDGET_MIN  = 5000;
const BUDGET_MAX  = 500000;
const BUDGET_STEP = 1000;

const BUDGET_PRESETS = [
  { label: "Budget",    value: 10000  },
  { label: "Moderate",  value: 50000  },
  { label: "Comfort",   value: 150000 },
  { label: "Luxury",    value: 500000 },
];

const SURPRISE_PROMPTS = [
  "Long weekend from Mumbai — hills or beach, under ₹15,000 per person",
  "Family trip to Rajasthan, forts and culture, 7 days, ₹80,000 total",
  "Honeymoon in Kerala backwaters and Munnar, 6 nights, moderate budget",
  "Solo adventure to Spiti Valley or Ladakh, 10 days, budget trip",
  "First international trip — Thailand or Bali, 7 nights, ₹1,00,000",
  "Pilgrimage to Varanasi, Ayodhya & Prayagraj, 5 days, family of 4",
];

/* ── Types ── */
type TripType = "domestic" | "international";

interface FormState {
  tripType: TripType;
  state: string;
  city: string;
  duration: string;
  travelers: number;
  budget: number;
  styles: string[];
  notes: string;
}

const DEFAULT: FormState = {
  tripType:  "domestic",
  state:     "",
  city:      "",
  duration:  "7 days",
  travelers: 2,
  budget:    50000,
  styles:    [],
  notes:     "",
};

/* ── Prompt builder ── */
function buildPrompt(form: FormState): string {
  const dest = form.tripType === "domestic"
    ? [form.city, form.state].filter(Boolean).join(", ")
    : [form.city, form.state].filter(Boolean).join(", ");
  const parts: string[] = [];
  parts.push(`Plan a ${form.duration} trip${dest ? ` to ${dest}` : " in India"}`);
  parts.push(`for ${form.travelers} traveler${form.travelers > 1 ? "s" : ""}`);
  parts.push(`with a total budget of ${fullINR(form.budget)} INR`);
  if (form.styles.length) parts.push(`Travel style: ${form.styles.join(", ")}`);
  if (form.notes.trim()) parts.push(form.notes.trim());
  return parts.join(". ") + ".";
}

/* ── Sub-components ── */
function Label({ children }: { children: React.ReactNode }) {
  return (
    <p style={{ fontSize: 11, fontWeight: 700, color: "#1E1B4B", textTransform: "uppercase", letterSpacing: "0.08em", marginBottom: 7 }}>
      {children}
    </p>
  );
}

const selectStyle: React.CSSProperties = {
  width: "100%", appearance: "none", WebkitAppearance: "none",
  background: "white", border: "1.5px solid #E5E7EB",
  borderRadius: 10, padding: "11px 34px 11px 13px",
  fontSize: 13, color: "#1E1B4B", fontFamily: "inherit",
  outline: "none", cursor: "pointer",
  boxShadow: "0 1px 3px rgba(109,40,217,0.05)",
};

const inputStyle: React.CSSProperties = {
  width: "100%", background: "white", border: "1.5px solid #E5E7EB",
  borderRadius: 10, padding: "11px 13px", fontSize: 13, color: "#1E1B4B",
  fontFamily: "inherit", outline: "none",
  boxShadow: "0 1px 3px rgba(109,40,217,0.05)",
};

function SelectWrap({ value, onChange, children }: { value: string; onChange: (v: string) => void; children: React.ReactNode }) {
  return (
    <div style={{ position: "relative" }}>
      <select value={value} onChange={(e) => onChange(e.target.value)} style={{ ...selectStyle, color: value ? "#1E1B4B" : "#9CA3AF" }}>
        {children}
      </select>
      <svg style={{ position: "absolute", right: 11, top: "50%", transform: "translateY(-50%)", pointerEvents: "none", color: "#9CA3AF" }} width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="6 9 12 15 18 9" />
      </svg>
    </div>
  );
}

/* ── Main ── */
interface Props { onSubmit: (query: string) => void; loading: boolean; }

export default function TripForm({ onSubmit, loading }: Props) {
  const [tab, setTab]         = useState<"structured" | "surprise">("structured");
  const [form, setForm]       = useState<FormState>(DEFAULT);
  const [surpriseText, setSurpriseText] = useState("");

  function set<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((f) => {
      const next = { ...f, [key]: value };
      if (key === "state") next.city = "";
      return next;
    });
  }

  function toggleStyle(s: string) {
    setForm((f) => ({ ...f, styles: f.styles.includes(s) ? f.styles.filter((x) => x !== s) : [...f.styles, s] }));
  }

  function handleSubmit() {
    if (loading) return;
    if (tab === "structured") {
      if (!form.state && !form.city) return;
      onSubmit(buildPrompt(form));
    } else {
      const q = surpriseText.trim();
      if (!q) return;
      onSubmit(q);
    }
  }

  const stateOptions = form.tripType === "domestic" ? DOMESTIC : INTERNATIONAL;
  const cityOptions  = form.tripType === "domestic" ? (DOMESTIC_CITIES[form.state] ?? []) : [];
  const canSubmit    = tab === "structured" ? !!(form.state || form.city) : surpriseText.trim().length > 0;

  const tabBtn = (active: boolean): React.CSSProperties => ({
    padding: "9px 18px", borderRadius: 9, fontSize: 13, fontWeight: 600,
    fontFamily: "inherit", border: "none", cursor: "pointer", transition: "all 0.2s",
    background: active ? "linear-gradient(135deg, #7C3AED, #8B5CF6)" : "transparent",
    color: active ? "white" : "#6B7280",
    boxShadow: active ? "0 4px 12px rgba(124,58,237,0.25)" : "none",
  });

  return (
    <div style={{ background: "rgba(255,255,255,0.93)", borderRadius: 20, border: "1.5px solid rgba(124,58,237,0.15)", boxShadow: "0 8px 40px rgba(124,58,237,0.13)", backdropFilter: "blur(12px)", overflow: "hidden" }}>

      {/* ── Tab bar ── */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "12px 14px 10px", borderBottom: "1px solid rgba(124,58,237,0.08)" }}>
        <div style={{ display: "flex", gap: 3, background: "rgba(124,58,237,0.06)", padding: 4, borderRadius: 11 }}>
          <button style={tabBtn(tab === "structured")} onClick={() => setTab("structured")}>🗺 Plan My Trip</button>
          <button style={tabBtn(tab === "surprise")}   onClick={() => setTab("surprise")}>🎲 Surprise Me</button>
        </div>
        <span style={{ fontSize: 10, color: "#9CA3AF" }}>6 AI agents • INR</span>
      </div>

      {/* ════ STRUCTURED FORM ════ */}
      {tab === "structured" && (
        <div style={{ padding: "16px 16px 0" }}>

          {/* Trip type toggle */}
          <div style={{ marginBottom: 14 }}>
            <Label>Trip Type</Label>
            <div style={{ display: "flex", gap: 8 }}>
              {(["domestic", "international"] as const).map((t) => (
                <button
                  key={t}
                  onClick={() => { set("tripType", t); set("state", ""); set("city", ""); }}
                  style={{
                    flex: 1, padding: "9px 0", borderRadius: 10, border: "1.5px solid",
                    fontSize: 13, fontWeight: 600, cursor: "pointer", fontFamily: "inherit", transition: "all 0.15s",
                    borderColor: form.tripType === t ? "#7C3AED" : "#E5E7EB",
                    background: form.tripType === t ? "linear-gradient(135deg, #7C3AED, #8B5CF6)" : "white",
                    color: form.tripType === t ? "white" : "#6B7280",
                    boxShadow: form.tripType === t ? "0 3px 10px rgba(124,58,237,0.22)" : "none",
                  }}
                >
                  {t === "domestic" ? "🇮🇳 India" : "✈️ International"}
                </button>
              ))}
            </div>
          </div>

          {/* Destination */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 14 }}>
            <div>
              <Label>{form.tripType === "domestic" ? "State / Region" : "Country"}</Label>
              <SelectWrap value={form.state} onChange={(v) => set("state", v)}>
                <option value="" disabled>{form.tripType === "domestic" ? "Select state…" : "Select country…"}</option>
                {stateOptions.map((s) => <option key={s} value={s}>{s}</option>)}
              </SelectWrap>
            </div>
            <div>
              <Label>{form.tripType === "domestic" ? "City / Area" : "City (optional)"}</Label>
              {form.tripType === "domestic" && cityOptions.length > 0 ? (
                <SelectWrap value={form.city} onChange={(v) => set("city", v)}>
                  <option value="">Any city</option>
                  {cityOptions.map((c) => <option key={c} value={c}>{c}</option>)}
                </SelectWrap>
              ) : (
                <input
                  type="text"
                  value={form.city}
                  onChange={(e) => set("city", e.target.value)}
                  placeholder={form.tripType === "domestic" ? "e.g. Jaipur, Munnar…" : "e.g. Bangkok, Bali…"}
                  style={inputStyle}
                />
              )}
            </div>
          </div>

          {/* Duration + Travelers */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, marginBottom: 14 }}>
            <div>
              <Label>Duration</Label>
              <SelectWrap value={form.duration} onChange={(v) => set("duration", v)}>
                {DURATIONS.map((d) => <option key={d.value} value={d.value}>{d.label}</option>)}
              </SelectWrap>
            </div>
            <div>
              <Label>Travelers</Label>
              <div style={{ display: "flex", alignItems: "center", background: "white", border: "1.5px solid #E5E7EB", borderRadius: 10, overflow: "hidden", boxShadow: "0 1px 3px rgba(109,40,217,0.05)" }}>
                <button onClick={() => set("travelers", Math.max(1, form.travelers - 1))} style={{ width: 40, height: 43, border: "none", background: "transparent", cursor: "pointer", fontSize: 18, color: "#7C3AED", flexShrink: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>−</button>
                <span style={{ flex: 1, textAlign: "center", fontSize: 14, fontWeight: 700, color: "#1E1B4B" }}>
                  {form.travelers}
                  <span style={{ fontSize: 11, fontWeight: 400, color: "#6B7280", marginLeft: 4 }}>{form.travelers === 1 ? "person" : "people"}</span>
                </span>
                <button onClick={() => set("travelers", Math.min(20, form.travelers + 1))} style={{ width: 40, height: 43, border: "none", background: "transparent", cursor: "pointer", fontSize: 18, color: "#7C3AED", flexShrink: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>+</button>
              </div>
            </div>
          </div>

          {/* Budget */}
          <div style={{ marginBottom: 14 }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 8 }}>
              <Label>Total Budget</Label>
              <div style={{ textAlign: "right" }}>
                <span style={{ fontSize: 17, fontWeight: 800, color: "#7C3AED", letterSpacing: "-0.02em" }}>{fullINR(form.budget)}</span>
                <span style={{ fontSize: 10, color: "#9CA3AF", marginLeft: 6 }}>per group</span>
              </div>
            </div>

            {/* Presets */}
            <div style={{ display: "flex", gap: 6, marginBottom: 10 }}>
              {BUDGET_PRESETS.map((p) => {
                const active = form.budget === p.value;
                return (
                  <button
                    key={p.label}
                    onClick={() => set("budget", p.value)}
                    style={{
                      flex: 1, padding: "6px 2px", borderRadius: 8, border: "1.5px solid",
                      fontSize: 10, fontWeight: 700, cursor: "pointer", fontFamily: "inherit", transition: "all 0.15s",
                      borderColor: active ? "#7C3AED" : "#E5E7EB",
                      background: active ? "linear-gradient(135deg, #7C3AED, #8B5CF6)" : "white",
                      color: active ? "white" : "#6B7280",
                      boxShadow: active ? "0 2px 8px rgba(124,58,237,0.22)" : "none",
                    }}
                  >
                    <div>{p.label}</div>
                    <div style={{ fontSize: 9, marginTop: 1, opacity: 0.85 }}>₹{formatINR(p.value)}</div>
                  </button>
                );
              })}
            </div>

            {/* Slider */}
            <style>{`
              input[type=range].budget-slider {
                -webkit-appearance: none; appearance: none;
                width: 100%; height: 4px; border-radius: 999px; outline: none; cursor: pointer;
                background: linear-gradient(90deg, #7C3AED ${((form.budget - BUDGET_MIN) / (BUDGET_MAX - BUDGET_MIN)) * 100}%, #DDD6FE ${((form.budget - BUDGET_MIN) / (BUDGET_MAX - BUDGET_MIN)) * 100}%);
              }
              input[type=range].budget-slider::-webkit-slider-thumb {
                -webkit-appearance: none; width: 20px; height: 20px; border-radius: 50%;
                background: white; border: 3px solid #7C3AED;
                box-shadow: 0 2px 8px rgba(124,58,237,0.3); cursor: pointer; transition: transform 0.15s;
              }
              input[type=range].budget-slider::-webkit-slider-thumb:hover { transform: scale(1.2); }
            `}</style>
            <input
              type="range" min={BUDGET_MIN} max={BUDGET_MAX} step={BUDGET_STEP}
              value={form.budget}
              onChange={(e) => set("budget", Number(e.target.value))}
              className="budget-slider"
            />
            <div style={{ display: "flex", justifyContent: "space-between", marginTop: 3 }}>
              <span style={{ fontSize: 10, color: "#9CA3AF" }}>₹5,000</span>
              <span style={{ fontSize: 10, color: "#9CA3AF" }}>₹5,00,000</span>
            </div>
          </div>

          {/* Travel Style */}
          <div style={{ marginBottom: 14 }}>
            <Label>Travel Style <span style={{ fontSize: 9, fontWeight: 400, textTransform: "none", letterSpacing: 0, color: "#9CA3AF" }}>(select all that apply)</span></Label>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
              {STYLES.map(({ icon, label }) => {
                const active = form.styles.includes(label);
                return (
                  <button
                    key={label}
                    onClick={() => toggleStyle(label)}
                    style={{
                      padding: "6px 11px", borderRadius: 999, border: "1.5px solid",
                      fontSize: 11, fontWeight: 600, cursor: "pointer", fontFamily: "inherit",
                      display: "flex", alignItems: "center", gap: 4, transition: "all 0.15s",
                      borderColor: active ? "#7C3AED" : "#E5E7EB",
                      background: active ? "linear-gradient(135deg, #7C3AED, #8B5CF6)" : "white",
                      color: active ? "white" : "#6B7280",
                      boxShadow: active ? "0 2px 8px rgba(124,58,237,0.2)" : "none",
                    }}
                  >
                    <span>{icon}</span>{label}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Notes */}
          <div style={{ marginBottom: 12 }}>
            <Label>Anything specific? <span style={{ fontSize: 9, fontWeight: 400, textTransform: "none", letterSpacing: 0, color: "#9CA3AF" }}>(optional)</span></Label>
            <textarea
              value={form.notes}
              onChange={(e) => set("notes", e.target.value)}
              placeholder="e.g. vegetarian only, avoid monsoon season, need wheelchair access, budget for 2 kids…"
              rows={2}
              style={{ ...inputStyle, resize: "none", lineHeight: 1.6 }}
            />
          </div>

          {/* Prompt preview */}
          {canSubmit && (
            <div style={{ marginBottom: 12, padding: "9px 12px", background: "rgba(124,58,237,0.04)", borderRadius: 9, border: "1px dashed rgba(124,58,237,0.22)" }}>
              <p style={{ fontSize: 9, fontWeight: 700, color: "#7C3AED", textTransform: "uppercase", letterSpacing: "0.06em", marginBottom: 3 }}>Agent Prompt Preview</p>
              <p style={{ fontSize: 11, color: "#6B7280", lineHeight: 1.55, fontStyle: "italic" }}>"{buildPrompt(form)}"</p>
            </div>
          )}

          {/* Submit */}
          <div style={{ paddingBottom: 16 }}>
            <button
              onClick={handleSubmit}
              disabled={loading || !canSubmit}
              className="btn-primary"
              style={{ width: "100%", justifyContent: "center", fontSize: 14, padding: "13px", borderRadius: 11 }}
            >
              {loading ? (
                <><svg className="animate-spin" width="15" height="15" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="rgba(255,255,255,0.3)" strokeWidth="4" /><path fill="white" d="M4 12a8 8 0 018-8V0C5.4 0 0 5.4 0 12h4z" /></svg>Dispatching Agents…</>
              ) : canSubmit ? "Dispatch 6 Agents →" : "Select a destination to begin"}
            </button>
          </div>
        </div>
      )}

      {/* ════ SURPRISE ME ════ */}
      {tab === "surprise" && (
        <div style={{ padding: "20px 16px 16px" }}>
          <div style={{ textAlign: "center", marginBottom: 16 }}>
            <span style={{ fontSize: 34 }}>🎲</span>
            <h3 style={{ fontSize: 17, fontWeight: 700, color: "#1E1B4B", margin: "8px 0 5px" }}>Feeling adventurous?</h3>
            <p style={{ fontSize: 12, color: "#6B7280", lineHeight: 1.6 }}>
              Describe your trip vaguely — our agents will surprise you with a unique curated itinerary.
            </p>
          </div>

          {/* Example prompts */}
          <div style={{ display: "flex", flexDirection: "column", gap: 6, marginBottom: 14 }}>
            {SURPRISE_PROMPTS.map((ex) => {
              const active = surpriseText === ex;
              return (
                <button
                  key={ex}
                  onClick={() => setSurpriseText(ex)}
                  style={{
                    padding: "9px 12px", borderRadius: 9, textAlign: "left", cursor: "pointer",
                    fontFamily: "inherit", fontSize: 12, transition: "all 0.15s",
                    border: `1.5px solid ${active ? "#7C3AED" : "#E5E7EB"}`,
                    background: active ? "rgba(124,58,237,0.05)" : "white",
                    color: active ? "#7C3AED" : "#6B7280",
                    display: "flex", alignItems: "center", gap: 8,
                    lineHeight: 1.5,
                  }}
                >
                  <span style={{ fontSize: 13, flexShrink: 0 }}>{active ? "✓" : "→"}</span>
                  {ex}
                </button>
              );
            })}
          </div>

          <p style={{ fontSize: 10, fontWeight: 700, color: "#9CA3AF", textTransform: "uppercase", letterSpacing: "0.06em", textAlign: "center", marginBottom: 8 }}>— or type your own —</p>

          <textarea
            value={surpriseText}
            onChange={(e) => setSurpriseText(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSubmit(); } }}
            placeholder="e.g. Hill station trip from Bangalore, 3 days, budget under ₹20,000…"
            rows={3}
            disabled={loading}
            style={{ ...inputStyle, resize: "none", lineHeight: 1.6, marginBottom: 12, padding: "12px 14px" }}
          />

          <button
            onClick={handleSubmit}
            disabled={loading || !surpriseText.trim()}
            className="btn-primary"
            style={{ width: "100%", justifyContent: "center", fontSize: 14, padding: "13px", borderRadius: 11 }}
          >
            {loading ? (
              <><svg className="animate-spin" width="15" height="15" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="rgba(255,255,255,0.3)" strokeWidth="4" /><path fill="white" d="M4 12a8 8 0 018-8V0C5.4 0 0 5.4 0 12h4z" /></svg>Dispatching Agents…</>
            ) : "Surprise Me! 🎲"}
          </button>
        </div>
      )}
    </div>
  );
}
