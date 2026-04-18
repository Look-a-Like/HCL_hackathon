# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## Skills & Plugins Available

All permissions are pre-approved in `.claude/settings.json`. Invoke skills via the `Skill` tool before acting.

### Workflow Skills (invoke FIRST for any non-trivial task)
| Skill | When to use |
|-------|-------------|
| `superpowers:brainstorming` | Before any new feature or creative work |
| `superpowers:writing-plans` | When you have requirements for a multi-step task |
| `superpowers:executing-plans` | When executing a written plan |
| `superpowers:systematic-debugging` | Any bug, test failure, or unexpected behavior |
| `superpowers:test-driven-development` | Implementing any feature or bugfix |
| `superpowers:dispatching-parallel-agents` | 2+ independent tasks |
| `superpowers:subagent-driven-development` | Executing plans with independent subtasks |
| `superpowers:verification-before-completion` | Before claiming work is done |
| `superpowers:finishing-a-development-branch` | When implementation is complete |
| `superpowers:requesting-code-review` | Before merging |

### Implementation Skills
| Skill | When to use |
|-------|-------------|
| `sc:implement` | Feature implementation |
| `sc:build` | Build, compile, package |
| `sc:test` | Run tests with coverage |
| `sc:analyze` | Code quality/security/performance analysis |
| `sc:troubleshoot` | Debug deployments, builds, system issues |
| `sc:design` | Architecture, APIs, component design |
| `sc:improve` | Systematic code improvements |
| `sc:git` | Git operations with smart commit messages |
| `sc:research` | Deep web research |
| `sc:workflow` | Generate implementation workflows from PRDs |
| `sc:pm` | Project manager orchestration |
| `frontend-design:frontend-design` | Production-grade UI/UX |
| `andrej-karpathy-skills:karpathy-guidelines` | ML/AI implementation guidelines |

### Research & Memory
| Skill | When to use |
|-------|-------------|
| `claude-mem:mem-search` | Search cross-session memory |
| `claude-mem:make-plan` | Create phased implementation plan |
| `claude-mem:do` | Execute phased plan via subagents |
| `claude-mem:smart-explore` | Token-efficient codebase exploration |

### Specialized Tools
| Skill | When to use |
|-------|-------------|
| `codex:rescue` | Delegate heavy implementation to Codex |
| `vercel:nextjs` | Next.js App Router work |
| `vercel:ai-sdk` | Vercel AI SDK integration |
| `vercel:deploy` | Deploy to Vercel |
| `figma:figma-implement-design` | Translate Figma designs to code |
| `figma:figma-generate-design` | Generate designs from specs |
| `graphify` | Convert any input to knowledge graph |
| `humanizer` | Remove AI writing patterns from text |

### Active Plugins
- **superpowers** — core workflow skills
- **playwright** — browser automation & E2E testing
- **claude-mem** — persistent cross-session memory
- **context7** — live library/framework documentation
- **ralph-loop** — recurring task loops
- **frontend-design** — high-quality UI generation
- **codex** — OpenAI Codex delegation
- **andrej-karpathy-skills** — ML/AI coding guidelines
- **skill-creator** — create/modify skills
- **figma** — Figma design integration
- **vercel** — Vercel deployment & Next.js

---

_Update the sections above with project-specific commands, stack, and architecture as the codebase grows._
