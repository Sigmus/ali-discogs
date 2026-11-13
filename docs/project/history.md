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
