# Design Spec — Agentic AI Travel Planning Assistant
**Date:** 2026-04-18  
**Status:** Approved for implementation

---

## 1. Problem Statement

Travel planning is fragmented: users manually search destinations, compare prices, build itineraries, and manage bookings across multiple platforms. The solution is a multi-agent AI system where each agent owns one responsibility, and a Planner Agent orchestrates the whole flow — delivering a complete, budget-aware, personalized travel plan from a single natural language request.

---

## 2. Architecture Decision: LangGraph (not CrewAI)

**Chosen: LangGraph**

| | LangGraph | CrewAI |
|---|---|---|
| State control | Explicit typed state object passed between nodes | Implicit, agent-managed |
| Debugging | Full graph visualization, step-by-step tracing | Harder to trace |
| Hackathon speed | Medium setup, high payoff | Fast setup, low control |
| Production-readiness | High | Medium |

LangGraph gives us a `StateGraph` where each agent is a node, state flows through edges, and the Planner routes conditionally. This makes the agent pipeline transparent and debuggable — critical for a demo that needs to not break live.

---

## 3. System Architecture

### Agent Roles

```
User Input (natural language)
        │
        ▼
┌─────────────────┐
│  Planner Agent  │  ← Orchestrator. Parses intent, routes to agents, assembles final output.
│  (Supervisor)   │    Uses reasoning model (claude-opus-4-7 or o3).
└────────┬────────┘
         │ dispatches to (sequentially):
    ┌────┴─────────────────────────────────────────┐
    │                                              │
    ▼                                              ▼
┌───────────────────────┐          ┌───────────────────────┐
│ Destination Research  │          │   Budget Optimization  │
│       Agent           │          │        Agent           │
│ - Suggests destination│          │ - Estimates costs       │
│ - Key attractions     │          │ - Cost-saving options  │
│ - Travel seasons      │          │ - Validates affordability│
└───────────────────────┘          └───────────────────────┘
         │                                        │
         └──────────────────┬─────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │     Itinerary Agent      │
              │ - Day-by-day schedule    │
              │ - Route optimization     │
              │ - Timing between stops   │
              └────────────┬────────────┘
                           │
              ┌────────────┴────────────┐
              │                        │
              ▼                        ▼
┌─────────────────────┐   ┌──────────────────────────┐
│  Booking Assistant  │   │  Local Experience Agent   │
│       Agent         │   │ - Food, events, hidden    │
│ - Flight options    │   │   gems                    │
│ - Hotel options     │   │ - Personalized based on   │
│ - Transport options │   │   user interests          │
└─────────────────────┘   └──────────────────────────┘
              │                        │
              └────────────┬───────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │     Final Output         │
              │  Complete Travel Plan    │
              │  (structured JSON →      │
              │   rendered in Streamlit) │
              └─────────────────────────┘
```

### State Object (shared across all agents)

```python
class TravelState(TypedDict):
    user_input: str              # Raw user request
    budget: float                # Extracted budget
    duration_days: int           # Trip duration
    destination: str             # Confirmed destination
    interests: list[str]         # User interests/preferences
    travel_dates: str            # Travel dates if provided
    
    destination_info: dict       # Output of Destination Agent
    budget_breakdown: dict       # Output of Budget Agent
    itinerary: list[dict]        # Output of Itinerary Agent (day-by-day)
    booking_options: dict        # Output of Booking Agent
    local_experiences: list[dict]# Output of Local Experience Agent
    
    final_plan: str              # Assembled final output
    errors: list[str]            # Error accumulation
```

---

## 4. Technology Stack (Final Decisions)

| Component | Choice | Reason |
|-----------|--------|--------|
| Agent framework | **LangGraph** | Explicit state, conditional routing, debuggable |
| Orchestrator LLM | **claude-sonnet-4-6** | Best reasoning for planning/coordination |
| Worker LLM | **claude-haiku-4-5** | Fast, cheap for generation tasks |
| Backend | **FastAPI** | Python, streams LangGraph agent events via SSE |
| Frontend | **Next.js + shadcn/ui** | Professional UI, built-in streaming, Vercel AI SDK |
| Travel data | **Mock JSON + web search tool** | No paid API budget needed |
| Frontend deploy | **Vercel** | One-command deploy, free tier |
| Backend deploy | **Render (free tier)** | Python backend, easy Docker deploy |
| Language | **Python 3.11+ / TypeScript** | ML backend / React frontend |

---

## 5. Project File Structure

```
HCL_hackathon/
│
├── backend/                            # Python — FastAPI + LangGraph
│   ├── main.py                         # FastAPI app, /plan SSE endpoint
│   ├── requirements.txt
│   ├── .env                            # ANTHROPIC_API_KEY
│   ├── .env.example
│   │
│   ├── graph/
│   │   ├── state.py                    # TravelState TypedDict
│   │   ├── workflow.py                 # LangGraph StateGraph assembly
│   │   └── router.py                   # Planner routing logic
│   │
│   ├── agents/
│   │   ├── planner.py
│   │   ├── destination.py
│   │   ├── budget.py
│   │   ├── itinerary.py
│   │   ├── booking.py
│   │   └── local_experience.py
│   │
│   ├── tools/
│   │   ├── search.py                   # DuckDuckGo free search
│   │   └── travel_data.py              # Mock JSON loader
│   │
│   ├── prompts/
│   │   └── *.py                        # One file per agent
│   │
│   └── data/
│       ├── destinations.json
│       ├── hotels.json
│       └── flights.json
│
└── frontend/                           # Next.js — React + shadcn/ui
    ├── app/
    │   ├── page.tsx                    # Home — chat input
    │   ├── layout.tsx
    │   └── api/
    │       └── plan/
    │           └── route.ts            # Proxies to FastAPI (avoids CORS)
    │
    ├── components/
    │   ├── ChatInput.tsx               # User query input
    │   ├── AgentProgress.tsx           # Live agent step tracker
    │   ├── ItineraryCard.tsx           # Day-by-day display
    │   ├── BudgetBreakdown.tsx         # Budget pie/bar chart
    │   └── BookingOptions.tsx          # Flight + hotel cards
    │
    ├── lib/
    │   └── stream.ts                   # SSE stream reader utility
    │
    ├── package.json
    └── .env.local                      # NEXT_PUBLIC_API_URL
```

---

## 6. Implementation Order (Hackathon Sequence)

Build in this order — each step produces something runnable:

### Phase 1 — Skeleton (get something running first)
1. `backend/graph/state.py` — define `TravelState`
2. `backend/agents/planner.py` — parse user input, extract budget/destination/dates
3. `backend/graph/workflow.py` — single-node graph, planner only
4. `backend/main.py` — FastAPI `/plan` endpoint streaming SSE
5. `frontend/` — `npx create-next-app`, install shadcn/ui, simple text input → fetch `/plan`

**Verify:** App runs, user types a request, planner extracts structured data streamed to browser.

### Phase 2 — Core Agents
5. `src/agents/destination.py` — given destination, return attractions + info
6. `src/agents/budget.py` — given budget + destination, return breakdown
7. `src/agents/itinerary.py` — given attractions + duration, return day-by-day plan
8. Wire all three into the graph

**Verify:** "Plan a 3-day trip to Goa for ₹15,000" returns a structured itinerary.

### Phase 3 — Enrichment Agents
9. `src/agents/booking.py` — suggest flights, hotels with mock data
10. `src/agents/local_experience.py` — recommend food/events per destination
11. Wire into graph

**Verify:** Full 7-step workflow executes end to end.

### Phase 4 — Frontend Polish
12. Streamlit UI with:
    - Chat-style input
    - Streaming agent progress (show which agent is working)
    - Formatted output: itinerary cards, budget breakdown, booking options
13. Add error handling for bad inputs

### Phase 5 — Deploy
14. `requirements.txt`, `Dockerfile` or `render.yaml`
15. Push to GitHub → connect to Render

---

## 7. Key Implementation Details

### LangGraph Workflow Pattern

```python
# workflow.py pattern
from langgraph.graph import StateGraph, END

workflow = StateGraph(TravelState)

workflow.add_node("planner", planner_agent)
workflow.add_node("destination", destination_agent)
workflow.add_node("budget", budget_agent)
workflow.add_node("itinerary", itinerary_agent)
workflow.add_node("booking", booking_agent)
workflow.add_node("local_experience", local_experience_agent)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "destination")
workflow.add_edge("planner", "budget")          # destination + budget run in parallel
workflow.add_edge("destination", "itinerary")
workflow.add_edge("budget", "itinerary")
workflow.add_edge("itinerary", "booking")
workflow.add_edge("itinerary", "local_experience")
workflow.add_edge("booking", END)
workflow.add_edge("local_experience", END)

app = workflow.compile()
```

### Agent Pattern (same for all agents)

```python
# Each agent follows this pattern
def destination_agent(state: TravelState) -> TravelState:
    prompt = build_destination_prompt(state)
    response = claude_haiku.invoke(prompt)
    state["destination_info"] = parse_response(response)
    return state
```

### FastAPI SSE Streaming Pattern

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import json

app = FastAPI()

@app.post("/plan")
async def plan(request: PlanRequest):
    async def event_stream():
        for step in langgraph_app.stream(initial_state):
            agent_name = list(step.keys())[0]
            yield f"data: {json.dumps({'agent': agent_name, 'state': step})}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

### Next.js SSE Consumer Pattern

```typescript
// frontend/lib/stream.ts
export async function streamPlan(query: string, onChunk: (data: any) => void) {
  const res = await fetch("/api/plan", { method: "POST", body: JSON.stringify({ query }) });
  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const lines = decoder.decode(value).split("\n\n");
    for (const line of lines) {
      if (line.startsWith("data: ")) onChunk(JSON.parse(line.slice(6)));
    }
  }
}
```

---

## 8. Mock Data Strategy (No Paid APIs Needed)

Instead of real travel APIs (expensive/rate-limited), use:
- **`data/sample_destinations.json`** — 10-15 Indian destinations with attractions, costs, best season
- **`data/sample_hotels.json`** — budget/mid/luxury tiers per destination
- **`data/sample_flights.json`** — approximate flight costs between major cities
- **Web search tool** (DuckDuckGo free API) for live enrichment if needed

This is enough for the demo. Be ready to explain in the interview: "In production, we'd swap mock data for Skyscanner API / Google Places API."

---

## 9. Example Full Flow

**Input:** `"Plan a 3-day budget trip to Goa for ₹20,000 — I like beaches and local food"`

| Step | Agent | Output |
|------|-------|--------|
| 1 | Planner | `{destination: "Goa", budget: 20000, days: 3, interests: ["beaches", "local food"]}` |
| 2 | Destination | Baga Beach, Dudhsagar Falls, Anjuna Market, Fort Aguada |
| 3 | Budget | `{transport: ₹6000, hotel: ₹7500, food: ₹3000, activities: ₹2500, buffer: ₹1000}` |
| 4 | Itinerary | Day 1: North Goa beaches → Day 2: Dudhsagar + spice farm → Day 3: markets + south Goa |
| 5 | Booking | SpiceJet BOM-GOI ₹3200, Zostel Goa ₹800/night |
| 6 | Local Experience | Fisherman's Wharf for seafood, Saturday Night Market, beach shacks |
| 7 | Output | Complete formatted plan |

---

## 10. What to Know for Demo Day

- Know the state that flows between agents — they will ask "what happens if an agent fails?"
- Answer: errors accumulate in `state["errors"]`, Planner can retry or skip
- Know why LangGraph over CrewAI (control, debuggability, production-readiness)
- Know why Streamlit (fastest frontend for ML demos, not for production)
- Know the upgrade path: swap mock data → real APIs, Streamlit → React frontend, Render → GCP/AWS

---

*This design is locked. Proceed to implementation.*
