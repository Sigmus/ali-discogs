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

## 2026-11-12 — Preserve Qobuz enrichment as a resumable local PoC

Status: adopted for the user-requested PoC and handoff; production scoring and
collection writes remain proposed follow-up.

Use a local Qobuz user token and a pinned Sei969/qobuz-dl checkout for app-ID
discovery only. Share a catalogue-only adapter between single-query and batch
scripts; do not initialize the downloader or request audio/app secrets. Cache
successful responses outside Git with explicit offline/refresh modes. Persist
review evidence and distinguish recording/programme candidates from confirmed
album matches. Document token setup in .env.example without any real values.
The legacy Python client remains available for comparison, not the working path.
