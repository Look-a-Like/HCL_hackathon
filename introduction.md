# Cartographer AI — HCL Hackathon Project

## What This Project Is

This is a hackathon project built for **HCLTech**, targeting the **Senior Software Engineer 1 (AI/ML)** role. The core mandate from the JD:

> Design, develop, and deploy AI solutions to extract insights from large datasets — implementing and optimizing ML models, ensuring scalable data pipelines, and communicating findings via dashboards to business stakeholders.

The project is a clean slate being built from the ground up during the hackathon. Code, models, and architecture will be added as development progresses.

---

## What Goes Where

```
HCL_hackathon/
│
├── introduction.md          ← You are here. Project overview and file map.
├── README.md                ← One-liner project title (minimal, update as needed)
├── CLAUDE.md                ← Instructions for Claude Code — behavioral guidelines,
│                               skill references, and project conventions
├── ARCHITECTURE.md          ← High-level system architecture (to be filled as built)
│
├── .claude/
│   ├── settings.json        ← Claude Code project settings: all tool permissions
│   │                           pre-approved, effort level set to high, Stop hook
│   │                           configured to auto-log architectural decisions
│   └── settings.local.json  ← Local overrides (gitignored, personal only)
│
└── docs/
    ├── architecture_decisions.md   ← Auto-generated log. Every time Claude finishes
    │                                  a session where files changed, a subagent
    │                                  appends what changed, the decisions made,
    │                                  and the rationale. Do not edit manually.
    └── interview.md                ← Spontaneous interview prep: 12 sections covering
                                       ML concepts, system design, stakeholder
                                       framing, HCL-specific context, behavioral
                                       questions, and quick-fire concepts.
```

---

## How the Automation Works

**Architectural decision logging** is automatic. Configured via the `Stop` hook in `.claude/settings.json`:
- After every Claude session where files are changed, a subagent checks `git diff`
- It appends a structured entry to `docs/architecture_decisions.md` with: timestamp, files changed, decisions made, and rationale
- No manual intervention needed — just build and the log keeps itself updated

---

## Development Context

- **Role targeted:** Senior Software Engineer 1 — AI/ML focus
- **Key deliverables per JD:** AI insight extraction, ML model implementation, scalable data pipelines, stakeholder dashboards
- **Stack:** To be determined as the project takes shape — update this file when chosen
- **Interview prep:** `docs/interview.md` — questions will be spontaneous and based on what you build, so keep that file current
