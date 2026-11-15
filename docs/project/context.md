# Ali Discogs

Updated: 2026-11-15, Europe/Amsterdam

Static explorer for ajozi’s Discogs collection and Spotify/Qobuz evidence.
[README](../../README.md) owns setup/build; [Qobuz guide](../qobuz.md) owns evidence
and cache commands. This directory owns current planning.

## Current state

- Branch main; enrichment pushed through2c5742a on15November at user request.
  GitHub Pages deployment not verified; inspect Git before claiming remote state.
- Collection741copies/740unique. Saved labels: Spotify254Found/273Probable/
  210NotFound/4Unchecked; Qobuz12Found/142Probable/587Unchecked copies.
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
- All26secondary recording reviews complete: earlier3Probable plus final23
  (4Probable,18withheld,1wrong-recording rejection). No pending secondary reviews.
  [Final23results](../plans/2026-11-15-qobuz-secondary23.md) and frozen audit retain
  every source, alternative, track hash, decision and next action.
- New Probable: Janis34776194, Klemperer/Wagner2808874, StMatthew25537708,
  Otello7095769. These establish recording families, not exact takes/pressings.
- Single-vocal-work review requires all raw source singers/choir in that work,
  conductor/orchestra on every track, complete source programme and publisher proof.
  It cannot combine credits across different operas. LP-side audio cuts unverified.
- 231script tests, UI normalization, static build and local detail checks pass.
  Exactly4Unchecked→Probable publication changes; collection/Spotify unchanged.
- 586unchecked unique:357work/credit,160metadata,58withheld,4rejected recordings,
  6empty,1source hold. Work/credit queue:354zero-current-support,3known constraints;
  no open priority/secondary leads. No new Qobuz calls or push/deployment.

## Next action and limits

Active: user authorized caching all saved candidates for160metadata-needed
releases before ranking:936distinct albums,1080release/album associations.
[Fixed-scope retrieval plan](../plans/2026-11-15-qobuz-uncached160.md). Slow resumable
worker launched22:19CET under caffeinate; first album14tracks, no warning.
Inspect `.qobuz-poc/uncached160-2026-11-15/progress.json` and log before acting. No new
searches, audio, automatic promotions or warning retries. Then rank offline.

Continue verified cached reviews/commits autonomously. No unbounded retrieval,
warning retries, automatic push/deployment, source rewrites or musical-credit
waivers. Earlier holds need new evidence or a validated scoped rule: Casals/
Gieseking transfer, Prêtre named musicians, Reiner associated-role semantics,
Rubinstein source programme, Klemperer12690141timings and the twelve priority holds.
Bitches Brew and associated-credit policy remain proposals. Future Spotify
validation is separate. [Backlog](backlog.md), [decisions](decisions.md), [history](history.md).
