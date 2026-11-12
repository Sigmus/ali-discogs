# Ali Discogs

Updated: 2026-11-12, Europe/Amsterdam

Match Ali's Discogs collection (`ajozi`) against Spotify and browse the results
in a static explorer. See [README](../../README.md) for setup and matching rules.

## Current state

- Active branch: `codex/qobuz-poc`. User requested committing the reproducible
  Qobuz PoC, documentation and pending edits. Inspect Git for the resulting commit.
- Dataset generated 2026-11-11: 741 copies; Spotify 255 found, 276 probable,
  210 not found. Qobuz remains 741 unchecked. These are saved results, not a
  fresh production match run. Source: `data/summary.json`.
- Sonoteque-style album table and dedicated details are on main. Retained
  search, composer, genre/style, label, decade, sorting and match candidates.
  Main width is capped at 80%. Status tabs removed; title/cover open details,
  metadata/status are plain text. Qobuz search links live in details.
- Pending Year ascending default (undated last), including Clear reset, is
  included with this branch's changes. It is not yet published.
- GitHub Pages uses Actions, not branch/root. Live site verified 2026-11-12:
  741 rows, no status tabs/status hyperlinks. Deployment `43231078310` succeeded.
  Follow-up documentation was pushed as `0847175`. Inspect Actions for later runs.

## Qobuz enrichment handoff

- [Setup, token, cache, commands and next steps](../qobuz.md) is the current guide.
- Token-based catalogue access works with Sei969/qobuz-dl revision
  `28c3521c3c96e62d7da7166d3edef1aed92a202f` for app-ID discovery only.
  Anonymous search returned 401; authenticated search and album/get returned 200.
- Six deliberate samples (two per Spotify status) returned 19 candidates across
  five initial searches. One release remains unresolved after fallback.
  [Sample evidence](../plans/2026-11-12-qobuz-sample.md) records strong programme
  candidates and wrong-orchestra/compilation pitfalls; not a validated matcher.
- Shared scripts cache successful requests and support offline replay, refresh,
  explicit new sample batches, bounded timeouts and safe error messages.
  Local `.env`, source checkout and `.qobuz-poc/` responses are ignored by Git.
- `.env.example` documents QOBUZ_USER_AUTH_TOKEN. Real credentials stay local.
  Fresh machines need the pinned upstream checkout and their own token.
- No app secrets extracted, audio requested, collection JSON changed or automatic
  Qobuz classifications accepted. The older qobuz 0.0.2 probe remains for comparison.

## Validation and limitations

- Consolidated six-release live fetch and offline replay pass on 2026-11-12.
  Five mocked catalogue cache/error tests, existing offline matcher tests,
  UI normalization/query tests and static build pass. New tests run in make/CI.
- No production Qobuz matcher exists. Catalogue candidate availability is not
  independently verified recording identity or proof of complete coverage.
- Existing Spotify pipeline replaces Qobuz entries with unchecked on rescore.
  Design persistent reviewed overrides before merging enrichment into data.
- Match classifications are algorithmic, not a completed manual audit.
- `make serve` builds/serves localhost:8000. Check server availability on resume.

## Full-collection search in progress

User authorized slow searches for all albums on 2026-11-12. Started detached
`qobuz_all_poc.py` with caffeinate; 740 release queries cover 741 copies, up to
five candidates each, >=15 seconds between requests and 120 seconds rest every
50 uncached searches. Stops on any API/network error. No full candidate-track
fetch or accepted match/data merge in this pass. Check
`.qobuz-poc/all/progress.json`, `run.log` and worker PID for actual current state.
Use docs/qobuz.md to stop/resume. Do not assume the background run completed.
Thread heartbeat `qobuz-search-progress` now checks hourly with time remaining
and estimated finish in Europe/Amsterdam per user request;
the last 20-minute update was delivered at about 16:05 Europe/Amsterdam.
On warnings/errors or unexplained stalls, pause via
STOP and ask the user; never retry/resume without their response.

## Latest local UI change

Added “Most frequent first” switch before Clear, on by default. Orders Spotify
status/composer/label/genre/decade choices by collection count with alphabetical
ties; off restores alphabetical/chronological options. Retains active filters.
Browser verified both orders and selection preservation; normalization tests,
syntax, build and diff checks pass. User requested committing/pushing this
branch with the slow-search runner and docs. Not merged to main or published.

## Next action

First inspect full-search progress and handle any failure; after retrieval,
proposed AD-006: normalize Qobuz track credits/work IDs, score programme coverage
and performer agreement conservatively, and output candidates for manual review.
Coordinate override persistence with AD-004 before any production data merge.
See [backlog](backlog.md), [decisions](decisions.md) and [history](history.md).
