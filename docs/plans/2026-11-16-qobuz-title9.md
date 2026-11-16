# Nine leading explicit-work title candidates

16 November 2026, Europe/Amsterdam. User authorized one complete batch without
routine confirmation. Frozen IDs: 2845131,4431461,8567942,8860718,11883662,
11885637,11887204,13166114,16996626. Inspect all saved alternatives and original
source programmes, credits, dates, instruments and timings. No Qobuz requests,
production title/credit rule change, fuzzy identities or automatic promotions.

Use existing hash-bound source-leaf recording reviews for eligible programmes;
record explicit holds otherwise. A programme containing only movements II–IV or
movement I remains that LP programme, never an invented whole-symphony match.
Retain alternative cycles, source discrepancies and reissue/transfer limitations.
Validate the entire batch, publication diff, tests, static build and local UI;
refresh queues/docs and commit locally. No push/deployment.

Status: complete; all nine decisions saved, validated and published locally.

## Decisions

Six recording families qualify as Probable85 under existing source-leaf reviews:

-4431461 Gould: official1983album index, eight source bands and matching production
 credits; every printed timing fits existing tolerance.
-8567942 Toscanini Fifth/Eighth: select older RCA0828765570220with positive orchestra
 roles, not the associated-only diagnostic candidate. Preserve the joined LP
 third/fourth movement band. Source1952broadcast and publisher cycle evidence agree.
-11883662 Toscanini Ninth: source1952session dates and documented RCA cast match;
 map only movementsII–IV. MovementIis a digital extra, not a missing LP band.
-11885637 Toscanini Eighth/NinthI: source dates agree with publisher documentation;
 retain the source Allegro/Allegretto scherzando wording difference.
-11887204 Toscanini Fourth/Fifth: use later RCA cycle, not1939diagnostic best.
 Source1951/1952dates agree. Preserve raw Fourth finale Adagio versus digital/
 publisher Allegro discrepancy in the exact source-band mapping.
-16996626 Rubinstein Emperor: all three old RCA63036tracks have positive piano,
 conductor/orchestra and Beethoven-only composer roles. Institutional catalogue
 and contemporary RCA-session eyewitness text support the1956recording family.

Three explicit holds:

-2845131 Rubinstein First: old RCA adds Busoni Composer on all three tracks;
 modern alternative supplies orchestra only as Associated Performer.
-8860718 Toscanini Seventh: no saved source session/timing evidence binds Italian
 A12R-0005to the later RCA rather than another recording family.
-13166114 Toscanini Eroica: source1980issue date does not choose between1939and
 later RCA recordings; obtain original sleeve/label session or master evidence.

Primary-source observations are saved under `data/review_sources/title9-*`.
Gould’s album index and Pristine publisher pages were read directly; the Gould
individual detail page and National Library page were limited, so recording claims
there use explicitly identified indexed primary text. No audio downloaded.
Raw sources, caches, Spotify and global title/credit rules remain unchanged.
Exact LP pressing/takes/mastering remain unverified in all six accepted families.

Reproduce frozen decisions with `uv run --with requests python
scripts/qobuz_title9_audit.py`. All285script tests, normalization/static build, nine-case frozen audit and exact
publication comparison pass. Only these nine release records changed:6Probable85,
3workflow holds. Local browser verified all nine detail states; the only console
error was the existing missing favicon. No functional UI errors observed.
Qobuz copies:12Found/172Probable/225Reviewed · unresolved/332Unchecked.
Underlying Unchecked557copies/556unique. All provider caches, raw sources,
Spotify/collection and production scorer bytes remain unchanged. Title queue now
19pending(13completeness/6partial),6resolved,3held. No push/deployment.
