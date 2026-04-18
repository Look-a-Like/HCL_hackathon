"use client";

import { BookingOptions } from "@/lib/types";

function FlightCard({ flight, i }: { flight: BookingOptions["flights"][0]; i: number }) {
  const [from, to] = (flight.route ?? "").split(" → ");
  return (
    <div className="slide-up card-flat" style={{ padding: 16, animationDelay: `${i * 0.1}s` }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <div style={{ width: 28, height: 28, borderRadius: "50%", background: "linear-gradient(135deg, #7C3AED, #8B5CF6)", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M17.8 19.2L16 11l3.5-3.5C21 6 21 4 19.5 2.5S18 2 16.5 3.5L13 7l-8.2-1.8L3 7l7 4-2 3-4-1-1 1 3 2 2 3 1-1-1-4 3-2 4 7 2-1.2z" />
            </svg>
          </div>
          <span style={{ fontWeight: 700, fontSize: 13, color: "#1E1B4B" }}>{flight.name}</span>
        </div>
        <span style={{ padding: "2px 8px", borderRadius: 999, background: "#EDE9FE", fontSize: 10, fontWeight: 700, color: "#7C3AED", border: "1px solid #DDD6FE", textTransform: "uppercase", letterSpacing: "0.04em" }}>Hold 24h</span>
      </div>

      {from && to && (
        <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 8 }}>
          <span style={{ fontWeight: 700, fontSize: 14, color: "#1E1B4B" }}>{from.trim()}</span>
          <div style={{ flex: 1, position: "relative", borderTop: "1.5px dashed #E5E7EB", margin: "0 4px" }}>
            {flight.duration && (
              <span style={{ position: "absolute", top: "50%", left: "50%", transform: "translate(-50%, -50%)", background: "white", padding: "0 4px", fontSize: 10, color: "#9CA3AF" }}>
                {flight.duration}
              </span>
            )}
          </div>
          <span style={{ fontWeight: 700, fontSize: 14, color: "#1E1B4B" }}>{to.trim()}</span>
        </div>
      )}

      {flight.departure && flight.arrival && (
        <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, color: "#9CA3AF", marginBottom: 12 }}>
          <span>{flight.departure}</span><span>{flight.arrival}</span>
        </div>
      )}

      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <span style={{ fontSize: 15, fontWeight: 800, color: "#1E1B4B" }}>₹{flight.price?.toLocaleString("en-IN")}</span>
        <button className="btn-primary" style={{ padding: "8px 16px", fontSize: 12 }}>
          Confirm Flight →
        </button>
      </div>
    </div>
  );
}

function HotelCard({ hotel, i }: { hotel: BookingOptions["hotels"][0]; i: number }) {
  return (
    <div className="slide-up card-flat" style={{ padding: 16, display: "flex", gap: 12, animationDelay: `${i * 0.1 + 0.15}s` }}>
      <div style={{ width: 60, height: 60, borderRadius: 12, background: "linear-gradient(135deg, #EDE9FE, #DDD6FE)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 24, flexShrink: 0 }}>
        🏨
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <p style={{ fontWeight: 700, fontSize: 13, color: "#1E1B4B" }}>{hotel.name}</p>
        <p style={{ fontSize: 11, color: "#6B7280", marginTop: 2 }}>{hotel.notes ?? ""}</p>
        <div style={{ display: "flex", alignItems: "center", gap: 3, marginTop: 4 }}>
          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#059669" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="20 6 9 17 4 12" />
          </svg>
          <span style={{ fontSize: 11, fontWeight: 600, color: "#059669" }}>Agent Negotiated Rate</span>
        </div>
        {(hotel.rating ?? 0) > 0 && (
          <div style={{ display: "flex", gap: 1, marginTop: 4 }}>
            {[1,2,3,4,5].map((n) => (
              <span key={n} style={{ fontSize: 10, color: n <= Math.round(hotel.rating!) ? "#7C3AED" : "#E5E7EB" }}>★</span>
            ))}
          </div>
        )}
      </div>
      <div style={{ textAlign: "right", flexShrink: 0 }}>
        <p style={{ fontSize: 15, fontWeight: 800, color: "#1E1B4B" }}>₹{hotel.price?.toLocaleString("en-IN")}</p>
        <p style={{ fontSize: 10, color: "#9CA3AF" }}>/night</p>
      </div>
    </div>
  );
}

export default function BookingList({ bookings }: { bookings: BookingOptions }) {
  const hasFlights = (bookings.flights?.length ?? 0) > 0;
  const hasHotels = (bookings.hotels?.length ?? 0) > 0;
  if (!hasFlights && !hasHotels) return null;

  return (
    <div style={{ background: "#FFFFFF", border: "1px solid #E5E7EB", borderRadius: 16, boxShadow: "0 4px 16px rgba(109,40,217,0.08)", padding: "20px" }}>
      <h3 style={{ fontWeight: 700, fontSize: 15, color: "#1E1B4B", marginBottom: 14 }}>Pending Confirmations</h3>
      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {bookings.flights?.map((f, i) => <FlightCard key={i} flight={f} i={i} />)}
        {bookings.hotels?.map((h, i) => <HotelCard key={i} hotel={h} i={i} />)}
      </div>
    </div>
  );
}
