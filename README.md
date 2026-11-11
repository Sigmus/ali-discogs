# ali-discogs

Match [Ali’s Discogs collection](https://www.discogs.com/user/ajozi/collection) (user `ajozi`, 741 classical releases) against the Spotify catalogue, and browse the result in a static explorer.

Spotify today: **255 found**, **276 probable**, **210 not found**. Qobuz is `unchecked` on every row. `www.qobuz.com` answers 403 from the network that built this, so each row keeps a `qobuz.search_url` and the card links there. There is no Qobuz matcher.

The explorer is the page that was published from `apps/ali-discogs/` in the sigmus web app (live at <https://sigmus.fly.dev/ali-discogs/>). This repo is its long-term home. GitHub Pages serves it at <https://sigmus.github.io/ali-discogs/>.

## Layout

```
data/collection_matches.json   741 match rows (the file the page loads)
data/summary.json              counts from the last match run
raw/discogs/page_*.json        collection pages (8 pages, 100 per page)
raw/discogs/releases/<id>.json release detail, one file per release id (740; one id is in the collection twice)
raw/spotify/<16 hex>.json      cached Spotify search response, {"q", "resp"}
raw/qobuz/                     empty; nothing is fetched
explorer/                      static page (index.html, app.js, style.css, fixture, loader test)
src/ali_discogs/               matcher
```

Spotify cache filenames are the first 16 hex chars of `sha1("album|{limit}|{query}")` with the default `limit` of 10. A rerun reads those files and does not call Spotify when the query is already cached. Discogs pages and release details work the same way: if `raw/discogs/...` exists, it is used.

No file in the cache is large enough to need Git LFS (largest is `data/collection_matches.json`, about 3.5 MB).

## Matching

`make match` walks the collection in page order. For each copy it builds composers, performers, a conductor, and key performers from the release detail, runs a handful of album searches, and scores every distinct album returned.

Text is folded with `unidecode`, lowercased, and stripped of Discogs disambiguation `(2)`. Work titles are translated before comparison (`Sinfonie` / `symphonie` → symphony, `moll` → minor, `KV` → K, and the other pairs in `text.TRANS`). Catalogue numbers (`op`, `bwv`, `k`, `d`, `hob`, `rv`, `hwv`, `sz`, `bb`, `wwv`, `l`) and lists such as “symphonies nos 3 to 5” become a set of ids. Performer names match at 88 or above: exact, fuzzy token sort, same surname with a shared initial, or the shorter significant-token set contained in the longer one. A few orchestra aliases are applied (`Berliner Philharmoniker` → Berlin Philharmonic, and the others in `ORCH_ALIASES`).

Key performers are the conductor, plus the first soloist unless there is a conductor and at least two soloists. If that set is empty, the first performer is used. A Spotify credit counts only when `name_match` against an album artist is at least 88. A name that appears in the album title can still raise the looser performer hit, but it does not satisfy `p_in_artists`.

Confidence, roughly:

- 0.35 if every key performer hits, plus 0.15 times the fraction of the first four performers that hit
- 0.15 times the fraction of the first three composers that hit (1 when none are known)
- 0.30 times the title token-set score (0–1), after composer and performer names are removed from the Spotify title
- +0.08 when catalogue numbers agree, −0.25 when they conflict
- +0.04 when the Spotify release year is within two years of the Discogs year
- −0.10 when a known conductor misses, −0.10 when a known ensemble misses a Spotify ensemble credit, −0.08 when Spotify says live and the Discogs title does not

The result is clamped to 0–1 and rounded to three decimals.

`classify` then applies the thresholds. **Found** (`confidence >= 0.80`) only when all of these hold:

- every key performer hits, and each one matches a Spotify artist credit (`p_in_artists`), not only the album title
- at least half the composers hit (or no composer is known)
- title score ≥ 70, and title sort ≥ 55 or the catalogue numbers agree
- catalogue numbers are not a partial mismatch (`num_agree != 0`) or a hard conflict
- the conductor is not a miss, the ensemble is not a miss, and it is not a live/studio mismatch

**Probable** (`confidence >= 0.62`, or one of the extra branches) when it is not found and:

- numbers conflict, but the key performers hit, confidence ≥ 0.62, and the title score ≥ 60
- confidence ≥ 0.62, the key performers hit, and the title is usable (score ≥ 50 or the numbers agree)
- confidence ≥ 0.72, title score ≥ 85, and some performer hit
- the conductor hits, the title score ≥ 85, and the numbers are not in hard conflict

Anything else is **not found**. If the release has no performer at all it cannot be confirmed: probable only at confidence ≥ 0.75 and title score ≥ 80.

A hard number conflict is two non-overlapping “no. N” sets, or opus-like ids with no overlap. A volume number that differs also blocks a found.

## Commands

Requires [uv](https://docs.astral.sh/uv/) and Python 3.11+.

```bash
uv sync
cp .env.example .env   # only for searches that are not already cached
make fetch             # Discogs pages and any missing release details
make match             # rescore; Spotify/Discogs are called only on a cache miss
make match-offline     # same, but a cache miss is an error (no credentials needed)
make test              # offline rescore must stay 255 / 276 / 210, plus the page loader test
make build             # dist/ with the page and the results JSON
make serve             # http://127.0.0.1:8000
```

`make match` is safe to repeat. Cached Spotify responses are served from `raw/spotify/` with no API call and no credentials. A query that is not cached uses the [client-credentials flow](https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow): set `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` in `.env` (or the environment). `.env` is gitignored. Do not commit those values.

Discogs works anonymously. `DISCOGS_TOKEN` is optional and lifts the limit from about 25 to about 60 requests per minute. The client sends `Authorization: Discogs token=…` when the variable is set, and it sleeps on `X-Discogs-Ratelimit-Remaining` and `Retry-After`. Cached pages and release files skip the network.

`--rescore` is an alias of `--offline`.

The package layout:

| Module | Role |
| --- | --- |
| `discogs.py` | collection and release fetch, cache, rate limit |
| `spotify.py` | client-credentials search and `raw/spotify/` cache |
| `text.py` | normalization, catalogue numbers, name matching |
| `model.py` | one collection copy → composers, performers, queries |
| `score.py` | confidence and found / probable / not_found |
| `pipeline.py` | load, match, write `data/*.json` |
| `cli.py` | `ali-discogs fetch` and `ali-discogs match` |

## Explorer

`explorer/index.html`, `app.js`, and `style.css` are the page. Paths are relative (`style.css`, `app.js`, `data/collection_matches.json`), so the same files work at the site root and under the `/ali-discogs/` prefix GitHub Pages uses for this repo. `?data=fixture` loads eight invented rows from `explorer/data/fixture.json`.

`make build` writes `dist/` with the page, the fixture, `collection_matches.json`, and `summary.json`. `make serve` builds and serves that directory. The loader test is `node explorer/test/normalize.test.js`.

## GitHub Pages

`.github/workflows/pages.yml` runs `make build` on every push to `main` and deploys the `dist/` artifact with GitHub Actions. After the first successful run the site is:

<https://sigmus.github.io/ali-discogs/>

The workflow can only publish once the repository’s Pages source is **GitHub Actions**. If that is not set yet: **Settings → Pages → Build and deployment → Source → GitHub Actions**. Nothing else (no branch, no custom domain) is required. The test workflow (`.github/workflows/test.yml`) reruns the offline matcher on pull requests and checks that the counts stay 255 / 276 / 210.
