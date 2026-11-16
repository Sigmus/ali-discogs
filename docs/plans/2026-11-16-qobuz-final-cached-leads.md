# Final two supported cached leads and blocker grouping

16 November 2026, Europe/Amsterdam. User authorized continuing the recommended
Schubert9283162 and Mozart15660391 cached reviews, followed by grouping unresolved
releases by shared blockers. No new Qobuz calls or metadata expansion. Preserve
all source credits, prior holds and Spotify. Use existing scoped review kinds;
positive recording-family evidence is required. Grouping is diagnostic and does
not authorize broad identity/role waivers. Save exact decisions, validate the
publication diff and refresh queues/docs before a local checkpoint.

## Completed reviews

- Schubert9283162 → Probable85: five raw source bands map to cached Decca4307732.
  Archival Decca discography V213 explicitly links SXL6090 and the1991CD to the
  Kertész/Vienna October1963 session. Preserve raw B1 “Luftschloss”; bind to
  D84 “Lustschloss” only within this exact review. All three overtures and both
  Unfinished movements retain positive composer/conductor/orchestra credits.
- Mozart15660391 → reviewed, unresolved: six source concertos20/21/23/24/26/27.
  The credited21/27 album is partial; the four-concerto album lacks24/26 and
  orchestra credits. The complete-cycle tracks omit English Chamber Orchestra
  for five required concertos. No borrowing credits across works or albums.
- All twelve cached alternatives have frozen hashes/title inventories. Six
  uncached saved hits remain outside scope; they are not claimed reviewed or
  absent. Exact LP transfer, mastering and takes remain unverified.

`data/qobuz_final_cached2_recording_audit.json` preserves the two decisions,
source programmes, alternatives and next actions. Reproduce with
`uv run --with requests python scripts/qobuz_final_cached2_audit.py`.
Publication diff: one Unchecked→Probable plus one explicit review-progress field;
all other release payloads and collection/Spotify bytes unchanged.265script tests,
normalization and static build pass. No Qobuz calls or push/deployment.

## Shared blocker grouping

`python3 scripts/qobuz_blocker_groups.py` rebuilds
`data/qobuz_blocker_groups.json` from the unmatched inventory/publication and
completed review reports.565unique unresolved releases:204saved unresolved
reviews and361without a saved decision. UI counts include one additional copy:
12Found/163Probable/204Reviewed · unresolved/362Unchecked.

The unreviewed361split by current programme evidence:

-179work/title/catalogue mapping unresolved: no work support under current rules.
-171credit support unresolved: a work is recognized, but no programme item has
 accepted credits. This may reflect source roles, performer identity, provider
 metadata or a different recording—not proven missing credit alone.
-6without a cached candidate and5partial/completeness cases.

Across all565, label-based planning families group221credit,179work/title,
64source/programme,34recording identity,56other saved blockers,6no candidate and
5partial/completeness. These families are keyword-based planning aids; preserve
individual saved findings as authoritative. Counts are not promotion estimates.
Next use a bounded sample of171credit cases to identify a repeated cause before
proposing any collection-wide rule. Source-role/associated-credit policy changes
remain unadopted; no new calls follow automatically from this grouping.
