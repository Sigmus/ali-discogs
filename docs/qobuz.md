# Qobuz catalogue enrichment: setup and resume

Status: metadata retrieval complete and conservative offline matcher v1 prepared
on `codex/qobuz-poc`. UI builds use versioned sanitized `data/qobuz_matches.json`;
raw responses and credentials stay local. No audio or automatic deployment.
See the [audit](plans/2026-11-13-qobuz-audit.md) for rules and limitations.

## One-time setup

Requires Git, uv and Python 3.11+. Run commands from the repository root.
Scripts use isolated uv dependencies; no downloader installation is required.

```sh
mkdir -p .qobuz-poc
git clone https://github.com/Sei969/qobuz-dl.git .qobuz-poc/upstream
git -C .qobuz-poc/upstream checkout --detach 28c3521c3c96e62d7da7166d3edef1aed92a202f
```

The adapter verifies the upstream revision and unmodified `bundle.py` before
loading it. It uses only application-ID discovery, not app-secret extraction or
the full downloader client (whose initialization probes audio). Upstream is
GPL-3.0; its source stays in a separate ignored checkout, not copied here.

If `.env` does not exist, copy `.env.example` to `.env`. If it already exists,
add `QOBUZ_USER_AUTH_TOKEN=` without replacing the existing settings. From your
own logged-in Qobuz browser session, open developer tools, find an `api.json`
request in Network, and copy its `X-User-Auth-Token` request-header value into
that setting. Do not paste the token in chat, logs or committed files. Environment
variables take precedence over `.env`. Scripts never print token/app-ID values.

## Run and resume

```sh
# Search five candidates; inspect the first album's full metadata.
uv run scripts/qobuz_catalog_poc.py --query 'Glenn Gould Byrd Gibbons'

# Reproduce the six-release trial, up to five candidate albums per release.
uv run scripts/qobuz_sample_poc.py

# Reuse cached responses without any network or token/source requirement.
uv run scripts/qobuz_sample_poc.py --offline

# Explicitly refetch after account/territory changes or stale results.
uv run scripts/qobuz_sample_poc.py --refresh
```

An alternate trusted source checkout can be selected with `--source PATH`.
For a new bounded batch, create an ignored `.qobuz-poc/next-sample.json`:

```json
[
  {"discogs_id": 1445439, "query": "Glenn Gould Byrd Gibbons"}
]
```

```sh
uv run scripts/qobuz_sample_poc.py --sample-file .qobuz-poc/next-sample.json
```

Each ID must exist in `data/collection_matches.json`. Queries are explicit so
future work can refine retrieval without committing arbitrary automatic rules.
The current sample output is one file per release; changing a query for that
release replaces its assembled output. Per-request caches retain both queries.

## Cache and errors

- `.qobuz-poc/cache/`: successful search/album responses, timestamp, request
  parameters and upstream revision. No auth headers or app credentials stored.
- `.qobuz-poc/sample/<discogs_id>.json`: assembled review evidence for each release.
- `.qobuz-poc/catalog-result.json`: latest single-query review output.

All are ignored by Git. Keep `.qobuz-poc/` on the same machine to resume; on a
fresh checkout, rerun the setup and fetch. Every completed HTTP response is cached
atomically, so an interrupted batch resumes without repeating earlier successful
requests. Existing pre-consolidation sample files are evidence, not the new
per-request cache: the first new run fetches them again. Failures are never cached
as empty results. A zero-result search remains inconclusive, not proof of absence.

The cache is local to this account/territory; it does not include token values
in its keys. Use `--refresh` after changing account/territory. Offline cache misses
fail explicitly. `--offline` and `--refresh` are mutually exclusive. Requests have
20-second timeouts; batches pause 250 ms between candidate metadata fetches.

HTTP 401 indicates invalid/expired credentials or missing authentication; replace
the user token locally and retry. For 403/429 or network failures, stop and check
access/rate limits before retrying. If app-ID discovery breaks after a web-player
change, inspect upstream and intentionally update the pinned revision in
`scripts/qobuz_catalog.py`; do not silently use arbitrary newer code.

## Generate and preserve matching results

Run `uv run python scripts/qobuz_match.py` entirely offline using the portable
evidence snapshot included in the repository. It writes atomic `data/qobuz_matches.json`, with schema/matcher versions,
metadata completion date and source manifest/collection fingerprints. The source
checkout/token is not used by matching or `make build`.

The explorer overlays this separate file on collection rows by Discogs release
ID; duplicate copies share evidence. Spotify rescoring cannot overwrite it.
`summary.json` continues to describe the original pipeline output, not the overlay.
Never edit generated match data expecting edits to survive regeneration. Future
reviewed overrides must use a separate keyed file, take precedence over generated
results and be validated; no manual overrides have been accepted in v1.

Found (95%) and Probable (85%) are two heuristic evidence levels, not statistical
probabilities. Found requires one-to-one programme/track mapping with required
credits and equal track counts. Probable retains grouped/superset candidates for
review. Unsupported catalogue aliases/performer names and empty queries remain
unchecked. See the audit for false-negative limitations and remaining work.

No download functionality is part of this PoC. `scripts/qobuz_poc.py` remains the
older taschenb/python-qobuz comparison probe; it needs an independently issued
`QOBUZ_APP_ID`. The token-based scripts above are the working path.

## Validation

```sh
uv run --with 'requests>=2.32,<3' python -m unittest discover -s scripts/test -v
make test
make build
```

Unit tests use mocked network responses. The dated sample report records live
API evidence; neither proves automated match accuracy for the full collection.

## Slow search of the full collection

User authorized a full candidate-search pass on 2026-11-12. Run:

```sh
uv run scripts/qobuz_all_poc.py
```

This searches 740 distinct releases (741 copies), one query each, up to five
candidates. It uses the six tested queries where available; otherwise the first
key performer (or first performer), composer surname and first ten normalized
title words. This is a first retrieval pass, not an exhaustive search or matching
classification. Empty searches will need later work/track-based fallbacks.
It does not fetch every candidate's full track metadata in this pass.

All live requests, including app-ID discovery, are serial and spaced at least
15 seconds apart. After each 50 uncached searches it rests two minutes. This is
an intentionally conservative policy, not a published guarantee against Qobuz
limits. Any access, rate-limit or network error stops the run; no automatic
retries. Existing successful responses are reused. Duplicate copies share one
release search. A file lock prevents two copies of this runner at once.

Results and the exact query plan live under ignored `.qobuz-poc/all/`:
`manifest.json`, `<discogs_id>.json`, `progress.json`, and `run.log` when launched
with output redirection. Progress includes PID, status, counts and timestamps.
A detached run was started with `caffeinate -i` to prevent idle system sleep;
closing the laptop/restarting may still interrupt it. Resume with the same command.

```sh
cat .qobuz-poc/all/progress.json
# Request a clean stop; results already fetched are preserved.
touch .qobuz-poc/all/STOP
# Remove the marker before resuming.
rm .qobuz-poc/all/STOP
uv run scripts/qobuz_all_poc.py
```

A changed collection/query manifest stops rather than mixing plans silently.
Do not delete it without preserving existing evidence and reviewing the change.
The final `status: complete` means all first-pass searches finished, not that
all albums were found. The runner writes no production data. Inspect progress
and the process before starting another run; the launcher PID and actual worker
PID differ. Eight mocked tests cover caching/errors plus pacing, stop markers
and duplicate handling.

## Review in the local explorer

Run `make serve` and open localhost:8000. The Qobuz column sorts by status and
confidence; table and detail use the same score/status format as Spotify. Details
show candidate artwork, metadata, explanations and expandable programme evidence.
Build copies the versioned publication file directly, so it works without local
caches and without Qobuz requests. No auth token is needed to browse results.

## Full candidate metadata retrieval

`uv run scripts/qobuz_metadata_poc.py` retrieves each unique saved search candidate
once, reusing album/get cache entries. Progress, manifest and per-album records
live in `.qobuz-poc/metadata/`. Inspect progress.json/run.log; pause by creating
STOP in that directory. Never resume a warning/error without user direction.
No new searches, scores, production writes or audio requests. See the
[ordered preparation plan](plans/2026-11-12-qobuz-deployment.md).

Large albums are assembled from cached album/get pages (offset/limit), with
strict total/offset and unique track checks. Requests remain >=15 seconds apart;
rest 120 seconds per 50 HTTP requests including pagination. Partial page caches
are preserved, and any API or pagination inconsistency pauses for user direction.

## Portable evidence for collaborators

`data/qobuz_evidence.json.gz` is a deterministic, gzip-compressed JSON snapshot
(schema 1). It preserves all 740 release searches (including empty responses),
search and metadata manifests, all 1,036 complete albums / 27,770 track entries,
work/catalogue titles, role-labelled credits, composer/artist identities, ISRC,
UPC, durations, track/disc numbers, relevant release metadata, source revision
and completion date. It is about 1.8 MB compressed. Catalogue availability flags
are dated observations from the fetching account/territory, not universal access.

Ali can clone/checkout this branch, run `uv sync`, then:

```sh
uv run python scripts/qobuz_match.py  # offline; uses the committed snapshot
make serve                          # browse http://127.0.0.1:8000/
```

Initial dependency installation may need internet; matching itself does not.
No `.env`, Qobuz account or upstream source checkout is required for offline work.
The snapshot is not copied into the Pages artifact; only sanitized UI results are.

Inspect it without extracting thousands of files:

```sh
python3 - <<'PYTHON'
import gzip, json
with gzip.open('data/qobuz_evidence.json.gz', 'rt') as f:
    evidence = json.load(f)
print(evidence['albums']['0886445075762']['tracks']['items'][0])
PYTHON
```

For future authorized collection: preserve the local caches, run the resumable
fetchers as documented, then `python3 scripts/qobuz_snapshot.py` to export a new
whitelisted snapshot after metadata completion. Rerun the matcher, review the
diff/audit and commit snapshot plus generated results together. Export is atomic
and excludes unknown fields. Gzip timestamps are fixed for reproducible exports.

Local `.qobuz-poc/` still contains raw response duplicates, progress/logs, locks,
STOP markers and third-party source; it remains ignored. Credentials stay in
ignored `.env`. Re-fetch only new queries/albums or explicitly stale data.

## Shared request cache

User requested sharing the raw caches in addition to the compact evidence.
`data/qobuz_request_cache.tar.gz` preserves all 1,759 successful request-cache
JSON files byte-for-byte (~5 MB compressed / ~78 MB on disk). This includes
search responses, album/get responses and pagination, plus earlier sample calls.
Requests retain endpoint/parameters, timestamps and source revision; responses
retain the catalogue metadata rather than only the snapshot's selected fields.
There are no auth headers or tokens. Observations remain account/territory/date
specific; availability flags are not proof of another account's access.

After checkout:

```sh
python3 scripts/qobuz_cache_archive.py restore
# Replay the initial sample without network, credentials or source checkout:
uv run scripts/qobuz_sample_poc.py --offline
```

Restore validates flat hashed filenames, request keys/endpoints and sensitive
field names, checks all entries before writing, skips identical existing files
and refuses to overwrite differing local cache entries. For conflicts, use a
separate `--cache PATH` and inspect; do not discard fresher local responses.
Nothing is extracted using unrestricted tar paths or symlinks.

After future authorized requests, explicitly update the shared archive with:

```sh
python3 scripts/qobuz_cache_archive.py export
```

Review/scan and commit the updated archive. Private `.env`, app headers/secrets,
third-party source, process logs, STOP markers and locks remain excluded. The
mutable `.qobuz-poc/` working directories stay ignored; sharing happens through
this versioned archive. Neither evidence/cache archive is copied into Pages.
The offline matcher still uses the compact evidence snapshot by default;
restoring request caches is optional for algorithm work and useful for query tools.

## Reviewed offline cache expansion

The matcher also reads `data/qobuz_expansion_scope.json` and
`data/qobuz_work_inventory.json`. These are required versioned inputs: a bounded
reviewed candidate scope and independently sourced movement expectations. Scope
entries do not override scoring; every generation recomputes original credit
checks and completeness, without the discovery pilot's experimental name aliases.
Added candidates are capped at Probable 85%. The original first-pass v1 candidate
rules remain unchanged, so the new gate is not a retrospective baseline audit.

`uv run python scripts/qobuz_completeness.py` reproduces the fixed pilot audit in
`data/qobuz_completeness_pilot.json`. The original discovery artifact is a frozen
research sample: rerunning `scripts/qobuz_coverage_pilot.py` against newer match
output selects a different sample and does not authorize broadening publication.
Neither research JSON nor the work/scope inventories are copied into the website
artifact; the generated match sidecar includes the relevant candidate evidence.

The completeness checker supports sourced whole-work movement ordinals, explicitly
numbered target child tracks and unique timed target-track correspondences
(within max(5 seconds, 3%)). Unknown, ambiguous, split/joined, duplicate or reordered
movements stay unresolved. Track timing is supporting metadata, not an audio-cut
or session guarantee. See the [pilot review](plans/2026-11-13-qobuz-coverage-pilot.md)
for the selected cases, sources, limits and validation.

## Reproduce the original-baseline audit

`uv run python scripts/qobuz_baseline_audit.py` audits the frozen original 66
selected albums from `data/qobuz_baseline_audit_scope.json` against shared evidence.
It writes only `data/qobuz_baseline_audit.json`; publication matches are untouched.
The scope excludes the ten bounded expansion releases. Audit input fingerprints
make replay traceable; Git history and credentials are not needed to rerun it.

The raw completeness checker measures **credited** movement coverage: an
`incomplete` result can mean existing movements lack required performer metadata,
not that the music is missing. The audit adds title-only movement evidence and
separate supported/insufficient-credit/unresolved categories. Diagnostic flags
are review leads, not automatic downgrades. See the [complete baseline audit](plans/2026-11-13-qobuz-baseline-completeness-audit.md)
for findings, all 66 selections and proposed next work.

## Work-aware performer evidence

Current publication scoring uses `scripts/qobuz_work_groups.py`; historical
`evaluate_v1`/`credits_v1` remain available solely for reproducible comparisons.
Shared multi-composer opus collisions require distinctive work identity;
abbreviated movements inherit context only across supported composer/anchor and
sequence boundaries. Explicit vocal roles count as performance credits.

Role-specific performers can be supported across a coherent contiguous work
group with conductor/ensemble anchors on every track. Unknown additional main
artists, restarts, disjoint runs and ambiguous composer identity block repair.
No performer credits are copied from album membership or another recording.
This remains heuristic programme evidence, not session verification.

Newly qualifying candidates must pass the completeness gate before becoming
Probable; otherwise evidence stays Unchecked with no score. Existing reviewed
matches retain their previous statuses while their evidence mappings improve.
`uv run python scripts/qobuz_group_audit.py` reproduces comparison of all 76
reviewed selections. See [work-group implementation and review](plans/2026-11-13-qobuz-work-groups.md)
for rules, controls, withheld cases and limitations.

## Thirty-release service comparison

The fixed 2026-11-13 comparison includes twenty fallback queries for ten empty
Qobuz searches, ten cached unresolved Qobuz controls and ten cached Spotify
Found/Probable cases. See [comparison findings](plans/2026-11-13-service-comparison-pilot.md).
The separate portable `data/qobuz_comparison_evidence.json.gz` preserves all new
searches and eight selected complete albums; original evidence remains unchanged.
The shared raw-request archive now contains 1,786 responses, including this pilot.

Offline replay: `uv run --with requests python scripts/qobuz_comparison_pilot.py --report`.
Preparation without flags is offline too. Explicit `--search`/`--metadata` modes
resume the fixed saved tasks with the existing slow/STOP safeguards; do not resume
a failed warning without user direction. `--export` rebuilds portable evidence
from completed local outputs. These commands never update publication matches.
Spotify search caches lack tracks; this pilot's Spotify findings are album-level
warnings, not a full recording/programme validation.

## Explicit target-credit evidence and query relevance

Current matching requires `data/qobuz_target_credits.json.gz`, a portable model
of explicit cached Discogs work/position credits with source hashes. Rebuild it
with `uv run python scripts/qobuz_target_credits.py`; matching itself needs no raw
Discogs files. Unscoped/unparseable requirements stay global, and only explicit
positive assignments may scope a performer to particular works. Historical v1
units/evaluation remain frozen for comparison. Target archive fingerprints are
recorded in regenerated matches.

`uv run python scripts/qobuz_query_plan.py` proposes improved bounded queries and
ranks cached hits offline; those scores are relevance, not accepted confidence.
The two-query validation is preserved separately, not merged into publication.
See [query/credit refinement and Spotify findings](plans/2026-11-13-query-credits-spotify-tracks.md).

The follow-up [refinement/Spotify track audit](plans/2026-11-13-query-credits-spotify-tracks.md)
now preserves all 227 Spotify pilot tracks and confirms two partial programmes.
Historical comparison files retain their original evidence/limitations; use the
new track audit for current findings. The raw Qobuz archive now has 1,788 responses
(two more corrected-query validations); matching labels remain unchanged.

## Canonical album URLs

The public website does not reliably resolve bare `www.qobuz.com/album/ID` links.
Use cached canonical locale/album/slug/ID URLs. `data/qobuz_album_urls.json` preserves
1,043 cached album URLs separately from immutable matching evidence/review hashes.
No login or new API calls are needed to regenerate this index:

```sh
uv run python scripts/qobuz_urls.py
uv run python scripts/qobuz_match.py
make build
```

The index is exported deterministically from shared `album/get` responses in
`data/qobuz_request_cache.tar.gz`; it contains public URLs only and records the
source archive hash. After newly authorized retrieval, export the request archive
before rebuilding the URL index. The publisher validates exact host, HTTPS,
locale/slug path and matching album ID. Missing or invalid URL evidence falls back
to a safely encoded title/artist search; it never invents a slug or bare album URL.
Existing evidence archives and review fingerprints do not need to be rewritten.
Canonical routes do not guarantee availability in every account territory.


## Reviewed source composer scopes

`data/qobuz_source_composer_reviews.json` preserves manually reviewed classical
work attributions lost from normalized composer fields. Each scope binds the
normalized target and full cached Discogs source with SHA256, then validates
source positions, titles and artist IDs/names. Only those explicit scopes require
a matching positive candidate Composer credit. Arbitrary track artists are not
automatically treated as composers; no artist-role or spelling inference is added.
The legacy matcher and normalized collection remain unchanged.

Reproduce the offline audit and discover other attribution gaps:

```sh
uv run python scripts/qobuz_source_composer.py
```

Output `data/qobuz_source_composer_audit.json` separates reviewed guards from
name-heuristic discovery candidates needing manual review. Current scope is
Gilels15221307: Beethoven-only material cannot cover the source MedtnerOp.22.
Rubinstein7971104is flagged for review, not automatically scoped. After approved
scope changes, run the script tests, matcher, screen/inventory and static build;
inspect publication diffs rather than assuming labels should change.


## Known source-programme gaps

`data/qobuz_source_programme_reviews.json` records inspected source conflicts that
block acceptance even when all normalized source titles appear supported. Each
hold binds the edition, normalized target, cached source and original photos.
Candidates and main status remain Unchecked until the source is reconciled.
Changed source/evidence fails closed rather than silently removing a hold.

Rubinstein7971104(RCA Victor LM20086) currently has13saved tracks versus14on the
label/cover: Albéniz's Sevillana is missing. A-side positions afterA2are shifted.
`data/qobuz_rubinstein_programme_proposal.json` records the proposed14work list,
not an activated source replacement. The composer scope remains unreviewed.
Screen and unmatched audits distinguish `source_programme_review_needed` from
missing provider metadata. Raw/normalized collection and Spotify stay unchanged.


Reviewed composer names are separate from performer aliases. The exact full-name
Felix Mendelssohn/Mendelssohn-Bartholdy equivalence requires positive Composer-role
credit and does not infer identity from surname or structured Composer fields
alone. `scripts/qobuz_composer_identity.py` owns the narrow rule; legacy scoring
and saved collection text are unchanged. See the
[identity review](plans/2026-11-15-qobuz-composer-identity.md).

Bound-track reviews may require `composer_equals` in a track mark. This checks a
positive Composer-role name using the reviewed composer identity policy; neither
album-level names nor a structured field alone satisfy it. Mixed-composer source
sides can therefore use explicit mappings without a global title/key translation
or borrowing a composer from another work. Existing reviews without the mark keep
their prior checks. Source/target/album hashes, full programmes and performer
requirements still apply.


Discogs normalization now ignores bracketed descriptive annotations when deciding
credit roles. A liner-note title mentioning cello does not make its author a
cellist. Previously recognized genuine vocal annotations remain supported. This
fix affects future builds of match items; refreshing saved collection/results is
a separate operation and must preserve or re-review source-bound evidence.
The15November Casals/source-role audit is diagnostic; no bulk refresh was applied.


`python scripts/qobuz_casals_audit.py` runs the saved source reconciliation and
suite-context diagnostic offline. Exact target/raw/label proof and exclusive
nonperforming roles are validated before deriving a temporary corrected copy.
It writes only `data/qobuz_casals_reconciliation_audit.json`, never collection or
publication files. Both complete source programmes remain recording-unresolved.

A bound-track recording review can explicitly reconcile source credits using
`source_credit_reconciliation`. Nonperformers require exact, exclusively
nonmusical cached roles; principal/work performers cannot be excluded. A scoped
performer requires an exact source work-level role and target list, plus a saved
complete expected requirement map. Global conductor/orchestra and every other
source requirement remain. This is a manual source/hash-bound decision, never a
global omission rule or credit borrowed from another work. Solti5972183uses it to
require Minton on the songs and remove the liner author from musical requirements.


A `source-heading-movements` recording review handles flat Discogs headings with
individually positioned movement bands. `qobuz_heading_movements_review.py`
requires the complete exact source projection, unique band positions, catalogued
unique headings and a saved child list for every heading. Repeated tempo titles
remain valid at different positions. Each source band must map to one numbered
digital movement; joined/split sections are deliberately unsupported here.
Existing whole-work, performer and movement checks run on a temporary heading-only
copy, then exact per-work track IDs and individual track fingerprints are checked.
Raw/normalized collection and generic unit extraction never change. This is a
manual recording-family review, not automatic acceptance of all headed sources.


`uv run python scripts/qobuz_pretre_audit.py` reproduces the CVL1920diagnostic
offline. It validates the source/target/album plus saved LP-image hashes, maps
13combined bands to20digital sections, compares per-band and side timings, and
lists literal surname mentions for additional source-image credits. It writes
only `data/qobuz_pretre_band_audit.json`; no source/publication change or recording
identity acceptance. Equal side totals do not waive per-band or performer gaps.
All recording-review kinds now validate `external_source_files` when present.


`uv run python scripts/qobuz_credit_role_audit.py` inventories associated-only
credit declarations across the shared metadata. It reports spelling, current
parser behaviour, other same-track credit support, track hashes and saved-candidate
references. It changes only its diagnostic JSON, never credit policy/publication.
[Semantic proposal](plans/2026-11-15-qobuz-associated-credit-roles.md).


`uv run python scripts/qobuz_brendel_audit.py` reproduces the33work/103movement
Brendel diagnostic from the source-bound recording review. It preserves each
source position and supplied duration field, then checks explicit diagnostic
`source_timing_groups` for complete, non-overlapping scope within works. A printed
time can cover several movements and can appear on the first or last member.
Only groups marked `image_verified` have inspected label images; other shared-time
interpretations remain inference. These diagnostic spans never change source
fields or waive programme/artist checks, and timing similarity is not take proof.

`uv run python scripts/qobuz_priority14_audit.py` validates the frozen
15 November fourteen-case batch against source, collection, review and album
hashes, including diagnostic mappings and cached alternatives. Two cases were
accepted as Probable; twelve have explicit blockers. Diagnostic mappings never
authorize a promotion. See the [batch report](plans/2026-11-15-qobuz-priority14-batch.md).
`uv run python scripts/qobuz_cached_review_queue.py` refreshes workflow triage
after `qobuz_unmatched_audit.py`; reviewed blockers do not automatically return
to the open queue because an alternate candidate has a high partial coverage.


### Complete single-work vocal reviews

`source-vocal-programme` is a source/target/album/track-hash-bound recording review
for the saved StMatthew old-numbered ranges and Otello whole acts. Every raw
musical source credit is required within that single work; conductor and source
orchestra plus positive conductor/composer roles remain required on every track.
External recording-family evidence is mandatory. It never borrows credits across
operas or claims exact LP-side audio boundaries. Old Passion section-order ranges
are not literal modern movement-number equivalences. Unsupported forms fail closed.
A grouped source display title must be an existing member of its preserved group;
headings and all physical pieces remain checked.

`uv run python scripts/qobuz_secondary23_audit.py` reproduces all23frozen decisions,
including cached-alternative manifests and rejection/hold precedence over a future
high score. [Results](plans/2026-11-15-qobuz-secondary23.md).


### Cache all candidates for the remaining160metadata-needed releases

The15November fixed936album scope is user-authorized before ranking. Prepare
offline with `uv run --with requests python scripts/qobuz_uncached160.py`;
`--fetch` starts retrieval and `--export` validates/exports completed checkpoints.
Do not rerun an active worker or remove STOP without user direction. Progress/logs
are under `.qobuz-poc/uncached160-2026-11-15/`. Full manifest, immutable evidence
hashes, per-album checkpoints and existing request cache make the run resumable.
[Plan and completion checklist](plans/2026-11-15-qobuz-uncached160.md).


Completed936album batch is validated by `qobuz_uncached160.load_completed()`
before the offline unmatched inventory reads it. Run
`uv run --with requests python scripts/qobuz_uncached160_ranking.py` after rebuilding
the inventory to rank every one of the160frozen releases. Ranking favors supported
complete programmes, then complete source-unit support needing completeness checks,
then partial/zero support; held/rejected pairs are excluded. This diagnostic path
never updates publication labels. Canonical routes and shareable request cache
were rebuilt offline, preserving all prior successful responses.


`expected_recording_groups` freezes each target's exact existing contiguous-work
recording-group object inside a source/target/album-bound review. Completeness
counts only those selected tracks rather than every alternate take in the box.
Every target must have the identical group/track IDs and full existing-policy
credit support; otherwise validation fails. This reuses existing conductor/
orchestra-throughout and soloist-within-one-work rules, never another recording.
`uv run --with requests python scripts/qobuz_fullsupport16_audit.py` reproduces
all16decisions, alternative manifests and high-score hold precedence.


### Reviewed raw source bands

`source-leaf-bands` preserves every raw source leaf's tree path, position, title
and duration, exact selected track fingerprints, composer and source-derived
musician requirements. Structural headings have explicit covered-source paths.
No track reuse, missing source leaf or undeclared candidate extra is allowed.
`source_duration_notes` freezes any individually reviewed printed/digital timing
discrepancy; without it the existing5second/3percent check fails closed.
`source_composer_spellings` records explicit full-name source/file spelling
corroboration within that exact review; no global alias. Recording-family sources
are mandatory. See `scripts/qobuz_source_leaf_review.py`.

`uv run --with requests python scripts/qobuz_partial38_audit.py` validates all38
frozen decisions, full alternative manifests and high-score hold precedence.
The generic16case validator now accepts a fixed expected batch count; existing
16case/38case entrypoints retain their respective frozen sizes.

`uv run --with requests python scripts/qobuz_zero104_audit.py` validates the
104 zero-support reviews, including all frozen candidate IDs/title inventories,
raw source programmes/credits and hold precedence. The report is
`data/qobuz_zero104_recording_audit.json`. Title-only work coverage and musician
names occurring somewhere in an album are explicitly diagnostic, never credit
or recording acceptance. Three source-band mappings reuse the existing review
kind; no general matching threshold, performer alias or credit waiver changed.


### Review progress in the explorer

The sidecar's optional `review` object has `state: reviewed_unresolved`, the saved
decision, reason and limitations. It is produced from explicit unresolved recording
reviews/source-programme holds, independently of candidate search membership.
Underlying `status`, confidence and candidates remain unchanged for compatibility
with audit/inventory tools. The explorer derives the `reviewed_unresolved` filter,
sort and label only when evidence status is `unchecked`; other unaccepted cases
remain Unchecked. This means no saved review decision, not no prior search.


`python3 scripts/qobuz_blocker_groups.py` groups unresolved releases for planning
without rescoring or retrieval. It preserves saved finding labels; unreviewed
work-title/credit groups use existing programme diagnostics and do not establish
recording identity or catalogue absence. Rebuild unmatched inventory first.
`uv run --with requests python scripts/qobuz_final_cached2_audit.py` verifies the
last Schubert/Mozart pair, complete alternative manifests and hold precedence.
