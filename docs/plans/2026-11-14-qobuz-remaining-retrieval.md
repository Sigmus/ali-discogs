# Remaining Qobuz retrieval

14November2026, Europe/Amsterdam. User explicitly authorized both12metadata-needed
releases and305no-saved-hit releases, with documentation and ongoing progress.
This supersedes earlier stops at new-search/download boundaries for this scope.

Frozen `data/qobuz_remaining_scope.json`:83distinct uncached candidate albums from
saved hits for12releases, followed by603new queries across305releases (up to2each,
excluding exact saved query strings). Broader headline performer/composer queries
and existing catalogue/title variants; no claim of universally corrected roles.
Some stored hits will be irrelevant; retrieval does not mean acceptance.

Worker: `uv run --with requests python scripts/qobuz_remaining_retrieval.py --run`.
Default prepares offline. `--export` exports completed local records without calls.
State: `.qobuz-poc/remaining-2026-11-14/{metadata,search}/progress.json`, immutable
manifests, per-task outputs, run.log; root STOP plus phase STOP markers. Serial
15second minimum HTTP spacing,120second rests every50requests incl discovery/
pagination. All metadata needs declared counts and unique IDs. Any access/auth/
rate-limit, API/network, pagination or unexpected warning stops and requires user
direction before retry/resume. No automatic acceptance, audio or scope expansion.
The root STOP prevents starting the next phase; for immediate safe interruption
also create STOP in the active phase folder. Do not remove STOP without permission.

Portable whitelisted outputs `data/qobuz_remaining_{metadata,search}.json.gz` are
exported on phase completion or warning; raw successful request caches remain
local until validated archive export. Never expose .env or token values.
Monitor hourly with ETA, per user's standing preference. Estimate fresh throughput
separately from cache reuse; no ETA when stopped. Completion requires counts,
metadataIDs/tracks, search outcomes, archive export and docs; stop monitor then.
Initial timing estimate around3.5–4.5hours depending on cache reuse/pagination.
Next stage after retrieval: offline candidate ranking and validation; no blind
promotion or unbounded downloading of newly found candidate albums.

Run started13:16Amsterdam. First2/83metadata albums completed without warnings
at13:17. Hourly heartbeat `qobuz-remaining-retrieval-progress` active; caffeinate
is attached to worker PID87248 to prevent idle sleep while it runs. Fixed-scope
offline/resume manifest regression passes. State/logs are the live progress source.

## Checkpoint and agreed follow-up — 14 November

At 14:11 Amsterdam: metadata complete83/83; search running124/603. No warning
in inspected log tail. Check progress files for live values; do not restart.

After retrieval, in order:
1. Verify manifest/output IDs, full unique track counts and all603 query outputs;
   report hits versus successful empty searches separately from accepted matches.
2. Export sanitized evidence and validate the shareable successful-request archive
   and canonical URL index offline. Keep credentials and live worker state ignored.
3. Rank candidates and rerun matching offline using complete saved evidence.
   Newly discovered albums lacking full metadata remain leads; a bounded metadata
   follow-up must be scoped before more calls, rather than fetching every hit.
4. Audit promising and uncertain Qobuz candidates; seek reusable work/credit/
   completeness improvements. Source-specific exceptions stay hash-bound. Test
   known wrong-performer, wrong-cycle and incomplete-programme controls.
5. Regenerate publication data only for supported outcomes; check UI details,
   statuses and local build. Preserve uncertain cases. No automatic push/deploy.
6. Next priority is comparable Spotify evidence checks, starting with a bounded
   risk-based sample. Legacy Found labels may need demotion; no collection-wide
   relabelling or extra Spotify retrieval is implied by this planning agreement.

Status and confidence are saved outputs, not UI thresholds. Qobuz85/95 are
heuristic evidence levels; Spotify’s legacy similarity score is not comparable.
Higher reliable coverage is the aim, not a larger accepted count at any cost.

Hourly checkpoint14:21Amsterdam: metadata83/83 complete; search160/603 in
planned120second rest until14:21:55. Search142nonempty/18empty;82releases
seen so far all have at least one hit (not validated matches).150fresh search
HTTP attempts/10cache reuses; metadata85HTTP attempts incl overhead. Search
throughput about3.7fresh requests/minute including rests. Rough remaining
2–2.3hours; finish16:20–16:45Amsterdam, conditional on no pauses/errors.
