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

### 16 November — safely paused on network/JSON failure

Worker stopped02:26CET after862/936albums (92.1%);74remain.865HTTP attempts.
Reason: `album/get: network/JSON failure; no matches classified.` No HTTP status
was reported, so this is not evidence of a rate limit. STOP is present; no retry
or resume performed. Partial whitelisted archive validates862albums/22297tracks,
with matching IDs/counts and unique track IDs. Await user direction before resume.
No running ETA while paused.

### 16 November08:00CET — user-authorized resume

User explicitly approved resume after the network/JSON failure. Offline export
revalidated all862saved outputs first. Original failure progress preserved as
`previous-run-*.json`; explicit local resume authorization saved. Confirmed no
existing worker, then removed STOP and resumed with caffeinate, PID6178.936album
manifest and existing checkpoints unchanged; only74remaining albums need fetch.
Same15second spacing/120second rests; any new warning stops again.

### 16 November08:20CET — retrieval complete

936/936distinct manifest albums exported and independently validated: 23632tracks,
exact IDs, complete counts and unique track IDs. User-authorized resume used76HTTP
attempts, with no new warning; completed08:20:44CET. Prior862outputs preserved.
Whitelisted archive saved. Offline loader integration, shared request archive/URL
validation and evidence ranking remain next; publication labels unchanged.

### 16 November — offline integration and ranking

New archive is validated as a complete frozen scope before inventory loading.
Shared request cache3440responses (936added); every2504prior member preserved
byte-for-byte. Canonical index2100routes, including all936new albums. No provider
requests during integration, and published Qobuz/Spotify labels unchanged.

`data/qobuz_uncached160_ranking.json` retains all160releases and all unheld cached
candidates, with source/metadata inventory fingerprints. Ranking is workflow
priority, not calibrated confidence or acceptance:

- 2supported complete programmes: Brahms6798013(Menuhin/Furtwängler/Lucerne) and
  12803844(Ferras/Karajan/Berlin), needing recording-family/source-credit review.
- 16fully supported source-unit programmes still need completeness checks.
- 38partial programme support.
- 104no support under current rules, not proof that the service lacks the recording.

Full unmatched inventory:497work/credit,57withheld,19completeness,2recording-review,
4rejected-recording,6empty,1source hold; no metadata-needed entries. Old recording
holds/rejections remain saved: an alternative becoming reviewable does not erase
a held pair. No global parser/credit-rule change. New metadata deliberately feeds
diagnostics first; publication matcher is not expanded to auto-promote new hits.

Reproduce with `uv run --with requests python scripts/qobuz_unmatched_audit.py`,
then `uv run --with requests python scripts/qobuz_uncached160_ranking.py`.
Next perform recording reviews of the two complete leads, then the16full-support
leads, preserving transfer, source and named-credit uncertainty.

Validation:235script tests pass; publication and collection byte hashes unchanged.
Full scope/ranking false-positive tests include excluded held candidates and
missing-release rejection. The earlier fixed305release screen is preserved; the
current full unmatched inventory and160ranking own this new diagnostic checkpoint.
