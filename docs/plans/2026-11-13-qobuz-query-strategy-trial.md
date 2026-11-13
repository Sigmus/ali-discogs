# Qobuz query strategy trial

2026-11-13, Europe/Amsterdam. User authorized committing round2 and continuing
with the recommended cached Richter audit and bounded query improvement.
Round2 committed as `877bc5a`; this follow-up is separate, with no push/deploy.

## Cached Richter audit

Portable review: `data/qobuz_richter_review.json`. Warner's own catalogue
<https://wmg.jp/richter/discography/33795> identifies Richter/Maazel, Bartok
No.2 Sz95 with Orchestre de Paris (28–31 October/3 November1969), and Prokofiev
No.5 Op55 in G major with London Symphony Orchestra (16–17 June1970).
This resolves the target's Sz83#/G-minor headings within this exact source-bound
review only. Original target text and work-specific orchestra credit keys remain.
Cached candidate m5in5vzcm30pa covers all3+5 movements, correctly credited.
Recomputed review passes: Probable85; exact take/LP mastering remains unverified.
No new metadata retrieval was needed. Full-track removal test withholds acceptance.

## Reusable query experiment

`scripts/qobuz_query_trial.py` prepares ten disjoint releases with empty original
searches, one normalized composer and available catalogue identifiers, excluding
all prior30comparison and20round2 releases. IDs evenly spaced, not representative.
Two strategies per release: headline performer/composer and the same plus a
catalogue number. Crucially, a headline ensemble precedes supporting members.
Multi-composer programmes remain excluded pending explicit per-work mapping;
lexically first catalogue number is not guaranteed to be the main work.

Fixed scope `data/qobuz_query_trial_scope.json` and hashed ignored manifest exist
before calls. Default prepares offline; explicit `--search` uses existing serial
15-second pacing,120-second rests every50requests, checkpoint/cache/STOP guards.
Any warning stops; no automatic retry. Top5hits only. No automatic metadata
expansion or match acceptance. Do not mistake hit yield for recording coverage.
`--export` reproduces whitelisted portable search evidence and per-strategy report
from completed local results. Original scope/query manifests remain immutable.

Commands:

```
uv run --with requests python scripts/qobuz_query_trial.py
uv run --with requests python scripts/qobuz_query_trial.py --search
uv run --with requests python scripts/qobuz_query_trial.py --export
```

Run outcome and validation are recorded below when complete.

## Completed outcome

Twenty queries completed13November17:34Amsterdam without API/access warnings.
Worker counted18network attempts including discovery;16new cached search responses,
with four query cache reuses. No new album metadata or audio fetched.
Performer/composer:10/10nonempty,50candidate entries. Catalogue-qualified:9/10,
34entries, of which31release–candidate pairs are absent from the corresponding
broad query's top5. The combined81pairs are leads, not accepted recording matches.

Both strategies are useful for this selected sample: retain broad search for
recovery and catalogue search for different editions. This does not establish
precision or population coverage, nor prove improvements against old queries
under identical historical catalogue conditions. Next proposed step: offline
screen the81pairs, then scope metadata for only the strongest uncached leads.
No further API batch or automatic promotion is implied by the report.

Portable `data/qobuz_query_trial_searches.json.gz` and `..._results.json` retain
whitelisted results and per-strategy observations. Request archive now1,845
responses; all prior1,829payloads verified byte-identical. Canonical URL index
re-exported offline (still1,045URLs; archive provenance hash updated).

Validation:78script+9pipeline tests pass, Node normalization and local build pass;
Spotify portable verification passes. Missing-track Richter regression fails
closed even with an updated album hash. Only release3667210 changes versus
checkpoint877bc5a; local unique12Found/71Probable/657Unchecked (copies12/71/658).
Follow-up remains uncommitted and unpublished after the requested initial commit.


## Offline screening follow-up

User authorized screening and scoping on13November. Reproducible command:
`uv run python scripts/qobuz_query_screen.py`. No catalogue calls or publication
writes. Shared report `data/qobuz_query_trial_screen.json` deduplicates by release
and album, checks source hashes and reuses original, comparison and round2 full
metadata. The correct combined count is81pairs (50broad+31additional), correcting
the earlier85count; the prior summary was arithmetic, not lost search evidence.

19pairs have complete cached metadata;62need metadata. None passes all current
work/credit/completeness guards. Three full-title/credit leads remain unresolved:
Schnabel2966855 lacks movement inventory for five late sonatas; Barenboim9866861
has completeness gaps and DG-versus-target recording-cycle concerns; Klemperer
14934969 has supported Symphony6 but no reviewed Leonore1 completeness expectation.
These are parser/evidence limitations, not confirmed missing recordings.

Schnabel0190295866983 was already in the comparison archive, so no new fetch is
needed for its next audit. Prior trial `cached_complete_metadata` flags only
checked the original snapshot; the screen uses the additional archives as well.
Earlier relevance scores also use an older helper that excludes headline
ensembles; do not use that score to reject Prague Quartet leads.

`data/qobuz_query_trial_metadata_scope.json` proposes exactly two uncached albums:
Prague String Quartet0002894631652 (71tracks advertised) and Klemperer5099992803350
(6tracks advertised). Search identity/programme suggests these leads; it does
not establish recording identity. This scope is proposed, not fetched. No new API
calls, automatic promotions, commit, push or deployment in this screening step.
Next recommendation: review cached Schnabel and bounded completeness expectations
first, then fetch these two albums slowly if proceeding with catalogue work.


## Cached Schnabel late-sonata audit completed

User authorized the cached audit. Release2966855 lists Sonatas29,28,30,31,32;
all five are covered by cached0190295866983 with Schnabel credited per track.
The target notes date individual recordings to1932–1935. Warner's barcode-specific
catalogue documents the1932–1938 cycle, supporting the same recording family;
exact takes and LP-versus-digital mastering are not independently confirmed.

`data/qobuz_schnabel_late_review.json` preserves source/album hashes, original
cached source notes and movement lists. Sonata28 digital track36924128 joins
III/IV; Sonata31 track36924140 covers target Adagio/Fuga sections III/IV.
Only these hash-bound tracks receive joined-section interpretation. Other works
require ordered4,3,2movements respectively. No global parser relaxation.
Complete source-bound review promotes this release to Probable85. No Qobuz API
calls. Local copies12Found/72Probable/657Unchecked; unique12/72/656.

Validation:79script tests pass, including deletion of each joined track/final
movement and unrelated-title substitution with updated album hashes withholding
acceptance. Node normalization and local build pass. Publication comparison
against checkpoint877bc5a changes only2966855 and prior follow-up Richter3667210.
No commit, push or deployment requested in this step. Next proposed catalogue
work remains the two-album metadata scope; it has not been fetched.


## Two-album metadata retrieval completed

User authorized retrieval. `scripts/qobuz_trial_metadata.py --fetch` uses the fixed
scope and existing paced/resumable worker; default only prepares offline.
13November17:44Amsterdam complete: Prague Quartet71tracks, Klemperer6tracks;
IDs, declared counts and unique track IDs verified, no warnings/retries/audio.
Portable `data/qobuz_query_trial_metadata.json.gz` retains whitelisted metadata.
Scope remains unchanged for provenance (its original proposed status describes
creation time); completion is recorded here and in the metadata/audit artifacts.

`uv run python scripts/qobuz_trial_metadata_audit.py` reproduces findings offline:
Klemperer has all5Symphony6 movements plus Leonore1 with required named conductor
and Philharmonia. Existing completeness checks still lack an overture expectation;
1957 source-session identity requires explicit review. Prague Quartet candidate
has the ensemble, but production requirements include named individual members
not supported by candidate credits. The unnumbered-by-catalogue No.8 heading also
matches multiple groups. Keep both unpublished pending review; no threshold or
credit requirements weakened and match totals unchanged12/72/657copies.

All successful requests shared through archive export; canonical URL index
re-exported offline. This work does not request a commit, push or deployment.
Next proposed: bounded Klemperer source recording/overture review, then investigate
positive ensemble-membership evidence for the Dvorak source and candidate.

Validation:79script tests pass; shared archive1,847responses and1,047canonical
URLs exported. `git diff --check` passes. No live worker remains.


## Klemperer recording/programme review complete

User authorized continuation through related cached work and validation without
repeated confirmation. Source-bound `data/qobuz_trial_recording_reviews.json`
promotes14934969/5099992803350 to Probable85. Five ordered Symphony6 movements
and one complete titled Leonore1 track with Klemperer/Philharmonia credits pass.
Warner Japan16392 documents7–8October1957 at Kingsway Hall for the symphony,
consistent with cached target October1957 notes. Exact candidate Qobuz catalogue
identifies EMI/Warner reissue provenance. This is recording-family support;
overture session date, exact take and LP/digital mastering remain unverified.
Only the exact overture track hash can supply its single reviewed section.

No further API calls or weakening of ensemble member requirements. Dvorak stays
unresolved: positive quartet-level credits cannot prove the requested member
lineup, and No.8 heading ambiguity remains. Avoid assuming absent metadata means
absent performers. Cumulative new reviews remain unpublished on the current branch.
Local copies12Found/73Probable/656Unchecked; unique12/73/655.

Validation:80script tests pass, including deletion of each of six Klemperer tracks
and substitution of the wrong overture, with updated album hashes, withholding
acceptance. Node normalization, local build and whitespace checks pass.


## Cumulative checkpoint review

Only14934969(Klemperer),3667210(Richter) and2966855(Schnabel) match records differ
from committed877bc5a. Spotify records remain unchanged. All1,829previous request
cache payloads survive byte-identically in the1,847-response archive. Local
secret-value scan of evidence/publication outputs passes without printing secrets.

Corrected query reporting: relevance now uses the actual queried headline artist,
including ensembles, and full-metadata cache flags consider all shared pilot
archives. Re-export preserves the original query evidence and hit counts. Old
remarks about the trial report's helper/cache limitations describe the initial
report and are superseded by this correction. Reports stay dated observations;
no query rerun or automatic match promotion.

Full `make test` passes:9pipeline+80script tests, Node normalization, portable
Spotify verification. No merge/push/deployment performed. No active retrieval.

Portable replay from a temporary copy containing only code/shared data (no .env,
raw caches or .qobuz-poc), using uv offline, reproduced qobuz_matches byte-identically.
