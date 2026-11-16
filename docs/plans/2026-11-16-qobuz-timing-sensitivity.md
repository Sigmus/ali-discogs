# Timing sensitivity and approved Gould exception

16November2026. User identifies Gould2548602as the same album and asks whether
per-track tolerance or album-wide agreement should change, and how many other
albums could qualify. This is a read-only impact check; no promotion authorized
by a policy question, no published match/source/cache change or new Qobuz call.

`uv run --with requests python scripts/qobuz_timing_sensitivity.py` evaluates
all30existing full source-leaf review mappings at the pre-approval checkpoint
(29Probable,1held). Saved composer,
source-band and musician checks still run. It does not invent maps for generic
holds. Results/fingerprints are in `data/qobuz_timing_sensitivity.json`.

| Scenario | Held cases clearing timing gate |
| --- | --- |
| Current max5seconds/3% |0|
| max5seconds/5%,10%or20% |0|
| max5seconds/35% |1:Gould2548602|
| max15seconds/3% |0|
| Illustrative album consensus |1:Gould2548602|

No previously accepted mapped review regresses in these scenarios. This is not
a false-positive/accuracy estimate or a whole-catalogue promotion count.
Eleven other held reviews mention timing but lack a frozen complete leaf map:
12690141,22222342,10552903,2394378,2636984,9703869,8860718,13166114,5349319,
7946604,16108064. Their source structure, cast, transfer/session or other issues
remain; mentioning timing is not evidence that tolerance is their only blocker.
Other review kinds and unmapped cached candidates are outside numeric sensitivity.

Gould:14/15bands fit a15second/3%close gate; C5differs65seconds (31.4%of saved
207seconds).5%,10%or20%global tolerances therefore do not clear it. The consensus
experiment requires at least10timed bands,at least90%close,only1outlier up to90s/
35%,and summed absolute band error at most3%of the timed programme. These values
are illustrative, not calibrated or proposed for automatic bulk acceptance.

Recommendation: keep the strict baseline; permit an explicit hash-bound reviewed
timing exception when the full programme, positive cast and recording identity
are independently supported. Record the user’s album identification and exact
source/digital discrepancies; do not call those verified transcription errors or
claim audio listening/exact takes. Majority agreement is supporting evidence,
never permission to ignore missing music, wrong cast/instrument or source bands.
A global35%per-track rule is not recommended. Existing source_duration_notes can
express a reviewed exception; this analysis does not add one.

Three scenario tests pass: minimum corroboration/one-outlier limit,absolute-error
aggregation without cancellation,and absent-duration non-applicability. All saved
publication/ledger/collection byte hashes unchanged. No push/deployment.

## Approved recording-specific exception

User subsequently authorized the recommendation: Gould2548602is now Probable85
with exact source_duration_notes for B4 230/219s,C5 207/142s,D3 220/227s. All15
bands, positive musician/composer checks and source/album/track hashes retained.
No global35%or consensus policy adopted. The original hold and user confirmation/
approval are saved in `data/review_sources/gould-2548602-timing-exception/approval.json`;
that evidence file is itself hash-bound in the review ledger. No transcription
error or audio/exact-take verification asserted. The pre-approval sensitivity
report remains unchanged as dated evidence; rerunning uses the current ledger.

Only Gould’s publication record changes. All304script tests, normalization/static
build and local browser Probable/disclosure checks pass. Global scorer/tolerance,
raw sources, shared caches and Spotify bytes unchanged. Queue now2resolved/1held.
No Qobuz calls, push or deployment. Next suggested work:21cached work-title cases
with missing musician evidence, not blanket tolerance relaxation.
