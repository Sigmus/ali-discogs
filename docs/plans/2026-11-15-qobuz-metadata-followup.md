# Seven-album Qobuz metadata follow-up

Status: approved by user15November2026, Europe/Amsterdam; retrieval complete09:42Amsterdam.
Authorization covers only the fixed seven metadata albums, with warning stops.

Fixed scope: `data/qobuz_metadata_followup_2026_11_15_scope.json`,7distinct albums
for8unchecked release leads,97tracks reported by saved search responses. Pollini/
Brahms, Bernstein/Mendelssohn, Ciccolini/Tchaikovsky–Rachmaninov, Casals/Bach(two
releases), Barenboim/Mozart, Weissenberg/Tchaikovsky and Yepes/Bach. Source/search/
screen/request-archive fingerprints preserved. No selected album/getresponse in
the2497response shared archive. No audio or searches; leads are not matches.

Excluded tempting leads with obvious source mismatches: Cziffra's different
conductors/missing named works, Walter's omitted Wagner extras, Solti versus source
Jochum. Source Casals6628473Suite3/BWV1008 and Barenboim8274997A-minor title versus
A-major K488heading conflicts remain explicit for later review, not silently fixed.

## Ready worker

Offline preparation already passed, immutable manifest under
`.qobuz-poc/metadata-followup-2026-11-15/`. Worker has no network by default:

```sh
uv run --with requests python scripts/qobuz_metadata_followup_2026_11_15.py
```

Only after approval:

```sh
uv run --with requests python scripts/qobuz_metadata_followup_2026_11_15.py --fetch
```

Same existing fail-closed runner:>=15seconds between HTTP attempts,120second
rest per50including discovery/pagination. Full pagination, request cache and
per-album checkpoints. STOP on access/auth/rate/API/network/pagination warning;
no automatic retry/resume. New batch data under its own directory, never restart
or accelerate an existing run. About3–5minutes absent warnings; no hourly monitor
needed for this small batch. A sleep assertion may cover worker lifetime.

Two offline worker tests verify no network by default, fixed scope/manifest and
partial export with duplicate-track STOP. Current7album/8release scope is fixed;
prepare/resume verifies source fingerprints and immutable manifest.

## After successful retrieval

Validate all7IDs/full unique track counts; export sanitized
`data/qobuz_metadata_followup_2026_11_15.json.gz`, shared successful request archive
and canonical URLs. Preserve prior cache members. Integrate complete portable
metadata into offline review, not automatic promotions; compare source programmes,
credits and recording families. Keep source conflicts/unknowns explicit. Then
regressions, publication diff, UI/build and docs. No automatic push/deployment.


## Completion and offline triage — 15 November

All7albums/97tracks completed09:40–09:42Amsterdam,9HTTP attempts including
bootstrap/discovery, no warnings. Full album IDs, counts and unique track IDs
validated. Portable export saved; shared cache2504responses, all2497prior members
byte-preserved. Canonical index1164URLs, exported offline. Sleep assertion ended
with worker. No searches/audio, retry or automatic promotions.

Refreshed2227pair screen:15recording-review leads,1851metadata-needed,
352unresolved,9source-programme-held. Inventory606unchecked unique:
425work/credit,160metadata,1recording review,7withheld,6completeness,
6empty searches,1source hold. Metadata also resolved cached alternatives outside
the eight selected source relationships; categories are triage, not acceptance.

Next: recording review for Weissenberg1662708 (all3movements plus matching named
performer/conductor/orchestra). Other selected relationships retain inventory,
credit or source-identity gaps; Casals/BWV and Barenboim source conflicts remain.
New metadata is available to offline screen/inventory, not added to publication
review inputs until a justified recording review. Match labels unchanged.
All160script tests pass. An initial offline screen used the incomplete base venv;
reran successfully with the documented requests-enabled uv environment. No API
error or warning occurred. No push/deployment.


## Weissenberg review and remaining-lead audit

15November: reviewed source1662708 and saved album5099960276551. All three
Op.23movements positively credit Weissenberg/Karajan/Orchestre de Paris. Warner
Japan33813documents the Paris family (February1970), distinct from Berlin's
filmed performance; its2026remaster is not the saved2010edition. LP has no dates
or timings. Explicit review supports Probable85family, never exact pressing/takes/
mastering. Target/album hashes and ordered complete movements gate publication.
No source metadata overwritten. Only1662708published record changes; total
12Found/123Probable/606Unchecked copies (605unchecked unique).

Integrated complete scope-bound seven-album portable evidence into reviewed
matcher inputs. Two regressions reject missing movement and Berlin substitution,
even after updating candidate hashes.162script tests, UI normalization/static
build pass. No Qobuz calls, push or deployment.

Saved eight-relationship audit with evidence fingerprints. Pollini lacks required
individual quartet names; Barenboim lacks orchestra credit; Casals has source BWV
conflict/generic suite headings; Ciccolini has multilingual work/composer grouping
gaps; Yepes has spaced BWV1006a plus completeness gaps. Bernstein's composer
Mendelssohn-Bartholdy versus Mendelssohn is the next bounded reusable identity
review, with no automatic completeness/recording acceptance. No credit borrowing.


## Bernstein recording review; Gieseking follow-on audit

15November: official Bernstein discography page30identifies both Mendelssohn
symphonies with Israel Philharmonic/DG,23October1978TelAviv and exact2531097LP
catalogue. Cached source2531 097says concert recording; both works have four
explicit source movements, all8files have matching conductor/orchestra andLive.
Source/file timing differences0–8seconds, within existing max5seconds/3%guard.
Source/official discography call No5D-major, file saysD-minor; preserve discrepancy
without global alias. Hash-bound bound-track review requires exact8IDs, ordered
movements,Live/ISRC markers, source timings and positive credits. Probable85only;
exact pressing/takes/mastering unknown. Only3956949publication changes.

166tests pass including missing movement, wrong orchestra/conductor, changedLive,
ISRC and timing controls after candidate rehash. UI normalization/build pass.
Structured Bernstein timing/source audit saved. No provider calls/push/deployment.

Continued to8962178Gieseking:17of17opus/member pieces in source order, credited
pianist; eighteenth target is unnumbered Lieder Ohne Worte container. Warner
corroborates late1956family but also earlier/alternative Spinning Song takes.
BNF transfer lacks dates/version markers,1958release date is not a session date.
Keep Unchecked; structured programme audit records unresolved transfer/take. Do not
borrow Warner's identity for this third-party transfer. Next cached Yepes2857544
spaced BWV1006a and complete suite programme review.


## Yepes2857544 — missing movement hidden by equal counts

Cached source is an Archiv2708 030baroque-lute set, Madrid1972/1973. Digital
0002894457132has six BWV1006a tracks but they are I,II,III,IV,IV,V: Menuets
split across two tracks, final VI Gigue absent. Source has one combined Menuet
band and a final Gigue. Both complete albums total27tracks; equal counts hide the
gap. Several digital titles explicitly say guitar arrangements, whereas source
credits baroque lute. Arrangement metadata may itself be wrong, so this is an
unresolved instrument/session issue, not a claim to have identified different audio.

Hash-bound existing bound-track withhold records source/target/album identities,
current unmatched suite and six unused candidate tracks. No generic spelling fix,
source rewrite, added movement or new review kind. Shadow suffix correction gives
7/7work coverage but cannot supply final Gigue; six-movement inventory regression
rejects observed1,2,3,4,4,5. Known complete-source programme and instrument/recording
checks are independent of work similarity or whole-album track counts. Structured
source/candidate audit saved. Keep Unchecked; new metadata/search scope not started.


## Ciccolini2236260 — source-side and recording-family review

15November: LP source explicitly credits Tchaikovsky toA and Rachmaninoff toB;
each side has three movement labels. Warner's Ciccolini discography CD4(PDF
pages2–3) identifies Silvestri/French National Orchestra and1957SalleWagram
sessions; CD3separately identifies Cluytens/Conservatoire1951. Visually inspected
and saved source pages with hashes. All six candidate timings match CD4exactly.

Existing bound-track review maps each source side to its numbered concerto,
requiring complete distinct three-movement runs, all named performers, exact
ISRCs and reference timings. Added optional positive Composer-role mark to existing
validator so rehashed mixed-composer substitutions cannot pass. No global French
key/title/composer alias or raw/normalized source rewrite. Candidate remains a
third-party VinyleNumerique2023transfer, not authenticated Warner mastering.
Publisher's B-flat-major text differs from source B-flat-minor; preserve discrepancy.
Probable85recording family only; exact LP pressing/takes/mono-stereo unverified.

Two regressions exercise full two-concerto accounting and wrong composer/role,
Cluytens/orchestra substitution, missing movement, timing andISRC changes even
after candidate rehash. No provider retrieval calls or push/deployment.


Final170script tests pass against stable regenerated publication; shared binding
fixture includes the seven-album metadata archive. UI normalization/build pass.
Only2236260release changes; labels12Found/125Probable/604Unchecked copies.


## Casals6628473 source reconciliation and role-parser audit

Original Angel COLH17side1label visibly prints Suite3CmajorBWV1009, November1936;
side2prints Suite4EflatBWV1010, June1939. Saved browser screenshots/provenance.
Cached/live Discogs text incorrectly says1008forSuite3. Exact correction proposal
is source/target/hash-bound in qobuz_casals_source_audit.json, not activated and
not an upstream edit. No global1008/1009equivalence. Original download failed;
browser screenshot evidence is explicitly identified as a capture, not raw image.

Second blocker: normalized performer Guglielmo Barblan is actually a liner-note
author. Instrument word Violoncello appears only inside the note-title annotation.
Model role parsing now excludes bracketed annotation text before deciding roles;
keeps previously recognized genuine Vocals[Soprano]/AltoVocals[Choir] performers.
Audit compares old/new builders against740saved details using synthetic basic
information:9releases lose nonperforming credits,1has a violinist/conductor order
change. This is diagnostic, not a full refresh or count of accepted matches.
No saved collection, Spotify result or existing evidence hash overwritten.

Shadow Casals correction + removal of liner author gives full work support, but
Nar Classical2022candidate has no session/take markers. Do not borrow1930srecording
identity from source/programme alone. Remains Unchecked. Next apply evidence only
inside a bounded source-aware Qobuz review, validate complete suites/recording
provenance, then23950082suite context. No new provider retrieval authorized.


## Casals source-bound diagnostics completed

Offline reconciliation validates exact target/raw/label hashes, source image URLs,
original title existence and exclusively nonperforming credit evidence. Principal
or work-level performers cannot be removed. It returns a copy only; no normalized
source/publication integration. Suite3catalogue correction plus liner-author
removal supports6+6movements for6628473. Flat source23950082is bounded by explicit
Suite5/6headers, six numbered bands on each distinct side; candidate matches12
separate BWV1011/1012movements. Positive Bach Composer and Casals credits required,
movement names/ordinals agree, no catalogue borrowing between suites.

Four regressions cover stale/missing proofs, invalid credit exclusion, absent or
cross-side/reordered source movements, no network/publication writes. Both LPs
remain Unchecked: Nar Classical2022transfer has no session/take markers. Diagnostic
success is programme support, not a calibrated score or recording-family decision.
Eight-release follow-up now reviewed:3Probable,1withheld,4unresolved. No more
provider calls. Next cached Solti5972183/3386012false-role cases, using source-bound
evidence without a bulk collection refresh. Full final suite result in history.
