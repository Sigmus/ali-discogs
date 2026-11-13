# Ali Discogs

Updated: 2026-11-13, Europe/Amsterdam

Match Ali's Discogs collection (`ajozi`) against Spotify and browse a static
explorer. See [README](../../README.md) for setup and architecture.

## Current state

- Branch `codex/qobuz-poc`; portable evidence/matcher/UI (`ad1d7fd`) and full
  request-cache archive (`d7c3e98`) pushed to origin on 2026-11-13 at user request.
  Ali can check out the branch. No merge or Pages deployment performed.
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
  fetch remains necessary. Mutable cache directories/source/token remain ignored.
- User requested collaborator access: `data/qobuz_evidence.json.gz` now preserves
  all searches/full metadata in a whitelisted ~1.8 MB portable snapshot. Matcher
  uses this by default, with no local cache, token or source checkout needed.
- User additionally requested sharing raw caches: versioned ~5 MB archive
  `data/qobuz_request_cache.tar.gz` preserves all 1,759 request JSON responses.
  Restore with `python3 scripts/qobuz_cache_archive.py restore`; it validates
  members and refuses conflicting local files. No credentials/logs/source shared.
- [Qobuz guide](../qobuz.md) documents setup, preservation and resume commands.

## Offline matching and publication preparation

- Implemented qobuz-programme-v1 plus bounded reviewed-expansion-v2; all original
  1,217 candidate entries assessed offline, with ten additional matched releases.
  [Audit](../plans/2026-11-13-qobuz-audit.md) records rules, reviewed cases and limits.
- Unique releases: 12 Found / 64 Probable / 664 unchecked. Copies: 12 / 64 / 665.
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
- Removed the Sort dropdown; table headers control sorting. Added Qobuz match
  immediately after Spotify, with counts/frequency ordering and URL persistence.
  Browser verified filters, header sorting and Clear; Probable now has 64 rows.
  User requested committing/pushing this filter UI edit on codex/qobuz-poc;
  inspect Git for resulting commit. No merge or deployment requested.
- UI shows Qobuz status/confidence in table/details, sortable status column,
  linked candidates and expandable programme evidence. Browser verified desktop
  table/detail and narrow-screen horizontal table containment.
- Manual corrections are not implemented/accepted. Future separate overrides
  must take precedence over generated scores; don't hand-edit generated output.

## Validation and limitations

- Current validation: 33 Qobuz mocked/offline tests, UI normalization/overlay/sort,
  build and diff checks pass. Earlier full-suite Spotify tests also passed.
- Low recall is intentional in v1. Translation/ensemble aliases, catalogue
  equivalences, movement completeness and recording/take identity need more work.
  This is a conservative deployable first pass, not complete catalogue validation.
- No additional Qobuz calls after metadata retrieval; no audio requests.

## Next action

Bounded offline expansion integrated: ten new Probable releases, unchanged original
66 matched entries. All 33 Qobuz offline tests, UI tests/build pass; browser verified.
Twenty-four sourced work inventories, explicit child movements and timed target
tracks support the fixed scope. Alias-dependent and ambiguous cases withheld.
See [pilot](../plans/2026-11-13-qobuz-coverage-pilot.md). Next: retrospectively audit
v1 completeness, then select a new bounded offline sample. No additional Qobuz
calls or deployment. User requested committing this checkpoint, then auditing
the original 66 matches offline; no push requested.
See [backlog](backlog.md), [decisions](decisions.md) and [history](history.md).
