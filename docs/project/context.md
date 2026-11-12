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

## Next action

Proposed AD-006: normalize Qobuz track credits/work IDs, score programme coverage
and performer agreement conservatively, and output candidates for manual review.
Coordinate override persistence with AD-004 before any production data merge.
See [backlog](backlog.md), [decisions](decisions.md) and [history](history.md).
