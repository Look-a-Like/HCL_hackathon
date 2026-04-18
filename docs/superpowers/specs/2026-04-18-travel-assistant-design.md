# Design Spec — Agentic AI Travel Planning Assistant
**Date:** 2026-04-18  
**Status:** Approved for implementation

---

## Key Updates & Lock-Ins

1. **Framework & Architecture Lock-In:** The system will be built using LangGraph instead of CrewAI. This decision was driven by LangGraph's explicit state control and ability to visualize the graph for step-by-step debugging. LangGraph is noted as being more production-ready, which is critical for a demo that cannot break live.
2. **Explicit State Management (TravelState):** Instead of agents passing unstructured messages, the architecture now centers around a highly structured, shared state object. A `TravelState` class defined as a `TypedDict` acts as the single source of truth flowing through the graph edges. It captures the initial user input and tracks extracted constraints like budget, duration, and destination. It explicitly includes an errors list to accumulate faults, allowing the Planner Agent to retry or skip failed nodes.
3. **Parallel Graph Routing:** The workflow has evolved from a purely sequential list into a true graph structure with parallel execution. The Planner Agent acts as the Supervisor. The destination and budget agents are executed in parallel after the planner establishes the constraints. Once both are complete, their data flows into the itinerary agent, which then feeds into the booking and local_experience agents.
4. **Specific Technology Stack Selection:** 
   - Orchestrator LLM: `claude-sonnet-4-6` for the Planner Agent.
   - Worker LLM: `claude-haiku-4-5` for specialized task agents.
   - Language & Infrastructure: Python 3.11+, deployed on Render's free tier, frontend in Streamlit.
5. **Mock Data Strategy (Hackathon Constraints):** The architecture relies on local mock JSON files containing curated Indian destinations, hotel tiers, and flight costs to avoid API limits. A free web search tool like DuckDuckGo or Tavily will be integrated for live data enrichment.
6. **Enhanced UI Streaming:** The Streamlit app will utilize a chat-style input and stream the progress of the agents. As the `StateGraph` executes, the UI will display exactly which agent is currently working and output successes as they complete their tasks.

---

## 1. Problem Statement

Travel planning is fragmented: users manually search destinations, compare prices, build itineraries, and manage bookings across multiple platforms. The solution is a multi-agent AI system where each agent owns one responsibility, and a Planner Agent orchestrates the whole flow — delivering a complete, budget-aware, personalized travel plan from a single natural language request.

---

## 2. Why This Architecture

This design separates **orchestration** (Planner) from **execution** (specialist agents), which enables:
- **Modular scaling** — any agent can be upgraded independently without touching the pipeline
- **Parallel execution** — Destination and Budget agents run concurrently, cutting latency
- **Fault isolation** — one agent failing doesn't collapse the whole plan
- **Observability** — each agent's input/output is inspectable in the shared state

The Planner is a controller + validator, not just a router. It validates inputs before dispatching, tracks retries per agent, and assembles the final structured output.

---

## 3. Architecture Decision: LangGraph (not CrewAI)

**Chosen: LangGraph**

| | LangGraph | CrewAI |
|---|---|---|
| State control | Explicit typed state object passed between nodes | Implicit, agent-managed |
| Debugging | Full graph visualization, step-by-step tracing | Harder to trace |
| Async/parallel | Native `asyncio` support, parallel branches | Limited |
| Production-readiness | High | Medium |

LangGraph gives us a `StateGraph` where each agent is a node, state flows through typed edges, and the Planner routes conditionally. This makes the pipeline transparent and debuggable — critical for a live demo.

---

## 4. System Architecture

### Agent Roles

```
User Input (natural language)
        │
        ▼
┌──────────────────────────────────────┐
│            Planner Agent             │  ← Orchestrator + Controller + Validator
│  - Intent classification             │    Sonnet (reasoning model)
│  - Entity extraction (budget/dates)  │
│  - Missing field detection           │
│  - Retry orchestration               │
│  - Final plan assembly               │
└────────────────┬─────────────────────┘
                 │
     ┌───────────┴────────────┐
     │ (parallel dispatch)    │
     ▼                        ▼
┌──────────────┐   ┌───────────────────────┐
│ Destination  │   │  Budget Optimization  │
│ Research     │   │  Agent                │
│ Agent        │   │  - Cost estimation    │
│ - Attractions│   │  - Budget breakdown   │
│ - Seasons    │   │  - Cost-saving options│
└──────┬───────┘   └───────────┬───────────┘
       └──────────┬────────────┘
                  │ (both complete before proceeding)
                  ▼
       ┌──────────────────────┐
       │    Itinerary Agent   │
       │ - Day-by-day schedule│
       │ - Route optimization │
       │ - Timing between stops│
       └──────────┬───────────┘
                  │
     ┌────────────┴────────────┐
     │ (parallel dispatch)     │
     ▼                         ▼
┌──────────────────┐  ┌─────────────────────────┐
│ Booking Assistant│  │  Local Experience Agent  │
│ - Ranked flights │  │  - Food, events, gems    │
│ - Ranked hotels  │  │  - Personalized per      │
│ - Budget-filtered│  │    user interests        │
└──────────────────┘  └─────────────────────────┘
          │                      │
          └──────────┬───────────┘
                     │
                     ▼
          ┌────────────────────┐
          │   Final Output     │
          │ (structured dict   │
          │  → Next.js UI)     │
          └────────────────────┘
```

### State Object

```python
class TravelState(TypedDict):
    # Input
    user_input: str
    conversation_history: list[str]   # Enables iterative refinement ("make it cheaper")

    # Extracted by Planner
    budget: float
    duration_days: int
    destination: str
    interests: list[str]
    travel_dates: str
    missing_fields: list[str]         # Triggers follow-up question if non-empty

    # Agent outputs
    destination_info: dict
    budget_breakdown: dict
    itinerary: list[dict]
    booking_options: dict             # Ranked by budget proximity
    local_experiences: list[dict]

    # Final structured output (not a string — renderable by frontend)
    final_plan: dict                  # {summary, itinerary, budget, bookings, experiences}

    # Reliability
    errors: list[str]
    retries: dict[str, int]           # {"destination": 1, "budget": 0, ...}

    # Observability
    metrics: dict                     # {latency_per_agent, cost_per_agent, completeness_score}
```

---

## 5. Technology Stack

| Component | Choice | Reason |
|-----------|--------|--------|
| Agent framework | **LangGraph** | Explicit state, parallel branches, async-native |
| Orchestrator LLM | **claude-sonnet-4-6** | Reasoning for planning, validation, routing |
| Worker LLM | **claude-haiku-4-5** | Fast + cheap for generation tasks (`max_tokens=400, temperature=0.3`) |
| Backend | **FastAPI** | Python, streams LangGraph events via SSE |
| Frontend | **Next.js + shadcn/ui** | Professional UI, streaming-ready, Vercel deploy |
| Travel data | **Mock JSON + DuckDuckGo** | No paid API needed |
| Frontend deploy | **Vercel** | One-command deploy, free tier |
| Backend deploy | **Render (free tier)** | Python backend, Docker-based |
| Language | **Python 3.11+ / TypeScript** | ML backend / React frontend |

---

## 6. Project File Structure

```
HCL_hackathon/
│
├── backend/
│   ├── main.py                         # FastAPI app + /plan SSE endpoint + rate limiting
│   ├── requirements.txt
│   ├── .env                            # ANTHROPIC_API_KEY
│   ├── .env.example
│   │
│   ├── graph/
│   │   ├── state.py                    # TravelState TypedDict
│   │   ├── workflow.py                 # LangGraph StateGraph (parallel branches)
│   │   └── router.py                   # Conditional routing + retry logic
│   │
│   ├── agents/
│   │   ├── planner.py                  # Intent classification + validation + assembly
│   │   ├── destination.py
│   │   ├── budget.py
│   │   ├── itinerary.py
│   │   ├── booking.py                  # Includes ranking logic
│   │   └── local_experience.py
│   │
│   ├── tools/
│   │   ├── search.py                   # DuckDuckGo free search
│   │   ├── travel_data.py              # Mock JSON loader
│   │   └── ranking.py                  # Hotel/flight ranking by budget proximity
│   │
│   ├── middleware/
│   │   ├── rate_limit.py               # SlowAPI rate limiter
│   │   └── guard.py                    # Prompt injection detection
│   │
│   ├── prompts/
│   │   └── *.py                        # One prompt file per agent
│   │
│   └── data/
│       ├── destinations.json
│       ├── hotels.json
│       └── flights.json
│
└── frontend/
    ├── app/
    │   ├── page.tsx                    # Home — chat input
    │   ├── layout.tsx
    │   └── api/plan/route.ts           # Next.js proxy → FastAPI (avoids CORS)
    │
    ├── components/
    │   ├── ChatInput.tsx
    │   ├── AgentProgress.tsx           # Live step tracker (6 agents)
    │   ├── ItineraryCard.tsx
    │   ├── BudgetBreakdown.tsx         # Chart component
    │   ├── BookingOptions.tsx
    │   └── MetricsBadge.tsx            # Latency + cost display
    │
    ├── lib/
    │   └── stream.ts
    │
    └── .env.local
```

---

## 7. Key Implementation Details

### Planner Agent — Full Responsibilities

```python
def planner_agent(state: TravelState) -> TravelState:
    # 1. Prompt injection guard
    if is_injection(state["user_input"]):
        state["errors"].append("Invalid input detected")
        return state

    # 2. Intent classification + entity extraction
    extracted = claude_sonnet.invoke(PLANNER_PROMPT.format(input=state["user_input"]))
    state.update(extracted)  # budget, destination, dates, interests

    # 3. Missing field detection — ask follow-up instead of guessing
    state["missing_fields"] = [f for f in ["budget", "destination"] if not state.get(f)]

    # 4. Conversation memory — support "make it cheaper" on second turn
    state["conversation_history"].append(state["user_input"])

    return state
```

### Parallel Execution (Destination + Budget simultaneously)

```python
# workflow.py — parallel branches reduce latency
workflow.add_edge("planner", "destination")
workflow.add_edge("planner", "budget")        # fires at the same time as destination
workflow.add_edge("destination", "itinerary") # itinerary waits for BOTH
workflow.add_edge("budget", "itinerary")
workflow.add_edge("itinerary", "booking")
workflow.add_edge("itinerary", "local_experience")  # also parallel
```

### Retry + Fallback per Agent

```python
# router.py
MAX_RETRIES = 2

def with_retry(agent_fn, agent_name: str):
    def wrapper(state: TravelState) -> TravelState:
        retries = state["retries"].get(agent_name, 0)
        try:
            return agent_fn(state)
        except Exception as e:
            if retries < MAX_RETRIES:
                state["retries"][agent_name] = retries + 1
                return wrapper(state)  # retry
            else:
                state["errors"].append(f"{agent_name} failed after {MAX_RETRIES} retries")
                return apply_fallback(state, agent_name)  # use mock data
    return wrapper
```

### Booking Agent — Ranked Recommendations

```python
# tools/ranking.py
def rank_options(options: list[dict], budget: float, key: str) -> list[dict]:
    """Rank by proximity to target budget — not just cheapest."""
    return sorted(options, key=lambda x: abs(x[key] - budget))[:3]

# booking.py
def booking_agent(state: TravelState) -> TravelState:
    hotels = load_hotels(state["destination"])
    flights = load_flights(state["destination"])
    hotel_budget = state["budget_breakdown"].get("hotel", state["budget"] * 0.4)
    state["booking_options"] = {
        "hotels": rank_options(hotels, hotel_budget, "price_per_night"),
        "flights": rank_options(flights, state["budget_breakdown"].get("transport", 0), "price"),
    }
    return state
```

### Metrics Collection

```python
# Every agent wrapper records latency + estimated token cost
import time

def tracked(agent_fn, agent_name: str):
    def wrapper(state: TravelState) -> TravelState:
        start = time.time()
        state = agent_fn(state)
        state["metrics"]["latency"][agent_name] = round(time.time() - start, 2)
        return state
    return wrapper
```

### Structured Final Output (dict, not string)

```python
# planner.py — final assembly
state["final_plan"] = {
    "summary": f"{state['duration_days']}-day trip to {state['destination']}",
    "itinerary": state["itinerary"],          # list of day objects
    "budget": state["budget_breakdown"],
    "bookings": state["booking_options"],
    "experiences": state["local_experiences"],
    "metrics": {
        "latency_total": sum(state["metrics"]["latency"].values()),
        "completeness_score": compute_completeness(state),
    }
}
```

### Security Middleware

```python
# middleware/guard.py
INJECTION_PATTERNS = ["ignore previous", "forget instructions", "you are now", "system:"]

def is_injection(text: str) -> bool:
    return any(p in text.lower() for p in INJECTION_PATTERNS)

# main.py — rate limiting via SlowAPI
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/plan")
@limiter.limit("5/minute")
async def plan(request: PlanRequest): ...
```

### FastAPI SSE Streaming

```python
@app.post("/plan")
async def plan(request: PlanRequest):
    async def event_stream():
        for step in langgraph_app.stream(initial_state):
            agent_name = list(step.keys())[0]
            yield f"data: {json.dumps({'agent': agent_name, 'output': step[agent_name]})}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

### Next.js SSE Consumer

```typescript
export async function streamPlan(query: string, onChunk: (data: any) => void) {
  const res = await fetch("/api/plan", { method: "POST", body: JSON.stringify({ query }) });
  const reader = res.body!.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    for (const line of decoder.decode(value).split("\n\n")) {
      if (line.startsWith("data: ")) onChunk(JSON.parse(line.slice(6)));
    }
  }
}
```

---

## 8. Implementation Order (Hackathon Sequence)

### Phase 1 — Skeleton (45 min)
1. `backend/graph/state.py` — full `TravelState` including metrics + retries
2. `backend/agents/planner.py` — input parsing + validation + missing fields
3. `backend/graph/workflow.py` — single-node graph, planner only
4. `backend/main.py` — FastAPI `/plan` with SSE + rate limiter
5. `frontend/` — `npx create-next-app`, shadcn/ui, text input → stream display

**Verify:** App runs, planner extracts structured data, streams to browser.

### Phase 2 — Core Agents (1.5 hrs)
6. `backend/agents/destination.py`
7. `backend/agents/budget.py`
8. Wire both in parallel into graph + add `tracked()` + `with_retry()` wrappers
9. `backend/agents/itinerary.py`

**Verify:** "Plan a 3-day trip to Goa for ₹15,000" → structured itinerary with metrics.

### Phase 3 — Enrichment Agents (1 hr)
10. `backend/tools/ranking.py` + `backend/agents/booking.py` with ranked output
11. `backend/agents/local_experience.py`
12. Wire both in parallel after itinerary

**Verify:** Full 7-step workflow end to end, `final_plan` is a complete dict.

### Phase 4 — Frontend Polish (1.5 hrs)
13. `AgentProgress.tsx` — live step tracker with checkmarks
14. `ItineraryCard.tsx`, `BudgetBreakdown.tsx`, `BookingOptions.tsx`
15. `MetricsBadge.tsx` — show total latency + completeness score
16. Conversation memory: input box persists history, supports "make it cheaper"

### Phase 5 — Deploy (30 min)
17. `backend/` → Render (add `render.yaml`)
18. `frontend/` → Vercel (`vercel deploy`)

---

## 9. Mock Data Strategy

- **`destinations.json`** — 10-15 Indian destinations: attractions, avg costs, best season
- **`hotels.json`** — budget/mid/luxury tiers per destination with price_per_night
- **`flights.json`** — city pairs with approximate prices (INR)
- **DuckDuckGo search** — live enrichment fallback if mock doesn't match destination

Demo pitch: *"Mock data simulates real APIs. In production, swap for Skyscanner / Google Places — the agent interfaces stay identical."*

---

## 10. Example Full Flow

**Input:** `"Plan a 3-day budget trip to Goa for ₹20,000 — I like beaches and local food"`

| Step | Agent | Output |
|------|-------|--------|
| 1 | Planner | `{destination: "Goa", budget: 20000, days: 3, interests: ["beaches", "local food"], missing_fields: []}` |
| 2+3 | Destination + Budget (parallel) | Attractions + `{transport: ₹6000, hotel: ₹7500, food: ₹4500, buffer: ₹2000}` |
| 4 | Itinerary | Day 1: North Goa → Day 2: Dudhsagar → Day 3: Markets |
| 5+6 | Booking + Local Experience (parallel) | Ranked hotels/flights + food/events list |
| 7 | Final plan dict | Completeness: 0.94, Total latency: 4.2s |

---

## 11. Demo Day — Defend These Points

| Question | Answer |
|----------|--------|
| "What if an agent fails?" | Retry up to 2× per agent; fallback to mock data; error logged in state |
| "Why LangGraph?" | Explicit typed state, parallel branches, full graph visualization — debuggable in production |
| "Why not real APIs?" | Interfaces are API-agnostic; swap mock loader for Skyscanner SDK without changing agents |
| "How do you measure quality?" | Completeness score + latency per agent tracked in `state["metrics"]` |
| "Can users refine the plan?" | Yes — `conversation_history` enables "make it cheaper" on follow-up turns |
| "Is it safe?" | Rate limiting (5 req/min), prompt injection detection, input validation before any LLM call |
| "Why Haiku for workers?" | Cost optimization — non-reasoning tasks don't need Sonnet; `max_tokens=400, temperature=0.3` |

---

*This design is locked. Proceed to implementation.*
