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
