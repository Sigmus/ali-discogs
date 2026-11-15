# Ali Discogs

Updated: 2026-11-15, Europe/Amsterdam

Static explorer for ajozi’s Discogs collection and Spotify/Qobuz evidence.
[README](../../README.md) owns setup/build; [Qobuz guide](../qobuz.md) owns evidence
and cache commands. This directory owns current planning.

## Current state

- Branch main; last known push7945944. Later work committed locally; no deployment
  verified. Inspect Git before claiming remote state.
- Collection741copies/740unique. Saved labels: Spotify254Found/273Probable/
  210NotFound/4Unchecked; Qobuz12Found/127Probable/602Unchecked copies.
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

## Next work

1. Ten cached leads reviewed:5photographer cases withheld for missing positive
   musical credits/wrong programme;5Barenboim EMI LPs blocked against later DG cycle
   (2chronological rejections,3undated unresolved holds). No metadata shortcut.
   Recording-review precedence enforced;12evidence records changed, no label changes.
   Next active review: Karajan7064777complete Mendelssohn set, including split
   Lobgesang Sinfonia; preserve source key discrepancy and recording caveats.
   [Source-credit plan](../plans/2026-11-15-qobuz-source-credit-reviews.md).
2. Keep Casals/Gieseking transfer identity unresolved until recording-specific
   evidence exists. Source correction alone does not authorize promotion.
3. Continue programme/credit/recording audits and meaningful false-positive tests;
   then build/UI consistency checks. [Offline plan](../plans/2026-11-14-qobuz-offline-followup.md).
4. Design comparable Spotify evidence sample after Qobuz; wider retrieval or
   relabelling needs a concrete scope first.

Prefer reliable matches to higher counts. No unbounded new-hit downloads, warning
retries, pushes or deployment. Bitches Brew credit exception remains a proposal.
Do not invent identity, overwrite source text or loosen credit gates for counts.
Current pass:189script tests, UI normalization/build pass.601unchecked unique:
412work/credit,160metadata,17withheld,3recording rejections,2completeness,6empty,
1source hold. No Qobuz calls/push; accepted counts unchanged.
[Backlog](backlog.md), [decisions](decisions.md), [history](history.md).
