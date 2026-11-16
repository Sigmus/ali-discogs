# Ali Discogs

Updated: 2026-11-16, Europe/Amsterdam

Static explorer for ajozi’s Discogs collection and Spotify/Qobuz evidence.
[README](../../README.md) owns setup/build; [Qobuz guide](../qobuz.md) owns evidence
and cache commands. This directory owns current planning.

## Current state

- Branch main; enrichment pushed through3632140 on16November at user request.
  New104case batch verified locally, not pushed. Pages deployment not verified.
- Collection741copies/740unique. Saved labels: Spotify254Found/273Probable/
  210NotFound/4Unchecked; Qobuz12Found/162Probable/567Unchecked copies.
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
- Qobuz UI separates203Reviewed · unresolved from364Unchecked copies. Saved
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

- Earlier14priority,26secondary and16full-support batches complete; detailed
  recording decisions remain in history and their linked frozen audits.
- All38partial-support reviews complete:6Probable,32explicit holds.
  [Results](../plans/2026-11-16-qobuz-partial38.md) retain every source programme,
  raw credit, full alternative title list, hash, blocker and next action.
- New Probable: Kertész9297226,Pollini4031075,Barbirolli6748142,Karajan10707559,
  Gilels17748481,Pires5980586. Exact source-band/heading coverage, positive credits
  and recording-family corroboration; pressing/takes/mastering unverified.
- All104zero-rule reviews complete:3Probable,101explicit holds.
  [Results](../plans/2026-11-16-qobuz-zero104.md): Heifetz8923384,
  Mitropoulos6544574 and Schuricht36163426 use existing source-band validation.
  Full alternative inventories, raw roles, evidence hashes and next actions saved.
- Latest260script tests, normalization and static build pass. Batch had3label changes;
  collection/Spotify and all out-of-scope release payloads unchanged.
- 566unchecked unique:355work/credit,195withheld,5completeness,4rejected,
  6empty,1source hold. Reviewed holds remain searchable evidence, not Not found.
- Key holds include named ensemble members/chorus masters, associated-only roles,
  Oistrach identity, source-role conflicts, incomplete or unbound recording families.
  No general alias, threshold or credit waiver adopted.

## Next action and limits

936album cache integrated;23632tracks validated. All160original leads reviewed:
20recording families accepted,140explicit holds,0open in that frozen cohort.
Completed reviews do not imply all recordings are matched. No new provider calls.
Next inspect cached9283162(Schubert) then15660391(Mozart); these two are outside
this completed batch. Broader355work/credit inventory is a separate population.
Revisit each held case only when its saved evidence/rule prerequisite is met.
Broader source-role parser audit is proposed, not adopted. Krips finale is not
proven missing; joined-band mapping remains unresolved.

Continue verified cached reviews/commits autonomously. No unbounded retrieval,
warning retries, automatic push/deployment, source rewrites or musical-credit
waivers. Earlier holds need new evidence or a validated scoped rule: Casals/
Gieseking transfer, Prêtre named musicians, Reiner associated-role semantics,
Rubinstein source programme, Klemperer12690141timings and the twelve priority holds.
Bitches Brew and associated-credit policy remain proposals. Future Spotify
validation is separate. [Backlog](backlog.md), [decisions](decisions.md), [history](history.md).
