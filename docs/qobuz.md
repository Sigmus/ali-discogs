# Qobuz catalogue enrichment: setup and resume

Status: working read-only catalogue PoC on `codex/qobuz-poc`. It retrieves
candidate metadata; it does not automatically accept matches, update collection
JSON, download audio or publish to GitHub Pages. Six-release findings are in
[the sample report](plans/2026-11-12-qobuz-sample.md).

## One-time setup

Requires Git, uv and Python 3.11+. Run commands from the repository root.
Scripts use isolated uv dependencies; no downloader installation is required.

```sh
mkdir -p .qobuz-poc
git clone https://github.com/Sei969/qobuz-dl.git .qobuz-poc/upstream
git -C .qobuz-poc/upstream checkout --detach 28c3521c3c96e62d7da7166d3edef1aed92a202f
```

The adapter verifies the upstream revision and unmodified `bundle.py` before
loading it. It uses only application-ID discovery, not app-secret extraction or
the full downloader client (whose initialization probes audio). Upstream is
GPL-3.0; its source stays in a separate ignored checkout, not copied here.

If `.env` does not exist, copy `.env.example` to `.env`. If it already exists,
add `QOBUZ_USER_AUTH_TOKEN=` without replacing the existing settings. From your
own logged-in Qobuz browser session, open developer tools, find an `api.json`
request in Network, and copy its `X-User-Auth-Token` request-header value into
that setting. Do not paste the token in chat, logs or committed files. Environment
variables take precedence over `.env`. Scripts never print token/app-ID values.

## Run and resume

```sh
# Search five candidates; inspect the first album's full metadata.
uv run scripts/qobuz_catalog_poc.py --query 'Glenn Gould Byrd Gibbons'

# Reproduce the six-release trial, up to five candidate albums per release.
uv run scripts/qobuz_sample_poc.py

# Reuse cached responses without any network or token/source requirement.
uv run scripts/qobuz_sample_poc.py --offline

# Explicitly refetch after account/territory changes or stale results.
uv run scripts/qobuz_sample_poc.py --refresh
```

An alternate trusted source checkout can be selected with `--source PATH`.
For a new bounded batch, create an ignored `.qobuz-poc/next-sample.json`:

```json
[
  {"discogs_id": 1445439, "query": "Glenn Gould Byrd Gibbons"}
]
```

```sh
uv run scripts/qobuz_sample_poc.py --sample-file .qobuz-poc/next-sample.json
```

Each ID must exist in `data/collection_matches.json`. Queries are explicit so
future work can refine retrieval without committing arbitrary automatic rules.
The current sample output is one file per release; changing a query for that
release replaces its assembled output. Per-request caches retain both queries.

## Cache and errors

- `.qobuz-poc/cache/`: successful search/album responses, timestamp, request
  parameters and upstream revision. No auth headers or app credentials stored.
- `.qobuz-poc/sample/<discogs_id>.json`: assembled review evidence for each release.
- `.qobuz-poc/catalog-result.json`: latest single-query review output.

All are ignored by Git. Keep `.qobuz-poc/` on the same machine to resume; on a
fresh checkout, rerun the setup and fetch. Every completed HTTP response is cached
atomically, so an interrupted batch resumes without repeating earlier successful
requests. Existing pre-consolidation sample files are evidence, not the new
per-request cache: the first new run fetches them again. Failures are never cached
as empty results. A zero-result search remains inconclusive, not proof of absence.

The cache is local to this account/territory; it does not include token values
in its keys. Use `--refresh` after changing account/territory. Offline cache misses
fail explicitly. `--offline` and `--refresh` are mutually exclusive. Requests have
20-second timeouts; batches pause 250 ms between candidate metadata fetches.

HTTP 401 indicates invalid/expired credentials or missing authentication; replace
the user token locally and retry. For 403/429 or network failures, stop and check
access/rate limits before retrying. If app-ID discovery breaks after a web-player
change, inspect upstream and intentionally update the pinned revision in
`scripts/qobuz_catalog.py`; do not silently use arbitrary newer code.

## Continue toward a production matcher

1. Normalize Qobuz album/work/track metadata, including role-labelled credits,
   orchestra aliases, catalogue IDs, ISRC, label and availability.
2. Compare programme coverage and recording identity. Distinguish exact programmes
   from recordings contained in larger compilations; verify ambiguous takes.
3. Produce review candidates and retain manual decisions separately so later
   enrichment/rescoring cannot overwrite them. Access errors remain unchecked.
4. Only then design an explicit merge into collection JSON. The existing Spotify
   pipeline currently rewrites Qobuz entries as unchecked: do not insert accepted
   results there until preservation/override precedence is implemented.

No download functionality is part of this PoC. `scripts/qobuz_poc.py` remains the
older taschenb/python-qobuz comparison probe; it needs an independently issued
`QOBUZ_APP_ID`. The token-based scripts above are the working path.

## Validation

```sh
uv run --with 'requests>=2.32,<3' python -m unittest discover -s scripts/test -v
make test
make build
```

Unit tests use mocked network responses. The dated sample report records live
API evidence; neither proves automated match accuracy for the full collection.

## Slow search of the full collection

User authorized a full candidate-search pass on 2026-11-12. Run:

```sh
uv run scripts/qobuz_all_poc.py
```

This searches 740 distinct releases (741 copies), one query each, up to five
candidates. It uses the six tested queries where available; otherwise the first
key performer (or first performer), composer surname and first ten normalized
title words. This is a first retrieval pass, not an exhaustive search or matching
classification. Empty searches will need later work/track-based fallbacks.
It does not fetch every candidate's full track metadata in this pass.

All live requests, including app-ID discovery, are serial and spaced at least
15 seconds apart. After each 50 uncached searches it rests two minutes. This is
an intentionally conservative policy, not a published guarantee against Qobuz
limits. Any access, rate-limit or network error stops the run; no automatic
retries. Existing successful responses are reused. Duplicate copies share one
release search. A file lock prevents two copies of this runner at once.

Results and the exact query plan live under ignored `.qobuz-poc/all/`:
`manifest.json`, `<discogs_id>.json`, `progress.json`, and `run.log` when launched
with output redirection. Progress includes PID, status, counts and timestamps.
A detached run was started with `caffeinate -i` to prevent idle system sleep;
closing the laptop/restarting may still interrupt it. Resume with the same command.

```sh
cat .qobuz-poc/all/progress.json
# Request a clean stop; results already fetched are preserved.
touch .qobuz-poc/all/STOP
# Remove the marker before resuming.
rm .qobuz-poc/all/STOP
uv run scripts/qobuz_all_poc.py
```

A changed collection/query manifest stops rather than mixing plans silently.
Do not delete it without preserving existing evidence and reviewing the change.
The final `status: complete` means all first-pass searches finished, not that
all albums were found. The runner writes no production data. Inspect progress
and the process before starting another run; the launcher PID and actual worker
PID differ. Eight mocked tests cover caching/errors plus pacing, stop markers
and duplicate handling.
