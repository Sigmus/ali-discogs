# History

## 2026-11-12 — Repository setup and local UI

Connected the empty workspace to `https://github.com/Sigmus/ali-discogs` and
checked out `main` tracking `origin/main`, at application baseline `99589fb`.
The checkout was clean after fetching.

Built the static explorer and started the local HTTP server on localhost:8000.
Opened it in the in-app browser and observed 741 releases and match counts.
This verified UI loading, not matching accuracy or the full test suite.

## 2026-11-12 — Project documentation established

Compared CulturaFM's single `docs/PROJECT.md` and automatic Cursor rule with
Sonoteque's separated project docs and maintenance skill. The user adopted a
small repo-local structure: context, backlog, history, decisions, and on-demand
implementation plans, maintained through `AGENTS.md`.

Added four proposed backlog items without treating them as approved work.
Checked initial counts against the committed `data/summary.json` (generated
2026-11-11). Public deployments and current Qobuz access remain unverified.
Documentation changes do not change application behavior; no application tests
were run for this work.

## 2026-11-12 — UI replacement investigation

Created `codex/sonoteque-ui` at the user's request. Inspected Sonoteque's base
template, album listing and cell components, and running album listing on
localhost:5177. Reference uses compact tables, small covers, muted metadata,
thin borders, violet accents, and paired light/dark tokens. Scope questions
pending; no application code changed and no tests run for this investigation.

## 2026-11-12 — Sonoteque-style UI implemented locally (AD-005)

User confirmed table only, equal browsing/match-review emphasis, detail views,
Qobuz links in details, and retention of all named filters. Replaced card/grid
presentation with table and copy-specific hash routes preserving filters on return.
Applied Sonoteque's light/dark colors, type scale, header, table and control spacing.
Detail views show complete tracks/credits and Spotify match/alternate candidates.

Validation: `node --check explorer/app.js`, `node explorer/test/normalize.test.js`
(741 releases), and `make build` pass. Browser verified 741 table rows, 210 missing
Spotify filter, combined Bach/Deutsche Grammophon/Baroque/1970s filter yielding one
row, sorting, details and return with filters, empty search and clear. Mobile table
and details and light/dark views visually checked; no horizontal page overflow at
observed mobile width, console error check empty. No matcher/data changes or
Python matcher rerun. Ready for user review, uncommitted and unpublished.
[Implementation plan](../plans/2026-11-12-sonoteque-ui.md).

## 2026-11-12 — Exact Sonoteque dropdown styling

Replaced browser-native select arrows with Sonoteque's exact `.view-select` CSS
blocks: appearance reset, embedded SVG chevron, light/dark stroke colors,
background size/position, padding and line height. Applied the class to all six
selects. Source-block equality check (ignoring indentation) and build pass;
visually verified both themes in the local browser. Changes remain uncommitted.

## 2026-11-12 — Align filter grid

Made the filter form a four-column grid (two columns on mobile) so Decade and
Sort match the widths above. Clear follows Sort. Removed the A to Z control and
its UI handlers; existing query direction support remains for compatibility.
JavaScript syntax, build and whitespace checks pass; desktop layout visually
verified in the browser. Changes remain uncommitted.

## 2026-11-12 — Match Clear button height

Matched Clear to the dropdowns with 13px text, 1.3 line height and 3px vertical
padding, retaining compact horizontal padding and bottom alignment. Build and
whitespace checks pass.

## 2026-11-12 — Sortable table columns

Inspected Sonoteque's base template: clickable headings, ascending on first
selection, repeat click reverses, and ▲/▼ indicators. Added equivalent controls
to Album, Year, Composer, Artists and Spotify, retaining the decorative cover
column. Copied Sonoteque's indicator CSS, with keyboard-operable buttons and
aria-sort. Header sorting shares URL/filter state and the Sort selector.
Artists sorts performance credits; Spotify sorts found/probable/not found/pending/
unchecked, with confidence descending within ascending status order (reversed
when descending). Missing numeric values remain last.

Validation: syntax check, normalization/query tests including new bidirectional
ordering cases, build and whitespace checks pass. Browser clicked every header
and verified active sort state, then reversed Spotify using Enter. Changes
remain uncommitted on `codex/sonoteque-ui`.

## 2026-11-12 — Main content width

Set the main container max-width to 80%, replacing the 48rem/90rem caps and
removing the 1536px widening override. Existing internal padding remains.
Build and whitespace checks pass.

## 2026-11-12 — Inline Spotify confidence and status

Changed the table Spotify cell to a single line, e.g. `100% (Found)`, with
status alone when confidence is absent. Widened that column to fit the full
label. JavaScript syntax, normalization tests and static build pass.

## 2026-11-12 — Publication authorized and checks complete

User requested committing all changes, merging to main, pushing and waiting for
GitHub Pages. `make test` passes both offline matcher tests and the 741-release
UI suite, including new sorting cases; `make build` and `git diff --check` pass.
Fresh fetch shows remote main unchanged at the imported application baseline;
local main also holds the project-documentation commit. Publishing the redesign
and all documentation together; inspect Git/Actions for final outcome.

## 2026-11-12 — Redesign merged and pushed

Committed all redesign/docs changes as `c0ed7a3`, fast-forwarded main and pushed
to origin. Local and remote main matched with a clean working tree immediately
after push. Pages and test workflows triggered for that SHA. Public site:
https://sigmus.github.io/ali-discogs/. Deployment completion is checked in GitHub
Actions; this entry records the verified push, not an assumed deployment result.

### 2026-11-12 — Remove status tabs

Removed the All/Found/Probable/Not found tab row and its UI handlers/styles at
the user’s request. Spotify match filtering remains available in the dropdown.
Validated JavaScript syntax, existing normalization/query tests and static build.

### 2026-11-12 — Clarify link affordances

Made composer, artist and Spotify status table cells plain text; titles and
covers retain detail navigation. Removed accent coloring from static composer
and match labels. Syntax, normalization/query tests and static build pass.

### 2026-11-12 — Fix GitHub Pages source and verify live UI

Live browser inspection found the README published because Pages used the
legacy main/root source. Changed the repository Pages source to GitHub Actions
and pushed `8e9f638`. Deployment `43231078310` succeeded. Browser inspection of
https://sigmus.github.io/ali-discogs/ confirmed the album UI, 741 table rows,
no status tabs and no status hyperlinks.

### 2026-11-12 — Default to chronological sorting

Changed default sorting and Clear reset to Year ascending, oldest to newest,
with undated albums last. Explicit sort links still override the default.
JavaScript syntax, normalization/query tests and static build pass.

### 2026-11-12 — Prepare Python Qobuz PoC

Created `codex/qobuz-poc`, preserving pending sorting edits. Added an isolated,
read-only search/metadata probe with ignored output and no dataset mutations.
qobuz 0.0.2 installs under Python 3.12; 46 upstream mocked tests pass. Live
search awaits QOBUZ_APP_ID; no claim of working API access yet. See the PoC plan.

### 2026-11-12 — Inspect alternate Qobuz client

Inspected user-specified Sei969/qobuz-dl. It offers catalogue search, full
metadata and downloads, but initialization requires a user token and probes
audio access. Recorded integration concerns in the PoC plan; no live execution
or new credential extraction performed.

### 2026-11-12 — Test alternate catalogue access

Sei969/qobuz-dl application-ID discovery succeeded. Anonymous catalog/search
returned HTTP 401, reproduced using the new catalogue-only script. No audio
requests or dataset updates. Authenticated trial awaits a locally supplied
QOBUZ_USER_AUTH_TOKEN. Script syntax checked; live rejection is explicit.

### 2026-11-12 — Authenticated Qobuz catalogue success

Using the user-supplied local token, the catalogue-only PoC returned HTTP 200
for catalog/search and album/get, with five Bach/Gould/Goldberg candidates.
Raw metadata remains ignored locally. No audio requests or published data changes.

### 2026-11-12 — Six-release Qobuz sample

Tested two releases each from Spotify found/probable/not_found. All six initial
searches and 19 candidate metadata fetches succeeded; five queries had hits.
Gould Byrd/Gibbons has the same eight-piece programme; other strong candidates
include reissue supersets, with a concrete wrong-orchestra Eroica false positive.
Gilels Russian Keyboard Masters remains unresolved after fallback. No automated
match claims or collection updates. See the dated sample report. Syntax and
diff checks pass; live API calls and complete returned track counts verified.

### 2026-11-12 — Make Qobuz enrichment resumable and commit handoff

User requested environment template, code/docs handoff and committing all work.
Added QOBUZ_USER_AUTH_TOKEN placeholder to .env.example and docs/qobuz.md with
pinned source setup, token renewal, resume, offline, refresh and custom batches.
Consolidated catalogue access with per-request atomic caching, revision checks,
20-second timeouts and credential-safe errors; never initializes audio handling.
Live six-release fetch and offline replay pass. Five new mocked cache/error tests,
existing offline matcher/UI tests and static build pass; tests added to make/CI.
Retained the older app-ID comparison probe. Published data remains unchanged.
Pending Year-default UI edits are included in the requested commit scope. Real
.env, upstream checkout, response caches and Python caches remain ignored.

### 2026-11-12 — Start slow full-collection catalogue searches

User authorized all-album searches at a conservative pace. Added a resumable,
locked runner with exact query manifest, duplicate handling, request pacing
(15 seconds minimum), two-minute rests each 50 new searches, and stop-on-error.
Eight mocked tests pass. Launched detached with caffeinate to prevent idle sleep.
Actual progress is in ignored .qobuz-poc/all/progress.json; completion is not
yet claimed. No automatic matches or published data writes.

### 2026-11-12 — Schedule progress checks and pause on warning

User requested updates every 20 minutes and a pause/question at any danger sign.
Created thread heartbeat `qobuz-search-progress` at 20-minute intervals. It
checks saved progress/logs, pauses on access/rate-limit/API/network problems or
unexplained stalls, and asks before any retry/resume. Successful empty searches
are not failure signals. Existing runner stops on the first API/network error.

### 2026-11-12 — Change progress cadence after next update

User requested keeping the next update, then switching to hourly. Updated the
existing heartbeat prompt to perform that transition at its next firing, leaving
the immediate 20-minute schedule intact. Search pacing and stop-on-error stay unchanged.

### 2026-11-12 — Hourly progress cadence enabled

At the final 20-minute check (~16:05 Europe/Amsterdam), 154/740 releases were
searched: 78 with candidates, 76 zero-result queries, 243 candidates saved.
Run was in its expected 120-second batch rest, with no errors reported.
Switched `qobuz-search-progress` to hourly as requested.

### 2026-11-12 — Include ETA in hourly updates

User requested ETA in progress updates. Updated the existing hourly heartbeat
to estimate remaining time and local finish from observed throughput and planned
rests, show uncertainty, and omit running ETAs while paused/failed.

### 2026-11-12 — Toggle filter option ordering

Added an accessible switch before Clear, default on, sorting filter dropdown
choices by total collection frequency then name. Off restores alphabetical
ordering (chronological decades). Placeholders stay first, current selections
survive reordering, and Sort still controls album-table sorting. Browser checked
Beethoven/Bach frequency ordering, alphabetical mode and retained Bach selection.
UI normalization tests, JavaScript syntax, build and diff checks pass. Versioned
UI asset URLs prevent stale browser caches. Background Qobuz run untouched.

### 2026-11-12 — Commit and push filter toggle and slow-search tooling

User requested commit/push of current work on codex/qobuz-poc: frequency-order
toggle, resumable slow full-collection runner, pacing/stop tests and updated docs.
Credentials, upstream checkout and candidate caches stay ignored. No main merge
or Pages publication is part of this push; active search is not restarted.

## 2026-11-12 — Full Qobuz search completed (AD-007)

- Finished at 18:46:59 Europe/Amsterdam after about 3h24m; final worker status
  complete, with no reported API/network errors.
- Independently verified saved responses for all 740 manifest releases covering
  741 copies: 370 with candidates, 370 with zero results, 1,217 candidate entries.
- All results remain unreviewed in ignored local caches. Empty first-pass queries
  do not establish catalogue absence; no production data or match statuses changed.
- Completed hourly monitoring and removed its heartbeat. Next proposed work is
  AD-006 candidate normalization/review, coordinated with AD-004 persistence.

## 2026-11-12 — Connect cached Qobuz evidence to local explorer

- Added a sortable Qobuz candidate-count column and detail candidate list with
  artwork, metadata, query/date and album links, with explicit unreviewed wording.
- Build exports only selected catalogue fields from ignored cached responses;
  collection match JSON and credentials remain unchanged. No new API requests.
- Verified 740 exported releases, 1,217 candidates and 370 empty searches;
  browser verified 741 table rows and a five-candidate detail view. JS syntax,
  existing normalization tests, static build and diff checks pass.
- Cache is local: clean remote builds show Not searched. Publishing review data
  remains a separate decision. No commit or push requested for this change.

## 2026-11-12 — Small Qobuz validation pass

- User authorized starting small. Fetched four existing search candidates with
  >=15-second spacing and shared cache reuse; no repeated searches or warnings.
  All four full track lists match advertised counts (8/10/20/50).
- Reviewed programme and track credits plus two cached controls: three strong
  programme candidates, two candidate rejections, one unresolved L./K. numbering
  case. Detailed evidence in plans/2026-11-12-qobuz-validation.md.
- No fabricated confidence percentages, accepted matches or production writes.
  Retrieval script is bounded/resumable and stops on its first catalogue error.

## 2026-11-12 — Begin full Qobuz metadata retrieval

- User approved the ordered validation/deployment-preparation plan. Started
  detached caffeinate metadata worker for 1,036 deduplicated candidate albums;
  23 cached / 1,013 missing at launch. No repeated searches.
- Added fingerprinted manifest, exclusive lock, atomic checkpoints, complete-track
  validation, 15-second pacing, 120-second rests per 50 fetches and error STOP.
- Ten Qobuz tests pass, including candidate deduplication and incomplete metadata
  rejection. Hourly progress/ETA automation qobuz-metadata-progress enabled.
- Recorded matching/audit and clean-checkout publication readiness criteria in
  plans/2026-11-12-qobuz-deployment.md. Initial retrieval estimate 5–6 hours;
  no production statuses, commits, remote changes or deployment performed.

## 2026-11-12 — Metadata retrieval paused for incomplete large album

- Worker stopped at 20:29 Europe/Amsterdam after 131/1,036 albums (127 fetched,
  four reused). STOP confirmed at hourly check; no retry or resume performed.
- Offline inspection of cached album 0002894778167, “111 Years of Deutsche
  Grammophon”: returned ID agrees, advertised/total 730 tracks, returned 500,
  limit 500 and offset zero. Pagination is the apparent cause, not evidence of
  throttling or authentication failure. Incomplete metadata was not accepted.
- Await user direction to add slow resumable pagination handling and continue,
  or skip this album as unresolved. No running ETA while paused.

## 2026-11-12 — Authorized pagination support and metadata resume

- User approved adding slow/resumable pagination and continuing retrieval.
  Added cached album page assembly with ID/total/offset, progress and duplicate
  track validation. Original first-page caches are preserved; partial pages can
  be reused after interruption. No retry on access/network/API warnings.
- Thirteen offline Qobuz tests pass, covering assembly, overlapping/empty pages,
  incorrect offsets and failure propagation without retries.
- Resumed detached worker from 131 saved albums. Batch rests now count every
  HTTP request, including discovery/extra pages, with >=15-second spacing.
  Previous-run progress checkpoint preserved locally for pause-aware ETA.
- Live recovery verified: album 0002894778167 now has all 730 tracks with 730
  unique track IDs; worker advanced beyond it (133/1,036 at observation).

## 2026-11-13 — Metadata complete; conservative matching prepared (AD-006)

- Metadata finished 01:15:30 Europe/Amsterdam. Verified 1,036 album IDs, complete
  track counts, unique per-album track IDs and 27,770 track entries. Deleted
  hourly metadata monitor. No further API calls during matching/preparation.
- Assessed all 1,217 candidate entries offline. Final unique-release overlay:
  12 Found, 54 Probable, 674 unchecked; copy counts 12/54/675. No Not found
  inferred from absence, no 100% scores or statistical calibration claims.
- Broader catalogue audit includes all final Found correspondences, 15 spread
  Probable mappings and negative/uncertain controls. Fixed standalone item
  omission and Part II A/B/C confusion; added meaningful regression checks.
- Prepared separate sanitized, versioned match overlay with provenance, consumed
  directly by build and merged in UI by release ID; survives Spotify rescoring.
  Table/detail show consistent status/confidence, linked candidates and evidence.
- `make test` passes (two offline matcher tests, UI checks, 18 Qobuz tests), build
  and JS syntax pass. Browser verified table sorting, Gould detail, responsive
  horizontal containment. Clean-copy build without local caches preserves output;
  sensitive-field/token scan passed. No commit, merge, push or deployment.
- Limit: low recall and uncertain recording identity remain explicit. AD-008 is
  proposed for broader queries/aliases and movement/session validation.

## 2026-11-13 — Portable offline evidence for Ali

- User requested committing cached evidence for collaborator checkout. Exported
  deterministic whitelisted data/qobuz_evidence.json.gz (~1.8 MB): 740 searches,
  including empty responses, 1,036 complete albums and 27,770 track entries.
- Matcher now reads portable snapshot by default. Clean-copy run with no .env,
  Qobuz variables, raw cache or upstream checkout reproduces exact match output;
  static build succeeds. Updated README/setup and snapshot inspection/export docs.
- Twenty Qobuz tests pass, including snapshot field exclusion and complete
  candidate coverage; UI normalization/overlay/sorting checks pass. Deterministic
  re-export and decompressed snapshot credential/sensitive-field scans pass.
- Raw duplicate responses, logs, locks, STOP markers, third-party source and .env
  remain ignored. Snapshot is excluded from Pages build; only UI match data ships.
- Included portable evidence with the related matcher/UI/retrieval/docs work in
  the requested local commit. No push, merge or deployment authorized/performed.

## 2026-11-13 — Share complete successful Qobuz request cache

- User explicitly requested caches in addition to portable evidence. Archived all
  1,759 successful request responses, byte-for-byte, in a ~5 MB versioned tar.gz.
- Credential-value and sensitive-field-name scans passed. No auth headers,
  credentials, process logs, STOP/lock state or third-party source included.
- Added deterministic export and validated restore; existing conflicting files
  are preserved. Two tests pass for offline cache replay/conflict handling and
  traversal rejection. Full archive restored into a temporary directory and
  compared byte-for-byte with all original responses.
- Documented collaborator restore/offline sample commands. Included in requested
  local cache-sharing commit; no push, merge, refresh or deployment performed.

## 2026-11-13 — Share Qobuz branch on GitHub

- User requested push. Successfully pushed ad1d7fd and d7c3e98 to
  origin/codex/qobuz-poc, including portable evidence and request caches.
- No merge to main or Pages deployment; collaborator checkout is now available.

## 2026-11-13 — Simplify sorting and add Qobuz match filter

- User requested removing Sort dropdown and placing Qobuz match after Spotify.
  Kept header sorting and URL sort state; wired Qobuz control to filtering,
  count/frequency ordering, hash restoration, detail navigation and Clear.
- Browser verified URL-restored Found (12), selecting Probable (54), sorting via
  Qobuz header with filter preserved, and Clear back to 741 releases/Year default.
- UI normalization/overlay tests, JS syntax, build and diff checks pass. Restarted
  local server on localhost:8000 for preview. No commit/push/deployment requested.

## 2026-11-13 — Commit and share service filter UI

- User requested committing/pushing the Sort-dropdown removal and Qobuz match
  filter addition with related docs on codex/qobuz-poc. Prior browser, build,
  normalization, syntax and diff validation passed; no additional code changes.

## 2026-11-13 — Qobuz coverage improvement recommendations

- Inspected current matcher and generated evidence at user request for ideas.
  Of 674 unresolved unique releases, 370 have empty first-pass searches and 304
  have candidates. Among those 304, 51 have some credited programme coverage;
  94 have a candidate with title/work support for every target but fail full
  credited coverage. These groups overlap and are leads, not validated matches.
- Recommended offline failure audit, verified credit/title/catalogue aliases,
  hierarchical movement matching and cross-searching the existing 1,036-album
  snapshot before separately authorized slow fallback API searches. No matcher
  changes, API requests or new match claims made.

## 2026-11-13 — Bounded offline coverage pilot

- Added reproducible cache-wide discovery script and separate research output;
  no publication matcher/data changes or API calls. Inspected 219 unresolved
  releases to find 12 proposals/15 candidates, eight formerly empty searches.
  Eleven releases have a candidate passing unchanged rules; one requires an
  experimental explicit name alias. Reviewed all target-to-track correspondences.
- Review caught two single-movement compilations satisfying v1 work-heading
  coverage. Documented exclusions and prioritised explicit movement completeness
  before expansion. Remaining candidates are catalogue leads, not confirmed
  recording-session identities. See dated pilot plan for the 12-case audit.
- All 24 Qobuz mocked/offline tests pass using the optional requests dependency,
  including two new discovery/alias/negative-control tests. Diff check passes.

## 2026-11-13 — Fail-closed movement completeness pilot

- Added separate completeness checker and four-work movement inventory, grounded
  in independently inspected LA Phil, Berliner Philharmoniker and Atlanta
  Symphony/UGA programme references. No Qobuz calls or publication-data changes.
- Reran fixed 15-candidate pilot: five candidates across four releases pass
  movement coverage; one incomplete and nine unknown are withheld. Both known
  partial Kleiber compilations are prevented from passing; missing/ambiguous
  labels, duplicates, order changes and split/joined movements remain unresolved.
- Added real-data negative/positive controls and credit/identity checks; all 28
  mocked/offline Qobuz tests pass. Report includes input fingerprints. Target
  child-track handling, wider sourced inventory and session verification remain
  incomplete; no automatic promotion, commit, push or deployment.

## 2026-11-13 — Extend pilot and integrate ten offline candidates

- Expanded sourced work inventory to 24 works; added numbered target-child and
  timed standalone-track evidence, plus rejection of overlapping assignments.
  Fixed pilot now supports 12 candidates across 11 releases; experimental alias
  case, split Karajan finale and two partial Kleiber compilations not promoted.
- Integrated ten releases/eleven candidates via a fixed reviewed discovery scope;
  all original credit and completeness checks recompute on generation, no aliases
  or score overrides. All additions Probable 85%. Unique counts now 12 Found /
  64 Probable / 664 unchecked; copies 12 / 64 / 665. All previous 66 matched entries
  verified unchanged. No Qobuz calls or retrieval-cache changes.
- All 33 Qobuz mocked/offline tests, UI normalization/overlay/sort, build and diff
  checks pass. Browser verified Gilels details and 64-row Probable filter. Recording
  identity and retrospective baseline completeness still need review; no automatic
  commit, push, merge or deployment. Repeated generation checked for reproducibility.

## 2026-11-13 — Checkpoint before baseline audit

- User requested committing the tested bounded offline expansion, then auditing
  completeness of the original 66 Qobuz matches. Existing validation: 33 offline
  Qobuz tests, UI tests/build, browser inspection and byte-identical regeneration.
- This checkpoint includes the discovery/completeness scripts, research evidence,
  sourced inventories, bounded candidate scope, regenerated matches and docs.
  Audit follows separately; no push, merge or deployment requested.

## 2026-11-13 — Audit original 66 matches after checkpoint

- Committed the tested bounded expansion as c1857a7, then froze original 66
  selections from 7ea8898 for reproducible offline auditing. No push requested.
- All original statuses reproduce. Stricter checker supports seven, flags one
  incomplete credit-evidence case and leaves 58 unresolved. In the flagged Mozart
  case all six movements exist; four lack Mutter in track credits. This is not
  evidence of missing music. All twelve original Found entries retain one-to-one
  catalogue correspondence, not independent session/completeness verification.
- Inspected all eleven diagnostic cases: abbreviated Berlioz work context, vocal
  participation/missing credits, Kiril/Kirill spelling, and Grieg/Sibelius Op.46
  track-assignment collision. Candidate albums often contain more relevant music
  than the current evidence mappings show; no confirmed missing-music conclusion.
- Added frozen audit scope/report, offline replay script, three regression tests
  and complete 66-selection table. All 36 mocked/offline tests pass; replay is
  byte-identical. Publication bytes unchanged from checkpoint (12/64/664 unique).
- Proposed work-group/composer identity and role-aware credits before further
  expansion. No matcher fix or reclassification implemented in this audit.
  Audit files/docs remain uncommitted; no Qobuz calls, push, merge or deployment.

## 2026-11-13 — Work-group and role-aware evidence

- Implemented bounded movement-title context, shared multi-composer opus
  disambiguation, explicit vocal/chorus credits and conservative contiguous
  recording-group performer coverage. Unknown extra musical artists, changed
  anchors/composers, disjoint/repeated runs and context-boundary changes block repair.
- Preserved evaluate_v1/credits_v1 for historical audit replay. Added current
  76-selection comparison: all statuses unchanged, five evidence mappings improved,
  zero shared target-track assignments. Berlioz 1→5 movements, Winterreise 23→24
  songs, Pergolesi 7→12 sections and Grieg/Sibelius 4/4/9 separate mappings.
- Two new choral leads remain Unchecked pending completeness review. No general
  name aliases enabled. All 740 classification labels match checkpoint c1857a7;
  unique totals stay 12/64/664. No Qobuz calls or retrieval-data changes.
- All 43 offline tests, UI tests, JS syntax/build and diff checks pass. Browser
  verified group-credit and inherited-title evidence explanations. Updated docs
  and added reproducible group comparison report. Work remains uncommitted and
  unpushed; no merge or deployment.

## 2026-11-13 — Commit audit and work-group improvements

- User requested committing all pending changes: frozen baseline audit, current
  group comparison, role/context/work identity implementation, regenerated match
  evidence, UI explanations, regression tests and project/technical docs.
- Existing validation: 43 offline Qobuz tests, UI normalization/overlay/sort,
  JS syntax/build, browser evidence inspection and byte-identical regeneration.
  All 740 classification labels remain unchanged. No push/deployment requested.

## 2026-11-13 — Begin 30-release service comparison

- User authorized starting the proposed 10-empty / 10-unresolved Qobuz and
  10-Spotify comparison pilot. Fixed a disjoint dated sample and twenty shorter
  Qobuz queries; added resumable serial worker with persisted pacing, lock,
  per-query saves and first-warning STOP/no-retry handling. Three mocked safety
  tests pass. Initial sample selection correctly refused an already-Probable ID;
  replaced it with an unresolved control before any network calls.
- Offline inspection found Spotify cache holds album results, not full tracks;
  comparable programme-level audit is not possible from that evidence. A Brahms
  multi-work collection mapped to a Symphony No.1 album is a strong partial-programme
  warning, not a completed track-level rejection. Qobuz retrieval is running;
  final counts/findings pending. No publication changes or Spotify API calls.

## 2026-11-13 — Complete 30-release comparison pilot

- Twenty slow fallback searches completed without warnings: 17 nonempty queries,
  hits for all ten originally empty releases. Eight selected full albums inspected
  (seven newly fetched/one reused), all 423 tracks verified; metadata completed
  13:04 Europe/Amsterdam. Three target-heading programme/credit leads (Schnabel,
  Tennstedt, Kubelik) remain unpromoted pending completeness/session review.
- Reviewed ten cached unresolved controls and ten Spotify album-level cases.
  Spotify lacks tracks; one Brahms whole-collection→Symphony No.1 partial-programme
  warning and nine unverified cases, not a measured error rate. Target-wide credits
  and query relevance remain material bottlenecks; no catalogue-size conclusion.
- Preserved portable whitelisted search/metadata evidence, generated results and
  all-30 manual observations. Refreshed previously requested shared raw-cache
  archive to 1,786 responses: all old 1,759 member payloads unchanged, 27 added.
- All 47 mocked/offline tests pass. Export/report byte replay, credential-value
  scan and publication-byte preservation checked. Scores remain 12/64/664 unique,
  with no Spotify API or audio requests. Pilot changes uncommitted/unpushed;
  no automatic further fetches, matching-rule changes or deployment.

## 2026-11-13 — Query/target-credit refinement and Spotify track evidence

- User authorized refinements and track caching, requested local Spotify .env
  placeholders, then asked where sp holds secrets. Added placeholders preserving
  existing settings; found sp PKCE config/token cache under ~/.config/sp. Reused
  existing login with one successful refresh, no secret copying/display.
- Cached ten Spotify albums / 227 complete tracks at slow spacing, without
  warnings/audio/library calls. Added whitelisted shared archive, conflict-safe
  offline restore and audit. Confirmed Brahms collection→Symphony No.1 partial
  candidate and Found Dvorak Sixth/My Home candidate missing My Home. Eight other
  recording validations unresolved; no published Spotify labels changed.
- Implemented album-lead/compound-composer query proposals and relevance ranking.
  Two scoped query validations succeeded: Coltrane A Love Supreme editions found,
  with live variant flagged, and Casals/Mendelssohn trio candidates. Cached outputs
  shared; raw-request archive refreshed to 1,788 responses. No collection run.
- Derived explicit target performance scopes for 128 releases, with raw-source
  hashes. Added parent/child hierarchy, full cross-side range parsing, retained
  global-credit protection and ambiguity/non-musician guards. Real Bitches Brew
  credit-range regression prevents discarding required Joe Zawinul/Larry Young.
  Barenboim pilot improves from 23/31 flattened items to 8/8 work units, unpromoted.
- All 58 offline tests, UI tests/build/diff pass; Qobuz regeneration identical,
  all 740 labels preserved (12/64/664 unique). Secret scans pass. New work remains
  uncommitted/unpushed; no automatic scoring corrections, merge or deployment.

## 2026-11-13 — Commit service-comparison and refinement checkpoint

- User requested committing current work and a next-step recommendation. Checkpoint
  includes resumable comparison evidence/caches, query planning/validation,
  explicit target-credit model, Spotify track caching/audit, regression tests and
  technical/project docs. Local .env and OAuth credentials remain excluded.
- Prior validation: 58 offline tests, UI tests/build/diff, identical regeneration,
  unchanged published statuses and private token-value scans. No new tests or
  API calls needed solely for this commit. No push, merge or deployment requested.
- Recommend verifying the strongest Qobuz pilot leads for promotion before another
  search batch, plus a Spotify full-programme safeguard before publication.
  Recommendation does not authorize implementation or further fetching.

## 2026-11-13 — Validate four Qobuz pilot leads

- User approved the proposed next stage. Reviewed cached programmes, required
  credits and public recording documentation. Three new Probable candidates:
  Schnabel4429613, Tennstedt12130939 and Kubelik37312800. Barenboim3066447 excluded:
  EMI1966–69 target versus later DG cycle. No new Qobuz/Spotify requests.
- Added portable, hash-bound review ledger and reproducible offline audit, with
  exact Schnabel joined-track handling and Tennstedt target-only Adagio scope.
  Current matcher/complete movement checks still required; recording/edition
  limitations appear in local details. Original66+10 review scope unchanged.
- 63 offline/mocked tests pass; UI normalization/overlay/sort, JS syntax, static
  build and diff checks pass. Repeated generation identical; only the three
  intended labels change. Unique totals12Found/67Probable/661Unchecked; copies
  12/67/662. Spotify labels unchanged. Local detail views verified.
- Work remains uncommitted/unpushed; no merge/deployment. Next proposal: Spotify
  full-programme safeguard for the two confirmed partial matches before publishing.
  [Review and reproducible commands](../plans/2026-11-13-qobuz-lead-validation.md).

## 2026-11-13 — Spotify partial-programme safeguard

- User approved proceeding. Added portable candidate-specific negative review
  ledger and source-hash checks to the normal matching pipeline. Confirmed partial
  Brahms1012732 and Dvorak6119238 now Unchecked, with accepted album/confidence
  cleared; raw similarity signals, partial album and alternatives preserved.
  Details explain missing works. No unaudited replacement is silently accepted.
- Seven pipeline/guard tests and63 offline/mocked script tests pass; UI tests,
  syntax/build/diff checks pass. All741-copy comparison shows only the two intended
  Spotify objects change:254Found/275Probable/210NotFound/2Unchecked. Qobuz prior
  three promotions remain intact (12/67/662 copies). Local detail views verified.
- Used cached portable evidence only; no service calls, commit, push or deployment.
  Next proposal: examine Dvorak complete-cycle alternatives, cache first.
  [Implementation/limits](../plans/2026-11-13-spotify-programme-safeguard.md).

## 2026-11-13 — Commit validated leads and programme safeguard

- User requested a commit and next-step briefing. Checkpoint contains the three
  reviewed Qobuz Probable additions, rejected Barenboim cycle, Spotify partial-
  programme guard, portable evidence ledgers, UI explanations, tests and docs.
- Prior validation: seven pipeline/guard tests and63 offline/mocked script tests,
  UI normalization, JS syntax/build and diff checks pass. No implementation change
  since validation; no additional service calls needed for the commit.
- Recommend reviewing Dvorak complete-cycle alternatives using existing caches
  first, then a small broader Spotify programme audit. Further work, fetching,
  push, merge and deployment are not authorized by this status request.

## 2026-11-13 — Dvorak replacement, broader Spotify audit and readiness review

- User requested all three recommended stages in order. Reviewed two Dvorak
  alternatives (101tracks); selected39-track set supplies Sixth I–IV +MyHome with
  required artists, becomes explicitly reviewed Probable85. Original bad album
  preserved as rejected. Exact take/mastering remains unverified.
- Eight new multi-work risk cases (4Found/4Probable,140tracks) reviewed: wrong jazz
  concert1252193, unrelated Debussy/Ravel5249935 and Mendelssohn missing Scottish
  9458258 now Unchecked. Three listed-programme and two opera act-heading supports
  retained, recording identity unresolved. No population accuracy claim.
- Fetching slow/resumable, no API warnings/retries. Fixed local export/checkpoint
  variable bug; Dvorak finalized offline without re-fetching. Shared separate
  archives/scopes/audit; original pilot and Qobuz archives byte-identical.
- Fresh prospective checkout without .env/ignored caches passes9pipeline/guard
  +66script tests, audit verification, identical Qobuz replay, UI/JS/build. Secret
  scan, whitelist/build-boundary and local browser checks pass. Spotify copies
  254Found/273Probable/210NotFound/4Unchecked; Qobuz unchanged12/67/662.
- Readiness review fetched origin/main0847175 (ancestor; no conflict expected).
  Fixed CI test discovery, added portable evidence verification and Pages test
  gate. Locally ready for PR with documented match-quality limitations; remote CI
  not run for uncommitted follow-up. No commit/push/merge/deployment in this task.
  [Findings, scope and release handoff](../plans/2026-11-13-spotify-followup-readiness.md).

## 2026-11-13 — Commit Spotify follow-up and readiness checkpoint

- User requested committing completed follow-up work: Dvorak replacement, eight-
  album audit and three new programme rejections, shared evidence/reviews, worker
  scope support, UI findings and CI/Pages validation gate. Credentials/state excluded.
- Prior fresh-checkout validation:75Python tests, portable audit, identical Qobuz
  replay, UI/JS/build and credential/build-boundary checks passed. No code changes
  since those checks; no service calls required for this commit.
- No push, merge or deployment requested. Next release action remains push/PR
  when authorized, with green remote checks before merge.

## 2026-11-13 — Merge and verify Qobuz/Spotify release

- User authorized push, PR, green-check merge and live Pages verification. Pushed
  feature, opened [PR2](https://github.com/Sigmus/ali-discogs/pull/2), PR test run
  [43452252865](https://github.com/Sigmus/ali-discogs/actions/runs/43452252865) passed;
  merged expected feature headb0c93bc as02ec297. Local main fast-forwarded.
- Main test43452407943 and Pages43452407863 both succeeded. Verified live HTML,
  JS, CSS, collection/summary/Qobuz JSON byte-identical to release. Deployed browser
  Dvorak detail shows explicit85%Probable replacement and independent Qobuz result.
  Live figures: Spotify254Found/273Probable/210NotFound/4Unchecked copies;
  Qobuz12Found/67Probable/662Unchecked. Four withheld programmes preserved.
- [Live collection](https://sigmus.github.io/ali-discogs/). No new Spotify/Qobuz
  catalogue calls; matched scores retain previously documented limitations.
- Release documentation updated separately on main; no product/data changes.
  Further matching work remains proposed, not part of this completed release.

## 2026-11-13 — Diagnose Qobuz album-link404

- User reported /album/0002894786633 returning404, including while logged in.
  `public_album()` synthesizes a bare /album/ID URL; cached API metadata and shared
  raw archive instead contain a full locale/album/slug/ID URL. Portable whitelist
  currently discards url/slug. This is an application URL-generation bug, not
  evidence of a failed match, login issue or album removal.
- Qobuz public search indexes the same ID under its full us-en album route. No
  authenticated catalogue calls made. Proposed follow-up: preserve canonical
  cached URL/slug and use it for publication, with offline replay/link tests.

## 2026-11-13 — Fix Qobuz links everywhere from cached canonical routes

- User authorized fix, commit and push. Added deterministic portable index of
  1,043 canonical URLs from shared successful metadata; publisher uses provider
  locale/slug route with exact host/ID validation and safe search fallback.
  Corrected selected albums, all candidates, historical pilot URLs and sample
  links. Historical completeness report updates only its pilot-file fingerprint.
- Matching evidence archives byte-identical. URL-stripped all740 publication
  records are identical: no score, status, programme or recording-review change.
  No new authenticated catalogue calls. Browser opened the reported album's full
  cached fr-fr URL successfully (album title visible behind cookie consent).
- Four new URL tests cover reported regression, invalid/missing routes, complete
  published/pilot coverage and deterministic offline index export. Total79Python
  tests, UI URL normalization, syntax/build/diff checks pass. Documentation updated.
- Main push will trigger the existing validated Pages workflow; verify its result
  before claiming the link correction is live.

## 2026-11-13 — Qobuz round2 completes with three new Probables

- User authorized cached near-matches first, then20-release slow fallback batch.
  Isolated on `codex/qobuz-coverage-round2`. Klemperer6381208 and Ancerl6599326
  pass exact named-section/performer reviews. New deVito8151148 pair passes7
  movements/both performers after bounded malformed-heading interpretation.
  Local counts12Found/70Probable/659Unchecked copies; unique12/70/658.
- Forty fixed queries yield27nonempty,18/20releases with hits,107release-candidate
  pairs. Twelve pairs with existing metadata have no unmodified full acceptance.
  Two selected new metadata albums complete (15tracks). Richter3667210 remains
  Unchecked for target catalogue/key conflicts; no guessed opus alias enabled.
- Retrieval serial, >=15second spacing including discovery, resumable, no API
  warnings/retries/audio. Shared41new responses; archive1,829, all prior1,788
  payloads unchanged. Original evidence archives unchanged; canonical URLs1,045.
- Nine pipeline tests +75script tests (84total), audit/replay, UI/JS/build/diff and
  private credential-value checks pass. Only3intended publication records change;
  repeated output identical; local Klemperer/deVito details verified. Spotify
  untouched. Work uncommitted/unpushed; deployed main still12/67/662Qobuz copies.
- [Scope, outcomes, evidence and next proposals](../plans/2026-11-13-qobuz-round2.md).
  No additional batch, commit/push or deployment authorized by this completed run.

## 2026-11-13 — Round2 checkpoint and query-strategy follow-up

- User-requested round2 commit `877bc5a` saves three reviewed matches and reusable
  evidence. No push/deploy requested.
- Cached Richter/Maazel audit resolves Sz95/G-major source conflicts against
  Warner publisher catalogue; complete3+5 movements and correct work-specific
  orchestras pass. Source-bound review adds one Probable, local copies12/71/658.
- Authorized ten-release/twenty-query paired strategy trial started with fixed
  scope, headline-ensemble preference and existing paced/resumable STOP worker.
  No full metadata expansion or automatic search-hit acceptance.
- Validation:78script+9pipeline tests, Node normalization and local build pass;
  original round2 audits remain historical. Trial outcome recorded in its plan.

- Query trial completed20/20without warnings: broad10/10nonempty versus catalogue9/10,
  with31additional candidate pairs; no new metadata or search-hit promotions.
  Shared archive1,845responses preserves all1,829previous payloads. No active worker.


## 2026-11-13 — Offline query-trial candidate screen

Screened81deduplicated release/candidate pairs (correcting earlier85arithmetic),
19with complete cached metadata across all shared archives and62uncached.
No candidate passes all existing guards; three programme/credit leads still
need completeness/recording review. Schnabel complete set reused from comparison
archive, avoiding a proposed fetch. Fixed proposed metadata scope narrowed to
Prague Quartet Dvorak and exact Klemperer pairing; no API calls/publication changes.
Report replay verified deterministic; publication bytes unchanged.


## 2026-11-13 — Cached Schnabel late-sonata validation

User-authorized review promotes2966855 to Probable85: five complete sonatas with
required pianist; two hash-bound joined sections reconcile LP/digital divisions.
Warner barcode catalogue and preserved target dates support recording family,
not exact take/mastering. No API calls; reused comparison archive. Local copies
12/72/657.79script tests, Node normalization/build pass; no commit/push/deploy.


## 2026-11-13 — Two scoped metadata albums retrieved

User-authorized paced fetch completes Prague Quartet71tracks and Klemperer6tracks,
full counts/IDs validated, no warnings. Portable metadata and reproducible offline
audit saved; request cache and canonical URLs exported. Klemperer programme/credits
supported but overture/session review remains; Dvorak member credits and No.8
ambiguity unresolved. No new promotions or publication actions.


## 2026-11-13 — Klemperer follow-up review

Bounded review promotes14934969: complete5-movement Symphony6 and Leonore1,
required artists and Warner October1957 recording-family support. Exact overture
session/take/mastering caveats preserved. Dvorak remains unresolved for individual
member credits and heading ambiguity; no additional API calls or relaxed rules.
Local copies12/73/656.80script tests plus Node/build checks pass. User authorized
continuation without routine confirmation; no commit/push/deploy requested.


## 2026-11-13 — Cumulative follow-up checkpoint review

Fixed query-report lead scoring for headline ensembles and expanded cache flags
to all shared metadata archives; saved queries/hit counts unchanged. Exactly three
follow-up match records differ from877bc5a. All1,829prior cache payloads preserved;
archive now1,847. Secret-value scan passes. Full make test passes9pipeline and
80script tests plus Node/Spotify checks. No publication operations performed.

Portable replay from a temporary copy containing only code/shared data (no .env,
raw caches or .qobuz-poc), using uv offline, reproduced qobuz_matches byte-identically.

## 2026-11-13 — Follow-up commit and branch push

User requested committing and pushing the validated follow-up on
`codex/qobuz-coverage-round2`: three reviewed Probables, portable query/metadata
evidence, preserved request cache, report corrections and reproducibility checks.
No merge or Pages deployment requested.

## 2026-11-13 — PR3 deployed and unmatched audit started

Merged PR3 as8afd7dd after passing CI. Main test/Pages succeeded; live Qobuz
asset byte-identical to main, copies12/73/656. New branch codex/qobuz-unmatched-audit
classifies655remaining unique releases offline:324no saved hits,14metadata needed,
316work/credit unresolved,1completeness gap. Prior rejected recording excluded
from usable leads. No new API calls or promotions; next scope strongest metadata leads.

## 2026-11-13 — Four unmatched metadata leads fetched and audited

Slow resumable batch saves77tracks across4albums without warnings. Previn Nevsky
is wrong orchestra (Los Angeles versus required London); opera cast/context and
Karajan musical hierarchy/Op71a/71 remain unresolved. No promotions. Corrected
query validation archive included in audit, recovering Coltrane hits in inventory.
Current655triage324/10/320/1. Shared metadata/cache preserved; no publication actions.

## 2026-11-13 — Karajan bounded hierarchy correction

All original source units partitioned into two works without global parser change;
complete9tracks and required artists support Probable85 for10738828. DG catalogue
and1983provenance support recording family; takes/mastering unresolved.81script
tests including missing source/candidate sections pass, Node/build pass. No API
calls, commit or publication. Local copies12/74/655; deployed12/73/656 unchanged.

## 2026-11-13 — Opera cast audit against raw target credits

Both cached operas compared to original source actor/role lists. Earlier Tannhauser
additional-singer concern corrected: those bass singers are in target too. Four
boy-page credits absent by exact candidate key; chorus-master role differs. Tristan
has all named singers but chorus/translated orchestra unresolved. No promotions;
missing credit keys are not wrong-cast proof. Portable report and script saved.


### 2026-11-13 — Tristan chat-link404 correction

The assistant supplied a guessed/shortened nl-en slug; saved canonical route was
already correct. Opened exact saved fr-fr route in browser and verified album
page/29tracks. Resolver now prefers canonical index over plausible supplied URL;
--album-id prints safe links offline. Regression for reported slug passes; all
publication Qobuz links match index. AGENTS requires exact resolver use in chat
as well as code/docs. Five URL tests pass. No commit/push requested.

## 2026-11-13 — Major cross-service validation gap documented

User explicitly requested recording the Spotify/Qobuz standards difference.
Tristan Spotify Probable0.737 is legacy album-level evidence, not full-edition
validation. Qobuz remains unresolved for work/credit grouping; raw target also
contains29:20rehearsal side absent by label from cached Qobuz tracks. Corrected
prior conversational overstatement: Spotify rehearsal omission is not yet
track-verified; Qobuz rehearsal gap is not its sole implemented blocker. No
status/score/code changes in this documentation task.

## 2026-11-13 — Unmatched enrichment checkpoint publication

User requested commit everything, merge to main and push. Includes bounded
Karajan Probable, four-album portable metadata/cache, opera cast audit, canonical
URL precedence/CLI/regression guard, and major Spotify/Qobuz validation-gap docs.
No credential files or ignored run state included.

PR4 merged as20dc0e8 after GitHub CI passed (run43475914824). All work saved
in f64bb7f and merged/pushed to main; local full checks91Python tests plus
Node/Spotify checks passed. Deployment completion not yet verified.

## 2026-11-13 — Opera source roles and act coverage

Hash-bound review equates ensemble names only with a recording-specific reason,
keeps every musical credit, and checks acts. Tristan2996680 becomes Probable85
for acts I–III (29 tracks); side J rehearsal stays a visible edition gap.
Tannhäuser4365080 stays Unchecked because four page singers are absent, the
chorus master is credited as director, Act III scene 2 is unlabelled, and a
joined credit names Orchester der Deutschen Oper Berlin. Published copies
12/75/654, unique 12/75/653. No API calls. Browser confirmed the Tristan detail,
canonical album route, and Qobuz counts. Focused script and normalization tests
passed. Not committed.

## 2026-11-13 — Gould Well-Tempered Clavier pairs

The nearest cached lead after Tristan was Barenboim volume 9866861. It is an
EMI/La Voce del Padrone issue of the cycle already rejected against DG 4631272,
so it stays unpublished. Gould2175684 / Sony 0886443628625 has all 48 prelude
and fugue pairs, BWV 846–893, with Gould on every track. Three untitled preludes
are bound to the following fugue. Volume headings are containers. Probable85;
1975 LP mastering is not verified. Copies 12/76/653, unique 12/76/652. No API
calls. Focused tests and normalization passed. Not committed.

## 2026-11-13 — Michelangeli mazurka headings

DG 2530 236, Michelangeli6678433, matches the 13-track DG album
`uoihym7lfe48a`. The heading Mazurkas is a container; each numbered mazurka,
the Prelude, Ballade and Scherzo keeps its own track, with Michelangeli
credited. Probable85. The 2018 digital issue is not verified as the 1972
mastering. Copies 12/77/652, unique 12/77/651. No API calls. Container tests
passed. Committed with the Tristan and Gould reviews as 0d37bcb.

## 2026-11-13 — Eight cached near-misses planned as one pass

The remaining close cached albums are Kempff Op. 81a, Rubinstein Op. posth. 72
No. 1 on two Discogs releases, Davis’s Swan of Tuonela, Haebler’s two F-major
sonatas, Time Out’s Audrey, Jazz Samba’s Baia, Dutoit’s *La Jeunesse d’Hercule*
and Ellington’s two Shepherd takes. The pass reviews all eight before reporting.
A missing named piece stays unpublished. No implementation in this step.

## 2026-11-13 — Eight cached near-misses reviewed together

Probable85: Kempff11562013, all 32 sonatas, including Op. 81a and the mis-tagged
Op. 26 scherzo; Rubinstein3475547 and11168177, all 19 nocturnes on the Warner
superset; Davis/Sibelius6029612, the Boston box works including the English
Swan title; Jazz Samba5177097, Baia spelled Bahia, with the short second
Desafinado left out; Ellington7525022, both Shepherd takes bound by order and
duration. Withheld: Haebler4641786, Time Out2383925 and Saint-Saëns10102576.
Copies 12/83/646, unique 12/83/645. No API calls. Binding tests and
normalization passed.

## 2026-11-13 — Unmatched inventory refreshed after publication

Offline audit now follows the published matches. 645 unique unchecked releases:
324 no saved hits, 10 metadata-needed, 306 work/credit unresolved, 4 reviewed
withholds (Tannhäuser4365080, Haebler4641786, Time Out2383925,
Saint-Saëns10102576), and one completeness caution, Barenboim9866861 against
the later DG cycle. No new searches, fetches, or promotions. The audit script
completed and wrote `data/qobuz_unmatched_audit.json`.

## 2026-11-13 — Seven metadata-needed albums fetched

Paced album/get for seven saved hits, 410 tracks, archived in
`data/qobuz_metadata_needed.json.gz`. No publication. A Love Supreme594243 has
all four parts and the joined Pursuance/Psalm duration, but McCoy Tyner is not
in the credit string. Rachmaninoff4469662 lacks the Etudes-Tableaux. Shostakovich
6105272 has the quartets and quintet in the work field, credited to a later
Borodin lineup rather than Berlinsky or the Beethoven Quartet. Richter6465567
is the Matthew Passion. Serkin6907296 lacks the three-piano concertos. Rilling
7975379 lacks BWV 149 and 188. Souzay9850479 has two of twelve Duparc songs.
Matthew Passion5140330, Schütz6091545 and Chopin12419639 were not fetched:
their saved hits name different works or Erich Bergel. Inventory is 324/3/313/4/1.

## 2026-11-13 — Menuhin Paganini concertos published locally

Discogs 2527568 / Qobuz 0077774708852 is Probable 85. The source heading is not
a third work. Op. 6 and Op. 7 each keep three movements, with Menuhin, Erede and
the Royal Philharmonic on every track. The source calls Op. 6 D major; the file
says E-flat, the sounding key. Warner digital is not the 1975 La Voix De Son
Maître pressing. Bitches Brew 7609610 was inspected and not published: Larry
Young is absent from the two tracks that name him. Copies 12/84/645, unique
12/84/644. Heading tests and normalization passed. No API calls.

## 2026-11-13 — Bitches Brew credit gap recorded

Discogs 7609610 stays unchecked. The six titles are the 1970 album. Larry Young
is required on four of them; Qobuz 0886443874428 and 0074646577424 credit him
on Pharaoh’s Dance and Spanish Key only. The six-track file names Zawinul on
John McLaughlin, and the seven-track file adds Feio. The open questions are
whether a review may accept that gap, and which facts the explorer should
show. No matcher or UI change. See
[Bitches Brew credits](../plans/2026-11-13-bitches-brew-credits.md).

## 2026-11-13 — Half-coverage cached albums reviewed together

Probable 85: Bach two-piano concertos 4483876, including BWV 1062; Ravel
7119504, both piano concertos; Stern 6472687, Tchaikovsky and Mendelssohn;
Busch Brandenburg 3–5, 8165012; Rubinstein mazurkas 5939010, all 51.
Withheld: Ciccolini 2486104 because Op. 22 is absent, Francescatti 3584044
because Concerto No. 3 is absent, Furtwängler 7844349 because Oberon and The
Merry Wives of Windsor are absent. Twelve other albums from this band stay
unchecked. Bitches Brew stays parked. Copies 12/89/640, unique 12/89/639.
Inventory of the 639 still unchecked: 324 no saved hits, 3 metadata-needed,
304 work or credit gaps, 7 reviewed withholds, and the Barenboim completeness
caution. Review tests and normalization passed. No API calls.

## 2026-11-13 — Twenty searches for releases with no saved hit

Forty paced queries, fifteen seconds apart, at most five albums each. Thirty-one
queries returned something. Nineteen of the twenty releases now have hits, 126
pairs in `data/qobuz_empty_searches.json.gz`. Sellheim’s complete cello-and-piano
set, 7421796, came back empty; that is not confirmed absence. No album metadata
was fetched and no match was published. Inventory of the 639 unchecked releases
is now 305 no saved hits, 18 metadata-needed, 308 work or credit gaps, 7 reviewed
withholds, and the Barenboim completeness caution.

## 2026-11-13 — Five title-aligned albums downloaded

Downloaded 37 tracks for BWV 201, Toscanini, Barbirolli’s Fifth, Barbirolli’s
Ninth, and Cluytens Psyché. Harasiewicz’s 10-track hit was not the Philips box
and was not downloaded. Toscanini 10757104 is Probable 85: both symphonies, four
movements each, Toscanini and the NBC Symphony on every track. The BNF file is
not verified as the 1980 Victrola pressing. BWV 201 has all 15 numbers and the
named singers, and stays unpublished because the LP lists two side ranges.
Barbirolli’s Fifth is the New Philharmonia and the Ninth is Berlin; neither file
has both symphonies. Cluytens has Psyché and the Rédemption excerpt, not Le
Chasseur maudit. Copies 12/90/639, unique 12/90/638. Inventory of the 638 still
unchecked: 305 no saved hits, 14 metadata-needed, 311 work or credit gaps, 7
reviewed withholds, and the Barenboim caution. Binding and URL tests passed.
The explorer shows 85% and 2/2 for Toscanini. No further search.

## 2026-11-13 — BWV 201 side ranges published

Musique Royale 199 021 lists the cantata as Nr. 1–7 and Nr. 8–15. The BNF file
has those fifteen movements in order. The heading is not a third work. Kurt
Thomas and the Gewandhaus are on every track, the Thomanerchor is on both sides,
and Leib, Adam, Fleischer, Stolte, Apreck, and Rotzsch each appear. Probable 85.
Dropping a singer or moving a movement onto the other side fails the review.
Copies 12/91/638, unique 12/91/637. Inventory of the 637 still unchecked: 305
no saved hits, 14 metadata-needed, 310 work or credit gaps, 7 reviewed
withholds, and the Barenboim caution. The explorer shows 85% and 2/2. The BNF
file is not verified as that LP. Barbirolli and Cluytens stay unpublished.

## 2026-11-13 — Hungarian Quartet published; Klien stays unpublished

Downloaded the DG Klien/Amadeus file and the Hungarian Quartet Fifths and Lark
file, 14 tracks. The quartet file has both works, four movements each, and
credits the Hungarian String Quartet on every track. Probable 85 for 15980846.
The 2015 file is not the 1958 Columbia pressing. Klien 12329947 has K. 478 and
K. 493 with Klien and the Amadeus Quartet, but Norbert Brainin, Peter Schidlof,
and Martin Lovett are not named, so it stays unpublished. Wand’s Bruckner 5
hit is the Berlin Philharmonic, not Cologne. The Klemperer Eroica files omit
Fidelio or substitute Leonore overtures, so neither was downloaded. Copies
12/92/637, unique 12/92/636. Inventory of the 636 still unchecked: 305 no saved
hits, 12 metadata-needed, 311 work or credit gaps, 7 reviewed withholds, and
the Barenboim caution. The explorer shows 85% and 2/2.

## 2026-11-13 — Brendel’s late Liszt recital published

Philips 9500 775 has nine late pieces. The Decca file has those nine, with
Brendel on every track. Probable 85 for 4395895. N° 2 of the third year is
Aux cyprès No. 1, the first threnody. The file is not verified as that Philips
pressing. Carnaval 13671866 stays unpublished: the LP joins movements that the
file splits, and Prêtre is not credited on the piano-only numbers. François
12419718 stays unpublished: the saved file is the 176-track Chopin box, not
Columbia FCX 30120. Copies 12/93/636, unique 12/93/635. Inventory of the 635
still unchecked: 305 no saved hits, 12 metadata-needed, 310 work or credit
gaps, 7 reviewed withholds, and the Barenboim caution. The explorer shows 85%
and 9/9. Commit 8e38da9.

## 2026-11-13 — A verified publication continues without another prompt

A started fail-closed Qobuz pass now commits each publication that passes its
tests, the build, and the explorer check, then reviews the next cached
candidate in the same turn. A failed candidate is recorded and the pass
continues. It stops when the next step needs a new search, a new download, a
new review kind, or a decision that is still a proposal. No push. The current
cached band is already judged, so this pass stops there.

## 2026-11-13 — The next cached albums stay unpublished

No new search or download. Barenboim 3066447 is the 102-track DG sonata cycle,
not the eight-sonata box. Karajan 7860979’s 1970s anthology is not the 1982
nine, and the 35-track file names the symphonies in the work field under a
1962 date. Berman 15263974’s cached files are the Années, the concertos, or
the etudes, not the sonata coupling. Furtwängler 3737065’s file says Entracte
III and Ballet II, not Entr’acte No. 2 in D major and Ballet No. 2 in G major.
Trouard 8291074 is the stop: Qobuz 3610154901657 has the fourteen waltzes in
the CBS 51 003 order, with Trouard on every track, but “N°2” does not count as
the file’s “No. 2”. That exception stays a proposal. Op. 70 No. 2 is F minor
on the file and A-flat on the CBS label. Copies unchanged, 12/93/636.

## 2026-11-14 — Trouard’s fourteen waltzes published

A printed N° is that subnumber. It does not cover a different number. CBS
51 003 has fourteen Chopin waltzes. The 1961 file has those fourteen, in that
order, with Raymond Trouard on every track. Probable 85 for 8291074. Op. 70
No. 2 is F minor on the file and A-flat on the LP label. The file is not
verified as that CBS pressing. Columbia FCX 30205 and FCX 30097 stay
unpublished: their order is not this file, and the 1953 and 1959 files use
another order. Copies 12/94/635, unique 12/94/634. Inventory of the 634 still
unchecked: 305 no saved hits, 12 metadata-needed, 309 work or credit gaps,
7 reviewed withholds, and the Barenboim caution. Binding tests passed. The
explorer shows 85% and 14/14.

## 2026-11-14 — Salome stays unpublished

The next cached album is Salome 7657012. Qobuz kkjll119bbov7 names Hildegard
Behrens and Herbert von Karajan, in 26 scene tracks. The LP is four scene-sides,
and the act review does not classify them. Munrow 6364992’s file has 61 tracks
against 79. The Four Seasons hits for 17623039 are compilations, not the
Schwalbé and Karajan concertos. No further publication.

## 2026-11-14 — Karajan’s Salome published

Scene sides may cover one opera when the file numbers those scenes in order
from 1, with no gap. His Master’s Voice SLS 5139 has four scene-sides. The
file has scenes 1–4, 26 tracks, with Karajan and the Wiener Philharmoniker on
every track and every named singer. Probable 85 for 7657012. The file does not
mark the part boundaries inside a scene. Angervo is contralto on the file and
alto on the LP. Van Dam is bass-baritone on the file and baritone on the LP.
The 2026 file is not that HMV set. Copies 12/95/634, unique 12/95/633.
Inventory of the 633 still unchecked: 305 no saved hits, 12 metadata-needed,
308 work or credit gaps, 7 reviewed withholds, and the Barenboim caution. Opera
tests passed. The explorer shows 85% and the canonical album link.

## 2026-11-14 — The Ring needs a review the current kinds do not cover

No new search or download. Schwarzkopf 6257908 stays unpublished: Qobuz
5099991845955 is a 197-track anthology, not Columbia 33CX 1044 with Gerald
Moore. Otello 7095769 stays unpublished: the Karajan files name Tom Krause,
who is not on Decca SET 209-11, and the Tebaldi file is Alberto Erede with
Santa Cecilia. Rubinstein 13927062 stays unpublished: the cached file is the
concerto, not the waltzes and polonaises. Furtwängler 4256464 is the stop.
Dacapo 1C 147-02 275/92 M lists Rheingold, Walküre, Siegfried and
Götterdämmerung as scene-sides with Teil cuts. Qobuz qs49hef2mbbsb has those
four operas in order, 310 tracks, with Furtwängler and the Rome orchestra on
every track. Scene-sides and the act review each cover one opera, and the
file names singers this LP does not. No publication. Counts unchanged.

## 2026-11-14 — St Matthew Passion uses another number count

The Ring file has the four operas in order, but Siegfried Act 1 Scene 3 is
not a numbered scene. The forging cues are labeled Scene 2. Getz/Gilberto
4073133 has the eight songs in order on the eight-track file, and Milton
Banana is not named. Moldau 13538423’s file has Vyšehrad, Vltava and the
meadows, then Slavonic Dances, and not Tábor. Klemperer 25537708 is the
stop. Columbia SAXF 243 / 7 lists Nos. 1 to 78. The file’s numbers run
through 68, and some of those numbers are split into lettered tracks. That
is a different count, so it is not this side scheme. No publication. Counts
unchanged.

## 2026-11-14 — Mancini’s Pink Panther score published

DOL DOL996HG has twelve film cues. Qobuz 0886445007398 has those twelve in
that order. The performer credit is Henry Mancini & His Orchestra, and the
theme adds the chorus. Probable 85 for 11938972. The file does not mark which
It Had Better Be Tonight is instrumental and which is vocal. No singer is
named on the vocal cue. James Galway’s track and the uncredited Meglio Stasera
stay outside the twelve cues. The 2014 file is not that DOL pressing.
Gieseking 12977198 stays unpublished: Absolutely Classical Volume 122 is 17
tracks, not the box. Copies 12/96/633, unique 12/96/632. Inventory of the 632
still unchecked: 305 no saved hits, 12 metadata-needed, 307 work or credit
gaps, 7 reviewed withholds, and the Barenboim caution. Binding tests passed.
The explorer shows 85% and 12/12.

## 2026-11-14 — Kondrashin’s New World published

Decca LXT 5495-6-7 and SXL 2101/03 name Paul Kuen. The cached Rheingold files
name Paul Kuentz, so 1989694 and 4268630 stay unpublished. The notes do say
the mono set is auto-coupled. Abbado’s Brahms file is the Berlin
Philharmonic throughout and adds other works; the LP also names Vienna,
Dresden, and the London Symphony. Tilson Thomas’s Tchaikovsky file is another
set of orchestras. Paukenmesse’s files are other masses. The Duparc file is a
mixed recital. The cantata file is C.P.E. Bach. The cello-sonata file is
Chopin. Karajan’s file is the Eroica, not the Seventh.

Decca SXDL 7510 is Kondrashin’s New World with the Wiener Philharmoniker.
The file has the four movements, in order, with both names on every track.
Probable 85 for 9739139. The LP prints Kiril and the file spells Kirill. The
1980 file is not verified as that pressing. Copies 12/97/632, unique
12/97/631. Inventory of the 631 still unchecked: 305 no saved hits, 12
metadata-needed, 306 work or credit gaps, 7 reviewed withholds, and the
Barenboim caution. Binding tests passed. The explorer shows 85% and the
four movements under the one symphony.

## 2026-11-14 — Fasano’s four Vivaldi concertos published

Argo ZRG 515 has the Harmoniemesse in six movements, with Spoorenberg, Watts,
Young, Rouleau, Guest, Runnett and the Academy. The file has those six. Neville
Marriner is Leader on the LP and is not named, so 9398840 stays unpublished.
Decca SXL 6162 is Maazel and the Wiener Philharmoniker in the Little Russian.
The cached symphony file is the Pittsburgh Symphony and adds Rimsky-Korsakov’s
Antar. Jazz Images 37008 names Oscar Peterson, Buddy Rich, Herb Ellis and Ray
Brown. The eleven-song file names Ella and Louis, and Brown on one song. The
75-track duet box names Peterson and still omits Rich, Ellis and Brown.

La Voix de Son Maître FALP 428 lists four Vivaldi concertos: G major, C minor,
E-flat la Tempête En Mer, and A major. The 1957 file has those four, three
movements each, in that order, with Fasano and I Virtuosi Di Roma on every
track. Probable 85 for 9343746. The LP does not print RV 532, RV 120, RV 253
or RV 546. The cover says Virtuosi Di Roma and the labels add Collegium Musicum
Italicum. The file is not verified as that pressing. Solti’s Götterdämmerung
8982341 is the stop. Decca SET 292-7 has fourteen Teil sides. The file has 54
prologue and act cues, which the scene review does not classify. Copies
12/98/631, unique 12/98/630. Inventory of the 630 still unchecked: 305 no saved
hits, 12 metadata-needed, 305 work or credit gaps, 7 reviewed withholds, and
the Barenboim caution. Binding tests passed.

## 2026-11-14 — Albums use the header’s side inset

The main column is no longer capped at 80%. Filters, the table, and album
details grow with the window. Both sides use the header’s 16px inset, so the
left edge lines up with “Ali’s collection” and the right gap matches. The
“Albums” heading and the release-count line under it are gone. The filtered
count above the table remains. The space above the filters is the same 16px
as the side inset. Shelf and Captions sit beside the table as a prototype.
Covers was dropped. The layout switch uses the line icons, ordered table,
captions, then the hover shelf. Long titles stay on the sleeve.

## 2026-11-14 — Reviewed Cursor changes and restarted local UI

Reviewed commits since66ba56a, current matching integration/review decisions and
latest full-width/Shelf/Captions UI changes. Main is ahead of origin by two local
UI commits (6bccef0,e5ea3bd); no push requested. Node normalization and JavaScript
syntax checks pass. Rebuilt dist and restarted local server127.0.0.1:8000.
No enrichment, status changes, commits or deployment actions performed.

## 2026-11-14 — Remaining12+305 retrieval prepared

User authorized both groups and progress tracking. Frozen83deduplicated uncached
metadata albums and603new queries for305empty releases; phase checkpoints and
STOP guards, whitelisted exports. No automatic matches or new-hit downloads.

Started13:16Amsterdam;2/83metadata outputs saved initially without warnings.
Hourly monitor qobuz-remaining-retrieval-progress active; idle-sleep assertion tied
to worker. Fixed-scope/resume test passes; no API warning retries authorized.

## 2026-11-14 — Multi-select UI options prototyped

Separate real-data comparison for six filters: compact checklist, searchable
chips, draft/apply panel. OR within/AND across; main collection unchanged. Browser
verified527SpotifyFound+Probable,43Brahms,254panelFound; build/JS/normalization pass.
No design chosen or main-filter implementation yet. Qobuz retrieval continues.

## 2026-11-14 — Searchable multi-select filters implemented

User selected B. Six native selects now backed by searchable checkbox menus and
removable chips; repeated URL params preserve old single-value links. Scoped
checkbox/menu styles fix prototype collision/clipping. Browser527status union,
29withBrahms,527afterchip removal; Escape/search/reload checked. Node filter
regressions, syntax and build pass. Qobuz worker unaffected; no commit/push.

## 2026-11-14 — Multi-select pushed; per-picker order options

Pushed6a48d70to main. New independent ordering prototype compares segmented
MostFrequent/A–Z, Alphabetical checkbox and Order menu; defaults frequency.
Browser verifies selection preservation and independent order. No main ordering
change yet; choice pending. Qobuz retrieval continues independently.

## 2026-11-14 — Per-picker footer ordering implemented

User chose Alphabetical checkbox between selected count and Clear selection.
Removed global switch; frequency default independently per dropdown. Browser
checks ordering, selection preservation and reopening; filter regression/JS/build
pass. No matching/data changes or Qobuz worker interference. No commit/push.

## 2026-11-14 — Collection title renamed

User requested ajozi vinyl (corrected spelling from vynils). Updated main
header brand and browser title; rebuilt local UI.

## 2026-11-14 — Discogs link moved to header

Removed collection footer (cover note, duplicated Discogs link and sample/back
link). Header now reads ajozi vinyl on Discogs, linking directly to the Discogs
collection. Fixture URL remains supported; removed obsolete footer bindings.

Header refinement: on Discogs link reduced to11px, retaining baseline alignment.

Search moved after Decade in the same single-column grid width as the pickers.

Clear now occupies one grid cell immediately after Search.

Search input height/padding matched to multi-select triggers (26px,3px 8px).

## 2026-11-14 — Non-table sorting bar aligned with result count

Captions/Shelf sorts now sit immediately after release count, limited to Year,
Composer, Spotify and Qobuz, using table-header uppercase type styling. Table
column sorts unchanged; sorting event handling covers the count row as well.

Non-table sort refinement: removed Spotify/Qobuz buttons; Captions/Shelf offer
Year and Composer only. Table sorting remains available on all columns.

## 2026-11-14 — Active documentation simplified and next sequence agreed

Replaced accumulated context/backlog handoffs with current state, explicit work
status and one ordered follow-up. Preserved previous backlog detail in a dated
archive and linked existing case plans. Recorded retrieval → validation/export →
offline Qobuz audit/rule refinement → UI checks → scoped Spotify evidence audit.
Clarified saved statuses, heuristic scores and possible Spotify demotions.
Metadata checkpoint83/83 complete; search124/603 running at14:11 Amsterdam,
with no warning in inspected tail. UI changes through749ba61 pushed to main;
retrieval changes remain local. Documentation-only cleanup; no matcher changes.

Commit preparation: offline fixed-scope/resume regression passes using uv with
requests; diff whitespace check passes. Includes the completed83-album sanitized
metadata export, frozen scope and worker/test. Live credentials/state excluded.

## 2026-11-14 — Discogs-style detail options

Removed Albums back button; corrected runtime page title to ajozi vinyl. Added
three switchable detail layouts using saved Schumann7946604 metadata and service
statuses, retaining the current theme. Browser confirmed populated metadata,
tracklist/credits and service evidence. Explicitly surfaced published-data gaps
(no movement detail, instrument roles or notes); no invented source fields.
Build, JS syntax and normalization regressions pass. Layout selection pending;
retrieval untouched.

## 2026-11-14 — Detail layout C implemented

User selected catalogue sidebar. Preserved all existing service evidence and
alternates; moved programme and credits before services. Normalization retains
source track positions/types/durations and country/released for display without
changing matching inputs. Responsive single-column layout. Browser inspected
Schumann7946604 with facts, heading, credits and service candidates populated;
JS syntax, normalization regressions and build pass. Not committed or pushed.

## 2026-11-14 — Retrieval setup and detail layout pushed

User-requested push succeeded: main749ba61 →66b35d4, including5545435.
Latest checkpoint notes remain local; deployment not verified. Worker untouched.

## 2026-11-14 — Filter surface options prototyped

Four switchable treatments around the real interactive collection: soft raised
band/bottom border, dark band/border, violet tint/border, inset outlined panel.
Light/dark comparison included. Browser loaded all741 releases and working
picker controls; build/diff checks pass. Main styles unchanged; choice pending.

## 2026-11-14 — Filter band A and header pin implemented

Applied soft raised band/bottom border; inputs retain collection background.
Added accessible pressed-state pin button before theme, sticky below dynamically
measured header, hidden in details. Browser verified toggled static/sticky state
and matching54.9px header offset. JS/normalization/build/diff checks pass.
Retrieval unaffected; no commit/push.

Filter band refinement: reduced text-colour mix from4% to2% at user request
for a quieter background; bottom border retained. Local build passes.

## 2026-11-14 — Sticky table column headers

Column labels/sort buttons stay below the header and optional pinned filters.
ResizeObserver measures filter/header height, including multi-select chip wraps.
Removed nested horizontal scroll container so document-sticky headers can work;
table uses available width with existing mobile column rules. Build and Node
normalization checks pass.

2026-11-14: User-requested push of9877231to origin/main succeeded. Pages
deployment not verified; active retrieval untouched.

## 2026-11-14 — Align filters when chips are selected

Grid items now align at the top; Clear uses the same label-height offset as
Search/dropdown controls. Selected chips grow underneath without shifting
adjacent controls down. Local build and whitespace checks pass.

## 2026-11-14 — Compact caption cards

Combined composer/year on one metadata line; tightened caption gaps and title/
status line heights. Shelf/table unchanged. JS syntax, normalization and build
checks pass. Not committed or pushed.

## 2026-11-14 — Clear/Pin icon prototypes

Three interactive layouts after Search: outlined reset/pin, unboxed eraser/pin,
grouped reset/pin. Every icon has title, accessible name and hover/focus tooltip;
pin tooltip updates with state. Browser loaded options; build/diff checks pass.
Main UI unchanged pending selection.

User selected outlined action treatment A; added interactive four-by-four icon
choice preview with tooltips, selected pair and numbered choices. Browser loaded
all choices; build passes. Main placement/icon change awaits selection.

## 2026-11-14 — Selected filter action icons implemented

Outlined Clear3/filter-cross and Pin1/upright now follow Search. Header keeps
theme only. Existing Clear disable/reset and pin/sticky behavior retained. Added
dynamic theme title; action buttons and view icons have tooltips. Build, syntax
and normalization checks pass. Not committed/pushed.

Tooltip correction: native titles were insufficient for the requested visible
treatment. Added shared positioned hover/focus tooltip for Clear, Pin, Theme and
view icons; disabled Clear is included via pointer events. Escape/scroll dismiss,
viewport bounds and dynamic action text handled. Syntax/build checks pass.

Tooltip/pin refinement:250ms cancellable hover/focus delay,10px tooltip font,
theme surface background (dark in dark mode). Selected pin uses the same neutral
text/surface/border tokens as selected view icons. JS/build/diff checks pass.

## 2026-11-14 — Remaining retrieval complete and exported

Finished16:02Amsterdam.83metadata albums/1,313tracks validated against every
manifest ID, declared count and unique track IDs.603query tasks validated:
520nonempty/83empty;299of305releases have at least one hit,6empty. Search
503fresh HTTP attempts/100cache reuse, metadata85HTTP attempts incl overhead.
Offline exports complete; shared request archive2,488responses, all1,857prior
members byte-preserved. Canonical URL index1,148routes;5URL tests pass.
Hourly monitor deleted after completion. No accepted-match changes, extra calls,
new-hit metadata expansion or push. Next: offline ranking and conservative audit.

## 2026-11-14 — Remaining evidence screened and first audit recorded

Offline screen validates fixed exports and aggregates complete portable metadata:
2,227pairs,8programme/credit-complete leads across7releases,335cached unresolved,
1,884metadata-needed pairs. Audited8leads plus4near-misses with target/album
hashes; no recording-family confirmation invented and no promotion. Identified
shared movement-inventory gaps as a reusable follow-up. Two regressions pass:
reject incomplete/duplicate metadata; network-forbidden replay preserves public
match bytes. No Qobuz calls. Follow-up plan records4491358 as next bounded case.

## 2026-11-14 — Michelangeli Op.73 published Probable; shared inventories expanded

Publisher DG supports the same artists/live televised Vienna family as cached
LP4491358 notes. Three movements/current credits pass a hash-bound existing
review kind; Probable85 with exact take/date/mastering limits, not Found. Added
independently sourced Beethoven Op.31/3,49/1,49/2,53,78,81a movement inventories
from DCML overview. Replay changes only4491358; all previous statuses retained.
Qobuz12Found/99Probable/630Unchecked copies.113script tests, UI normalization,
build and browser detail inspection pass. Test429/STOP messages are mocked
fixtures, not new provider warnings. No Qobuz calls or push.

## 2026-11-14 — Three Klemperer recording-family reviews published

Warner describes the exact2025collection as the stereo cycle; Warner Japan
documents1957Symphonies1/8,1959stereo Fifth versus1955mono Fifth, and1957Coriolan.
12004072/24965038 and26149832 now Probable85, with complete movement/credit
checks and exact hash-bound overture section.24964822 and26149643 withheld:
multiple versions remain plausible from target evidence.3285095 remains pending
stronger recording provenance. Qobuz12Found/102Probable/627Unchecked copies;
other status changes limited to the prior Michelangeli lead. Four review tests
pass, UI/build and browser details pass. No Qobuz calls or push.

## 2026-11-14 — Three additional DG family leads and inventory replay

3285095 Michelangeli Op.7,3672809 Michelangeli Op.15 and7914875 Gilels
Op.79/81a/90 promoted Probable85 with hash-bound sources and explicit limits.
Independent QSO/Henle inventories for Op.15/79/90 unblock two reusable checks.
DG shop swaps25/26 movement headings; did not import that error.117script tests
pass sequentially (initial overlap with generation correctly tripped preservation
check); UI/build/browser detail pass. Counts12Found/105Probable/624Unchecked
copies. No Qobuz calls. Next discovered reusable gap: comma before roman movement
label in Toscanini10757120 titles; current checker sees None for all five.

## 2026-11-14 — Reusable catalogue-comma movement parsing

Accept roman movement after comma only with a preceding explicit catalogue.
Reject bare comma numerals, joins, suffixes and multiple markers. Toscanini
10757120 now has five complete credited movements; recording provenance still
unresolved, no promotion. Replay changes no accepted statuses.119script tests,
UI normalization/build and diff checks pass. Saved source-bound cautions for
four HMV/EMI Barenboim targets against DG cycle; no broad label alias. All API
429/STOP output in test log is mocked; no new Qobuz calls.

## 2026-11-14 — François concerto validated; next metadata scope proposed

8264568 Chopin Op.11 now Probable85: all three movements and François/Frémaux/
Monte-Carlo credits, with Warner1965 sessions distinguished from1954Tzipine.
Added independently sourced Op.11 inventory; only this status changes.120script
tests, UI normalization/build/browser details pass. Toscanini provenance still
insufficient; split Schnabel headings and Ninth-finale groups need new bounded
review treatment. Proposed9distinct metadata albums for11release leads; checked
portable and raw request caches, none already complete. No Qobuz calls, fetching,
push or deployment. Counts12Found/106Probable/623Unchecked copies.

## 2026-11-14 — Nine-album metadata follow-up authorized

User authorized prepared9album/11release scope and subsequent offline audit.
Resumable fixed worker reuses slow pacing/pagination/STOP safeguards; no searches
or audio. Docs updated before retrieval. No automatic retry after warnings.

## 2026-11-14 — Nine-album fetch/audit complete; two Probables

9albums/216tracks completed18:36Amsterdam without warnings,11HTTP attempts
including discovery. Exported shared archive2,497responses (all2,488prior bytes
preserved) and1,157URLs. Audited11leads: Lipatti14waltzes and Kreisler Brahms
concerto Probable85;9withheld with explicit blockers.125script tests, UI/build/
browser checks pass. Brahms inventory adds one structurally supported historical
baseline case, retaining original labels. Global unmatched inventory updated to
all retrieval evidence:620unique unchecked, only6with no saved hits. No push.


### 2026-11-14 — Nielsen positional audit

Offline audit binds target11412875 Aa/Ab/Ba/Bb to four distinct saved Op.29
movements, retaining Barbirolli/Hallé track credits. Repeated Allegro labels expose
title-keyed review limitations. Added reproducible diagnostic/report and3passing
regressions covering wrong opus/artist, reorder, missing/duplicate tracks and
source positions. Publication unchanged; no API requests. Scoped a position-keyed
review in the follow-up plan; new review kind not implemented automatically.


### 2026-11-14 — Nielsen position-bound publication

User-authorized implementation retains separate Aa/Bb Allegro identities, full
ordered track hashes, target/album/raw-source hashes and required artists. Warner
supports work/artists; exact sessions/mastering remain unverified. Only11412875
becomes Probable85. Qobuz copies12Found/109Probable/620Unchecked.129script tests,
UI normalization and static build pass; dependency-complete uv run resolves the
initial requests import failures. No Qobuz API calls or push/deployment.


### 2026-11-14 — Gould nested programme publication

All15raw-source bands bind to30distinct Sony tracks with explicit paired BWVs,
matching keys/order and Gould/Bach credits. Official artist discography confirms
full sequence. New frozen nested-pair review preserves nested source programme;
wrong BWV/pianist, incomplete/swapped tracks and source changes reject. Only1458083
becomes Probable85; exact takes/mastering unverified. UI normalization/build pass.
No Qobuz API calls or push. User's autonomous continuation preference recorded.


### 2026-11-14 — Three Katchen programmes reviewed

6264736 (Op.5 plus Scherzo),7291398 (Op.1/2) and6347314 (Op.39/79/10) become
Probable85. Existing bound-track review now checks optional exact work-field
bindings and numbered movement runs. Narrow exceptions preserve explicit named
Rhapsody numbers and only Op.10Ballades1–4. Complete source programmes, Katchen
credits, exact album/raw-source hashes and excluded compilation extras retained.
Decca Eloquence supports stereo recording family; Henle corroborates16waltzes and
four Ballades. Exact takes/mastering unverified. UI normalization/build pass.
Diagnostic/test evidence committed alongside publication; no global work-field
matching change or Qobuz calls. Copies12Found/113Probable/616Unchecked.
Mozart5254294 inspected: digital ensemble/conductor credits do not evidence all
named source wind players; catalogue KA.226 also unresolved. No credit weakening.

Validation checkpoint:138script tests passed; no new provider warnings (429/STOP
messages in suite output are mocked fixtures). Only the3Katchen status changes
follow the prior Gould commit.


### 2026-11-14 — Nabucco cached follow-up checkpoint

Continued after Katchen: source3167056has11audio bands plus4part headings,
matching candidate track count. Report binds source/target/album hashes and records
all11track-level conductor/orchestra/chorus credit gaps. Scene roles need scoped
requirements; neither equal counts nor album artists replace evidence. Kept
unchecked, no provider calls. Next primary publisher cast/recording evidence.


### 2026-11-14 — Nabucco publisher evidence and Klemperer finale review

DG confirms Nabucco recording family/cast/ensembles, but later complete-opera
reissue evidence does not fill saved highlights track credits. Report updated;
kept3167056unchecked and continued to cached Klemperer leads.

6113868/6119375 become Probable85 via frozen source-split-finale review:8Ninth
tracks account for four movements including all5finale sections, plus two named
overtures. All source voices/chorus positively present within sung finale;
conductor/orchestra/Beethoven required on every selected track. No credit borrowing.
Warner cycle/chorus archive support recording family; no exact session claim.
Leonore suffix conventions, Hotter Contralto label and French printed overture
duration mismatch remain explicit. Only these2labels changed; UI normalization
and static build pass. Copies12Found/115Probable/614Unchecked. No Qobuz calls,
push/deployment. Next source-bound Schnabel side partition/key audit.

Validation:142script tests pass after the older Klemperer missing-track test was
updated to expect the new frozen adapter’s explicit ValueError rejection.


### 2026-11-14 — Schnabel side partition and next source checks

4352998 becomes Probable85 using existing bound-track review:26distinct tracks
cover ten sonatas, Op.54 Beginning/Conclusion partitioned into I/II across C3/D1.
No source title overwrite: Op.49No.1 G Major discrepancy explicitly contrasted
with Henle G minor. Warner identifies saved digital barcode/2016shellac remaster.
145script tests, UI normalization and build pass; only4352998status changed.
Copies12Found/116Probable/613Unchecked. No API calls or push/deployment.

Continued inspection:6265501has13listed pieces (Op.117/119/118) with cached
correspondences.8836514source Op.116has only6children and an E-key conflict;
1697514saved Paganini version1965 versus publisher1966 requires reconciliation.
Do not silently invent missing source tracks or conflate alternate recordings.


### 2026-11-14 — Further Katchen source discrepancies preserved

Hash-bound offline source audit saved for6265501/8836514/1697514.6265501Op.119
third piece is G in source versus C in candidate; no promotion from counts alone.
8836514B4may join two Intermezzi, so earlier six-child observation is not evidence
of a missing work.1697514Paganini1965saved label versus1966publisher narrative
unresolved; multiple recordings noted. No labels/source text changed or API calls.
Next independent publisher/score verification of6265501key discrepancy.


### 2026-11-14 — Three further Katchen source reviews

6265501/8836514/1697514 become Probable85. Publisher evidence resolves Op.119No.3
C major versus source G (disclosed). Original label photo confirms joined B4;
Bärenreiter sequence corroborates all7Op.116pieces across6bands. CHARM Decca
entries1199/1379visually checked: HandelJune1962and PaganiniSeptember1965,
Vol.7issueApril1966. Session and issue dates separated; no date overwrite.

Saved label/selected discography page images with provenance/hash checks. Binding
review validates complete source-band mapping and optional exact version/ISRC
markers; regressions reject dropped photo/piece, changed version/ISRC or pianist.
Only3statuses changed; UI normalization/build pass. Exact LP transfers/takes remain
unverified. Copies12Found/119Probable/610Unchecked. No Qobuz calls or push.
Next cached RCA/Toscanini recording-family audit.

Validation:149script tests pass; UI normalization/build and all saved external
evidence SHA checks pass. Mock429/STOP fixtures are not provider warnings.


### 2026-11-14 — Toscanini RCA recording-family evidence

10757120becomes Probable85. Inspected/saved original RCA sleeve gives Carnegie
Hall14January1952; Pristine documents official RCA reissue date and five movement
timings. Cached differences9/4/1/2/13seconds allwithin3%; no audio identity claim.
Binding requires all5movements, Toscanini/NBC, source/photo hashes, year marker,
exact ISRCs and duration guard. Numbered-run checks reuse existing strict movement
parser including catalogue-qualified comma Romans. Third-party Arturo transfer
and source Stereo-tag treatment remain unverified. Only1status changes; UI/build
checks pass. Copies12Found/120Probable/609Unchecked; no Qobuz calls or push.
Next two Klemperer source-version holds; artist/work similarity alone insufficient.

Validation:151script tests pass; changed-year/timing/orchestra/photo regressions
and UI normalization/build pass. Mock warnings are fixtures, not live errors.


### 2026-11-15 — Two Klemperer stereo-label reviews

24964822/26149643 become Probable85 after inspecting/saving source labels:
explicitSTEREO and1959/1961label years. Warner confirms stereo cycle and Seventh
1960studio dates. Complete symphony/overture programmes and Klemperer/Philharmonia
credits retained; exact takes/mastering unverified. Second finale6:57vs7:11
14second discrepancy remains explicit; timing is not sole identity evidence.
153script tests/UI normalization/build pass; exactly2statuses changed. Copies
12Found/122Probable/607Unchecked. No Qobuz calls, push/deployment.

Continued cached audit found Gilels15221307false full-coverage lead: source B1
attributes MedtnerOp.22, normalized row has empty composer list, candidate is a
Beethoven-only sonata box. Completeness already prevented promotion. Next add a
source-bound per-work composer safeguard and audit impact without legacy relabels.


### 2026-11-15 — Reviewed per-work source composer safeguard

Gilels15221307raw per-track attributions supply Beethoven/Medtner identities lost
from empty normalized composer field. Manual hash-bound scope now prevents
BeethovenOp.22from covering MedtnerOp.22. Grouped lead support5/5→4/5; Medtner
support removed. Legacy scorer and normalized collection unchanged, every published
release record unchanged (matcher version/provenance only). Source/target hashes,
all positions/titles and artist IDs/names validated; no global role inference.

Offline audit flags2source-attribution gaps: reviewed Gilels and unreviewed
Rubinstein7971104. Boosey independently corroborates Medtner work.156script tests,
UI normalization/build pass; screen/inventory refreshed (418work/credit,170metadata,
7withheld,6no-hits,5completeness;606unique). No provider calls, push/deployment.
Next explicit Rubinstein source review, preserving missing works and uncertain leads.

Final validation:156script tests pass with explicit out-of-scope rejection;
publication release records remain byte-equivalent as JSON values, and refreshed
screen provenance hashes match current inputs. Mock warnings are fixtures only.


### 2026-11-15 — Rubinstein source gap and bounded retrieval proposal

Original RCA LM20086 label and cover show 14 works for Rubinstein7971104;
cached Discogs tracklist has13, omitting Albéniz’s Sevillana. Saved both inspected
photos and a separate reconciliation proposal. Added hash-bound source-programme
hold with stale-evidence regressions; all nine candidate pairs remain Unchecked.
No normalized/raw source overwrite or composer-scope activation. Qobuz counts
unchanged:12Found/122Probable/607Unchecked copies. Screen/inventory refreshed.

Prepared immutable seven-album metadata scope for8release leads (97reported
tracks) and resumable fail-closed worker; no network by default. Two offline worker
tests pass. Approval requested before new provider retrieval; no fetch started.
No push/deployment. All160script tests pass; warning/STOP messages in the suite are fixtures.


### 2026-11-15 — Approved seven-album metadata batch complete

Fetched7albums/97tracks09:40–09:42Amsterdam with9HTTP attempts, slow spacing,
no warnings. Verified all IDs/full counts/unique tracks; exported portable data,
2504response archive with2497prior members byte-preserved,1164canonical URLs.
Worker and sleep assertion ended normally.160script tests pass.
Offline screen/inventory updated; Weissenberg1662708 now ready for recording
review, other selected relationships retain explicit gaps.606unchecked unique:
425work/credit,160metadata,1recording review,7withheld,6completeness,6empty,
1source hold. Match labels unchanged; no push/deployment or new scope expansion.


### 2026-11-15 — Weissenberg reviewed, seven-album gaps inventoried

Source1662708 and full digital Op.23programme share Weissenberg/Karajan/Paris
credits on all three movements. Warner corroborates Paris recording family;
2026remaster differs from saved2010edition, source dates/timings unknown. Explicit
hash-bound review publishes Probable85only; exact take/mastering caveats retained.
Only1662708release record changed:12Found/123Probable/606Unchecked copies.
162script tests pass including missing movement/wrong orchestra controls; UI
normalization and static build pass. Eight-relationship offline audit records
remaining programme/source/credit blockers. Next composer identity review for
Mendelssohn-Bartholdy/Mendelssohn; no provider calls or push/deployment.


### 2026-11-15 — Reusable Felix composer identity, no label changes

Authority-supported exact full-name Felix Mendelssohn/Mendelssohn-Bartholdy rule
requires positive Composer-role credit in grouped matching. Legacy scorer and
performer keys unchanged; Fanny/Moses/initial/surname-only names not aliased.
Eight cached screen pairs change; six gain support, two lack performer coverage.
No published status changes; four release evidence records updated. Two prior
hash-bound reviews retain identical programmes after removing9redundant manual
adds newly matched naturally. Initial duplicate-binding regression caught this;
validator kept strict and full164test rerun passes. UI normalization/build pass.
Docs and structured impact audit saved; no provider calls or push/deployment.
Next Bernstein3956949 completeness/recording-family review.


### 2026-11-15 — Bernstein Probable; Gieseking programme separated from identity

Official Bernstein discography corroborates exact DG2531097LP and both1978live
Israel Philharmonic symphonies. Source eight movement labels/timings support full
programme. Bound-track review requires source/target/album hashes, all8IDs, ordered
movements,Live/ISRC markers, conductor/orchestra and close timings; no key alias.
Only3956949published record changes to Probable85; exact pressing/takes/mastering
unverified. Counts12Found/124Probable/605Unchecked copies.166script tests plusUI
normalization/build pass. No provider calls/push/deployment.

Gieseking8962178all17pieces supported; heading is not additional work. Kept
Unchecked because third-party BNF transfer lacks session/take markers while Warner
acknowledges alternative Spinning Song recordings. Structured audits saved for
both. Next Yepes source/catalogue/suite completeness review, cached evidence only.


### 2026-11-15 — Yepes equal-count false lead withheld

Source2857544baroque-lute programme includes final BWV1006aGigue. Digital
0002894457132omits it, but splits Menuets into two tracks: both albums total27.
Several candidate titles say guitar arrangements, so instrument/session remains
unresolved. Added source/target/album-bound existing-kind withhold, no generic
catalogue normalization or source overwrite. Shadow spelling-fix regression shows
100%work coverage still fails ordered six-movement completeness (1,2,3,4,4,5).
168script tests pass; no provider calls, new retrieval scope, push/deployment.
Every published release record remains unchanged (provenance only); UI normalization
and static build pass. Inventory now422work/credit,160metadata,8withheld,7completeness,
6empty,1source hold. Next cached Ciccolini2236260work/source-key/recording review.


### 2026-11-15 — Ciccolini mixed-composer programme reviewed

Source2236260explicit composer sides and three movement labels map the six
cached concerto tracks. Warner CD4discography corroborates Silvestri/French
National Orchestra1957family; all six reference timings equal candidate. Saved
visually inspected pages2–3with source hashes. Publisher key-label discrepancy
retained. Hash-bound existing-kind review requires complete runs, named credits,
exactISRCs/timings and positive per-track Composer-role marks. No global key/title
aliases or source rewrite. Probable85only; third-party transfer, exact takes and
mono/stereo unverified. Only2236260release record changes:12Found/125Probable/
604Unchecked copies. All170script tests and UI normalization/static build pass.

Shared binding test fixture updated to include seven-album archive (otherwise
prior Yepes hold was missing its album). An overlapping publication writer caused
one preservation-check failure; final suite rerun sequentially after regeneration.
No provider requests, push/deployment. Next Casals original-source conflict review.


### 2026-11-15 — Casals label resolves catalogue typo; reusable credit-role fix

COLH17original labels inspected in browser:Suite3BWV1009andSuite4BWV1010with
1936/1939month/year labels. Saved screenshot evidence/hash provenance and separate
correction proposal; cached Discogs1008source and normalized collection unchanged.
Casals blocked also by liner author Guglielmo Barblan incorrectly required as a
performer because note title says Violoncello. Fixed annotation role parsing for
future normalizations, retaining genuine vocal annotations. Diagnostic old/new
builder audit740details:9nonperforming-credit removals,1violinist/conductor order
change. No provider/result refresh. Source-corrected shadow has full work support
but Nar Classical candidate has no recording-session/take markers; no promotion.
All173script tests and UI normalization pass. No Qobuz requests, push/deployment.


### 2026-11-15 — Casals source reconciliation diagnostic, no promotions

Added copy-only source reconciliation validating target/raw/label evidence hashes,
exact source title correction and exclusively nonperforming liner credit. Principal/
work performers cannot be removed. Both Casals LP source programmes mapped offline:
Suites3–6,24distinct movements; source23950082flat suite headers/side positions
bounded with complete numbered runs, positive Bach/Casals credits and named members.
No source/catalogue alias, raw rewrite, provider calls or publication integration.
Nar Classical recording/take provenance unresolved, so labels unchanged.
Four regressions cover stale/missing proofs, invalid credit exclusion, crossed or
missing/reordered suite bands and network/publication protection. All177script tests
and UI normalization pass. Seven-album/eight-release review complete:3Probable,1withheld,4unresolved.
Next cached Solti5972183/3386012source-role cases; no bulk refresh/push/deployment.


### 2026-11-15 — Source-bound Solti credits and complete Sixth reviewed

5972183Decca SET469/470family corroborated by BnF and Decca Eloquence. Eight
source movements/songs complete, positive Solti/Chicago/Minton/Mahler credits.
Existing bound-track review now supports exact source-role reconciliation:
exclusively nonperforming liner author removed, singer scoped from explicit
source work role, full expected requirement map frozen. Conductor/orchestra and
other source soloists cannot be omitted. Exact source/target/album hashes plus
numbered complete runs/title/ISRC guards. Only5972183published record becomes
Probable85; exact pressing/takes/mastering unverified. Counts12Found/126Probable/
603Unchecked copies.3386012Fifth withheld: Clevenger/Herseth absent from digital
credits; no inference from orchestra. All182script tests and UI/build pass.
No source/Spotify refresh, provider calls, push/deployment. Next14766559technician.


### 2026-11-15 — Say four-sonata LP reviewed; photographer cohort triaged

14766559technician credit reconciled using existing source-bound rules, without
new engine policy. Exact12movement IDs/work fields/ISRCs, positiveSay/Beethoven,
three-movement runs and source timing within1second support four-sonata programme.
101other complete-set tracks excluded. Warner confirms vinyl selection/cycle;
exact pressing/takes/mastering unverified. Only14766559publication becomes
Probable85:12Found/127Probable/602Unchecked copies.185script tests/UI/build pass.

Reproducible five-photographer shadow triage: all retain zero coverage after false
names removed; additional work/context/credit gaps recorded with source hashes.
Three have false normalized key-performer names, which active guard still rejects.
Nine-case nonperforming-credit first triage:2Probable,1withheld,6unresolved. No
source bulk refresh/provider calls/push/deployment. Next Kubelik14398300explicit
work-field context audit, preserving source soloist requirements.


### 2026-11-15 — Ten cached leads closed; recording reviews override scoring

Five photographer leads explicitly withheld: Kubelik pair lacks conductor/orchestra
track credits across42tracks; Ozawa compilation wrong orchestra/incomplete source
programme; Soltani/Rolla lack source-named players. Five Barenboim EMI/HMVLP leads
blocked against DG1981–84cycle:2dated1970chronological rejections,3undated holds.
No label-only assertion of different audio. Structured evidence audits saved.

Saved explicit review now caps its exact candidate Unchecked regardless of future
scorer improvement, with visible reasons. Positive review replaces candidate once;
unrelated candidates remain independent. Source hashes validated.189script tests,
UI normalization/build pass.12evidence records changed, no accepted statuses.
Inventory601unchecked unique:412work/credit,160metadata,17withheld,3recording
rejections,2completeness,6empty,1source hold. No provider calls/push/deployment.
Continued to Karajan7064777split Lobgesang completeness/family review.

### 2026-11-15 — Karajan complete programme accepted; Casals transfer held

Karajan7064777/0002894777581 now Probable85:28distinct tracks cover all five
Mendelssohn symphonies with positive Karajan/Berlin credits. Hash-bound section
proof checks the three separately indexed Lobgesang Sinfonia bands. Karajan
Institute corroborates the studio recording family; exact pressing/takes/mastering
remain unverified. Source Symphony5key discrepancy preserved. Casals5838140
remains Unchecked: complete programme does not establish Nar transfer identity.

192script tests, UI normalization and build pass. Only Karajan accepted status
changed. Qobuz12Found/128Probable/601Unchecked copies;600unchecked unique:
412work/credit,160metadata,18withheld,3recording rejections,6empty,1source hold.
No provider calls, push or deployment. Continue cached partial-programme audits.

### 2026-11-15 — Three partial-programme leads audited offline

Saved hash-bound `data/qobuz_partial_programme_audit.json`. Landowska9792325
/e1lsj7ytcfa8b lacks source K333; Lipatti11938919/5099996593059 lacks Op58.
No claim of service-wide absence and no publication change. Schnabel4694861
/0190295866983 contains35distinct pianist-credited movements for all ten source
sonata headings. Current scorer emits24units including isolated tempo labels,
which can collide across works. Saved all source positions/children and exact
track fingerprints as a diagnostic only. Existing grouping rejects duplicate
source titles; do not bypass that guard or discard repeated Allegretto labels.
Next: source-position-safe review using existing kinds if possible; a new review
kind needs concrete scope. Audit assertions verify35unique tracks and all named
pianist credits. No code/publication change, provider calls or push.

### 2026-11-15 — Push and Gilels joined-finale review

Pushed main7945944..cf7f263 as requested; deployment not checked. Continued
offline. Gilels13655367/0002894776360now Probable85 using existing target-unit
grouping: source A3b Attacca Prestissimo belongs to the Waldstein finale, whose
exact digital title explicitly contains Prestissimo. Seven distinct movements
cover Op53/101; source and exact reissue catalogue identify January1972Berlin.
Retained timing and transfer/mastering caveats. Regressions reject rehashed
missing coda/movement and wrong pianist.194script tests, UI normalization/build
pass. Only13655367accepted status changes. Counts12Found/129Probable/600Unchecked
copies. Next cached Campanella numbered-piece binding; no Qobuz calls.

### 2026-11-15 — Campanella numbered cycle accepted; two incomplete/identity holds

Campanella10100439/0002894383712now Probable85:19unique numbered rhapsodies,
nine explicit whole-title/work bindings, positive Liszt Composer and Campanella
credits and exact ISRC marks. Publisher confirms exact catalogue/performer/cycle.
Source No12major versus digital minor retained, no global key correction.
Böhm9932700held: source adds three Rosamunde selections absent from30track
symphony-only candidate. Undated Barenboim9861630held: no EMI-to-later-DGcycle
recording link, not a label-only rejection.196script tests, UI normalization/build
pass; only10100439accepted status changes. Counts12Found/130Probable/599Unchecked
copies. No Qobuz calls or further push. Continue source-heading Schnabel review.

### 2026-11-15 — Source heading/band review accepts Schnabel volume

Schnabel4694861/0190295866983now Probable85: ten source headings/35distinct
movements with required pianist. New bounded source-heading-movements adapter
validates all raw/normalized bands and unique positions, preserves repeated tempo
labels, then reuses whole-work credit/movement checks and freezes per-work IDs
and per-track hashes. No source/parser change or extra take/mastering assertion.
Warner exact barcode supports1932–1938recording family; source title1932–37scope
retained. Joined/split bands intentionally unsupported by this adapter.
199script tests, UI normalization/build pass; only4694861accepted status changes.
Qobuz12Found/131Probable/598Unchecked copies. No Qobuz calls or further push.
Scan of flat headed sources found no further immediate eligible promotion: prior
Barenboim rejection, Gieseking transfer hold, Furtwängler provenance/section-title
questions, and Prêtre joined-band/instrumentation questions. Continue offline.

### 2026-11-15 — Following headed sources diagnosed, evidence limits preserved

Saved hash-bound qobuz_headed_source_followup_audit.json for two further cases.
Furtwängler3737065BNFcandidate has five tracks and positive named performers,
but source Entr’acteII/Dmajor versus digital No5EntracteIII needs exact section
resolution; transfer provenance also unresolved. Prêtre13671866source explicitly
scopes both pianists to sideA; nine/four LPbands combine14/6digital sections.
Some Carnaval sections lack otherwise-global performer credits, potentially an
instrumentation issue requiring score proof. No principal removal, inferred
instrumentation exemption, new review rule or publication change. Warner supports
general coupling/performers, not this exact candidate’s section participation.
Audit assertions verified5/20cached tracks and exact disputed digital label; source/
album/track hashes saved. Next source-position/score-supported Prêtre diagnostic.
No Qobuz calls or further push; last full199tests/UI/build validation unchanged.

### 2026-11-15 — Prêtre original-image credits prevent false promotion

Mapped13CVL1920bands to20distinct cached digital sections, preserving all titles
and source timings. SideBaggregate21:20matches exactly while B3/B4differ90/96sec;
aggregate timing is not recording proof. Original liner names M.Cazauran double
bass; sideAlabel additionally names M.Debost flute, both absent from all candidate
track credits and omitted by cached Discogs extraartists. Images and precise
source URLs saved under review_sources/pretre-13671866. No initials expanded,
ensemble-membership credit inferred, source overwritten or instrumentation waiver.
Explicit recording hold keeps13671866Unchecked. Shared review entry point now
validates external source-file paths/hashes for every review kind, including
default holds, before returning. Offline diagnostic and regressions cover complete
band accounting, reused/missing sections, equal-total trap and broken image proof.
202script tests, UI normalization/build pass. No accepted status changes; counts
12Found/131Probable/598Unchecked copies. Inventory597uncheckedunique:406work/credit,
160metadata,21withheld,3rejections,6empty,1source hold. Five public LP images
inspected; no Qobuz requests or push. Next cached Böhm6810640Vienna5/8review.

### 2026-11-15 — Böhm Vienna Schubert5/8 accepted with live provenance

6810640/0002894318282now Probable85. Two bare-title Unfinished tracks bound to
exact D759work fields and1977Hohenemslive versions; four Fifth movements supported.
Original LP liner explicitly identifies liveSchubertiadeHohenems1977; sideBlabel
uses2531279matrix/1980phonogram. Source producer/engineer assignments align with
digital per-work credits. Universal primary sources corroborate HohenemsJune1977
and ViennaFifthDecember1979recording families. Source1982/phonogram dates kept
separate; no date inferred from ISRC. All six require Schubert Composer/Böhm/Vienna,
exact ISRC/version/title marks and source-timing tolerance; eight unrelated tracks
excluded. Timing/take/mastering caveats retained. Image proof saved/hash-validated.
204script tests, UI normalization/build pass. Only6810640accepted status changes;
12Found/132Probable/597Unchecked copies. No Qobuz request/push. Next Reiner2463301.

### 2026-11-15 — Six candidate holds and associated-role census

Reiner2463301complete5+8work bindings retained as unpublished diagnostic. Chinese
March279922682names Chicago solely as AssociatedPerformer; no cross-track credit
borrowing or role-policy change. Explicit hold preserves uncertainty. Source LMmono
versus LivingStereo family caveat retained. Five more exact-candidate holds:
Landowska9792325missingK333; Lipatti11938919missingOp58; Mozart2666680missingK595;
Rubinstein2700887SaintSaensOrmandy/Philadelphia versus sourceWallenstein/Symphony
OfTheAir; Mozart5065978K550Bernstein/Vienna versus sourceBöhm/Berlin. Partial
correct couplings do not supply missing/conflicting recordings.

Offline role census across1164albums:775associated-only declarations(540spaced/
235compact);540accepted solely through that declaration, five additionally named
through other accepted roles.288reference required saved-candidate names, not
necessarily accepted/selected tracks. Current parser treats spellings inconsistently;
DDEXdefinition does not settle Qobuz’s recording-field semantics. Proposal recorded,
no acceptance change.206script tests, UI normalization/build pass. No accepted
status changes;12Found/132Probable/597Unchecked copies. Inventory596uncheckedunique:
399work/credit,160metadata,27withheld,3rejections,6empty,1source hold. No Qobuz
requests or push. Continue independent cached Brendel5403356programme/family review.

### 2026-11-15 — Brendel complete analogue cycle reviewed Probable

5403356/0002894782607now Probable85: all32sonatas plus Andantefavori,103distinct
Brendel-credited movements;18concerto/ChoralFantasytracks excluded. Exact original
boxback and sideRlabel establish Sonata9EmajorOp14No1versus cached source14,2.
Bounded work-title corrections preserve all raw/normalized text, source order and
work identities. Decca official release description corroborates1970–77analogue
family; exact takes/LPtransfer/mastering remain unverified. Five original images
saved/hash-bound; no blanket opus/key/title alias.

Large apparent timing mismatches were shared source spans attached to individual
fields. Explicit86diagnostic groups account for103positions exactly once; Op101
values on Q1/Q3cover pairs, while other timings may appear at span ends. Only
marked image-verified groups have inspected label proof; other group interpretations
remain inference. Differences up to15sec retained, including9secOp79I. No timing
calibration/identity claim or generic source normalization. Offline audit command
and regressions cover full programme, missing Andante, wrong sonata/pianist/composer,
immutable source and complete timing scopes.209script tests, UI normalization/build
pass. Only5403356accepted status changes.12Found/133Probable/596Unchecked copies;
595uncheckedunique(398work/credit,160metadata,27withheld,3rejections,6empty,1source
hold). No Qobuz calls/push. Next original FALP317section identity diagnostic.

### 2026-11-15 — Furtwängler physical sleeve confirms unresolved section label

Original FALP317sleeve explicitly prints Entr’acteNo2, so3737065source wording is
not merely a cached transcription error. Candidate16234555says No5EntracteIII.
Original sleeve/sideBimages saved/hash-bound; precise source B2and digital track
retained in qobuz_furtwangler_section_audit.json. No claim of proven different
audio or silent source correction. Section identity and BNFtransfer provenance
remain unresolved under an explicit hold. New hold assessed, checked against a
syntheticFound99override;7targeted review/source-proof tests plus regenerated
inventory, UI normalization/build pass. Last full209suite remains the preceding
Brendel checkpoint; no code changes since it. No accepted labels change.
Counts12Found/133Probable/596Unchecked copies;595uncheckedunique:397work/credit,
160metadata,28withheld,3rejections,6empty,1source hold. No Qobuz requests or push.
Next cached du Pré1656511Favourite Cello Concertos programme/Haydn identity review.

### 2026-11-15 — Counted bounded cached-review queue before continuation

At user request to assess counting first, verified saved inventory input hashes
and triaged397unique work/credit cases.14priority reviews(>=50%current source-unit
support in an unheld cached candidate),26secondary partial leads,354no current
supported units,3documented constraints(Giesekingtransfer, Gilelscomposer collision,
BitchesBrewcredit proposal). Threshold is workflow triage, not confidence or a
prediction of promotion; source units can include misleading headings/parts.
Saved all397IDs, classifications, best candidate IDs, rules and inventory hash in
qobuz_cached_review_queue.json.160metadata-needed and38other held/rejected/empty/
source cases remain outside this screen. Count assertions/input hashes verified;
no matcher, publication or provider calls changed. Plan now bounds the next pass
to14priority cases, du Pré1656511first, before reassessing26secondary leads.

### 2026-11-15 — Completed fourteen priority reviews in one batch

Reviewed every frozen priority ID without routine confirmation. Two cached
recording-family matches are now Probable85: Stern/Ormandy6686688 (six work-field
bound movements, positive per-work composers and all named performers) and
Klemperer7002243 (four Eroica movements plus Fidelio, local Op72b/title correction
that explicitly excludes LeonoreIII). No exact pressing/take/mastering claim.
Twelve holds distinguish missing works, different cycles, source credit scope,
transfer/arrangement provenance and timing/container uncertainties. In particular,
du Pré lacks Silent Woods; Bernstein's DG cycle differs from the CBS source;
Klemperer12690141has an82-second Prometheus timing gap. Gould has40Partita
movements and7Toccatas mapped diagnostically, with two BWV914versions retained.

Saved complete source programmes, source/target/album hashes, cached alternatives,
manual diagnostic track hashes and per-case next actions in the batch audit;
appended14candidate-specific recording decisions and inspected source images.
Added offline batch validator and reproducible queue triage. Partial alternatives
do not automatically requeue a reviewed blocker. The original-ad PDF and Gould
source-image requests were unavailable (public403); no false visual-proof claim.

Validation:215script tests pass, including wrong soloist/composer, wrong work-field,
missing finale, Fidelio/Leonore collision, future-score hold and complete14scope
regressions. One old shared-album test was corrected to distinguish positive
reviews from explicit holds. Batch hash validator, regenerated publication,
unmatched inventory, role census, UI normalization and static build pass. Frozen
before/after diff confirms only6686688and7002243gain accepted labels; collection
SHA256and all Spotify statuses unchanged. Mock429/STOPtest messages are fixtures,
not live warnings. No Qobuz calls, global credit/threshold changes or push.

Qobuz copies:12Found/135Probable/594Unchecked (593unchecked unique:383work/credit,
160metadata,40withheld,3rejections,6empty,1source hold). The remaining cached queue
has26secondary leads,354zero-current-support cases and3known constraints;
all14priority reviews are complete. Next: reassess26as a separately bounded queue.

### 2026-11-15 — Screened26secondary leads; verified three recording families

Froze all26IDs and saved source programmes, raw/target/complete-album hashes,
candidate diagnostics, per-case findings and next actions. This is a screen for
23cases still pending full recording review; no blanket hold or rejection applied.

Lipatti1704535and François4067901now Probable85with14distinct complete waltzes
each. Frozen French-to-English member corrections prevent Op34/64/69/70subnumber
loss; Lipatti's three bonus tracks stay outside the programme. Warner Japan UPC
matches François's1958Paris mono release, consistent with1959mono source; no
later stereo substitution. Karajan7860979now Probable85with all9Bruckner symphonies,
35explicit-work-field movements, positive Bruckner/Berlin/Karajan credits. Primary
Institute evidence distinguishes the1982compiled Berlin cycle from later Vienna
recordings. Source/publisher date discrepancy retained; no exact take/mastering
verification. Existing review kinds used; no global parser/credit exception.

221script tests pass, including swapped opus member/composer, missing waltz/bonus
substitution, wrong Bruckner orchestra and wrong symphony work field. Regenerated
publication, inventory/queue, role census, UI normalization and static build pass.
Before/after accepted-label diff is exactly1704535/4067901/7860979; collection SHA
and Spotify labels unchanged. Qobuz copies12Found/138Probable/591Unchecked;
590uncheckedunique:380work/credit,160metadata,40withheld,3rejections,6empty,1source.
Queue now23secondary+354zero-support+3constraints. No Qobuz calls or push/deploy.
Next: source recording-family review of François12419718nine-piece recital, not
an automatic extension of the accepted waltz-cycle review.
