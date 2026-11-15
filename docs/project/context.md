# Ali Discogs

Updated: 2026-11-15, Europe/Amsterdam

Static explorer for ajozi’s Discogs collection and Spotify/Qobuz evidence.
[README](../../README.md) owns setup/build; [Qobuz guide](../qobuz.md) owns evidence
and cache commands. This directory owns current planning.

## Current state

- Branch main; pushed through cf7f263 on15November. Later work remains local;
  deployment not verified. Inspect Git before claiming remote state.
- Collection741copies/740unique. Saved labels: Spotify254Found/273Probable/
  210NotFound/4Unchecked; Qobuz12Found/135Probable/594Unchecked copies.
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

## Fourteen-case batch complete

- User authorized the 14 priority cases as one batch without routine questions.
  All 14 reviewed: Stern/Ormandy6686688 and Klemperer7002243 now Probable85;
  twelve candidate-specific holds retain explicit blockers and next actions.
- Stern: exact work fields bind six movements from the cached Sony original-jacket
  box, with positive performers and per-work composers. Klemperer: four Eroica
  movements plus Fidelio; local source-title correction excludes LeonoreIII despite
  the source Op72b wording. Exact pressing/take/mastering remain unverified.
- Holds separate missing programme, different recording family, transfer identity,
  source voice/orchestra scopes and unresolved timing/container structure.
  Klemperer12690141Prometheus differs by82seconds; no silent timing correction.
- Evidence and frozen14IDs: `data/qobuz_priority14_batch_audit.json`.
  [Batch plan/results](../plans/2026-11-15-qobuz-priority14-batch.md).
  Validators and workflow queue regenerate entirely offline; reviewed blockers
  cannot silently return to the priority list through a partial alternative.
- 215 script tests, all14 source/track-hash validations, UI normalization and build
  pass. Only6686688/7002243accepted labels changed. Collection/Spotify unchanged.
  No Qobuz requests, policy exceptions, push or deployment in this batch.
- 593unchecked unique:383work/credit,160metadata,40withheld,3rejections,6empty,
  1source hold. The383work/credit cases split into26secondary partial leads,
  354zero-current-support cases and3known constraints; no open priority cases.

## Next action and limits

Reassess the 26 secondary partial leads as a separate bounded queue. Their partial
source-unit support is triage, not confidence or a forecast of accepted matches.
Do not revisit the twelve new holds without new evidence or a tested scoped rule.

Continue verified cached reviews/commits autonomously. No unbounded retrieval,
warning retries, automatic push/deployment, source rewrites or new instrument-scope
exemptions. Prêtre missing named credits, Casals/Gieseking transfer provenance,
Reiner associated-role semantics and Rubinstein's source programme remain holds.
Bitches Brew and associated-credit policy remain proposals. Future Spotify
validation is separate; existing labels are not comparable accuracy measurements.
[Backlog](backlog.md), [decisions](decisions.md), [history](history.md).
