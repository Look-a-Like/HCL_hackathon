# Architecture Decisions

## 2026-04-18 08:54 — Changes
**Files modified:** .claude/settings.json
**Decisions:** 
- Configured Stop hook to automatically document code changes
- Set hook event to trigger on agent completion after file modifications
- Configured hook to run agent subtype for architecture decision logging

**Rationale:** Implementing automated documentation of architectural decisions whenever code changes occur. This ensures all reasoning and design choices are captured in a centralized location without manual intervention, improving project knowledge management and decision traceability.

---

## 2026-04-18 08:57 — Changes
**Files modified:** .claude/settings.json, docs/interview.md
**Decisions:** 
- Created comprehensive interview preparation guide with 12 core sections
- Prioritized project defense as the foundational section (most important)
- Structured preparation guide to cover ML concepts, data pipelines, system design, and behavioral responses
- Added HCL-specific context and closing question framework

**Rationale:** Building a structured interview preparation guide ensures all critical topics are covered and practiced. By prioritizing project defense first, the guide establishes that understanding and defending architectural choices is the most important skill for successful technical interviews.

---

## 2026-04-18 11:53 — Changes
**Files modified:** docs/superpowers/specs/2026-04-18-travel-assistant-design.md
**Decisions:** 
- Replaced Streamlit frontend with **Next.js + shadcn/ui** for better UX and real-time updates
- Implemented **Server-Sent Events (SSE)** streaming from FastAPI backend to frontend for live agent progress
- Designed real-time UI components: `AgentProgress`, `ItineraryCard`, `BudgetBreakdown`, `BookingOptions`
- Updated deployment strategy to **Vercel** (frontend) + **Render** (FastAPI backend) for scalability
- Revised 6-hour hackathon timeline with phased milestones: skeleton (1h) → core agents (1.5h) → enrichment (1h) → UI polish (1.5h) → deploy (0.5h) + buffer (0.5h)

**Rationale:** A modern Next.js frontend with streaming SSE provides a significantly more impressive user experience than Streamlit while remaining achievable within the 6-hour hackathon window. This architecture separates frontend and backend concerns, improves deployment flexibility, and enables real-time feedback as agents process travel data.

---
## 2026-04-18 12:18 — Changes
**Files modified:** docs/superpowers/specs/2026-04-18-travel-assistant-design.md
**Decisions:**
- Added retry + fallback mechanism per agent (with_retry wrapper, max 2× retries)
- Enabled explicit parallel execution for Destination+Budget and Booking+LocalExp workflows
- Upgraded Planner to controller+validator role with intent classification, entity extraction, missing field detection
- Integrated conversation_history in state to support follow-up refinements (e.g., "make it cheaper")
- Booking agent now ranks results by budget proximity rather than price alone
- Added metrics tracking (latency per agent + completeness score) to state
- Implemented security middleware with rate limiting (SlowAPI) and prompt injection guards
- Optimized LLM usage: Haiku for workers with max_tokens=400 and temperature=0.3
- Changed final_plan from string to dict format for better renderability
- Added "Why This Architecture" section for stakeholder alignment

**Rationale:** These improvements address scalability, reliability, and user experience by introducing retry logic, parallel execution, enhanced planning, cost optimization, security controls, and performance tuning. The architecture now handles edge cases gracefully while maintaining fast response times and clear auditability.

---

## 2026-04-18 16:15 — Changes
**Files modified:** frontend/tsconfig.tsbuildinfo
**Decisions:**
- TypeScript build cache updated from frontend compilation
- Incremental build state preserved for faster recompilation cycles

**Rationale:** Build cache updates are an expected byproduct of compilation. Preserving incremental build state improves subsequent TypeScript compilation performance during development.

---

## 2026-04-18 16:57 — Changes
**Files modified:** backend/main.py, backend/2/agents/booking.py, backend/2/agents/local_experience.py, backend/2/agents/planner.py, backend/2/tools/ranking.py, frontend/components/BookingList.tsx, frontend/components/GemsGrid.tsx, frontend/lib/types.ts

**Decisions:**
- Format-string fix in `main.py` ensuring `budget or 0` prevents `None` values in currency formatting
- Expanded EXPERIENCES_DB with Assam, Darjeeling, and Varanasi destinations (9+ curated experiences each)
- Fallback destination parser extended to cover 30+ destinations including all Northeast India cities
- Backend agent pipeline (booking, local_experience, planner) updated for enhanced routing and experience retrieval
- Frontend components (BookingList, GemsGrid) synchronized with enhanced experience data

**Rationale:** These changes improve destination coverage and travel experience curation while ensuring robust null-safety in formatting operations. The expanded fallback parser ensures graceful handling of diverse user queries across India's regions, reducing agent hallucination and improving user experience.

---

## 2026-04-18 17:07 — Changes
**Files modified:** backend 2/agents/booking.py, backend 2/agents/budget.py, backend 2/agents/local_experience.py, backend 2/agents/planner.py, backend 2/main.py, backend 2/tools/ranking.py, frontend/components/BookingList.tsx, frontend/components/GemsGrid.tsx, frontend/lib/types.ts, frontend/tsconfig.tsbuildinfo, docs/architecture_decisions.md

**Decisions:**
- Implemented robust fallback parsing in `agents/planner.py` with configurable defaults (days=3, budget=₹50K) when LLM extraction fails
- Added `_fallback_parse()` method to handle edge cases and prevent silent failures with missing user inputs
- Integrated fallback budget split in `agents/budget.py` using fixed allocation percentages (transport 25%, hotel 35%, food 25%, activities 10%, buffer 5%)
- Ensured graceful degradation across entire planning pipeline: prompt parsing → budget allocation → booking → local experiences
- Updated backend agents to work with optional inputs, enabling the system to function with minimal user information

**Rationale:** Fallback mechanisms prevent the entire pipeline from silently failing when users provide incomplete information (e.g., "trip to Assam" without budget/days). By applying intelligent defaults at multiple pipeline stages, users get usable itineraries even with sparse inputs, dramatically improving the system's robustness and real-world usability.

---
## 2026-04-18 17:10 — Changes
**Files modified:** backend 2/agents/booking.py, backend 2/agents/budget.py, backend 2/agents/local_experience.py, backend 2/agents/planner.py, backend 2/main.py, backend 2/tools/ranking.py, frontend/components/BookingList.tsx, frontend/components/GemsGrid.tsx, frontend/lib/types.ts, docs/architecture_decisions.md

**Decisions:**
- Implemented streaming SSE endpoints (`/plan` and `/plan/sync`) for real-time agent execution feedback
- Designed thin Next.js proxy at `/api/plan` to avoid CORS issues while forwarding backend streams to frontend
- Rate-limited the main `/plan` endpoint to 5 requests/minute to prevent abuse
- Added `/health` endpoint for system monitoring and health checks
- Frontend communicates exclusively through proxy layer, never directly with backend

**Rationale:** Streaming SSE provides a superior user experience by displaying agent progress in real-time rather than waiting for completion. The proxy pattern resolves CORS restrictions while maintaining clean separation of concerns, allowing the frontend and backend to evolve independently while the proxy handles integration concerns.

---

## 2026-04-18 17:11 — Changes
**Files modified:** backend 2/agents/booking.py, backend 2/agents/budget.py, backend 2/agents/local_experience.py, backend 2/agents/planner.py, backend 2/main.py, backend 2/tools/ranking.py, frontend/components/BookingList.tsx, frontend/components/GemsGrid.tsx, frontend/lib/types.ts, frontend/tsconfig.tsbuildinfo, docs/architecture_decisions.md

**Decisions:**
- Mapped backend endpoints to handler locations for debugging and code review: booking agent (lines 180, 185), budget agent (lines 215, 229) in main.py
- Documented frontend proxy layer route at `/api/plan/route.ts` with single POST handler for backend streaming communication
- Structured code documentation for future maintenance and contributor onboarding
- Verified type consistency across backend agents and frontend components

**Rationale:** Explicit documentation of backend endpoint locations and frontend proxy structure enables efficient debugging, code review, and future maintenance. By mapping exact line numbers and handler locations, the team can quickly locate and understand critical request/response paths without navigating through sprawling agent code.

---
