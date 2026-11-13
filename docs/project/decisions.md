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

## 2026-11-12 — Show Qobuz search evidence in the explorer

Status: adopted by user request; supersedes the earlier search-link-only UI scope.

Show a Qobuz column and detailed cached candidates without treating search hits
as accepted matches. Use a minimal build-time sidecar keyed by Discogs release
ID so duplicate copies share evidence and Spotify rescoring cannot erase it.
Keep raw caches and credentials ignored; publication of review evidence is not
part of this local UI change.

## 2026-11-13 — Independent Qobuz publication overlay and cautious evidence levels

Status: adopted implementation of the user's matching/deployment-preparation request.

Keep versioned sanitized Qobuz output separate from generated Spotify collection
JSON, keyed by Discogs release ID. Build copies it without local caches/token.
Found/Probable scores are documented heuristic evidence levels, not calibrated
probabilities. Empty/inconclusive searches stay unchecked. Future reviewed manual
overrides must be separate, validated and take precedence over generated scores;
none have been accepted yet. Do not infer recording-session certainty from titles.

## 2026-11-13 — Commit portable Qobuz evidence for offline collaboration

Status: adopted by explicit user request so Ali can check out and work offline.

Version a deterministic compressed JSON snapshot of whitelisted catalogue fields,
complete searches/tracks/credits and provenance. Matcher reads it by default.
Keep raw request duplicates, third-party checkout, credentials, logs, locks and
STOP markers ignored. Publication builds copy only the UI match file, not the
research snapshot. Export updated evidence explicitly after authorized retrieval.

## 2026-11-13 — Share raw successful request caches too

Status: adopted by explicit follow-up user request, extending the portable snapshot.

Commit a deterministic archive of all successful request-cache JSON responses,
not merely selected evidence fields. Scan for credential values/sensitive keys;
exclude machine state, credentials and third-party source. Validated restoration
must preserve existing conflicting responses. Mutable local caches remain ignored,
and archives stay outside the Pages artifact. No network refresh implied.
