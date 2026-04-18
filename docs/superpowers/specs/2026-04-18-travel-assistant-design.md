# Design Spec — Agentic AI Travel Planning Assistant

**Date:** 2026-04-18
**Status:** Approved for Implementation

---

## 1. Problem Statement

Travel planning is fragmented: users manually search destinations, compare prices, build itineraries, and manage bookings across multiple platforms. The solution is a multi-agent AI system where each agent owns one responsibility, and a Planner Agent orchestrates the whole flow — delivering a complete, budget-aware, personalized travel plan from a single natural language request.

---

## 2. Architecture Decision: Framework & Architecture Lock-In

The biggest update is the definitive choice of the underlying orchestration framework.

**Chosen: LangGraph**

| Feature                  | LangGraph                                        | CrewAI                  |
| ------------------------ | ------------------------------------------------ | ----------------------- |
| **State control**        | Explicit typed state object passed between nodes | Implicit, agent-managed |
| **Debugging**            | Full graph visualization, step-by-step tracing   | Harder to trace         |
| **Hackathon speed**      | Medium setup, high payoff                        | Fast setup, low control |
| **Production-readiness** | High                                             | Medium                  |

The system will be built using LangGraph instead of CrewAI. This decision was driven by LangGraph's explicit state control and ability to visualize the graph for step-by-step debugging. LangGraph is noted as being more production-ready, which is critical for a demo that cannot break live.

---

## 3. System Architecture

### Parallel Graph Routing & Agent Roles

The workflow has evolved from a purely sequential list into a true graph structure with parallel execution:

1. **Planner Agent (Supervisor):** Takes the natural language input, parses the intent, and dispatches tasks.
2. **Destination Research Agent & Budget Optimization Agent:** Executed in **parallel** after the planner establishes the constraints.
3. **Itinerary Agent:** Once both Destination and Budget are complete, their data flows here to build the schedule.
4. **Booking & Local Experience Agents:** Fed by the itinerary to handle logistics and personalization.

```text
User Input (natural language)
        │
        ▼
┌─────────────────┐
│  Planner Agent  │  ← Orchestrator (Supervisor). Parses intent, dispatches tasks.
│  (Supervisor)   │
└────────┬────────┘
         │ dispatches to (in parallel):
    ┌────┴─────────────────────────────────────────┐
    │                                              │
    ▼                                              ▼
┌───────────────────────┐          ┌───────────────────────┐
│ Destination Research  │          │  Budget Optimization   │
│       Agent           │          │        Agent           │
│ - Suggests destination│          │ - Estimates costs      │
│ - Key attractions     │          │ - Cost-saving options  │
│ - Travel seasons      │          │ - Validates affordability│
└───────────────────────┘          └───────────────────────┘
         │                                        │
         └──────────────────┬─────────────────────┘
                            │ (Wait for both to complete)
                            ▼
              ┌─────────────────────────┐
              │      Itinerary Agent     │
              │ - Day-by-day schedule    │
              │ - Route optimization     │
              │ - Timing between stops   │
              └────────────┬────────────┘
                           │ dispatches to (in parallel):
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
              │      Final Output        │
              │   Complete Travel Plan   │
              └─────────────────────────┘
```

### Explicit State Management (TravelState)

Instead of agents passing unstructured messages, the architecture now centers around a highly structured, shared state object. A `TravelState` class defined as a `TypedDict` acts as the **single source of truth** flowing through the graph edges.

- It captures the initial user input and tracks extracted constraints like budget, duration, and destination.
- It acts as a central repository for the outputs of every single agent, from `destination_info` to `local_experiences`.
- The state object explicitly includes an `errors` list to accumulate faults, allowing the Planner Agent to retry or skip failed nodes.

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
    errors: list[str]            # Error accumulation for retries
```

---

## 4. Specific Technology Stack Selection

The vague "Reasoning" and "Fast" AI models have been explicitly defined, and the frontend infrastructure is locked to Streamlit.

| Component        | Choice                     | Reason                                                                        |
| ---------------- | -------------------------- | ----------------------------------------------------------------------------- |
| Agent framework  | **LangGraph**              | Explicit state, conditional routing, debuggable                               |
| Orchestrator LLM | **claude-sonnet-4-6**      | Assigned to the Planner Agent for heavy reasoning, planning, and coordination |
| Worker LLM       | **claude-haiku-4-5**       | Used for specialized task agents; fast and cheap for generation tasks         |
| Frontend         | **Streamlit**              | Remains in Streamlit for rapid hackathon deployment and easy streaming        |
| Travel data      | **Mock JSON + Web Search** | No paid API budget needed                                                     |
| Deployment       | **Render (free tier)**     | Easy hosting for Python backends                                              |
| Language         | **Python 3.11+**           | ML standard                                                                   |

---

## 5. Project File Structure (Streamlit Standard)

```
HCL_hackathon/
├── app.py                          # Streamlit frontend entry point
├── requirements.txt
├── .env                            # API keys (ANTHROPIC_API_KEY)
├── .env.example
│
├── src/
│   ├── graph/
│   │   ├── state.py                # TravelState TypedDict definition
│   │   ├── workflow.py             # LangGraph StateGraph assembly
│   │   └── router.py               # Planner routing logic
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
│   │   ├── search.py               # DuckDuckGo or Tavily free search
│   │   └── travel_data.py          # Mock travel data loader
│   │
│   └── prompts/
│       └── *.py                    # Prompt templates
│
└── data/
    ├── sample_destinations.json
    ├── sample_hotels.json
    └── sample_flights.json
```

---

## 6. Implementation Order (Hackathon Sequence)

### Phase 1 — Skeleton (get something running first)

1. `src/graph/state.py` — define `TravelState`
2. `src/agents/planner.py` — parse user input, extract budget/destination/dates
3. `src/graph/workflow.py` — single-node graph, planner only
4. `app.py` — Streamlit text input → planner output displayed

### Phase 2 — Core Agents (Parallel Setup)

5. `src/agents/destination.py` — given destination, return attractions + info
6. `src/agents/budget.py` — given budget + destination, return breakdown
7. `src/agents/itinerary.py` — given attractions + duration, return day-by-day plan
8. Wire all three into the graph (Destination and Budget in parallel)

### Phase 3 — Enrichment Agents

9. `src/agents/booking.py` — suggest flights, hotels with mock data
10. `src/agents/local_experience.py` — recommend food/events per destination
11. Wire into graph

### Phase 4 — Enhanced UI Streaming

Update the Streamlit UI to include real-time feedback mechanisms:

- Chat-style input
- Streaming agent progress: As the `StateGraph` executes, the UI will display exactly which agent is currently working and output successes as they complete their tasks
- Formatted output: itinerary cards, budget breakdown, booking options

### Phase 5 — Deploy

14. Finalize `requirements.txt`
15. Push to GitHub → connect to Render

---

## 7. Key Implementation Details

### LangGraph Workflow Pattern (With Parallel Routing)

```python
# workflow.py pattern
from langgraph.graph import StateGraph, END

workflow = StateGraph(TravelState)

# Add Nodes
workflow.add_node("planner", planner_agent)
workflow.add_node("destination", destination_agent)
workflow.add_node("budget", budget_agent)
workflow.add_node("itinerary", itinerary_agent)
workflow.add_node("booking", booking_agent)
workflow.add_node("local_experience", local_experience_agent)

# Set Entry and Edges
workflow.set_entry_point("planner")

# Parallel Execution: Planner flows to both Destination and Budget
workflow.add_edge("planner", "destination")
workflow.add_edge("planner", "budget")

# Join: Both must finish before Itinerary starts
workflow.add_edge("destination", "itinerary")
workflow.add_edge("budget", "itinerary")

# Parallel Execution: Itinerary flows to Booking and Local Experience
workflow.add_edge("itinerary", "booking")
workflow.add_edge("itinerary", "local_experience")

workflow.add_edge("booking", END)
workflow.add_edge("local_experience", END)

app = workflow.compile()
```

### Enhanced Streamlit Streaming Pattern

```python
# app.py
import streamlit as st

with st.spinner("Initializing AI Travel Team..."):
    # Stream the progress of the agents
    for step in app.stream(initial_state):
        agent_name = list(step.keys())[0]
        st.success(f"✓ {agent_name.replace('_', ' ').title()} complete!")
```

---

## 8. Mock Data Strategy (Hackathon Constraints)

The architecture has been pragmatically updated to avoid the costs and rate limits of live travel APIs.

- The system will rely on local mock JSON files (`data/sample_*.json`) containing curated Indian destinations, hotel tiers, and flight costs.
- A free web search tool like DuckDuckGo or Tavily will be integrated for live data enrichment without consuming API budget.

> **Demo talking point:** "In production, we'd swap mock data for Skyscanner API / Google Places API."

---

## 9. Example Full Flow

**Input:** `"Plan a 3-day budget trip to Goa for ₹20,000 — I like beaches and local food"`

| Step           | Agent            | Output                                                                                |
| -------------- | ---------------- | ------------------------------------------------------------------------------------- |
| 1              | Planner          | `{destination: "Goa", budget: 20000, days: 3, interests: ["beaches", "local food"]}`  |
| 2 _(Parallel)_ | Destination      | Baga Beach, Dudhsagar Falls, Anjuna Market, Fort Aguada                               |
| 2 _(Parallel)_ | Budget           | `{transport: ₹6000, hotel: ₹7500, food: ₹3000, activities: ₹2500, buffer: ₹1000}`     |
| 3              | Itinerary        | Day 1: North Goa beaches → Day 2: Dudhsagar + spice farm → Day 3: markets + south Goa |
| 4 _(Parallel)_ | Booking          | SpiceJet BOM-GOI ₹3200, Zostel Goa ₹800/night                                         |
| 4 _(Parallel)_ | Local Experience | Fisherman's Wharf for seafood, Saturday Night Market, beach shacks                    |
| 5              | Output           | Complete formatted plan                                                               |

---

## 10. What to Know for Demo Day

- **State Management:** Know the state that flows between agents — they will ask _"what happens if an agent fails?"_
  Answer: errors accumulate in `state["errors"]`, Planner can retry or skip.

- **Architecture:** Know why LangGraph over CrewAI (control, debuggability, explicit state, production-readiness).

- **Frontend:** Know why Streamlit (fastest frontend for ML demos, built-in support for streaming the `StateGraph` execution).

- **Upgrade Path:** Swap mock data → real APIs, Streamlit → Next.js/React frontend, Render → GCP/AWS.

---

_This design is locked. Proceed to implementation._
