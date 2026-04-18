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
| Frontend | **Streamlit** | Fastest to build, streaming support |
| Travel data | **Mock JSON + web search tool** | No paid API budget needed |
| Deployment | **Render (free tier)** | Easier than Vercel for Python backend |
| Language | **Python 3.11+** | ML standard |

---

## 5. Project File Structure

```
HCL_hackathon/
├── app.py                          # Streamlit frontend entry point
├── requirements.txt
├── .env                            # API keys (ANTHROPIC_API_KEY)
├── .env.example                    # Template (committed)
│
├── src/
│   ├── graph/
│   │   ├── state.py                # TravelState TypedDict definition
│   │   ├── workflow.py             # LangGraph StateGraph assembly
│   │   └── router.py              # Planner routing logic
│   │
│   ├── agents/
│   │   ├── planner.py              # Supervisor agent — parses input, routes
│   │   ├── destination.py          # Destination research agent
│   │   ├── budget.py               # Budget optimization agent
│   │   ├── itinerary.py            # Day-by-day itinerary agent
│   │   ├── booking.py              # Booking assistant agent
│   │   └── local_experience.py     # Local experience agent
│   │
│   ├── tools/
│   │   ├── search.py               # Web search tool (DuckDuckGo or Tavily free)
│   │   ├── travel_data.py          # Mock travel data (flights, hotels, costs)
│   │   └── formatter.py            # Format final plan for display
│   │
│   └── prompts/
│       ├── planner_prompt.py
│       ├── destination_prompt.py
│       ├── budget_prompt.py
│       ├── itinerary_prompt.py
│       ├── booking_prompt.py
│       └── local_experience_prompt.py
│
└── data/
    ├── sample_destinations.json    # Curated destination data
    ├── sample_hotels.json          # Mock hotel options
    └── sample_flights.json         # Mock flight options
```

---

## 6. Implementation Order (Hackathon Sequence)

Build in this order — each step produces something runnable:

### Phase 1 — Skeleton (get something running first)
1. `src/graph/state.py` — define `TravelState`
2. `src/agents/planner.py` — just parse user input, extract budget/destination/dates
3. `src/graph/workflow.py` — single-node graph, planner only
4. `app.py` — Streamlit text input → planner output displayed

**Verify:** App runs, user types a request, planner extracts structured data.

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

### Streamlit Streaming Pattern

```python
# app.py
with st.spinner("Planner Agent analyzing your request..."):
    for step in app.stream(initial_state):
        agent_name = list(step.keys())[0]
        st.success(f"✓ {agent_name} complete")
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
