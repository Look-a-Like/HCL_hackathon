export type AgentStatus = "idle" | "running" | "done" | "error";

export interface AgentEvent {
  type: "agent_start" | "agent_done" | "agent_error" | "final_plan" | "error";
  agent?: string;
  data?: unknown;
  error?: string;
}

export interface BudgetBreakdown {
  flights: number;
  hotel: number;
  activities: number;
  food: number;
  transport: number;
  misc: number;
  total: number;
  currency: string;
}

export interface BookingOption {
  name: string;
  price: number;
  rating?: number;
  notes?: string;
  route?: string;
  duration?: string;
  departure?: string;
  arrival?: string;
  book_url?: string;
  search_url?: string;
  maps_url?: string;
}

export interface BookingOptions {
  flights: BookingOption[];
  hotels: BookingOption[];
}

export interface LocalGem {
  name: string;
  type: string;
  description: string;
  tip?: string;
  maps_url?: string;
  tripadvisor_url?: string;
  estimated_cost?: string;
}

export interface ItineraryDay {
  day: number;
  date?: string;
  theme: string;
  morning: string;
  afternoon: string;
  evening: string;
  meals: { breakfast?: string; lunch?: string; dinner?: string };
  estimated_cost: number;
}

export interface Metrics {
  total_latency_ms?: number;
  per_agent?: Record<string, number>;
  completeness_score?: number;
}

export interface FinalPlan {
  destination: string;
  trip_duration: string;
  travel_style: string;
  budget_breakdown: BudgetBreakdown;
  itinerary: ItineraryDay[];
  booking_options: BookingOptions;
  local_gems: LocalGem[];
  weather_notes?: string;
  packing_tips?: string[];
  emergency_contacts?: string[];
  metrics?: Metrics;
  summary?: string;
}

export interface AgentState {
  planner: AgentStatus;
  destination: AgentStatus;
  budget: AgentStatus;
  itinerary: AgentStatus;
  booking: AgentStatus;
  local_experience: AgentStatus;
}

export interface FeedMessage {
  id: string;
  agent: string;
  title: string;
  body: string;
  highlight?: { label: string; title: string; detail: string };
}

export const AGENT_LABELS: Record<string, string> = {
  planner:          "Master Planner",
  destination:      "Destinations",
  budget:           "Budget Optimizer",
  itinerary:        "Itinerary Builder",
  booking:          "Booking Agent",
  local_experience: "Local Oracle",
};

export const AGENT_DESCRIPTIONS: Record<string, string> = {
  planner:          "Synthesizing inputs and directing sub-agents for optimal routing.",
  destination:      "Scouting top destinations based on your preferences.",
  budget:           "Analyzing cost breakdowns and optimizing allocation.",
  itinerary:        "Crafting a day-by-day schedule with curated activities.",
  booking:          "Sourcing best-fit flights and accommodation options.",
  local_experience: "Curating hidden gems and insider recommendations.",
};

export const AGENT_ORDER: Array<keyof AgentState> = [
  "planner", "destination", "budget", "itinerary", "booking", "local_experience",
];
