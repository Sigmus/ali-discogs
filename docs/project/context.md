# Ali Discogs

Updated: 2026-11-15, Europe/Amsterdam

Static explorer for ajozi’s Discogs collection and Spotify/Qobuz evidence.
[README](../../README.md) owns setup/build; [Qobuz guide](../qobuz.md) owns evidence
and cache commands. This directory owns current planning.

## Current state

- Branch main; pushed through cf7f263 on15November. Later work remains local;
  deployment not verified. Inspect Git before claiming remote state.
- Collection741copies/740unique. Saved labels: Spotify254Found/273Probable/
  210NotFound/4Unchecked; Qobuz12Found/138Probable/591Unchecked copies.
- Qobuz publication `data/qobuz_matches.json` is separate from Spotify collection
  results. Labels/scores are saved data; Qobuz85/95 are heuristic levels, not
  probabilities. Legacy Spotify labels are not comparable accuracy measurements.
  [Validation gap](../plans/2026-11-13-cross-service-validation-gap.md).
- Local UI http://127.0.0.1:8000/ ; live https://sigmus.github.io/ali-discogs/ .
  Server/deployment status not rechecked by this source review.

## UI checkpoint

- ajozi vinyl with small on Discogs link. Table/Captions/Shelf; source/catalogue
  sidebar detail view; no Albums back button.
- Six searchable multi-select filters: OR within field, AND across fields. Each
  defaults to frequency with individual Alphabetical checkbox. Search after
  Decade; outlined Clear/Pin icons after Search, delayed theme-aware tooltips.
- Subtle full-width filter band; optional sticky pin below header. Table headers
  always sticky. Table sorts all columns; other views offer Year/Composer only.

## Retrieval complete

- Fixed12+305scope:83metadata albums/1313tracks;603queries (520nonempty/83empty).
  299of305releases have search hits;6empty, not proof of absence.
- Nine-album follow-up216tracks complete. Approved15November seven-album follow-up
  complete7albums/97tracks,9HTTP attempts, no warnings. Run/sleep assertion ended.
- Shared request archive2504responses; all2497prior members preserved. Canonical
  index1164URLs. Credentials/live run state ignored; portable evidence committed.
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
- Exact full-name Felix Mendelssohn identity requires positive Composer-role credit;
  no surname/performer alias or legacy-score change. [Identity plan](../plans/2026-11-15-qobuz-composer-identity.md).
- Future Discogs normalization strips role annotations;9false-performing credits
  and1ordering change found in740detail diagnostic. Genuine singers preserved.
  No collection refresh or bulk result/score changes applied.
- Casals original COLH17labels confirm BWV1009/1010; saved1008typo correction and
  liner-author removal apply only to a hash-bound offline diagnostic. Raw source,
  normalized collection, legacy score and publication remain unchanged.
- Both Casals LPs now have source-bound diagnostic mappings:24distinct movements,
  Suites3–6; complete programmes do not establish Nar Classical transfer identity.
  Candidate lacks session/take markers, so both remain Unchecked.

## Cached review progress

- Fourteen priority reviews complete:2Probable,12explicit holds.
  [Results](../plans/2026-11-15-qobuz-priority14-batch.md) and frozen audit retain
  every case, source/track hash, alternative, blocker and next action.
- All26secondary leads now have source/cache reassessments, not26recording approvals.
  Three full recording reviews completed: Lipatti1704535and François4067901
  (14waltzes each), Karajan7860979(Bruckner1–9,35movements) now Probable85.
  [Secondary plan/results](../plans/2026-11-15-qobuz-secondary26.md),
  `data/qobuz_secondary26_audit.json`.23recording reviews remain pending.
- Existing bounded review kinds reconcile source N°/opus-member wording and bare
  movement titles with explicit work fields. No global parser/credit-policy change.
  François1958mono UPC is publisher-confirmed; later stereo recordings are separate.
  Karajan Berlin cycle is distinct from later Vienna7/8. Exact takes/mastering unverified.
- 221script tests, UI normalization and static build pass. Publication diff has
  exactly1704535/4067901/7860979Unchecked→Probable; collection/Spotify unchanged.
- 590unchecked unique:380work/credit,160metadata,40withheld,3rejections,6empty,
  1source hold. Work/credit queue:23secondary leads,354zero-current-support cases,
  3known constraints; no open priority cases. No Qobuz calls, push or deployment.

## Next action and limits

Next recording-family review: François12419718nine-piece recital. Do not transfer
its recording identity from the accepted1958waltz cycle or choose compilation
tracks solely by composition. Other23screened cases have per-case next actions.
Source-unit fractions are triage, not match confidence or catalogue absence.

Continue verified cached reviews/commits autonomously. No unbounded retrieval,
warning retries, automatic push/deployment, source rewrites or musical-credit
waivers. Earlier holds need new evidence or a validated scoped rule: Casals/
Gieseking transfer, Prêtre named musicians, Reiner associated-role semantics,
Rubinstein source programme, Klemperer12690141timings and the twelve priority holds.
Bitches Brew and associated-credit policy remain proposals. Future Spotify
validation is separate. [Backlog](backlog.md), [decisions](decisions.md), [history](history.md).
