# Secondary cached leads

15 November 2026, Europe/Amsterdam. User authorized continuation after the fourteen
priority reviews. Freeze the 26 secondary IDs from the current workflow queue.
First reassess source programmes and cached alternatives across all 26, separating
real partial albums from title/heading/work-field parsing gaps. A screen is not a
full recording review. Save progress and per-case next actions.

Then complete bounded recording reviews where existing evidence supports them,
with original source hashes, whole-programme mappings, positive named performers
and composers, and explicit recording-family limitations. Use existing review
kinds where possible; do not waive musical credits or treat partial coverage as
confidence. No new Qobuz requests, raw-source changes, push or deployment.

Validate false-positive cases, regenerate publication and inventory sequentially,
verify accepted-label changes stay within reviewed IDs, update docs and commit
verified results. Leave source/transfer/policy gaps explicitly unresolved.

## Reassessment and first verified publications

All 26 sources and their cached candidate diagnostics have a saved assessment in
`data/qobuz_secondary26_audit.json`, including frozen IDs and source/target/album
hashes. Three recording reviews are complete; the other 23 are explicitly still
pending. Screening does not mean their recordings have been accepted or rejected.

- Lipatti1704535: all 14 waltzes occur in the source's unusual order in cached
  EMI/Warner0724356695658. The final three pieces are extra tracks. Positive
  pianist/composer credits and the studio collection family support Probable.
- François4067901: the cached Warner UPC matches its publisher's product for the
  Paris 2–4 July1958 mono cycle. The 1959 source is mono. All 14 catalogue members
  map one-to-one; a later stereo cycle is not substituted.
- Karajan7860979: all nine Bruckner symphonies, 35 distinct movements, are bound
  through explicit digital work fields and positive composer/Karajan/Berlin
  credits. The Institute corroborates the complete cycle compiled in1982, distinct
  from later Vienna recordings. Source1976–1982 and publisher1975–1981 dating are
  retained as different observations, not silently reconciled session dates.

These are Probable recording-family matches, not exact pressing/take/mastering
verification. The reviews use existing title-correction and bound-track kinds.
No global French-number, work-field or performer policy changed. Missing pieces,
wrong opus members, different orchestra and different composer remain failures.

Reusable findings: French N°/opus-member text and bare movement titles with a
separate work field can hide complete programmes. Source headings can also inflate
unit counts. A global parser change is not adopted here: it needs a separate
whole-collection diff and regression scope. The current manual mappings are frozen
by source and track hashes.

Other cases need explicit programme reconstruction, source casts/instrumental
scopes or recording-family proof. Examples: the full Vivaldi alternative is
Mutter/Vienna rather than Schwalbé/Berlin; the Rubinstein candidate is only the
concerto from a much larger source; Getz/Gilberto composer/featured-artist roles do
not by themselves establish Jobim's instrumental participation on every track.
The François nine-piece source12419718 remains a separate recording-family review;
its pieces must not inherit the waltz-cycle decision.

Primary references: [François mono session and product](https://wmg.jp/samson-francois/discography/23483),
[Lipatti studio collection](https://www.warnerclassics.com/release/chopin-waltzes-lipatti),
[Karajan complete-cycle distinction](https://karajan.org/news/karajan-digital-library-vol-21/).

## Validation and checkpoint

221 script tests pass, including wrong opus member/composer, missing waltz versus
bonus substitute, different Bruckner orchestra and wrong work-field regressions.
Regenerated publication/inventory/queue, role census, UI normalization and static
build pass. Exactly1704535/4067901/7860979changed Unchecked→Probable; no Spotify or
source changes. Copies12Found/138Probable/591Unchecked.23secondary recording reviews
remain pending, with François12419718recording-family/source check next. No Qobuz
requests, push or deployment; mocked429/STOPtest output is not a provider warning.
