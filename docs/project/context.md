# Ali Discogs

Updated: 2026-11-15, Europe/Amsterdam

Static explorer for ajozi’s Discogs collection and Spotify/Qobuz evidence.
[README](../../README.md) owns setup/build; [Qobuz guide](../qobuz.md) owns evidence
and cache commands. This directory owns current planning.

## Current state

- Branch main; pushed through cf7f263 on15November. Later work remains local;
  deployment not verified. Inspect Git before claiming remote state.
- Collection741copies/740unique. Saved labels: Spotify254Found/273Probable/
  210NotFound/4Unchecked; Qobuz12Found/133Probable/596Unchecked copies.
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

## Active offline review

- Prêtre13671866held after original images name M.Debost/M.Cazauran absent from
  candidate credits.13LPbands map to20digital sections, but equal sideBtotal
  does not erase per-band timing differences. Source and collection unchanged.
- Böhm6810640now Probable:2+4movements, exact work fields, source-image1977live
  marker and primary recording-family corroboration. Timing/take caveats retained.
- Reiner2463301complete5+8programme remains diagnostic: ChineseMarch orchestra
  has only compact AssociatedPerformer role, unresolved under adopted credit policy.
- Five further candidate holds:9792325missingK333;11938919missingOp58;
  2666680missingK595;2700887wrong concerto conductor/orchestra;5065978wrongK550
  conductor/orchestra. Other candidate recordings remain independent.
- Role census:775associated-only declarations across1164albums;540spaced/235compact.
  Parser spelling inconsistency is not a new acceptance rule. No blanket promotions
  or demotions. [Proposed semantics review](../plans/2026-11-15-qobuz-associated-credit-roles.md).
- Current pass209script tests, UI normalization/build pass.595unchecked unique:
  398work/credit,160metadata,27withheld,3rejections,6empty,1source hold.
  No Qobuz requests or further push. [Review plan](../plans/2026-11-15-qobuz-source-credit-reviews.md).

## Next action and limits

Brendel5403356now Probable:32sonatas+Andantefavori,103distinct tracks. Original
sideR/boxback confirm source Sonata9Op14No1; source text remains unchanged.
Joint timing fields mapped into86diagnostic spans; uninspected grouping marked
inference. Recording family supported, exact takes/mastering unverified.

Next: inspect original FALP317images for Furtwängler3737065Entr’acteII/IIIsection
identity; keep transfer provenance unresolved unless recording-specific proof exists.

Continue verified cached reviews/commits autonomously. No unbounded retrieval,
warning retries, automatic push/deployment, source rewrites or new instrument-scope
exemptions. Bitches Brew and associated-credit policy remain proposals. Future
Spotify evidence review is separate. Keep transfer-unresolved cases Unchecked.
[Backlog](backlog.md), [decisions](decisions.md), [history](history.md).
