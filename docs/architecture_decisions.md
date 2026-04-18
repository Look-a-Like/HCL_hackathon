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
