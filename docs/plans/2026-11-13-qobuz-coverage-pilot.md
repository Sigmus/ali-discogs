# Offline Qobuz coverage pilot

Date: 2026-11-13, Europe/Amsterdam. User-authorized bounded pilot; no API calls.

## Method and reproducibility

Run `.venv/bin/python scripts/qobuz_coverage_pilot.py` (or
`uv run python scripts/qobuz_coverage_pilot.py`). It uses the committed snapshot
and current publication matches, prioritises unresolved releases with partial
coverage, then release ID, and stops after 12 releases with proposals. It examined
219 unresolved releases to reach that bound. This is a selected sample, not a
coverage estimate. It does not alter the matcher, snapshot or publication output.

Search all cached albums using an index of production-required performer names,
then evaluate eligible albums with unchanged programme/credit rules. Separately
try three explicit experimental name variants: David Oistrach/Oistrakh, Kiril/
Kirill Kondrashin, and Chicago Symphony Orchestra/(CSO). These are discovery
aliases only, not independently sourced identities or enabled production rules.
No fuzzy artist matching, cross-catalogue guesses or relaxed credit requirements.

`data/qobuz_coverage_pilot.json` records all 15 candidate mappings, original-search
membership, baseline status, experimental alias dependence and inspected IDs.
It is a research artifact and is not included in the website build.

## Results and manual catalogue review

12 proposed releases, including eight originally empty searches. Eleven have a
candidate supported by unchanged rules; one depends on the Oistrach alias. All
new candidates came from other releases' cached search results. Publication
remains 12 Found / 54 Probable / 674 unchecked unique releases.

Reviewed each proposed target-to-track mapping, credited names and available
movement titles; not audio or independent recording-session documentation.

| Discogs ID | Candidate album | Review of cached programme |
| --- | --- | --- |
| 890111 | 0002894776360 | Gilels: Op.26 I–IV and Op.31/1 I–III; complete-looking work groups. |
| 1093216 | 0002894791000; y7nd66idm247a | Kleiber/Vienna: Beethoven Fifth I–IV. Reject 0002894778168 and 0002894805871 as complete-programme matches: each has only movement I. |
| 1469965 | 0886445221237 | Gould: all three Wagner transcriptions. Durations 582/795/1415 sec versus LP 572/792/1419 sec support a lead, not session proof. |
| 1517438 | 0002894779797 | Pollini/Böhm/Vienna: Beethoven Fourth Concerto I–III. |
| 1917259 | 0002894776360 | Gilels: Op.10/2 and Op.57, each I–III. |
| 2127229 | 0002894779797 | Pollini/Böhm/Vienna: Emperor I–III. |
| 2712474 | d4y2z1shovo2a | Oistrach/Oistrakh and Berlin: Mozart K.216 and K.219, each I–III. Alias identity requires confirmation before production adoption. |
| 3000698 | 0002894776360 | Gilels: Op.7 and Op.2/2, each I–IV. |
| 3275173 | 3610151639041 | Rubinstein/Golschmann/NBC: Rachmaninoff Second Concerto I–III. |
| 3441146 | 0002894776360 | Gilels: Op.27/2 I–III, Op.27/1 I–IV, Op.13 I–III. |
| 3699703 | 0002894791673 | Karajan/Berlin: all nine Beethoven symphonies, named movements present; Ninth finale split into IVa-b/IVc-j. Recording cycle identity still needs review. |
| 4382530 | 0002894190682 | Richter/Karajan/Vienna Symphony: Tchaikovsky First Concerto I–III. Keep Vienna Symphony distinct from Vienna Philharmonic. |

## Finding and next implementation

Cache-wide reuse is useful immediately, without relaxing name matching. But v1
accepts a single movement as support for a work-level heading, producing two
incomplete candidates in this pilot. Never promote this raw report to publication.
The existing Probable review caveat is insufficient for automatic expansion.

Next: represent parent works and child movements explicitly, with a reviewed
expected-movement inventory or explicit target child tracks. If completeness is
unknown, retain an unresolved discovery lead; do not infer completeness merely
from a sequence starting at I or from album track count. Add the two incomplete
Kleiber compilations as real-data negative controls, alongside wrong-orchestra,
opus-subdivision, omitted standalone items and Part II A/B/C controls. Handle
split/joined movements conservatively. Then rerun this bounded sample before
expanding cache-wide discovery or authorizing any new search requests.

Catalogue equivalences and additional translations are deferred: this pilot
already exposed a more urgent completeness issue without those changes.

## Follow-up: implemented completeness check

User requested continuing on 2026-11-13. `scripts/qobuz_completeness.py` now
checks the fixed 12-release pilot, without regenerating or promoting its proposals.
Run `uv run python scripts/qobuz_completeness.py`; output is the separate
`data/qobuz_completeness_pilot.json` research report with input fingerprints.

A small independently sourced inventory in `data/qobuz_work_inventory.json`
records composer + exact catalogue/subdivision + expected movement ordinals:

- Beethoven Fifth Symphony: [LA Phil work programme](https://www.laphil.com/works/symphony-no-5-in-c-minor-op-67).
- Beethoven Fourth Piano Concerto: [LA Phil work programme](https://www.laphil.com/works/piano-concerto-no-4-in-g-major-op-58).
- Beethoven Fifth Piano Concerto: [Berliner Philharmoniker programme note](https://www.berliner-philharmoniker.de/en/programme-notes/ludwig-van-beethoven-concerto-for-piano-and-orchestra-in-e-flat-major-op-73/).
- Tchaikovsky First Piano Concerto: [Atlanta Symphony/UGA concert programme, page 2](https://pac.uga.edu/wp-content/uploads/2024/05/Atlanta-Symphony-Orchestra-4.13.25-program-PDF.pdf#page=2).

References inspected 2026-11-13; no catalogue credentials or Qobuz requests used.
Only ordinal facts are stored, not copied programme essays or score material.

The checker requires every expected numbered movement in order, each backed by
production-required performer/composer credits. Duplicate, reordered, missing,
split/joined or ambiguous movement labels cannot pass. Unknown work structures,
multiple target composers/catalogue IDs and explicit single-movement targets
stay unknown in this first implementation. Target child-track hierarchy matching
is not yet implemented. The checker does not infer expected counts from a
candidate's apparent sequence, or turn experimental name aliases into accepted
identities. It does not verify unmarked musical cuts or recording sessions.

Results for the same 15 candidates:

- Five candidates pass catalogue-level movement completeness, covering four
  releases: 1093216 (two candidates), 1517438, 2127229 and 4382530.
- 0002894778168 for 1093216 is incomplete (only I of I–IV).
- 0002894805871 for 1093216 remains unknown (no ordinal movement label), and is
  withheld just like the incomplete compilation. The prior manual exclusion stands.
- Eight other candidates have no sufficient inventory, so total unknown is nine.
  Karajan's nine-symphony set cannot pass merely because its Fifth is documented.

All 28 Qobuz mocked/offline tests pass, including real cached Kleiber negatives,
both complete Kleiber controls and the prior wrong-orchestra control. Publication
matches and UI counts remain unchanged. Next extend the sourced inventory and
explicit target child-track handling across the remaining bounded pilot before
integrating expansion into the publication matcher; do not blindly publish the
raw discovery report or treat movement coverage as session identity.

## Extended pilot and bounded integration

User requested continuing the remaining pilot on 2026-11-13. Expanded inventory
now covers 24 works. Additional ordinal facts were checked against:

- [DCML Beethoven piano-sonata corpus](https://dcmlab.github.io/beethoven_piano_sonatas/): opus identities and movement-file inventory for sonatas 2, 4, 6, 8, 12, 13, 14, 16 and 23. See Hentschel et al. (2024), [data report](https://doi.org/10.18061/emr.v18i1.8903). Only the relevant identity/ordinal facts retained; no scores or annotations copied.
- Eastman's authored [Beethoven Symphony Basics](https://www.esm.rochester.edu/beethoven/symphony-no-1/) articles for symphonies 1–4 and 6–9; per-work URLs are stored in the inventory. Sixth has five numbered movements; other symphonies have four.
- [LA Phil Mozart K.216 programme](https://www.laphil.com/works/violin-concerto-no-3-k-216): explicitly discusses the three-movement form for both K.216 and K.219.
- [RSNO Rachmaninov Second Concerto programme, page 12](https://www.rsno.org.uk/wp-content/uploads/2023/11/Rachmaninov-Piano-Concerto-No2-91011-Nov-2023.pdf#page=12): lists the three movements.

Checker v2 also handles numbered child tracks beneath a work heading when no
inventory exists. It compares those explicitly requested movement ordinals with
credited candidate movements, with scope `listed-target-movements`; it makes no
claim that the target itself requests the complete composition. Ambiguous children
stay unknown. Inventoried whole-work checks remain stricter. Distinct target items
cannot reuse the same candidate track.

For explicit standalone Discogs tracks, a single credited title correspondence
with duration within max(5 seconds, 3%) supports scope `listed-target-track`.
This bounded heuristic admits Gould's three Wagner transcriptions (all reviewed
above); it is not a whole-work, uncut-audio or recording-session guarantee. Missing
or distant durations, multiple matches and overlapping track assignments cannot
pass this route.

Final fixed-pilot result: 12/15 candidates have programme-completeness support,
covering 11/12 releases. One incomplete and two unknown candidates are withheld.
One of the 11 releases (2712474) still requires the experimental Oistrach alias;
it is not integrated. Karajan's nine-symphony set remains unknown because of the
split Ninth finale. The two incomplete Kleiber compilations remain excluded.

Integrated the remaining ten releases/eleven candidates into local generation as
Probable 85%, using `data/qobuz_expansion_scope.json` as a fixed, reviewed candidate
allowlist. It is not a manual score override. Generation recomputes all original
credits and completeness without experimental aliases on every run. Discovery
research output does not automatically enlarge this scope. The matcher records
scope/inventory fingerprints and candidate completeness evidence. Original v1
candidates are retained; the existing 66 matched releases were not rescored under
the new gate and their entries are byte-for-byte unchanged. A retrospective
completeness audit of that baseline remains future work.

Unique-release output is now 12 Found / 64 Probable / 664 unchecked (copies:
12 / 64 / 665). No confidence thresholds were lowered and no new Qobuz requests
were made. Programme evidence does not establish recording-session identity.

Validation: all 33 Qobuz mocked/offline tests, UI normalization/overlay/sort tests,
static build and diff checks pass. Repeated generation is checked for identical
output. Browser verified a newly added Gilels release at 85% Probable, evidence
explanation in details and the 64-row Probable filter. No commit/push/deployment.
