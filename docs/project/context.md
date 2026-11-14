# Ali Discogs

Updated: 2026-11-14, Europe/Amsterdam

Browse ajozi’s Discogs collection and review Spotify/Qobuz matches in a static
explorer. [README](../../README.md) owns setup and architecture;
[Qobuz guide](../qobuz.md) owns evidence/cache commands.

## Current state

- Branch `main`; pushed through `7945944` (filter band, pin control and sticky
  table headers). Retrieval complete; first offline screen/audit complete. Deployment not verified.
- Collection: 741 copies / 740 unique releases. Current saved labels: Spotify
  254 Found / 273 Probable / 210 Not found / 4 Unchecked; Qobuz
  12 Found / 116 Probable / 613 Unchecked copies (14 November snapshot).
- Spotify’s legacy album-level labels and stricter Qobuz evidence levels are
  not comparable accuracy or catalogue-coverage measurements. Both status and
  score are saved data. Qobuz 95/85 are heuristic levels, not probabilities.
  [Validation gap](../plans/2026-11-13-cross-service-validation-gap.md).
- Qobuz publication is separate: `data/qobuz_matches.json`; Spotify results live
  in `data/collection_matches.json`. Portable evidence and successful request
  archives support offline work; credentials and live run state stay ignored.
- UI: ajozi vinyl + small on Discogs link; Table, Captions and Shelf views.
  Six searchable multi-select filters use OR within a field / AND across fields.
  Each picker defaults to frequency order with its own Alphabetical checkbox.
  Search follows Decade; Clear follows Search. Table sorts all columns;
  Captions/Shelf offer Year and Composer beside the result count.
- Local server: http://127.0.0.1:8000/ . Live site:
  https://sigmus.github.io/ali-discogs/ . Latest deployment not checked here.

## Filter actions

- Adopted outlined treatment A, Clear3 (filter/cross) and Pin1 (upright).
  Both after Search; pin removed from header. Tooltips/accessible names on both,
  theme tooltip follows current action; layout icons retain their titles.

## Filter surface and pin

- User selected A: lighter full-width filter band with bottom border implemented.
  Pin beside Clear toggles sticky filters below measured header;
  default unpinned, page-lifetime preference, hidden on detail pages. Table
  column headers always stick below the header/optional pinned filters.

## Detail UI

- User chose C: catalogue sidebar implemented locally. Cover/facts left;
  artist/title, tracklist, credits and existing service evidence right. Stacks
  on mobile. Albums back button removed. No new source data or match changes.
- Track positions/types/durations retained when saved; country/released shown.
  Schumann7946604 still has only a work heading in the saved source.

## Retrieval and follow-up complete

- Fixed 12 +305 scope completed14November16:02Amsterdam:83 metadata albums,
  1,313tracks;603queries,520nonempty/83empty.299/305releases have a hit,
  6remain empty. Hits are leads, not accepted matches.
- Verified every manifest task, album ID and full unique track count. Offline
  exports saved in `data/qobuz_remaining_{metadata,search}.json.gz`.
- Shared request archive exported/validated:2,488responses, all1,857 prior
  members byte-preserved. Canonical index1,148URLs;5URL tests pass.
- Follow-up9albums/216tracks complete18:36Amsterdam;11HTTP attempts including
  discovery, no warnings. Request archive2,497responses (all previous preserved),
  canonical index1,157URLs. Both runs stopped normally; sleep assertion ended.
- Retrieval exports and first reviews committed locally, not pushed. See
  [run plan](../plans/2026-11-14-qobuz-remaining-retrieval.md).

## Offline follow-up checkpoint

- Screened2,227pairs:14complete programme/credit leads,
  345cached unresolved pairs,1,868pairs missing full metadata. Eighteen new
  Probable releases now published locally after bounded reviews.
- Michelangeli sonata3285095/Concerto1 3672809 and Gilels7914875 completed.
  Nine Beethoven plus Chopin Op.11 inventory additions;145script tests pass.
- [Offline plan](../plans/2026-11-14-qobuz-offline-followup.md) owns findings and
  exact next steps. Two network-forbidden/fail-closed regression tests pass.

## Agreed next sequence

1. Retrieval/export complete; preserve shared evidence and source fingerprints.
2. Rank and rerun Qobuz matching offline using available evidence. New search
   hits without full metadata remain leads, not accepted matches.
3. Audit promising and uncertain cases. Improve reusable rules where evidence
   supports them; add meaningful regressions against known false positives.
4. Regenerate publication data, inspect details/status consistency and build.
   Preserve unresolved cases and visible edition/recording limitations.
5. Then plan comparable evidence checks for Spotify; broader Spotify retrieval
   and any collection-wide relabelling need a concrete bounded scope first.

Prefer reliable matches to higher counts. Retrieval does not authorize unbounded
new-hit downloads, automatic promotions, pushes or deployment. Bitches Brew’s
credit exception remains a proposal. Preserve source/hash-bound review safeguards;
never loosen credits or invent recording identity to improve a count.

Next action: review Katchen6265501’s13listed pieces using cached source.
Schnabel4352998 now Probable: Op.54 partitioned by side, no reused movement;
source Op.49No.1 G-major discrepancy disclosed against Henle G minor.
Katchen8836514 source lists only6Op.116pieces and has key/text conflicts;
1697514 saved Paganini says1965 versus publisher1966: audit before promotion.
Current612unchecked unique.145script tests/UI normalization/build pass.
No Qobuz calls, push or deployment. Nabucco/Mozart credit gaps remain.
[Backlog](backlog.md), [decisions](decisions.md), [history](history.md).
