# Qobuz round two: cached near-matches, then20 empty searches

User authorized beginning the recommended sequence on2026-11-13,
Europe/Amsterdam. Work isolated on `codex/qobuz-coverage-round2`. No commit, push,
merge or deployment requested. No confidence threshold reduction.

## Cached review completed

Two previous full-programme/performer leads now pass bounded exact-section review:

- 6381208 Klemperer Missa solemnis → kno5hz96hygbc. Eleven digital sections cover
  the target's five mass movements:1 /2–4 /5–7 /8–9 /10–11. Five summed digital/LP
  timings agree within3%. Named cast and New Philharmonia group match the
  documented1965 EMI recording family; not every singer performs every section.
  Sources: [Warner](https://www.warnerclassics.com/de/release/beethoven-missa-solemnis),
  [library recording description](https://ci.nii.ac.jp/ncid/BA56807310).
- 6599326 Ancerl Dvorak Requiem → tzrc8oc3d248a. All13 named target sections and
  required singers/orchestra supported. Introitus/Kyrie, DomineJesu and Sanctus/
  Benedictus mapped to Requiemaeternam, Offertorium and Sanctus in this exact
  candidate. [Composer-site discography](https://www.antonin-dvorak.cz/en/work/requiem-recordings/)
  distinguishes the1959 cast from a different1964 Ancerl recording;
  [library description](https://ge.nii.ac.jp/ncid/BB24443630) documents DG1959
  Rudolfinum sessions. Selected candidate is a third-party reissue: transfer,
  exact take and mastering remain unverified, explicitly visible in reasons.

Both capped at Probable85 heuristic. `data/qobuz_round2_reviews.json` preserves
selected raw target tracklists/source hashes, complete candidate/target hashes,
exact section track hashes, recording sources and limitations. Current production
work/performer support and every reviewed section still required on replay.
General movement parser and aliases unchanged; no automatic liturgical title alias.
Only these two publication labels change: unique12Found/69Probable/659Unchecked,
741copies12/69/660. Other cached identity/credit gaps remain unresolved.

## Fixed search scope

`data/qobuz_round2_scope.json`:20 unique currently unchecked releases whose original
Qobuz search was empty, excluding all30 prior comparison releases. Evenly spaced
by numeric release ID among eligible targets with two distinct improved queries.
Forty fixed queries, at most5 hits each. Deliberate diagnostic scope, not random
or representative. A hit/relevance score is not an accepted match.

Before any network calls, inspected all queries. Applied bounded query-only
corrections for Richter versus orchestra/conductor, Konwitschny/Bernstein DirectedBy
credits, Rubinstein in target title, primary concerto rather than filler piece,
and English/German work names. No target credits/composer requirements altered to
fit results. Prior unstarted manifest preserved locally; scope finalized before run.

`scripts/qobuz_round2.py` is offline by default. Explicit `--search` uses the
existing Catalogue/STOP worker: >=15seconds per request including discovery,
120-second rest after50 attempts, no retry, atomic query output, manifest equality,
lock and resumable shared request cache. Ignored state at
`.qobuz-poc/coverage-round2/`; any warning creates STOP and requires user direction.
Successful empty searches alone are not warnings. No audio requests.

On completion, export40 whitelisted results to
`data/qobuz_round2_searches.json.gz` and relevance/summary to
`data/qobuz_round2_results.json`. Do not publish hits automatically. Prefer existing
complete metadata for validation; bound any newly selected album metadata scope
before retrieval. Preserve uncertain matches and recording differences.

Commands:

```sh
uv run --with requests python scripts/qobuz_round2.py          # prepare offline
uv run --with requests python scripts/qobuz_round2.py --search # explicit live
uv run --with requests python scripts/qobuz_round2.py --export # completed cache only
```

Initial validation:73 offline script tests pass, including3 new section/scope
regressions. Publication change limited to2 intended reviews; full final checks
and retrieval findings to be appended after completion. No commit/push/deployment.

## Early diagnostic observations (search running)

- Richter paired Bartok/Prokofiev concertos appear together in a search result.
  Cached target assigns the two orchestras explicitly by LP side; existing target
  credit archive already preserves that distinction. However its Bartok heading
  saysSz83 while the returned album saysSz95, and the Prokofiev finale joinsIV/V.
  These need explicit catalogue/section review, not relaxed automatic acceptance.
- Barenboim Op61 piano-arrangement query finds known complete-concerto albums,
  but their work/performer checks do not support the requested English Chamber
  Orchestra recording. Search recovery alone is insufficient.
- Richter Schumann large DG box from a search hit does not supply all four target
  pieces under current title/credit checks. An anthology hit is not full coverage.

## Bounded metadata follow-up

Before the search stage completes, fixed two promising paired-programme leads in
`data/qobuz_round2_metadata_scope.json`: Richter Bartok2/Prokofiev5 and deVito
Brahms1/3. At most one candidate per release, no search expansion. Retrieve after
all40 searches, serially through the same slow/STOP worker and output directory
so last-request spacing persists. Complete counts/unique tracks must validate;
share whitelisted evidence and evaluate current work/credit/completeness rules.
The Richter catalogue typo/joined finale remains a blocker until explicitly
reviewed; an exact album title is not sufficient. No automatic publication.

## Completed search and metadata findings

Search completed without warnings:40 fixed queries,27 nonempty,18/20 releases
with hits,107 distinct release–candidate pairs. WernerHaas/Mendelssohn and
Bernstein/Haydn queries remained empty; this is not catalogue absence. A number
of long title queries returned nothing while broad performer/composer searches
returned anthologies. Twelve recovered candidate pairs already had complete
metadata in the original snapshot; none passes all unmodified credit/completeness
checks. See `data/qobuz_round2_cached_hits.json`.

Both selected metadata albums completed with full unique track counts: Richter8,
deVito7,15 total. No API warnings, retries, audio or additional search expansion.
At least15seconds spacing maintained between discovery/search/metadata requests;
under50 attempts across the whole serial run, so no batch rest was due. All40
query outputs and2 album outputs resumable. Portable metadata/review findings:
`data/qobuz_round2_metadata.json.gz`, `data/qobuz_round2_metadata_audit.json`.

**deVito8151148 →3614591254543 qualifies as Probable85.** Target requests Brahms
Sonatas1/3 with deVito/Fischer; digital has all3+4 movements with both names on
every track. The malformed first source heading repeats Op78 and joins No1 into
`78N`; strict catalogue parsing therefore withheld it. An exact hash-bound review
interprets this as Sonata1 Op78 while preserving the original source text. The
review adapter retains original target-credit lookup keys when cleaning a title;
no generic opus tolerance/alias or lower confidence threshold is introduced.
[Hyperion publisher notes](https://www.hyperion-records.co.uk/dc.asp?dc=D_APR7314)
and [library recording description](https://ci.nii.ac.jp/ncid/BA47147480) identify
the1954 deVito/Fischer EMI recordings. BNF transfer/mastering/take unverified;
recording-family evidence supports Probable, not Found.

**Richter3667210 remains Unchecked.** Correct musicians/orchestras on3Bartok +
5Prokofiev movements, but target saysSz83# versus digitalSz95 and Prokofiev Gminor
versus Gmajor. LP joinsIV/V, digital separates them. The raw source has clear
per-work orchestra assignments, already preserved by the credit model. Do not
apply an unreviewed catalogue correction to force a match. Publisher catalogue
identifies [Prokofiev5 in Gmajor Op55](https://www.boosey.com/publications/sheet-music/Serge-Prokofieff-Piano-Concerto-No-5-in-G-major-op-55/1427);
a bounded source/catalogue/recording review is the concrete next proposal.

## Final local result and validation

Three new Probable releases: two from original cached near-matches, one from
this search follow-up. **12Found /70Probable /658Unchecked unique releases**;
741copies **12/70/659**. Only6381208,6599326,8151148 publication records change.
Spotify data and all other Qobuz evidence/statuses unchanged. Neither18 search
recoveries nor107 hits are claimed as18/107 matches.

- Nine pipeline/guard +75offline script tests pass (84 total), including missing
  section/title tampering, fixed20-case offline default, bounded metadata scope,
  and preservation of original per-work credits through reviewed title cleanup.
- UI normalization/sorting/canonical URL checks, JS syntax/build and diff pass.
  Repeated matching output identical; local Klemperer and deVito details verified.
- Original matching/comparison/target-credit/Spotify archives byte-identical.
  Shared raw request archive now1,829 responses:41 additions (39search +2metadata),
  all previous1,788 payloads byte-preserved. Canonical URL index now1,045 albums.
  Rebuild from shared archive; no invented links. Private credential-value and
  export whitelist checks pass. Raw archives stay outside Pages artifact.
- Worker scopes/progress, raw cached pages and STOP policy preserved. No active
  retrieval remains; both stages complete. No commit/push/merge/deploy requested.

Reproduce the completed audits without live requests:

```sh
uv run --with requests python scripts/qobuz_round2.py --audit
uv run python scripts/qobuz_match.py
make build
```

`--metadata` explicitly runs only the fixed two-album scope using the same worker;
shared portable metadata is sufficient for ordinary offline matching after checkout.
Next proposed work: review Richter's source catalogue conflicts, then improve
short work-title queries and role/composer normalization before another bounded
batch. Keep blank source credit assignments unresolved until supported by source
material; do not infer away performers from a candidate's convenience.
