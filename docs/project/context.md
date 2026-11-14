# Ali Discogs

Updated: 2026-11-14, Europe/Amsterdam

Browse ajozi’s Discogs collection and review Spotify/Qobuz matches in a static
explorer. [README](../../README.md) owns setup and architecture;
[Qobuz guide](../qobuz.md) owns evidence/cache commands.

## Current state

- Branch `main`; UI changes pushed through `749ba61`. Retrieval code, fixed scope, completed metadata export and planning docs are
  included in the next local commit; search remains in progress. Check Git before continuing.
- Collection: 741 copies / 740 unique releases. Current saved labels: Spotify
  254 Found / 273 Probable / 210 Not found / 4 Unchecked; Qobuz
  12 Found / 98 Probable / 631 Unchecked copies (14 November snapshot).
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

## Active retrieval — do not restart or speed up

- User authorized 12 metadata-needed releases + 305 previously empty releases:
  83 distinct candidate albums, then 603 new queries. See
  [run plan](../plans/2026-11-14-qobuz-remaining-retrieval.md).
- Run state/log: `.qobuz-poc/remaining-2026-11-14/`; metadata complete 83/83.
  Search checkpoint at 14:11 Amsterdam: 124/603, running, no warning in log tail.
  These are dated observations; read progress files for current status.
- Hourly ETA monitor: `qobuz-remaining-retrieval-progress`; idle-sleep assertion
  attached to worker. Preserve checkpoints, caches and credentials.
- On API/auth/rate-limit/network/pagination warning or unexplained stall >5min
  outside a planned rest: root and active-phase STOP, report evidence and ask.
  Never retry/resume after a warning without the user’s answer.

## Agreed next sequence

1. Finish retrieval; verify all outputs/counts/track completeness and export
   portable evidence plus validated request archive/canonical URL index.
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

Next action: monitor the existing worker, then validate/export its completed
outputs before the offline audit. [Backlog](backlog.md), [decisions](decisions.md),
[history](history.md) preserve priorities, policy and completed work.
