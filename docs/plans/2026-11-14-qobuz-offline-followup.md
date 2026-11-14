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
