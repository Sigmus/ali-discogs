# Ali Discogs

Updated: 2026-11-16, Europe/Amsterdam

Static explorer for ajozi’s Discogs collection and Spotify/Qobuz evidence.
[README](../../README.md) owns setup/build; [Qobuz guide](../qobuz.md) owns evidence
and cache commands. This directory owns current planning.

## Current state

- Branch main; enrichment pushed through3632140 on16November at user request.
  Local enrichment/review-progress checkpoints not pushed. Pages not verified.
- Collection741copies/740unique. Saved labels: Spotify254Found/273Probable/
  210NotFound/4Unchecked; Qobuz12Found/186Probable/543Unchecked copies.
- Qobuz publication `data/qobuz_matches.json` is separate from Spotify collection
  results. Labels/scores are saved data; Qobuz85/95 are heuristic levels, not
  probabilities. Legacy Spotify labels are not comparable accuracy measurements.
- Local UI http://127.0.0.1:8000/ ; live https://sigmus.github.io/ali-discogs/ .

## UI checkpoint

- ajozi vinyl with small on Discogs link. Table/Captions/Shelf; source/catalogue
  sidebar detail view; no Albums back button.
- Six searchable multi-select filters: OR within field, AND across fields. Each
  defaults to frequency with individual Alphabetical checkbox. Search after
  Decade; outlined Clear/Pin icons after Search, delayed theme-aware tooltips.
- Subtle filter band with optional pin; table headers always sticky.
- Qobuz UI separates254Reviewed · unresolved from289Unchecked copies. Saved
  review progress is independent of match status; detail shows the saved blocker.
  Table sorts all columns; other views offer Year/Composer only.

## Retrieval complete

- Fixed12+305scope:83metadata albums/1313tracks;603queries (520nonempty/83empty).
  299of305releases have search hits;6empty, not proof of absence.
- Nine-album follow-up216tracks complete. Approved15November seven-album follow-up
  complete7albums/97tracks,9HTTP attempts, no warnings. Run/sleep assertion ended.
- Shared request archive3440responses; all2504prior members preserved. Canonical
  index2100URLs. New936album cache validated; credentials/live run state ignored.
- [Run plan](../plans/2026-11-14-qobuz-remaining-retrieval.md),
  [seven-album follow-up](../plans/2026-11-15-qobuz-metadata-followup.md).

## Offline review checkpoint

- Recording-family acceptance never verifies exact LP pressing/takes/mastering.
  Preserve source discrepancies, unknown transfer provenance and missing credits.
- Gilels15221307source-bound composer guard prevents Medtner/Beethoven Op22collision.
  Rubinstein7971104source label has14works versus saved13; publication hold remains.
- Reviewed Mendelssohn composer identity is exact and source-bound; no general
  performer alias. Source-role normalization/Casals mappings remain diagnostic;
  raw collection and historical results unchanged, transfer holds retained.

## Cached review progress

- Earlier14priority,26secondary and16full-support batches complete; detailed
  recording decisions remain in history and their linked frozen audits.
- Earlier38partial-support reviews:6Probable/32holds. All104zero-rule reviews:
  3Probable/101holds. Frozen audits retain sources, alternatives and next actions.
- Latest326script tests pass; remaining18batch adds18explicit holds.
  Collection/Spotify, scoring rules and cache bytes unchanged; explicit review
  lookup now includes the older metadata-needed archive.
- 542unchecked unique:280work/credit,246withheld,5completeness,4rejected,
  6empty,1source hold. Reviewed holds remain searchable evidence, not Not found.
- Key holds include named ensemble members/chorus masters, associated-only roles,
  Oistrach identity, source-role conflicts, incomplete or unbound recording families.
  No general alias, threshold or credit waiver adopted.

## Next action and limits

936album cache integrated;23632tracks validated. All160original leads reviewed:
20recording families accepted,140explicit holds,0open in that frozen cohort.
Completed reviews do not imply all recordings are matched. No new provider calls.
Earlier source/recording holds and completed work-context reviews remain in
[history](history.md).150credit-support cases still lack saved decisions. Vocal-role
and source-role experiments remain diagnostic; no role waiver adopted.
All28title-context leads reviewed:15Probable/13holds,0pending.
Frozen151title/work diagnostic complete:409pairs; all3gains now reviewed.
Heifetz7065721and Gould2548602Probable; Dido24278222split-act mapping held.
[Three-case results](../plans/2026-11-16-qobuz-title3.md). Queue:2resolved/1held/
0pending;127title/work cases still have no saved decision. Gould’s approved
hash-bound timing exception retains all3discrepancies; global tolerance unchanged.
[Analysis/approval](../plans/2026-11-16-qobuz-timing-sensitivity.md).
All21musician-gap cases triaged:11programme/cast,6missing positive credits,
2collective-identity issues,2name leads. Both leads now Probable85 with existing
source-bound aliases:11876845Francescatti/Bernstein and21490438Fischer/Furtwangler.
[Review/limits](../plans/2026-11-16-qobuz-name2.md).8535848trio diagnostic complete:
8/8positive members/composer/timings; user approved exact collective decomposition.
NowProbable85with exact source/candidate/approval hashes, every member/instrument
required on every band. [Approval/limits](../plans/2026-11-16-qobuz-trio-identity.md).
Remaining18musician-gap reviews complete:18holds,37candidate comparisons,
0promotions. [Results/reopening prerequisites](../plans/2026-11-16-qobuz-musician18.md).
Original21cohort now3accepted/18held; no open cases. RobinHoodDell/RCA attribution
remains unresolved, not an alias. Next suggested batch:read-only triage of40frozen
catalogue-ID-gap cases; no new provider calls or rule adoption.
Broader source-role parser audit is proposed, not adopted. Krips finale is not
proven missing; joined-band mapping remains unresolved.

Continue verified cached reviews/commits autonomously. No unbounded retrieval,
warning retries, automatic push/deployment, source rewrites or musical-credit
waivers. Earlier holds need new evidence or a validated scoped rule: Casals/
Gieseking transfer, Prêtre named musicians, Reiner associated-role semantics,
Rubinstein source programme, Klemperer12690141timings and the twelve priority holds.
Bitches Brew and associated-credit policy remain proposals. Future Spotify
validation is separate. [Backlog](backlog.md), [decisions](decisions.md), [history](history.md).
