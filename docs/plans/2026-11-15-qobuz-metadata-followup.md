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
