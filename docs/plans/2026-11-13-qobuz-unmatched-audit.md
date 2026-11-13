# Remaining Qobuz releases: offline triage

13November2026, Europe/Amsterdam. User authorized merge/deployment followed by
work on unmatched albums. PR3 merged as8afd7dd after PR CI passed; main test and
Pages runs43469716247/43469716318 succeeded. Deployed qobuz_matches asset verified
byte-identical to merged main. Live copies12Found/73Probable/656Unchecked.

New work branch: `codex/qobuz-unmatched-audit`. Reproduce without catalogue calls:
`uv run python scripts/qobuz_unmatched_audit.py`.

The report `data/qobuz_unmatched_audit.json` combines saved original, comparison,
round2 and query-trial hits, reuses full metadata from all those archives, and
recomputes work/credit/completeness evidence for every remaining unique release.
Previously rejected target/candidate pairs are excluded from usable leads.
No new query, metadata fetch, acceptance or score/threshold change.

655unique unmatched releases:

- 324 have no hits in the included saved searches.
- 14 have saved hits but no complete metadata among those hits.
- 316 have cached metadata but unresolved work/credit evidence (including the
  known rejected Barenboim recording, which is explicitly flagged).
- 1 has programme/credit support but incomplete completeness evidence:
  Barenboim9866861 vs DG0002894631272. Similar EMI/DG cycle conflicts already
  disqualified another target, so this is a caution lead, not an automatic match.

These categories prioritize cached evidence and are not catalogue-absence claims.
Some releases also have uncached alternatives. No candidate currently passes all
checks and only needs recording verification. Next action: inspect the14metadata-
needed targets and choose a small programme/artist-aligned scope; independently
investigate recurring credit/heading failures before changing general matching.


## Four-album metadata batch completed

User reiterated authorization to continue without routine confirmation. Fixed
`data/qobuz_unmatched_metadata_scope.json` selects Tristan2996680, Tannhauser4365080,
Nevsky8970069 and Karajan10738828 from saved programme/artist-aligned hits.
`scripts/qobuz_unmatched_metadata.py --fetch` uses serial15-second pacing and
existing checkpoint/STOP/error guards. Completed29+27+12+9=77tracks without
warnings; complete counts/IDs verified, portable whitelisted metadata saved.
No audio or automatic retries. Offline audit is reproducible with
`uv run python scripts/qobuz_unmatched_metadata_audit.py`.

Findings:
- Previn candidate has Los Angeles Philharmonic, target requires London Symphony:
  wrong recording candidate, no promotion despite same conductor/work.
- Tristan needs multilingual ensemble/cast and opera-context interpretation.
- Tannhauser needs Dresden-version and cast checks; target/candidate contain
  different additional singer names. Do not silently equate casts.
- Karajan source flattens musical heading/group/tempo labels into13targetunits;
  actual advertised programme is Romeo/Juliet plus NutcrackerSuite. Suite heading
  combines Op71a/Op71. A bounded hierarchy/catalogue interpretation is needed;
  no global relaxation or match promotion in this step.

Audit now includes the formerly omitted corrected-query validation archive,
including Coltrane's actual A Love Supreme hits. Current655unique triage:
324nohits/10metadata-needed/320work-credit-unresolved/1completeness-needed.
No changes to accepted matches. Prior14metadata-needed is superseded by this
fetch and broader evidence inventory, not catalogue absence inference.
Request cache/canonical index exported for collaboration. Next implementation
priority: source-bound Karajan hierarchy and opus interpretation with regression
checks; then positive cast/ensemble evidence, preserving the wrong-orchestra veto.


## Bounded Karajan hierarchy review

User authorized continued implementation. `target_unit_groups` in source-bound
review partitions every original target unit, in original order, into exactly two
canonical works. Missing/duplicate/unassigned source labels fail closed; target
fingerprint binds all original labels. Original displayed work titles and credit
lookup keys remain. This leaves general `units()` parsing unchanged.

Karajan10738828/0002894390212 has Romeo/Juliet and all8NutcrackerSuite sections
with required conductor/orchestra. DG catalogue3321 documents the exact candidate
barcode/pairing; cached target1983DG2532096/2561408 and candidate1983 provenance
support the recording family. Exact takes/mastering remain unverified, with
LP/digital timing differences explicitly noted. Approved Probable85, not Found.
Portable review `data/qobuz_unmatched_recording_reviews.json` plus full four-album
metadata are required matcher inputs. No further catalogue calls.

Regression removes each of9candidate tracks and one source label: all withhold
or reject incomplete evidence even after an album hash update.81script tests pass,
Node normalization and build pass. Only Karajan changes relative deployed main;
local copies12Found/74Probable/655Unchecked, unique12/74/654. No push/deploy.


## Raw-source opera cast audit

Reproducible offline `uv run python scripts/qobuz_opera_cast_audit.py` preserves
source-role mappings, source hashes and exact normalized candidate-name presence
in `data/qobuz_opera_cast_audit.json`. No changes to publication.

Tristan's named singers and chorus master occur in candidate metadata. Orchestra
uses BayreutherFestspielorchester rather than OrchesterDerBayreutherFestspiele;
chorus's exact name key is absent. Do not equate either automatically or claim
complete scene-level coverage from album-level presence.

Tannhauser's ReinerSuss/RudolfGonszar are present in the raw target credits too:
the earlier concern about additional candidate singers is superseded. KarlSchmidt
is target ChorusMaster versus candidate Director. Four target boy-page singers
(ArnoldSchremm,KarlHeinzVoortmann,ManfredKoop,MichaelWein) lack exact candidate name
keys. Target orchestra's leading Das also differs. No wrong-cast conclusion from
these missing/variant names. Production target normalization omits some raw bass/
treble actors, so passing its existing subset would not independently verify cast.

Do not promote either opera yet. Next useful shared improvement: explicitly
source recording roles and ensemble aliases, with scene/act completeness checks;
never silently remove uncredited secondary artists to obtain a match.


## Source-role and act review

Implemented offline in `scripts/qobuz_opera_review.py`. Ensemble names differ
only with a recording-specific reason. Chorus master is not director. Every
musical Discogs credit must stay in the review. Candidate track IDs are bound.

Tristan2996680 / 0002894497722 is Probable85. Acts I–III cover all 29 tracks
(7/11/11). Bayreuther Festspielorchester and Festspielchor are the reviewed
names for Orchester/Chor der Bayreuther Festspiele. Wilhelm Pitz is ChorusMaster.
Ludwig, Nienstedt and Heater keep explicit voice-type conflicts. Side J, the
Böhm rehearsal, is absent and stated as an edition gap. Scenes are not aligned
because the candidate uses libretto incipits. Canonical route verified in the
browser: `https://www.qobuz.com/fr-fr/album/wagner-tristan-und-isolde-orchester-der-bayreuther-festspiele-karl-bohm/0002894497722`.

Tannhäuser4365080 stays ineligible. Blockers: Act III scene 2 unlabelled;
Orchester der Deutschen Oper Berlin on a joined credit; Karl Schmidt is Director;
Arnold Schremm, Karl-Heinz Voortmann, Manfred Koop and Michael Wein are absent.
The leading "Das" on the Staatsoper orchestra is an explicit alias and does not
override those blockers. Published copies are now 12 Found / 75 Probable /
654 Unchecked. No new API calls.

## Gould pairs and the Barenboim caution

The strongest remaining cached lead, Barenboim9866861, is La Voce del Padrone
3C063-02000 from the EMI sonata cycle. Its three sonatas also occur on DG
0002894631272, the later Paris cycle already rejected for another Barenboim
target. Same pianist and works are not the same recording, so this pair stays
unpublished.

Gould2175684, CBS Masterworks 77427 with a 1975 phonographic copyright, matches
Sony Classical 0886443628625. All 96 tracks are used once: prelude and fugue for
BWV 846–893, Gould on every track. Three preludes omit their BWV and are bound
to the next fugue. The two volume headings and the overall BWV range heading are
containers. Probable85. Copies were 12/76/653. Canonical route:
`https://www.qobuz.com/fr-fr/album/glenn-gould-plays-bach-the-well-tempered-clavier-books-i-ii-bwv-846-893-glenn-gould/0886443628625`.

## Michelangeli headings

Michelangeli6678433, DG 2530 236 (1972 LP), matches DG `uoihym7lfe48a`, released
2018-09-28, UPC 0028948361939. The source heading Mazurkas matches no track. The
other 13 units each match one track and those 13 tracks are the whole album:
Op. 67/2, 56/2, 67/4, 68/2, 68/1, 33/1, 30/3, 30/2, 33/4, 68/4, Prelude Op. 45,
Ballade Op. 23, Scherzo Op. 31. Michelangeli is credited on every track. German
B-moll for the scherzo is B-flat minor and was already matched by opus. A
numbered work cannot be reclassified as a container; dropping a piece or the
pianist fails the review. Probable85. The 2018 file is not verified as the 1972
mastering. Copies 12/77/652, unique 12/77/651. Canonical route:
`https://www.qobuz.com/fr-fr/album/chopin-10-mazurkas-arturo-benedetti-michelangeli/uoihym7lfe48a`.


### 2026-11-13 — Tristan chat-link404 correction

The assistant supplied a guessed/shortened nl-en slug; saved canonical route was
already correct. Opened exact saved fr-fr route in browser and verified album
page/29tracks. Resolver now prefers canonical index over plausible supplied URL;
--album-id prints safe links offline. Regression for reported slug passes; all
publication Qobuz links match index. AGENTS requires exact resolver use in chat
as well as code/docs. Five URL tests pass. No commit/push requested.

## Inventory after the eight-album pass

13 November 2026, Europe/Amsterdam. Rebuilt with
`PYTHONPATH=scripts uv run python scripts/qobuz_unmatched_audit.py` after
`d0afc9a`. No new searches, metadata fetches, or publication changes. Recorded
withholds are a separate category.

645 unique unchecked releases:

- 324 have no hits in the included saved searches.
- 10 have saved hits and no cached album among those hits.
- 306 have cached metadata whose work or credit evidence is unresolved.
- 4 are recorded withholds: Tannhäuser4365080, Haebler4641786, Time Out2383925,
  and Saint-Saëns10102576. They stay unmatched.
- 1 has programme support and unknown completeness: Barenboim9866861 versus
  DG 0002894631272. That is the later Paris cycle already kept unpublished.

The 10 metadata-needed releases are A Love Supreme594243, Rachmaninoff4469662,
St Matthew Passion5140330, Schütz6091545, Shostakovich6105272, Bach cantatas
6465567, Bach three-piano concertos6907296, Bach cantatas7975379, Duparc9850479,
and Chopin12419639. Every saved hit for those ten is still uncached. Fetching
them is a new scope.

## Seven album files fetched

13 November 2026, Europe/Amsterdam. User continued into the metadata-needed
scope. `scripts/qobuz_metadata_needed.py --fetch` retrieved seven fixed albums
at the existing 15-second pace. 410 tracks passed the complete-count and unique-ID
checks. Archive: `data/qobuz_metadata_needed.json.gz`. No searches and no
promotion.

| Discogs | Album | Result |
|---|---|---|
| 594243 | `0060253742084`, 4 tracks | All four parts of A Love Supreme. Pursuance plus Psalm is 17:44 against the LP’s joined 17:40. McCoy Tyner is absent from every credit string. |
| 4469662 | `0002894667272`, 7 tracks | Concertos Nos. 2 and 4 plus a two-piano rhapsody. Etudes-Tableaux, Op. 39, is absent. |
| 6105272 | `g4nhgjv3d6wbc`, 75 tracks | Quartets 1–15 and the piano quintet are in the work field, with extra pieces. Credits name a later Borodin lineup, not Valentin Berlinsky or the Beethoven Quartet. |
| 6465567 | `0002894637012`, 222 tracks | The file is the St Matthew Passion, not the Advent, Christmas and Easter cantatas. |
| 6907296 | `0886446492919`, 10 tracks | Italian Concerto and Chromatic Fantasy movements. The three-piano concertos are absent. |
| 7975379 | `a6g9640whj71a`, 87 tracks | Cantatas without BWV 149 or BWV 188. |
| 9850479 | `3614590915896`, 5 tracks | Two Duparc songs, *Chanson triste* and *L’invitation au voyage*. Ten named songs are absent. |

Not fetched: 5140330, because the Lehmann hits are the Christmas Oratorio and
sacred cantatas; 6091545, because the Ehmann hits are other Schütz collections;
12419639, because the Rigutto hits are nocturnes and waltzes and the concerto
hit is conducted by Erich Bergel. Inventory after including the archive:
324/3/313/4/1.
