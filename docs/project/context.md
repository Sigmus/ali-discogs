# Ali Discogs

Updated: 2026-11-13, Europe/Amsterdam

Match Ali's Discogs collection (`ajozi`) against Spotify and browse a static
explorer. See [README](../../README.md) for setup and architecture.

## Current state

- Branch `codex/qobuz-poc`; user requested committing portable evidence and
  related work for Ali. Inspect Git for resulting commit.
  No merge, push or deployment performed for Qobuz preparation.
- Original dataset (2026-11-11): 741 copies, Spotify 255 found / 276 probable /
  210 not found. Pipeline JSON still has Qobuz unchecked; explorer overlays the
  separate generated `data/qobuz_matches.json` file so Spotify rescoring cannot
  erase Qobuz evidence. `data/summary.json` describes pipeline data, not overlay.
- Sonoteque-style table/details, 80% main width, no status tabs. Branch includes
  Year ascending default and frequency-order switch. These are not yet published.
- Pages uses Actions on main. Last recorded live verification was 2026-11-12;
  inspect Actions/current live page before asserting later deployment status.

## Retrieval complete

- 740 unique release queries cover 741 copies: 370 with candidates, 370 empty,
  1,217 candidate entries / 1,036 unique Qobuz albums. Empty searches unresolved.
- Metadata completed 2026-11-13 01:15:30 Europe/Amsterdam. Independently verified
  all 1,036 album IDs, complete track counts and unique IDs within each album:
  27,770 track entries. No retries after warnings without authorization.
- One large album returned 500/730 tracks; user authorized cached pagination.
  Recovery verified; retrieval finished with no further warnings. Caffeinate
  prevented idle sleep during retrieval; worker has now finished.
- Search and metadata hourly monitors deleted after completion. No background
  fetch remains necessary. Raw caches/source/token remain ignored/local.
- User requested collaborator access: `data/qobuz_evidence.json.gz` now preserves
  all searches/full metadata in a whitelisted ~1.8 MB portable snapshot. Matcher
  uses this by default, with no local cache, token or source checkout needed.
- [Qobuz guide](../qobuz.md) documents setup, preservation and resume commands.

## Offline matching and publication preparation

- Implemented qobuz-programme-v1; all 1,217 candidate entries assessed offline.
  [Audit](../plans/2026-11-13-qobuz-audit.md) records rules, reviewed cases and limits.
- Unique releases: 12 Found / 54 Probable / 674 unchecked. Copies: 12 / 54 / 675.
  No Not found labels derived from first-pass absence. No 100% scores.
- Found 95% requires one-to-one programme/track mapping, equal count and required
  performer/ensemble/conductor plus composer evidence. Probable 85% retains
  grouped/superset cases. Scores are heuristic levels, not calibrated accuracy or
  independently verified recording sessions. Unresolved aliases stay unchecked.
- Audit corrected omitted standalone programme items and confused Part II A/B/C;
  regression tests added. Reviewed all final Found title/credit correspondences,
  15 spread-out Probable mappings and known negative/uncertain controls.
- `data/qobuz_matches.json` contains selected public metadata, explanations,
  programme evidence and provenance fingerprints, no token/headers/audio URLs.
  Build copies it directly; clean-copy build without ignored caches verified.
- UI shows Qobuz status/confidence in table/details, sortable status column,
  linked candidates and expandable programme evidence. Browser verified desktop
  table/detail and narrow-screen horizontal table containment.
- Manual corrections are not implemented/accepted. Future separate overrides
  must take precedence over generated scores; don't hand-edit generated output.

## Validation and limitations

- `make test` passes: two Spotify offline tests, UI normalization/overlay/sort
  tests and 20 Qobuz mocked/offline tests. Build, JS syntax and diff checks pass.
- Low recall is intentional in v1. Translation/ensemble aliases, catalogue
  equivalences, movement completeness and recording/take identity need more work.
  This is a conservative deployable first pass, not complete catalogue validation.
- No additional Qobuz calls after metadata retrieval; no audio requests.

## Next action

Present the prepared branch for user review and deployment instruction. Broader
fallback queries and matcher coverage improvements remain proposed follow-ups.
See [backlog](backlog.md), [decisions](decisions.md) and [history](history.md).
