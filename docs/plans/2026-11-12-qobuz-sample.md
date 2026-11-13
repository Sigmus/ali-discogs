# Qobuz six-release catalogue trial

Date: 2026-11-12. Branch: codex/qobuz-poc.

Purpose: check live retrieval and metadata usefulness before building a matcher.
Six deliberately selected releases: two each from Spotify found, probable and
not_found. These are not random or representative; candidate yield is not an
estimate of catalogue coverage or matching accuracy.

Used Sei969/qobuz-dl revision 28c3521c3c96e62d7da7166d3edef1aed92a202f
for application-ID discovery only. A locally supplied user token authenticated
catalog/search and album/get. No application secret or audio endpoint was used.

## Results

Six initial searches succeeded, returning 19 candidate albums in total.
All 19 full album metadata fetches succeeded, with returned track counts equal
to the advertised counts. Five queries returned candidates; one returned none.
A broader fallback search for the empty result also succeeded and returned five
candidates, but did not establish a match. Evidence is cached locally under
ignored `.qobuz-poc/sample/`; no token is written to those files.

| Discogs release / Spotify status | Candidate and assessment |
| --- | --- |
| 2175684 — Gould, Well-Tempered Clavier / found | [0886443628625](https://open.qobuz.com/album/0886443628625): Gould, Sony Classical, complete Books I & II, BWV 846–893, 96 tracks. Strong programme/performer candidate. Other hits contain only parts of the collection. Recording identity is not independently verified. |
| 15282801 — Kleiber, Eroica / found | [0002894756080](https://open.qobuz.com/album/0002894756080): Decca anthology includes all four Eroica movements credited to Erich Kleiber and Royal Concertgebouw Orchestra. Also contains a Vienna Eroica, requiring track-level grouping. A separate search hit ezfmmvuhlu4uc has the right work/conductor but Vienna orchestra: reject for this Concertgebouw target. |
| 15081257 — Münchinger, Brandenburg 2/4/5 / probable | [br1wm2balrsvb](https://open.qobuz.com/album/br1wm2balrsvb): all movements of 2/4/5, Münchinger and Stuttgart Chamber Orchestra, plus concerto 1. Reissue/superset candidate; matching performer and programme do not prove recording/take identity. |
| 28220854 — Gilels, Beethoven sonatas 17/18 / probable | [0002894630792](https://open.qobuz.com/album/0002894630792): DG, Gilels, all movements of Op.31/2 and Op.31/3, plus sonata 15. Strong reissue/superset candidate; another label also offers these works with Gilels, so label/recording evidence matters. |
| 15221307 — Gilels, Russian Keyboard Masters Vol.1 / not_found | Exact compilation-title search returned zero. Fallback Gilels Beethoven Schumann returned unrelated programmes; inspected first album has Beethoven sonatas 16/12 and Schumann Toccata, not the target Beethoven Op.2/3 and Schumann Op.22. Unresolved, not confirmed absent. |
| 1445439 — Gould, Byrd/Gibbons / not_found | [0886445075762](https://open.qobuz.com/album/0886445075762): Sony Classical, Gould, same eight pieces in order, including First/Sixth Pavan and Galliard, Fantasy, Italian Ground, Hugh Aston, Lord of Salisbury, A Voluntary, Sellinger's Round. Strongest programme match; digital title differs from the LP. |

## Implications

Catalogue access works for this authenticated session. Rich metadata includes
work, composer, role-labelled performer strings, label, ISRC, UPC and streamable
flags. The selected candidates above reported streamable at fetch time; account
and territory may affect availability. This was metadata inspection, not playback.

Do not reuse title similarity as the sole acceptance criterion. Normalize
composer/work catalogue IDs and track credits; compare target programme coverage,
require performer/conductor/orchestra agreement per matching track, and separate
whole-album matches from recordings contained in larger reissues. Recordings with
matching credits but multiple takes remain review candidates. Original LP year
should not be treated as the digital reissue year.

Recommended next scope: an adapter/cache plus conservative candidate scoring and
manual review output, retaining unchecked for access errors. No collection JSON,
Spotify status, Qobuz classification or published UI changed in this trial.

## Reproduce

```sh
uv run scripts/qobuz_sample_poc.py --source /tmp/ali-qobuz-dl-poc
```

For current cache/resume options and pinned checkout setup see
[the Qobuz guide](../qobuz.md). The consolidated script uses a per-request cache
to preserve successful partial batches.

Requires a trusted local source checkout and QOBUZ_USER_AUTH_TOKEN in ignored
.env. Script uses fixed search queries, max five results each, caches completed
release results and pauses 250 ms between requests. Fallback was run separately
with qobuz_catalog_poc.py using `--query 'Gilels Beethoven Schumann'` and saved as
`.qobuz-poc/sample/15221307-fallback.json`. No automated acceptance rules have
been implemented or validated by this sample.
