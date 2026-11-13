# Qobuz programme audit and publication readiness

Date: 2026-11-13, Europe/Amsterdam. Offline only; no new API calls.

## Retrieval integrity

Completed at 01:15:30 Europe/Amsterdam. Independently verified all 1,036
manifest albums: matching album IDs, advertised track counts and unique track
IDs within each album; 27,770 track entries. Final resumed run reused 150 outputs
or cached responses and fetched 886 albums. Earlier run fetched 127; overall
1,013 new unique album metadata fetches plus discovery/pagination requests.
Hourly metadata monitor deleted after completion.

## Rules and scores

v1 requires target work/title evidence plus all listed non-composer performers,
conductor and ensembles on supporting tracks, and a matching composer surname
where the target lists composers. Uses the existing small orchestra alias list;
no fuzzy person names or cross-catalogue equivalences are invented.
Catalogue prefixes, opus subdivisions, numbered sections and ordinal work names
are preserved. Generic movements under explicit headings can be omitted;
standalone named items remain part of the target programme.

Found (95%) requires one-to-one supporting tracks covering all target items,
with candidate track count equal to target count. Probable (85%) means each target
item has supporting tracks but grouping/extra material prevents that stricter
criterion. These are two heuristic evidence levels, NOT calibrated probabilities
or independent recording-session verification. Grouped work headings can leave
movement completeness uncertain; Probable therefore requires review, not acceptance.
No 100% scores assigned. All other cases stay unchecked with reasons and no score.
No Not found classifications are produced from first-pass queries.

## Broader evidence review

Reviewed all final Found target-to-candidate title correspondences (including
required credits), and inspected 15 spread-out Probable programme mappings plus
the known incomplete/mismatched/unresolved controls. This is a deliberately
selected catalogue-level audit, not a blinded evaluation or listening test.
No statistical precision/recall claim follows from it.

Audit found and corrected two implementation problems before this output:
work-heading selection omitted standalone programme items, and token-set matching
confused Part II A/B/C. Regression tests cover both. A matching title/artist
alone is not sufficient. Known strong candidates can remain unchecked when
catalogue aliases, grouped tracks, missing named credits or translations are unresolved.

| Discogs ID | Target | Final status | Evidence review |
| --- | --- | --- | --- |
| 7001990 | Four Suites For Orchestra | Found | One-to-one programme title mapping and required credits; recording sessions not independently verified. |
| 8316658 | Preludes Book I | Found | One-to-one programme title mapping and required credits; recording sessions not independently verified. |
| 4478666 | Disney Songs The Satchmo Way | Found | One-to-one programme title mapping and required credits; recording sessions not independently verified. |
| 2939272 | Sketches Of Spain | Found | One-to-one programme title mapping and required credits; recording sessions not independently verified. |
| 1445439 | Glenn Gould Plays Music Of William Byrd And Orlando Gibbons | Found | One-to-one programme title mapping and required credits; recording sessions not independently verified. |
| 8597411 | Satchmo Sings | Found | One-to-one programme title mapping and required credits; recording sessions not independently verified. |
| 3759065 | The Köln Concert | Found | One-to-one programme title mapping and required credits; recording sessions not independently verified. |
| 9521183 | Les Scherzos Les Impromptus | Found | One-to-one programme title mapping and required credits; recording sessions not independently verified. |
| 2279849 | Les Ballades | Found | One-to-one programme title mapping and required credits; recording sessions not independently verified. |
| 2799449 | Sings The Blues | Found | One-to-one programme title mapping and required credits; recording sessions not independently verified. |
| 4719816 | The Chopin Scherzos | Found | One-to-one programme title mapping and required credits; recording sessions not independently verified. |
| 1477603 | Back To Back (Duke Ellington And Johnny Hodges Play The Blues) | Found | One-to-one programme title mapping and required credits; recording sessions not independently verified. |
| 1855288 | Piano Concerto No. 1 / Piano Concerto No. 2 | Probable | Supporting work/credit groups; retain review requirement for grouping or extra material. |
| 7871589 | "Carnival" Overture; Scherzo Capriccioso; The Golden Spinning Wheel | Probable | Supporting work/credit groups; retain review requirement for grouping or extra material. |
| 6115836 | Symphony No.4 / Overture: In Nature's Realm | Probable | Supporting work/credit groups; retain review requirement for grouping or extra material. |
| 15282801 | Symphony No. 3 In E Flat Major Opus 55 "Eroica" | Probable | Supporting work/credit groups; retain review requirement for grouping or extra material. |
| 28133197 | Symphonie No. 1 / Karelia Suite | Probable | Supporting work/credit groups; retain review requirement for grouping or extra material. |
| 7678883 | The Piano Sonatas | Probable | Supporting work/credit groups; retain review requirement for grouping or extra material. |
| 12189169 | Cello Concerto No.2 / Chant Du Ménestrel | Probable | Supporting work/credit groups; retain review requirement for grouping or extra material. |
| 6919420 | Eroica-Variationen / Piano Sonata No.7 | Probable | Supporting work/credit groups; retain review requirement for grouping or extra material. |
| 6175022 | Sonaten (No. 15 »Pastorale« ∙ No. 3) | Probable | Supporting work/credit groups; retain review requirement for grouping or extra material. |
| 2949124 | Sonate No.3 / Polonaises Nos. 3 · 4 · 6 | Probable | Supporting work/credit groups; retain review requirement for grouping or extra material. |
| 9387170 | The Piano Concertos | Probable | Supporting work/credit groups; retain review requirement for grouping or extra material. |
| 7159852 | Études Op. 10 Et Op. 25 | Probable | Supporting work/credit groups; retain review requirement for grouping or extra material. |
| 18770818 | Symphony No. 4 | Probable | Supporting work/credit groups; retain review requirement for grouping or extra material. |
| 1607240 | 12 Etudes D'Exécution Transcendante / 3 Etudes De Concert | Probable | Supporting work/credit groups; retain review requirement for grouping or extra material. |
| 4197603 | Requiem Mass In C Minor | Probable | Supporting work/credit groups; retain review requirement for grouping or extra material. |

Negative/uncertain controls: 7001990 candidate 3610154955247 supports only 2/4
suites and remains unchecked; a different complete candidate is Found.
15282801 candidate ezfmmvuhlu4uc fails Concertgebouw credits (Vienna orchestra).
8121703 remains unchecked (Longo/Kirkpatrick aliases unverified).
5820114 remains unchecked (5/8 items supported; variation catalogue aliases
unresolved), despite its initial promising manual programme inspection.
6678433 remains unchecked (13/14), preventing an incomplete mazurka-only album
from covering a larger LP programme. Empty searches remain unchecked.

## Output and limits

Final unique-release counts: 12 Found, 54 Probable, 674 unchecked (740 total).
Copy counts: 12 Found, 54 Probable, 675 unchecked (741 total).
The 674 unresolved releases include all 370 empty first-pass searches.
This is an intentionally cautious first release, not complete catalogue coverage.
Manual recording-session review, broader queries and multilingual/catalogue alias
work remain follow-ups. The date/year of a digital reissue is not recording proof.

`data/qobuz_matches.json` is generated offline, versioned and separate from
Spotify output. It contains selected public catalogue fields, programme evidence,
heuristic scores and source fingerprints; no auth headers, token or audio URLs.
Build copies it directly without reading raw caches. No hand-edited correction
has been accepted: future manual overrides must live separately, take precedence
over generated scores, and be validated before publication. Do not edit the
generated file expecting changes to survive regeneration.

No remote push, merge or deployment performed.
