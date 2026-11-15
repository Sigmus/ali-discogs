# Source-bound credit reviews

15 November 2026, Europe/Amsterdam. AD-008 cached-evidence refinement.
No provider retrieval or bulk collection refresh.

## Solti Sixth5972183 — reviewed Probable

Source Decca SET469-70contains four symphony movements and four Wayfarer songs.
Dettmer is explicitly a liner author. Minton has a source work-level Contralto
credit on the songs; the duplicate unscoped credit must not require her on the
instrumental symphony. Existing candidate is Decca, with eight complete tracks.
BnF cb37850459h identifies exact SET469/470coupling, performers and note authors;
Decca Eloquence documents the song-session/coupling family. Publication-year
observations differ1970/1971; preserved, not treated as precise take dates.

Adopted existing bound-track review with explicit source_credit_reconciliation:
- Exclusively nonperforming credits validated from exact cached source roles;
  raw main artists, principals and work performers cannot be excluded.
- Work-scoped performer requires exact source group/role/target list, never a
  guessed scope. Full expected per-work requirement map is frozen in the review.
- Global conductor/orchestra and other source requirements stay in force. Any
  additional source-scoped instrumental soloists remain required.
- Minton required on each of the four songs; no singer borrowing from symphony
  or another track. Four numbered symphony movements and four numbered songs
  mapped separately despite reversed album order, positive Mahler Composer and
  exact title/ISRC guards. Target/raw/album hashes apply.

Only5972183published record changes to Probable85. Exact pressing/takes/mastering
remain unverified. No global credit removal, performer alias or source rewrite.

## Solti Fifth3386012 — withheld

Source names Clevenger horn solo(sideB) and Herseth trumpet solo(A1); candidate
names neither on any track. Removing Dettmer does not supply these credits.
Orchestra membership and label recording-family similarity cannot substitute for
positive named-soloist evidence. Existing bound-track withhold freezes current gap;
metadata absence is not proof those musicians did not perform. No partial acceptance.

## Validation and next scope

Source-credit regressions cover misplaced Minton scope, attempts to exclude a
principal or omit her required song credit, rehashed wrong singer/orchestra/composer,
missing movement, and Fifth orchestra-present/soloists-absent hold. Existing Casals
copy-only source diagnostic reuses the same strict nonperforming-credit validator.
Additional regression rejects a supposed liner author who has any global or
nested Horn[Solo]credit; source exclusions use the broader explicit musical-role
validator, preserving source-named instrumentalists. Final suite result in project
history; UI normalization/static build pass.

Next cached false-credit case:14766559Fazıl Say, piano technician annotation.
Then remaining Ozawa/Kubelik/other photographer cases; preserve genuine source
credits and explicitly review any false principal-key effects. No refresh/push.


## Fazıl Say14766559 — reviewed Probable

Piano technician Franz Nistl is exclusively a technical credit; source requires
Say alone. Reused existing source-credit reconciliation with no engine change.
Selected12tracks for sonatas8/14/21/23from113track Warner complete set. Work fields
identify each sonata; movement-only titles do not inherit arbitrary nearby works.
Exact work fields/track IDs/ISRCs, ordered three-movement runs, positive Beethoven/
Say credits and source durations(max1second difference) are required.101extra
tracks explicitly excluded. Warner confirms companion double vinyl with this
four-sonata selection and Mozarteum cycle; precise pressing/takes/mastering remain
unknown. Only14766559published record becomes Probable85. Counts12Found/127Probable/
602Unchecked copies(601unique).185script tests, UI normalization/build pass.

Three regressions cover twelve unique selected movements, excluded101tracks,
wrong work/pianist/missing movement/timing after rehash, and real pianist exclusion.
No new title alias, source refresh or provider call. Source year2019versus digital
2020release retained rather than interpreted as recording mismatch.

## Remaining photographer cases — shadow triage

Reproducible `scripts/qobuz_photographer_triage.py` checks five saved cases without
publication writes. Removing only the false photographer names still gives zero
supported programme coverage in all five. Ozawa1638548has multilingual mixed-work
gaps; Kubelik14398300/13708175work titles/context unresolved;29719858has substantial
work-specific cello ensemble requirements;5987607still requires source-named
instrumentalists. Three also have false normalized key-performer names; these
cannot be silently removed by the active reconciliation guard. Metadata/source
fingerprints and per-work diagnostics saved in the triage report.

First triage of9nonperforming-credit cases is complete:2reviewed Probables(Solti6,
Say),1withheld(Solti5),6unresolved(Casals plus5photographer cases). The tenth role
audit item is performer ordering, not a false-credit removal. Next audit explicit
candidate work-field context for Kubelik14398300before designing a bounded rule;
no global alias, loosening source soloists or new retrieval scope authorized.
