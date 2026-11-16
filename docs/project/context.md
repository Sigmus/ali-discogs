# Ali Discogs

Updated: 2026-11-16, Europe/Amsterdam

Static explorer for ajozi’s Discogs collection and Spotify/Qobuz evidence.
[README](../../README.md) owns setup/build; [Qobuz guide](../qobuz.md) owns evidence
and cache commands. This directory owns current planning.

## Current state

- Branch main; enrichment pushed through3632140 on16November at user request.
  Local enrichment/review-progress checkpoints not pushed. Pages not verified.
- Collection741copies/740unique. Saved labels: Spotify254Found/273Probable/
  210NotFound/4Unchecked; Qobuz12Found/181Probable/548Unchecked copies.
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
- Qobuz UI separates235Reviewed · unresolved from313Unchecked copies. Saved
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

- Seven-album/eight-release review: Weissenberg1662708, Bernstein3956949 and
  Ciccolini2236260Probable85; Yepes2857544withheld (missing finale, instrument
  uncertainty); Casals6628473/23950082, Pollini4101347 and Barenboim8274997unresolved.
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
- Latest296script tests pass; title151diagnostic adds3review leads, no matches.
  Collection/Spotify, production matcher and cache bytes unchanged.
- 547unchecked unique:304work/credit,227withheld,5completeness,4rejected,
  6empty,1source hold. Reviewed holds remain searchable evidence, not Not found.
- Key holds include named ensemble members/chorus masters, associated-only roles,
  Oistrach identity, source-role conflicts, incomplete or unbound recording families.
  No general alias, threshold or credit waiver adopted.

## Next action and limits

936album cache integrated;23632tracks validated. All160original leads reviewed:
20recording families accepted,140explicit holds,0open in that frozen cohort.
Completed reviews do not imply all recordings are matched. No new provider calls.
Earlier supported cached leads and source/recording holds remain in their
[completed review history](history.md); no hold is cleared by diagnostic support.
Twelve credit-support cases reviewed:Reiner1896362Probable;11explicit holds.
All11work-context gains from the frozen171diagnostic are now reviewed.
Earlier work-context9follow-up:2HeifetzProbable/7holds.
[Results and preserved blockers](../plans/2026-11-16-qobuz-work-context9.md).
Credit cohort remains150without saved decisions. Vocal-role copy experiment
improves only two already-held partial Rheingold programmes; no complete candidate
or status/confidence gains. Live role parser unchanged.
[Results](../plans/2026-11-16-qobuz-vocal-role-diagnostic.md).
All28title-context leads reviewed:15Probable/13holds,0pending.
Remaining151title/work diagnostic complete:409pairs,2full-unit and1partial lead;
no production rule or publication change.21work-title cases expose musician gaps;
40lack shared recognized catalogue IDs,83need work-identity interpretation.
[Results](../plans/2026-11-16-qobuz-title151-diagnostic.md). Next:review Gould2548602
and Heifetz7065721for complete source bands/recording, then partial Dido24278222.
Broader source-role parser audit is proposed, not adopted. Krips finale is not
proven missing; joined-band mapping remains unresolved.

Continue verified cached reviews/commits autonomously. No unbounded retrieval,
warning retries, automatic push/deployment, source rewrites or musical-credit
waivers. Earlier holds need new evidence or a validated scoped rule: Casals/
Gieseking transfer, Prêtre named musicians, Reiner associated-role semantics,
Rubinstein source programme, Klemperer12690141timings and the twelve priority holds.
Bitches Brew and associated-credit policy remain proposals. Future Spotify
validation is separate. [Backlog](backlog.md), [decisions](decisions.md), [history](history.md).
