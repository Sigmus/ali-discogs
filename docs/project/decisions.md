# Decisions

## 2026-11-12 — Repo-local project documentation

Status: adopted by the user.

Keep current context, backlog, history, and durable decisions in `docs/project/`.
Use `AGENTS.md` to require reading context before work and maintaining it after
meaningful results. Use dated plans in `docs/plans/` only for substantial changes.

This combines CulturaFM's automatic upkeep with Sonoteque's separation of
current state and history. Keep context short; do not accumulate old handoffs.
The existing README remains the home for setup, commands, and architecture.
No separate roadmap or custom project skill is needed at this stage.

Backlog suggestions remain proposals until requested. Documentation upkeep does
not authorize implementation, commits, pushes, or external changes.

## 2026-11-12 — Sonoteque-style UI replacement

Status: adopted by the user.

Use Sonoteque's actual visual conventions. Table only, equal emphasis on browsing
and Spotify match review, dedicated detail views. Retain search, composer, label,
genre/style, decade and sorting. Qobuz is a search link in details; omit its
unchecked counts and filters from the main view. Feature parity with the previous
UI is not required. Work lives on `codex/sonoteque-ui`.
