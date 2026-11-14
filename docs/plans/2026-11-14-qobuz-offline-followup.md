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

## Nine-album batch authorized

User said “do it” after the9album/11release proposal. Fixed entries stay unchanged
so scope/search/collection fingerprints remain valid. Worker
`uv run --with requests python scripts/qobuz_remaining_followup.py --fetch`;
state `.qobuz-poc/remaining-followup-2026-11-14/` with immutable manifest, per-album
outputs, progress.json, run.log and STOP. Same15second pacing/120second rest per50
HTTP requests, complete pagination and no warning retry. Export sanitized
`data/qobuz_remaining_followup_metadata.json.gz`; no audio or automatic matches.
After completion: validate all9albums/fullunique tracks, export shared request
archive/canonical URLs, screen11target relationships offline, then audit within
existing review types. No further scope expansion/push/deploy.

## Nine-album batch complete and audited

Finished14November18:36Amsterdam:9/9albums,216tracks,11HTTP attempts including
discovery; no warnings. All manifest IDs/counts/unique tracks validated. Shared
archive2,497responses, prior2,488members byte-preserved;1,157canonical URLs.
No monitor needed; worker/sleep assertion ended normally.

Audit script/report:`qobuz_remaining_followup_audit.py` and corresponding data
JSON, all11target relationships. Lipatti7194998 Probable85:14waltzes in LP order,
explicit posthumous tokens source-bound,3extra pieces excluded; Warner1950Geneva
recording/production support. Kreisler10175959 Probable85:3Brahms movements,
Barbirolli/London Philharmonic; exact third-party transfer unverified.

Remaining9leads withheld: Nabucco track-credit/part headings, individual cellist
credits, Kid Ory four-versus16 programme, Nielsen duplicate Allegro position,
Gould nested BWV programme, Mozart credits/catalogue and3Katchen programme gaps.
No discarded required performers or invented metadata. Existing bound-track
review used for Lipatti; new source-bound types are not silently introduced.

Brahms Op.77 inventory also changes historical baseline audit4226783 from
unresolved to structurally supported; original66labels and v1scores unchanged.
Saved audit now8supported/57unresolved/1insufficient-credit.125script tests pass,
UI normalization/build/browser details pass. Publication diff exactly2new
Probables. Global unmatched inventory now uses all new archives:620unique
unchecked =422work/credit +170metadata-needed +12completeness +7withheld
+6no-hits +3recording-review. Broader retrieval remains unscoped.

## Nielsen position audit

Continued offline after user request. `scripts/qobuz_position_audit.py` writes
`data/qobuz_position_audit.json`: exact target11412875 / albumv96ulyegxutlc,
Aa/Ab/Ba/Bb map to four distinct I/II/III/IV track IDs. Each explicitly names
Op.29, Nielsen, Barbirolli and Hallé. This is structural evidence, not a new
recording-identity finding or publication promotion. Existing title-keyed review
dictionaries cannot distinguish the two source Allegro entries safely.

Diagnostic rejects reordered/missing/duplicate tracks, wrong opus or artist and
changed side positions;3regression tests pass. No catalogue calls or labels changed.
Proposed next bounded implementation: position-keyed review entries containing
source position+title, exact track IDs/hashes, required artists, explicit ordered
movement inventory, target/album/source hashes and recording-family evidence.
Keep generic title matching unchanged; reject duplicate source positions, reused
tracks, changed source data and silent ordinal pairing. Requires a new review
kind, so publication implementation remains outside this continuation.

## Nielsen position review implemented

User authorized continuation of the scoped implementation. New `position-bound`
review delegates to the frozen Nielsen diagnostic and checks raw source SHA,
complete ordered mapping/track hashes and unchanged required artists. It publishes
position-qualified target names, so Aa Allegro and Bb Allegro remain separate.
No generic ordinal matching or other target scope is enabled.

[Warner](https://www.warnerclassics.com/release/nielsen-4-barbirolli) independently
identifies the work, Barbirolli and Hallé. Cached digital original-release1963 is
consistent with source LP notes, supporting Probable85, not exact take/mastering
identity. Only11412875 changes status.129script tests pass (including4positional
regressions), UI normalization and static build pass. The initial bare-venv full
suite lacked requests; rerun with the documented uv dependency environment passed.
No Qobuz API calls, push or deployment. Diagnostic report remains the pre-publication
structural checkpoint; the current review ledger/publication supersede its hold.

## Autonomous cached-evidence continuation and Gould review

User explicitly requested committing verified improvements and continuing to the
next cached candidate without routine confirmation. This authorizes scoped offline
review treatments as needed; new retrieval, warning retries and pushes remain
outside scope. Retain fail-closed hashes, complete programme and artist checks.

Gould1458083: the raw source has15nested LP bands, each naming an Invention and
Sinfonia BWV pair. Saved Sony0886444299039 has30tracks in the same distinctive
order. Official Gould discography independently lists all30 in that order and
identifies the1964release. New frozen `nested-bwv-pairs` review validates raw source
hash, nested children, track hashes, exact paired numbers/keys, complete772–801
inventory and Gould/Bach credits. No global flattening or inferred missing works.
Three regression tests reject wrong BWV/pianist, missing/swapped tracks and stale
source binding. Exact takes/mastering remain unverified; publication is Probable85.
Next cached lead: Katchen’s bare movement titles have explicit saved `work` fields;
inspect a reusable guarded work-field context rule before considering publication.

## Katchen work-field and bounded programme reviews

Continued autonomously through the next cached leads. Diagnostic
`qobuz_work_field_audit.py` exposes explicit saved `work` fields on bare sonata
movements: work support becomes100% for6264736/7291398, but independent generic
completeness remains unknown. No global work-context matching rule was enabled.
The diagnostic is structural pre-review evidence, not current publication status.

Existing bound-track review extended with optional exact `work_equals` and
numbered movement-run checks.6264736 has all five Op.5 movements plus Op.4;
7291398 has all four movements of each Op.1/2, retaining source bands combining
movements2/3. Each has exact source/album hashes, explicit work-field bindings,
Katchen credits and compilation extras excluded.

6347314 has two explicit waltz ranges1–8/9–16, both Op.79Rhapsodies and four
Op.10Ballades. Source-bound exceptions require identical opus plus explicit named
Rhapsody number, or Op.10Ballades members1–4; they do not alias other opus works.
Henle corroborates16solo waltzes and four Ballades. Decca Eloquence documents the
stereo solo cycle,1964Third Sonata and1964Rhapsodies distinct from earlier
versions; saved Op.5/No.2Rhapsody version markers agree. Exact LP takes/mastering
remain unverified. New reviews use Probable85 only, never Found.

Four Katchen regressions plus two diagnostic regressions cover changed work field,
missing movements, wrong pianist, wrong opus/piece number and preservation of the
source. No Qobuz catalogue calls. Next cached case: Mozart5254294, where missing
named artists/catalogue ambiguity remain; do not inherit album credits silently.


Mozart checkpoint: saved target work-scoped requirements include named bassoon,
oboe, horn and basset-horn players (including a retained Ronald Waller requirement).
Digital files name London Wind Soloists/Brymer, not those individuals. Matching
ensemble names cannot substitute for that evidence. KA.226 is also unresolved;
no catalogue alias introduced. Keep5254294unchecked. Next audit Nabucco saved
part headings and track roles before proposing any review treatment.


## Nabucco cached audit

Continued after Katchen commit: `data/qobuz_nabucco_followup_audit.json` binds raw
source/normalized target/album hashes. Source3167056 contains11played bands and
4part headings; candidate0002894133212 has11tracks. Every saved track lacks
explicit Sinopoli and Berlin orchestra/chorus credits. Scene-specific singers
also invalidate a naive every-singer-on-every-track requirement. No label changed.
Next: primary publisher recording/cast/ensemble evidence, then a bounded source-role
and part-heading treatment. No generic credit inheritance, deletion of named
artists, new retrieval or unsupported recording-family claim.


## Nabucco publisher research and Klemperer split finale

DG’s Nabucco reissue page and Sinopoli obituary independently identify the cast,
conductor and Berlin chorus/orchestra. These support the recording family but
concern the complete opera, not the saved11track highlights edition. Existing
strict opera adapter requires track ensemble/conductor evidence. No external
ensemble-inheritance policy adopted; Nabucco stays unchecked. Audit report updated.

Continued to cached Klemperer6113868/6119375. New frozen `source-split-finale`
review binds exact source programmes/album/track hashes and ten selected IDs:
Ninth movementsI/II/III plusIV(a)–(e), Leonore3 and König Stephan. Requires
Klemperer/Philharmonia and Beethoven on every selected track; all four named
soloists and chorus remain positively required within the sung finale. Never
require singers on instrumental movements, or borrow album-level missing credits.

Warner documents the Philharmonia cycle; chorus archive documents the cast but
also its live performances, so cast agreement is explicitly not exact session
proof. LeonoreNo.3 printed72a versus saved72b is bound by the named overture,
not globally aliased (primary cataloguing conventions differ). Last finale track
mislabels Hotter Contralto, while an earlier section says Bass; discrepancy stays
visible. French LP prints König Stephan14:42 versus saved8:09; unresolved duration
retained. Recording-family Probable85 only; exact LP pressing/takes/mastering not
claimed. Four regressions reject missing/reordered/repeated finale sections,
missing named voice/chorus or wrong conductor/orchestra, stale source and hidden
voice discrepancy. No Qobuz requests or automatic push/deployment.


## Schnabel source-side partition

Continued after Klemperer commit to4352998, the three-LP sonatas18–27volume.
Existing bound-track review suffices: exact exclusions partition duplicate Op.54
Beginning/Conclusion matches into movementI on C3 andII on D1; neither track is
reused. All26digital movements across ten sonatas remain accounted for, including
source bands joining Waldstein/Les Adieux movements. Numbered movement-run checks
retain each ordered inventory; pianist remains required on every selected track.

Warner identifies the exact saved digital barcode190295866983 and2016shellac
remaster. Henle independently identifies Op.49No.1 as G minor; source G Major
text remains unchanged, explicitly disclosed. This is a reviewed source-label
conflict, not a global key equivalence or interchange with Op.49No.2. Cycle date
ranges differ across references; no precise session date is inferred. Probable85
recording family, no exact LP transfer/take/mastering claim. Three regressions
cover side disjointness, missing conclusion, wrong pianist and movement order.


## Further Katchen source discrepancies

After Schnabel publication, audited6265501/8836514/1697514against the saved77track
album; hash-bound checkpoint `data/qobuz_katchen_source_audit.json`. No promotions.
6265501has13group correspondences, but source Op.119third piece says G versus
candidate C Major. Group counts/opus/pianist do not resolve that key conflict.
8836514’s six Op.116bands may include a joined B4: its source text repeats
Intermezzo In E / Intermezzo In E Minor. Earlier omission wording was provisional;
this is ambiguous band grouping, not proof a work is absent.1697514Paganini files
say1965Recording versus Decca narrative1966; multiple recordings require review.
Next: independent Henle/source-image check of6265501 Op.119No.3, preserving raw
text and recording-family limits. No API expansion or automatic source correction.


## Remaining Katchen discrepancies resolved by bounded source evidence

6265501: DG independently identifies Op.119No.3 in C major. Source G wording
stays explicit; all13Op.117/119/118pieces bound. Discography entry1199corroborates
June1962sessions and Vol.1April1964issue, not a guessed session from copyright.

8836514: inspected original side2label photograph, which prints two Intermezzi
on band4. Bärenreiter corroborates Op.116pieces4/5(E major/E minor), then6/7.
B4maps to4/5; B5to6; B6to7. Thus six bands cover seven pieces. All8Op.76and
7Op.116pieces retained. Saved photo SHA is checked; joined-band mapping must
cover every raw source position and numbered piece without omission/reuse.

1697514: visually inspected CHARM-hosted Decca discography entry1199(page103)
and1379(pages151–152). They link HandelJune1962/PaganiniSeptember1965to Vol.7,
issuedApril1966. This distinguishes session and issue dates, resolving the earlier
1965/1966conflict. Candidate1965version markers and ISRCs now guarded against
substitution; both Paganini books remain required.

Selected source images, provenance and hashes saved under `data/review_sources/`;
no original504page PDF/audio/credentials committed. Source audit updated with
initial holds and subsequent decisions. All3are Probable85recording-family leads;
exact LP pressing/takes/mastering remain unverified. Existing bound-track policy
extended only with optional external-evidence hashes, complete source-band
mapping and version/ISRC guards. No global key alias, generic band splitting,
credit borrowing or provider calls.


## Toscanini RCA family review

Continued after Katchen commit to10757120/cachedlbd4bwo8ommnb. Inspected and
saved source RCA sleeve: Carnegie Hall14January1952. Pristine’s documented
reissue of the official RCA recording gives the same date and five movement
timings; candidate differences9/4/1/2/13seconds, allwithin3%. Exact transfer remains
unknown: third-party Arturo label and Albumof1952are not authenticated RCA audio.

Bound review requires all5movements, Toscanini/NBC on each, source/album/photo
hashes, year/version marker and exact ISRCs. Timing is a guard/corroboration, never
identity proof. Numbered-run checks now reuse the existing stricter movement
parser, including catalogue-qualified comma Roman labels; no bare-comma ordinal
inference. Two regressions cover changed year/timing/orchestra and photo hash.
Review retains third-party mastering and source Stereo-tag limitations. Probable85
family only, not Found. Structured timing/source audit saved; no Qobuz calls.


## Two remaining Klemperer stereo-family holds reviewed

Inspected/saved original labels for24964822/26149643. They explicitly saySTEREO
and carry1959/1961label years. This is new source evidence beyond the normalized
format/name/title fields that previously left version selection unresolved.
Warner's selected compilation identifies the stereo cycle; Warner Japan16393
independently dates the Seventh studio sessions to October–December1960.

Existing bound-track reviews retain Symphony2four movements plus Leonore2 and
Prometheus, and Symphony7four movements plus Consecration. Positive conductor/
orchestra on every selected track, exact title/ISRC marks, source/album/label-photo
hashes and ordered inventories. No mono/live/later orchestra substitution.
Symphony2finale source6:57 versus candidate7:11 differs14seconds (~3.4%): retained
as a discrepancy; timing is not an identity test here and no guard was relaxed.
Other source timings are close. Label years are not claimed to be session dates;
exact takes/LP pressing/mastering remain unverified. Both reviews Probable85 only.

Updated former-hold regression to require saved positive stereo evidence; two
new regressions reject changed label hashes, later orchestra and missing overture.
Source-note/timing audit saved in `data/qobuz_klemperer_stereo_audit.json`. No
Qobuz calls, source-format overwrite, push or deployment.


## 15 November — source-bound work-composer safeguard

After committing Klemperer, continued through remaining cached completeness
leads. Gilels15221307raw A1–A4credit Beethoven; B1credits Medtner. Normalized
composer list is empty. Beethoven-only box0002894776360had false100%work support
because its BeethovenOp.22was allowed to cover MedtnerOp.22. Completeness already
blocked publication, so no incorrect accepted label needed demotion.

Added reusable manual source-scope ledger/validator and narrow grouped-matcher
Composer check. Full target/source hashes, all source positions/titles and artist
IDs/names must agree. No automatic interpretation of arbitrary track artists as
composers, role inference, global spelling aliases or normalized-data rewrite.
Publisher Boosey independently identifies Medtner's G-minor Op.22. Legacy scoring
unchanged; scoped grouped support drops5/5to4/5, Medtner gets no Beethoven tracks.
Matcher version/provenance updated, all published release records unchanged.

Offline audit discovers2empty-normalized-composer source-attribution candidates:
reviewed Gilels and unreviewed Rubinstein7971104. Discovery is heuristic and may
miss names; all raw attributions retained. Three regressions cover cross-composer
opus collisions, stale/incomplete/changed source scopes and positive Composer
requirements.156script tests, UI normalization/build pass. Next review Rubinstein
scope against its cached source, then audit candidate impact before any acceptance.
