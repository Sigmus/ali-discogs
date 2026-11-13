# Qobuz matching and deployment preparation

Date: 2026-11-12, Europe/Amsterdam. User approved proceeding in this order.
Completed initial preparation 2026-11-13; see [audit](2026-11-13-qobuz-audit.md).
Work on codex/qobuz-poc. Prepare a reviewable deployable result; do not infer
permission to merge/push/deploy from this request.

## 1. Complete candidate metadata (complete)

Saved 740 release searches yield 1,217 candidate entries / 1,036 unique albums.
At launch, 23 unique albums already had cached metadata and 1,013 needed fetching.
Expected retrieval duration roughly 5–6 hours at current safe pacing, subject to
actual throughput, batch rests, response size and errors. No new searches here.

`scripts/qobuz_metadata_poc.py` deduplicates by album ID, preserves a fingerprinted
manifest, validates complete track counts and writes atomic per-album evidence
under ignored `.qobuz-poc/metadata/`. Existing request caches are reused.
One worker lock; >=15 seconds between requests including discovery; 120-second
rest after each 50 HTTP requests (including discovery and extra pages). No retries. SIGTERM/STOP pauses safely;
API/metadata/local errors create STOP and persist a failed checkpoint.

Inspect progress.json and run.log. `touch .qobuz-poc/metadata/STOP` pauses.
Resume with `uv run scripts/qobuz_metadata_poc.py` only after user direction if
there was a warning, removing STOP only then. Do not reset manifests or caches.
The worker has been launched detached with caffeinate. Hourly thread heartbeat
qobuz-metadata-progress reports progress and ETA, pauses on danger and records
completion. User authorized pagination support after the first 500/730 response. Assemble
cached pages with strict ID/total/offset and unique track checks; unexpected
pages still pause rather than accepting partial metadata.

Done when all 1,036 manifest album records exist, IDs match, track arrays are
complete and counts reconcile independently. Keep token and raw responses local.

## 2. Conservative offline matching and audit

Use the small validation report as regression evidence, not accuracy calibration.
Normalize work/movement structure and role-labelled credits. Compare programme
coverage and relevant performer/conductor/orchestra agreement at track level.
Handle compilation supersets, incomplete candidates, multiple recordings,
grouped LP tracks and verified catalogue aliases. Conflicting recording credits
must block automatic acceptance; insufficient metadata remains unresolved.

Score confidence as a documented heuristic, never a claimed statistical accuracy.
Avoid 100% merely for artist/title agreement. Store explanations, candidate IDs,
coverage and conflicts beside scores. Found/Probable require explicit conservative
criteria; no-query hits and unassessable programmes stay unchecked/unresolved.
A candidate rejection does not establish release-level Not found.

Audit a broader deliberately varied sample plus negative controls and inspect
threshold-boundary cases. Report both successes and limitations; tests should
exercise wrong orchestra, missing works, alternate numbering and compilation
subsets. Do not silently treat the initial six cases as a sufficient full audit.

Done when documented rules reproduce reviewed cases and a broader audit supports
the proposed acceptance thresholds, with ambiguous cases left for review.

## 3. Deployable data, UI and validation

Keep Qobuz evidence/results in a separate sanitized versioned data file keyed by
Discogs release ID so Spotify rescoring cannot erase it; duplicate copies share
results. Define generation/version/provenance and future manual-override precedence
before accepting reviewed corrections. Keep credentials and raw caches excluded.

Builds on a clean checkout must consume the committed sanitized publication file,
without depending on local ignored caches or authenticated network calls. Retain
local review evidence separately from published match output.

Main table and detail use consistent confidence/status formatting for Qobuz and
Spotify; show match explanations, linked candidates and unresolved states. Sorting
must match the displayed Qobuz status/confidence. No false Not found for empty
first-pass queries. Check narrow-screen table usability and error/loading states.

Run relevant matcher tests, UI normalization tests, static build and browser
checks. Check generated artifact for unintended private fields and verify a clean
checkout build yields the same data. Update setup/context/backlog/history.
Present branch changes, audit counts, remaining limitations and deployment-ready
status. Commit/merge/push/deploy only when explicitly authorized.

## Deferred

Broader fallback queries for the 370 empty first-pass releases are separate from
candidate metadata validation. Playback/download and exhaustive manual listening
are outside this work. A deployable release can retain unresolved albums.
