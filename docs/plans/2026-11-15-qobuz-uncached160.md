# Cache all saved candidates before ranking

15 November 2026, Europe/Amsterdam. User agreed to cache the remaining data first,
then triage/rank from complete evidence. Authorized fixed scope:160metadata-needed
releases,936distinct uncached candidate albums,1080release/album associations.
All candidates come from saved searches; no new search, audio or automatic match
promotion. Scope and source fingerprints: `data/qobuz_uncached160_scope.json`.
Deduplicate albums across releases; preserve every saved candidate, including
ones that may prove wrong. Uncached is unknown, not unlikely to match.

## Retrieval

Worker: `scripts/qobuz_uncached160.py`. Prepare offline without flags; `--fetch`
starts the authorized retrieval; `--export` exports completed checkpoints offline.
Uses existing15second minimum spacing,120second rest every50HTTP attempts,
including discovery and pagination. Expected baseline4½–5hours; long albums,
pagination and response latency may extend this. Reuse request cache and existing
per-album checkpoints. Never refresh, restart or speed up an active run.

Run directory: `.qobuz-poc/uncached160-2026-11-15/`, with manifest,progress.json,
run.log,run.lock,per-album outputs and STOP. `caffeinate -i` prevents idle system
sleep while the worker runs; closing the laptop can still interrupt execution.
On401/403/429, API/network/pagination error or unexplained stall>5minutes outside
planned rest, stop safely and ask the user; no automatic warning retry/resume.
Successful empty results are not warnings. Credentials and raw run state stay local.

## Completion and next stage

Validate all936album IDs and complete unique track counts, export whitelisted
`data/qobuz_uncached160_metadata.json.gz`, validate/share successful request caches
and resolve canonical URLs using saved provider routes. Then integrate the new
archive into offline evidence loading, rebuild the unmatched inventory and rank
programme/performer-supported leads. Keep rejected/held recordings and source
uncertainties intact. No score-only promotions or existing decision overrides.
No push/deployment. Record observed progress and final counts here/history.

## Progress

Prepared and scope/checkpoint validation tests pass (2tests). No provider request
made during preparation. Retrieval launch and initial observation follow below.

Launched22:19CET with`caffeinate -i`, PID61574. Observed 2026-11-15 22:20 CET:
2/936completed, 4HTTP attempts including discovery,
status running; first album14complete tracks. No live warnings in log.
233script tests pass; fixture warning messages are mocked, not provider failures.
Expected baseline finish around03:00–03:30CET on16November, subject to pagination
and latency. No matching/publication updates during retrieval. Inspect current
progress/log rather than treating this dated observation as live status.
