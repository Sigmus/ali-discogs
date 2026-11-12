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
