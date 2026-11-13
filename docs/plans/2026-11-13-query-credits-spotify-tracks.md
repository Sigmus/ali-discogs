# Query relevance, explicit target credits and Spotify track comparison

Date: 2026-11-13, Europe/Amsterdam. User authorized the next query/credit/cache work.
No collection-wide search, commit, push or deployment requested.

## Query improvements

`scripts/qobuz_query_plan.py` generates bounded query proposals and reranks the
already cached pilot hits. It chooses the album-listed non-classical-composer lead
before supporting key performers, retains Mendelssohn rather than only Bartholdy,
avoids repeating a composer name already in the performer, and proposes work or
catalogue-specific follow-ups. Ranking uses named-artist support, title similarity
and available track-title coverage. Possible live variants are flagged/downranked;
this is relevance, not match confidence, recording identity or acceptance.

`data/qobuz_query_improvements.json` preserves proposals/ranking for the ten pilot
empty-search cases. Two corrected queries were validated slowly through the
existing STOP/no-retry/cache worker (`scripts/qobuz_query_validation.py`):

- `john coltrane a love supreme` returned five hits including two nominal
  A Love Supreme editions, a live Seattle version and expanded collections.
  Earlier supporting-pianist queries had not found a title-promising candidate.
- `pablo casals mendelssohn` returned five relevant artist/composer hits, including
  Casals/Thibaud/Cortot trio albums. This is not proof of the full concerto/trio LP.

Both queries completed without warnings. Results and relevance explanations are
preserved in `data/qobuz_query_validation.json.gz`, with raw requests also added
to the shared cache archive (now 1,788 responses). No further query batch launched.

## Per-work target credits and hierarchy

`scripts/qobuz_target_credits.py` derives a versioned portable model from cached
Discogs release responses; `data/qobuz_target_credits.json.gz` currently covers 128
releases with explicit work/position performance assignments. Source release
hashes are retained. The matcher reads this archive without needing raw Discogs
files; its fingerprint is included in generated output.

Rules are positive and conservative:

- Nested work/track performance credits and explicit position/range assignments
  establish where a named performer is required. Those names are not blindly
  required on other works. New explicit soloists are added to their assigned work.
- Unscoped global requirements remain. If an actor also has an unscoped credit,
  or a scope cannot be fully parsed/mapped, the global requirement is retained.
  Candidate credits never determine which target requirements get removed.
- Ranges use the source record's ordered positions, including mixed vinyl sides
  (`A to C1, D2`). Partial parses, unknown endpoints, ambiguous duplicate positions
  and non-performance technical credits do not create permissive assignments.
  Side prefixes cannot spill from A into AA. Bitches Brew is a real regression
  control for Joe Zawinul/Larry Young's differing cross-side assignments.
- Original `units_v1`/`evaluate_v1` remain for frozen historical audit. Current
  target units recognize index/heading parents and numbered child movements;
  standalone named pieces stay required. Changed hierarchy cannot create a new
  Found result; newly qualifying candidates still pass the completeness gate.

In the cached Barenboim pilot, work-unit coverage is now 8/8 instead of the old
23/31 flattened-item mapping. This is still a candidate lead, not a publication
promotion: missing structure/session evidence remains unresolved. Bach/Cortot/
Haitink cases with blank target credit assignments retain their unresolved global
requirements. The implementation does not guess orchestra/choir participation
from a composition name alone, and no new person aliases were enabled.

All 740 publication statuses remain unchanged: Qobuz 12 Found / 64 Probable /
664 unchecked unique releases (copies 12/64/665). Improved evidence alone does not
justify relaxing scores or claiming independently verified recording sessions.

## Reuse the existing sp login

Local `.env` Spotify client ID/secret placeholders were added at the user's
request, preserving Qobuz settings. They were not sent to Spotify or filled with
actual secrets. The existing SP project uses PKCE: client ID at
`~/.config/sp/config.toml` and access/refresh tokens at `~/.config/sp/cache.json`
(or the equivalent XDG config directory). It has no client secret.

`scripts/spotify_pilot_tracks.py` uses the SP Python environment and existing
configuration. Its bridge keeps tokens in the subprocess, refreshes once under
SP's lock when needed, never invokes cache-clearing/interactive-login fallback,
and returns only status/catalogue metadata. Refresh HTTP retries are disabled;
any access/auth/rate-limit/network/metadata warning creates STOP without retry.
No credentials are copied into this repository or printed.

The ten fixed Spotify albums were fetched successfully at >=15-second spacing,
including full pagination for Götterdämmerung. All 227 tracks passed count and
position checks. API documentation: [Get Album Tracks](https://developer.spotify.com/documentation/web-api/reference/get-an-albums-tracks).
Market NL is requested; Spotify states that a user token's country takes
precedence. Artist lists do not supply explicit instrument/conductor/chorus roles,
so track caching does not make recording-credit verification equivalent to Qobuz.
No audio or preview URLs are stored/exported, and no library/playback API is used.

Ignored mutable state/pages live in `.spotify-poc/tracks/`; shared whitelisted
metadata is `data/spotify_pilot_tracks.json.gz`. `--restore` restores complete
album caches from that archive without authentication, refusing conflicting files.
`--fetch --sp-python PATH` explicitly fetches missing scope albums using an
installed SP environment. It does not use the placeholder client-secret values.

## Spotify findings

`data/spotify_pilot_audit.json`, reproduced by
`python scripts/spotify_pilot_audit.py`, records title/artist-list evidence for all
ten selected cases. Two partial programmes are confirmed directly from tracks:

| Release | Existing label | Selected album | Missing target material |
| --- | --- | --- | --- |
| 1012732, Brahms collection | Probable | Karajan: Brahms Symphony No. 1, four Op.68 movements | Symphonies 2–4, violin concerto, German Requiem and Haydn Variations. |
| 6119238, Dvořák Sixth / My Home | Found | Dvorák: Symphonies Nos.4-6, fifteen tracks | My Home Op.62. Extras are Nature's Realm Op.91, Carnival Op.92 and Scherzo capriccioso Op.66. |

The other eight remain unresolved for recording validation, not automatically
confirmed or rejected. Strict title matching has single-word opera, translation,
catalogue-alias and split-heading gaps. The audit guards against reusing these
manual partial-programme conclusions if their underlying evidence changes.
This nonrandom sample is not a population error-rate estimate.

Spotify publication labels/data have not been silently corrected. A programme-
completeness warning/scoring guard and a broader audit are proposed next work.
The evidence now demonstrates why Spotify's higher match count cannot itself be
read as a better catalogue or more accurate matching.

## Validation and status

All 58 mocked/offline tests pass, including target position/range/global-credit
retention, hierarchy preservation, ranking semantics, strict Spotify pagination,
no-retry/redaction and conflict-safe portable restoration. Existing 76 selected
Qobuz statuses and all 740 release labels are unchanged. Build/UI tests pass;
Qobuz regeneration is byte-identical and token-value scans of exports pass.
No API warnings encountered. All work after the existing checkpoints remains
uncommitted/unpushed. No automatic further fetching, merge or deployment.
