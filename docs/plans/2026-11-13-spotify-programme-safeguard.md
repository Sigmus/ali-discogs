# Spotify safeguard for reviewed partial programmes

Implemented 2026-11-13, Europe/Amsterdam, after user approval. No service calls,
commit, push, merge or deployment.

## Behaviour

Two album-level results conflict with the complete cached track programme:

| Discogs release | Reviewed Spotify album | Missing programme | Change |
| --- | --- | --- | --- |
| 1012732 Brahms collection | 6dm8J92KYKdS6QBdmUGg2S | Symphonies2–4, violin concerto, German Requiem, Haydn Variations; only Symphony1 present | Probable → Unchecked |
| 6119238 Dvorak Sixth / My Home | 5arfXVZ6Cp45OVLB8EBf0E | My Home Op.62; Sixth present with different extras | Found → Unchecked |

A confirmed partial album cannot remain a Found/Probable full-release result,
regardless of its similarity score. Preserve the raw scoring signals and reviewed
album as `best_candidate`, clear accepted `album` and public confidence, and attach
`programme_review` with the finding and evidence fingerprints. Retain alternatives
for inspection without automatically selecting an unreviewed replacement. Unchecked
means further review is needed, not that the service lacks the requested music.

The explorer table/filter uses existing Unchecked handling; details explain missing
works and link to the reviewed partial album. Other candidates retain their prior
similarity scores and are explicitly described as unverified for full programme
and recording identity. No new status or claim of calibrated confidence.

## Evidence and scope

`data/spotify_programme_reviews.json` contains two explicit, candidate-specific
negative reviews. `src/ali_discogs/spotify_programme.py` checks normalized target
programme/credit hashes, album ID/name/track count and full portable track evidence
against `data/spotify_pilot_tracks.json.gz`. Changed source data fails closed and
requires a new review; missing evidence is not ignored. Service scores are excluded
from target hashes. Normal source updates require re-review rather than silently
reusing old judgements.

This does not infer absence from an unmapped title, validate an alternate, or impose
a general movement parser on Spotify. The other eight pilot recording validations
remain unresolved, and the remaining collection has not had this track-level audit.
No population accuracy or catalogue-coverage estimate follows from these two cases.

The normal `ali-discogs match --offline` pipeline applies the guard before returning
the selected result. Both portable review files are required matching inputs after
checkout; no credentials, ignored local worker folders or network are required.

## Verification

- Five targeted tests cover high-score blocking/no silent fallback, candidate/target
  scope, changed programme/album evidence, missing/changed/incomplete track cache,
  and independence from service-result changes.
- Existing full offline pipeline reproduction plus cache-key test pass: seven
  tests total under `tests/`. `make test` now discovers this entire directory.
- All63 existing offline/mocked script tests pass; UI normalization checks preserve
  Unchecked/null confidence/partial finding, JS syntax and static build pass.
- Compared all741 copies with the checkpoint: only these two Spotify objects
  change. Counts: **254 Found /275 Probable /210 Not found /2 Unchecked** copies.
- Qobuz regeneration remains **12 Found /67 Probable /661 Unchecked** unique
  (12/67/662 copies); its separate overlay survives the Spotify rescore. New Qobuz
  three-lead integration from the preceding stage remains intact.
- Local browser details show the missing-work warning, reviewed album link and
  alternatives. Raw caches/review ledgers stay outside the static Pages bundle.

Next proposal: inspect the Dvorak complete-cycle alternatives first, using cached
tracks if available; fetch a bounded slow sample only if separately authorized.
Review the wider Spotify collection before treating existing Found/Probable totals
as verified full-programme coverage.
