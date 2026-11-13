# Thirty-release service comparison pilot

Date: 2026-11-13, Europe/Amsterdam. User accepted the proposed comparison pilot
and asked to start. No commit, push or deployment requested.

## Fixed scope and limits

`data/qobuz_comparison_scope.json` fixes 30 disjoint unique releases:

- Ten evenly spaced release IDs with empty original Qobuz searches and currently
  Unchecked status; two fixed shorter fallback queries per release, up to five
  results each. First performer + composer, then catalogue or shortened title.
- Ten purposive unresolved Qobuz failure controls spanning completeness, credit,
  alias, catalogue and incomplete-programme issues. These are cached-only reviews.
- Five Spotify Found and five Probable IDs, evenly spaced within status and
  disjoint from both Qobuz groups. These are cached-only reviews.

This is not a random or representative sample. Queries may still choose a
supporting musician or an unsuitable surname from the existing target fields.
No statistical catalogue-coverage/precision/recall claim follows.

The Spotify adapter caches album search results, not complete track lists.
Therefore its ten cases can receive only album-level title/artist/count checks;
full movement/credit parity with Qobuz cannot be established from this cache.
No Spotify API calls are authorized by this implementation or made automatically.
This limitation is part of the finding, not a successful full Spotify validation.

## Safe retrieval and reproduction

`uv run --with requests python scripts/qobuz_comparison_pilot.py` prepares/reviews
saved data without API calls. `--search` explicitly runs the fixed 20-query plan.
Evidence/progress/lock/STOP live under ignored `.qobuz-poc/comparison/`; successful
request responses also reuse the shared ignored request cache. The original
collection, Qobuz snapshot, archives and publication matches are not overwritten.

The worker spaces all HTTP attempts (including app-ID discovery) by at least
15 seconds, rests 120 seconds after every 50 requests, saves each result atomically,
checks a STOP marker and handles termination. Persisted last-request time prevents
a fast restart; a lock prevents concurrent pilot workers. Existing saved results
are reused. First auth/access/rate-limit/network/unexpected warning creates STOP
and fails without retry; no resume after a warning without user direction.

Three mocked tests cover warning→STOP/no retry, existing STOP blocking connection,
and result reuse without network. No audio requests are involved.

## Initial offline observations

Spotify release 1012732 requests four Brahms symphonies, violin concerto, German
Requiem and Haydn Variations. Its Probable candidate is `Karajan: Brahms Symphony
No. 1` (four tracks, heuristic score .86). This is a strong partial-programme
warning from available album metadata, not a completed track-level rejection.
It illustrates why a larger Spotify match count cannot be read as higher accuracy.

For the ten Qobuz unresolved cases, current evidence points to two withheld
completeness leads, four explicit performer/ensemble spelling-identity issues,
two catalogue/programme interpretation cases, one incomplete target-programme
control and one partial credit/programme case. Review details and final search
outcomes will be recorded after the fixed retrieval completes.

## Completed retrieval and comparison

The fixed search stage and selected metadata retrieval completed without warnings
on 2026-11-13; metadata finished at 13:04 Europe/Amsterdam. Twenty fallback queries
covered all ten empty-result releases. Seventeen queries returned results (68 raw
hits / 66 distinct release-candidate pairs). Every release had some hits; this is
search recovery, not a ten-album match result.

Selected eight diagnostic/title-promising albums, at most one per release, for
complete metadata inspection: seven newly fetched and one shared-cache reuse,
423 tracks total. Additional metadata for another search hit was already in the
original snapshot. No new metadata was fetched for the two wholly unrelated
result sets. Existing pagination/complete-count/unique-ID checks were reused.

Three releases have full target-heading programme/performer leads under current
matching rules: Schnabel (4429613, 7/7), Tennstedt (12130939, 2/2) and Kubelik
(37312800, 1/1). None passes every strict completeness check with the current
inventory; recording identity also remains unverified. No publication promotion.
The suspected Kubelik orchestra issue was cleared by actual track credits: the
selected cycle supports the requested Vienna Fourth. This illustrates why a
search-level orchestra assumption is not sufficient.

The other metadata cases expose different bottlenecks: Barenboim's target
hierarchy yields 23/31 supported items; the Bach masses, Cortot concerto/trio and
Haitink cycle are blocked by target-wide performer/ensemble requirements or naming.
The Brahms four-symphony album is genuinely partial for the much larger collection:
its track list covers symphonies, not the requested concerto/Requiem/variations.
Do not interpret zero fully credited headings as zero relevant music present.

The ten cached unresolved controls break down into two withheld completeness
leads, four performer/ensemble identity variants, two catalogue/programme
interpretation cases, one 13/14 coverage control and one partial 1/2 work/credit
case. No aliases or scoring rules were changed during this comparison.

Spotify review remains album-level: one strong partial-programme warning and
nine cases not verifiable at programme/recording level from the available cache.
No claim of ten Spotify confirmations or a measured false-positive rate. Some
sample releases are different physical editions of similar programmes, so even
the disjoint release IDs are not independent recording observations.

## Preserved evidence and replay

- `data/qobuz_comparison_offline.json`: ten cached unresolved Qobuz assessments,
  ten Spotify album/cache observations and the original Discogs programmes.
- `data/qobuz_comparison_evidence.json.gz`: deterministic whitelisted portable
  snapshot of all 20 search results and eight complete selected albums (~28 KB).
  No credentials, account records, audio URLs or machine state exported.
- `data/qobuz_comparison_results.json`: reproducible search/metadata assessment
  and summary; a search hit and a programme lead are explicitly separate.
- `data/qobuz_comparison_review.json`: dated manual observations for all 30 cases,
  not score overrides. Complete table below.
- Existing shared `data/qobuz_request_cache.tar.gz` refreshed at the user's
  standing request to share caches. It now contains 1,786 successful responses:
  27 added; all previous 1,759 member payloads verified byte-identical, none removed.
  Seven new album responses plus twenty searches; app-ID discovery is not archived.

`--metadata` reads the fixed eight-candidate metadata scope and uses the same
STOP/lock/pacing worker. `--export` explicitly exports completed local evidence.
`--report` computes results from the portable archive and original snapshot,
without needing the ignored pilot raw metadata or calling APIs. All flags are
mutually exclusive; ordinary invocation remains offline. Existing `--search`
outputs are reused and a changed collection/query plan is refused.

Validation: all 47 mocked/offline Qobuz tests pass, including four new pilot
safety/export tests. Report/export replay is checked for identical bytes; all
new metadata album IDs/counts/unique tracks validated. Credential-value scan and
sensitive-key whitelist checks pass. Publication matches are byte-identical to
HEAD: 12 Found / 64 Probable / 664 unchecked unique releases (741 copies: 12/64/665).
No Spotify API calls, audio, commit, push or deployment.

## Recommendation

1. Improve bounded fallback query selection: short artist/composer query, then
   a specific work/catalogue query, with a relevance filter. Fix supporting-player
   and composer-surname choices (e.g. Bartholdy alone), rather than merely taking
   more broad top-five results. Review a small next batch before a collection run.
2. Assign target credit requirements by work and role, especially multi-work sets.
   A choir/soloist from one symphony or an orchestra from a concerto must not be
   required on every unrelated work. Cached Discogs extraartist entries inspected
   for Cortot, Bach and Haitink often have empty track assignments, so missing
   target information cannot simply be inferred away automatically.
3. Cache Spotify track/credit metadata for this same ten-case sample before a
   fair programme-level comparison. Current album search data cannot validate
   the 531 Found/Probable copies to the same standard as Qobuz.

Further fetching, model changes and publication are proposals, not part of this
completed comparison. The pilot supports both search and interpretation work;
it does not establish a Spotify-versus-Qobuz catalogue-size difference.

## All 30 reviewed cases

| Group | Discogs ID | Target | Observation |
| --- | --- | --- | --- |
| qobuz_empty | 594243 | A Love Supreme | Broader queries returned other Coltrane/Tyner albums, not a title-promising A Love Supreme candidate; no metadata selected. |
| qobuz_empty | 3066447 | Les Plus Belles Sonates Pour Piano | Complete Barenboim cycle found; target hierarchy/normalization leaves 23/31 items supported. Not evidence of absence. |
| qobuz_empty | 4429613 | The Complete Beethoven Society Recordings, 1932–37 / Vol. 2: Sonatas, Nos. 11–17 | Schnabel complete cycle supports 7/7 target work headings. Promising superset; completeness/session review still needed. |
| qobuz_empty | 6091545 | Psalmen Davids, 1619 (Five Concertos For Soloists, Choruses & Instruments) | Other Schuetz works returned; no title-promising Psalmen Davids candidate selected. |
| qobuz_empty | 7103881 | Messen F-dur (BWV 233), A-dur (BWV 234) | Exact F/A mass pairing found, but all-required-performer checks support 0/2 target work headings. Credit interpretation remains unresolved. |
| qobuz_empty | 8534837 | Double Concerto / Piano Trio No. 1 | Exact concerto/trio pairing found; target-wide orchestra/performer requirements and names block support. Trio should not blindly inherit concerto orchestra requirements. |
| qobuz_empty | 10301402 | Die 4 Symphonien · Das Violinkonzert · Die Haydn-Variationen · Ein Deutsches Requiem | Four-symphony candidate is a partial programme for the much larger requested collection. Reject as a complete collection match. |
| qobuz_empty | 12130939 | Symphonie N° 5 / Symphonie N° 10 - Adagio | Tennstedt collection supports 2/2 target headings (Fifth and Tenth Adagio); completeness/session review still needed. |
| qobuz_empty | 15926362 | Symphonies Nos. 1-4 | Haitink cycle found, but shared target credits include singers/chorus not applicable to every symphony. Programme/role interpretation remains unresolved. |
| qobuz_empty | 37312800 | Symphonie Nr.IV e-moll | Kubelik cycle actually supplies the required Vienna Fourth in cached track credits; suspected orchestra mismatch cleared. 1/1 work supported; completeness/session review remains. |
| qobuz_unresolved | 6381208 | Missa Solemnis | Stronger Klemperer performer-group lead withheld for programme completeness. |
| qobuz_unresolved | 6599326 | Requiem Op. 89 | Stronger Ancerl performer-role lead withheld for programme completeness. |
| qobuz_unresolved | 8252155 | Messen | Only 1/2 works supported by current credit/programme interpretation. |
| qobuz_unresolved | 8121703 | Twenty Harpsichord Sonatas | Longo/Kirkpatrick catalogue equivalences remain unverified. |
| qobuz_unresolved | 5820114 | The Five Piano Concertos | 5/8 target items supported; remaining catalogue/programme equivalences unresolved. |
| qobuz_unresolved | 6678433 | 10 Mazurkas · Prélude Op. 45 · Ballade Op.23 · Scherzo Op. 31 | 13/14 target items supported; preserve the incomplete-coverage control. |
| qobuz_unresolved | 9739139 | Symphony No. 9 "From The New World" | Kiril/Kirill conductor spelling remains unverified. |
| qobuz_unresolved | 13069435 | Concerto Pour Violon & Orchestre | Oistrach/Oistrakh soloist spelling remains unverified. |
| qobuz_unresolved | 4841406 | Concerto No.1 / Concerto No.2 | Kondrashin/Kondrascin transliteration remains unverified. |
| qobuz_unresolved | 3198796 | Die Walküre | Bayreuth ensemble naming and required credits remain unresolved. |
| spotify_review | 669978 | The Man With The Horn | Nominal album/title/artist evidence inspected; programme and recording-credit verification unavailable without Spotify tracks. |
| spotify_review | 3569461 | Symfoni Nr. 3. "Espansiva" | Nominal album/title/artist evidence inspected; programme and recording-credit verification unavailable without Spotify tracks. |
| spotify_review | 6119238 | Symphony No. 6 / Overture 'My Home' | Nominal album/title/artist evidence inspected; programme and recording-credit verification unavailable without Spotify tracks. |
| spotify_review | 8982341 | Götterdämmerung | Nominal album/title/artist evidence inspected; programme and recording-credit verification unavailable without Spotify tracks. |
| spotify_review | 36163426 | Symphonie N° 9 | Nominal album/title/artist evidence inspected; programme and recording-credit verification unavailable without Spotify tracks. |
| spotify_review | 1012732 | Die 4 Symphonien · Das Violinkonzert · Die Haydn-Variationen · Ein Deutsches Requiem | Strong partial-programme warning: seven-work Brahms collection vs four-track Symphony No.1 album. No Spotify track-level validation. |
| spotify_review | 3985321 | Nabucco | Nominal album/title/artist evidence inspected; programme and recording-credit verification unavailable without Spotify tracks. |
| spotify_review | 7194998 | Dinu Lipatti Plays The Waltzes Of Chopin | Nominal album/title/artist evidence inspected; programme and recording-credit verification unavailable without Spotify tracks. |
| spotify_review | 11553633 | Sonatas, Volume 2 | Nominal album/title/artist evidence inspected; programme and recording-credit verification unavailable without Spotify tracks. |
| spotify_review | 34330297 | Khovanshchina | Nominal album/title/artist evidence inspected; programme and recording-credit verification unavailable without Spotify tracks. |
