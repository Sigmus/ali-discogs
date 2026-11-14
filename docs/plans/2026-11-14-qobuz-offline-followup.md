# Offline follow-up after remaining retrieval

14 November 2026, Europe/Amsterdam. Authorized continuation of AD-008.

## Reproducible screen

`uv run --with requests python scripts/qobuz_remaining_screen.py` uses portable
archives only. It validates fixed-scope export hashes/tasks and rejects incomplete,
duplicate-track or conflicting metadata. It never fetches or changes publication.
Report: `data/qobuz_remaining_screen.json`; evidence fingerprints retained.

2,227 distinct release/candidate pairs:
- 8 pass current work/credit plus completeness checks, across 7 releases.
- 335 have full metadata but unresolved work, credit or completeness support.
- 1,884 lack complete saved metadata for the candidate album.

Pairs are not unique albums or releases. Discovery rank combines title and queried
headline-artist similarity for triage only; it is not match confidence. Broad
queries also return irrelevant recordings. No accepted statuses changed.

## First bounded audit

`data/qobuz_remaining_audit.json` binds full target/candidate hashes and records
all eight passing pairs plus four near-miss examples. Strongest bounded next case:
4491358, Michelangeli/Giulini/Wiener Symphoniker Beethoven Op.73, candidate
g844jwmjmn7vb. All three numbered movements and required credits are supported;
DG label and 1982 year agree, but independent recording provenance still needs
review. Alternative i4ztk0dz6n6gc is a later compilation. Michelangeli sonata
3285095 also has all four Op.7 movements in that compilation.

Five Klemperer releases pass programme checks against vrg5q0y8vzvaa. These are
later compilation leads, not independently verified LP recording families:
12004072,24964822,26149643,24965038,26149832. All remain unpublished for now.

Near-misses show why work-title coverage alone is insufficient:
4352998 has 11/11 supported units but missing inventories and split source units;
7914875 has 3/3 works but incomplete inventory coverage;3672809 has the concerto
work/credits but no reviewed Op.15 movement inventory;6119375 has3/3 work support
but movement/completeness gaps. A parser failure is not proof the album lacks music.

## Reusable improvement to investigate

Expand independently sourced movement inventories for common Beethoven works,
with wrong-opus/subnumber, missing movement, credit and joined-track regressions.
The existing source [DCML piano sonatas](https://dcmlab.github.io/beethoven_piano_sonatas/)
was inspected on14November: it distinguishes Op.49 No.1 G minor from No.2 G major
and lists movement files for several omitted works. It is not a complete source
for every sonata: omitted rows must not be filled from guesses. No production
inventory or matching rule changed in this pass.

Next: recording-family review of4491358, then a source-backed inventory patch
and replay of affected cached cases. Before any extra Qobuz calls, prepare a
bounded candidate-metadata scope; do not fetch all1,884pairs. Spotify audit follows
Qobuz work. No automatic push/deployment.

Validation: two new regressions pass (incomplete/duplicate metadata fails closed;
network-forbidden screen preserves publication bytes). Existing five canonical
URL tests passed after archive export. No new Qobuz calls.

## Completed continuation

4491358 accepted as Probable85 using the existing hash-bound review mechanism.
[DG publisher](https://www.deutschegrammophon.com/en/catalogue/products/beethoven-klavierkonzert-5-michelangeli-3890)
names the artists and televised live Vienna concert, consistent with the cached
LP notes. Different reissue UPCs and unverified digital session date/takes remain
visible. Added six DCML-supported movement inventories (Op.31/3,49/1,49/2,53,78,81a).
Only one published status changes; inventories do not auto-promote any other case.
113script tests pass, browser details/build/UI normalization pass. Next cached
work: Klemperer recording-family sources for the five listed leads.

Klemperer continuation:12004072,24965038 and26149832 accepted Probable85.
Exact publisher2025page identifies stereo cycle; Warner Japan distinguishes
stereo Fifth1959 from mono1955 and supplies1957Symphonies1/8/Coriolan context.
Generic hash-bound reviews retain complete expected movements/current credits;
Coriolan uses an exact hashed single-section binding as in existing overture
reviews.24964822 and26149643 remain withheld because version selection is not
resolved.3285095 remains unpublished pending stronger provenance. Four review
regressions and browser/UI/build checks pass. Total four new Probable releases
this continuation; unique12Found/102Probable/626Unchecked,741copy counts12/102/627.

Further continuation: Op.15/79/90 inventories from QSO/Henle bring the screen
to10complete-work leads/333cached unresolved pairs. Three additional bounded
DG-family Probables:3285095,3672809,7914875.117script tests and UI/build/browser
checks pass. Publication changes only these three in this checkpoint. Discovered
next shared parser issue: Toscanini10757120 has five explicit roman movements
after a comma/catalogue number, which current colon-only parser misses.

## Catalogue-comma movement parser

Toscanini10757120 candidate lbd4bwo8ommnb has five explicit movements written
`Op.68, I.` through`V.`. The parser now accepts a comma followed by a roman
movement marker only when an explicit catalogue number precedes it; bare comma
numbers, joined labels, suffixes and multiple markers remain rejected. Two
regressions cover these negatives, full five-movement coverage and missing
movement/wrong-orchestra failure. The cached screen now has11complete-work pairs
(including previously published cases),332cached unresolved,1,884metadata-needed.
Toscanini remains unpublished pending recording provenance: the third-party
Arturo digital edition says Album of1952; target RCA Victrola booklet/issue does
not independently bind that saved audio to its edition.

Other high-coverage cautions:9769609,9866788,9876728 and7864758 are HMV/EMI
Barenboim LPs. Candidate0002894631272 is the DG cycle already excluded for
9866861. Do not mistake growing movement completeness for matching a recording
cycle. More recording evidence is needed before any promotion, even when
programme titles and pianist agree.15221307 is a Westminster programme against
a later DG Gilels collection; the same caution applies. No general label-alias
or cross-cycle rule has been introduced.

## François checkpoint and next retrieval proposal

8264568 becomes Probable85 after Op.11 inventory and existing hash-bound review.
[Warner](https://www.warnerclassics.com/release/chopin-concertos-francois) names
the target artists; [Warner Japan](https://wmg.jp/samson-francois/discography/23356)
CD33 identifies13–15July1965 Monte-Carlo, distinct from earlier Tzipine.
Copyright1966/1967 on LP is retained without calling it a session date.
Only this accepted status changed;120script tests/UI/build/browser checks pass.
Screen now13complete-work pairs,330cached unresolved,1,884metadata-needed.

`data/qobuz_remaining_metadata_followup_scope.json` is proposed, not fetched:
9unique albums for11release leads. Targets3167056,3290970,6781135,7194998,
11412875,1458083,10175959,5254294 and Katchen6264736/6347314/7291398.
Bound to screen/search/collection hashes. All absent from complete portable and
raw request caches. Excluded obvious programme-number conflicts, BBC-vs-NBC
Toscanini and a later Harnoncourt recording lead. Title similarity is not a
validation rule. Scope requires authorization before retrieval and then the same
pacing, warning stop, resumability and metadata-completeness checks as before.

The closest cached failures now need a new review treatment: Schnabel4352998
Op.54 split Beginning/Conclusion and conflicting G-major label for Op.49/1;
Klemperer6113868/6119375 has a multi-track split fourth movement and scoped
singer/chorus requirements. Keep them unpublished until a new bounded review
is explicitly scoped; do not simply collapse duplicate movement4 markers.
