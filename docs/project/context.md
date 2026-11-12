# Ali Discogs

Updated: 2026-11-12, Europe/Amsterdam

Match Ali's Discogs collection (`ajozi`) against Spotify and browse the results
in a static explorer. See [README](../../README.md) for setup and matching rules.

## Current state

- Checkout: `main`, tracking `origin/main`. Application baseline: `99589fb`.
  Inspect Git for subsequent changes and publication status.
- Committed dataset generated 2026-11-11: 741 collection copies; Spotify has
  255 found, 276 probable, and 210 not found. Qobuz has 741 unchecked.
  Source: `data/summary.json`; these are saved results, not a fresh match run.
- Explorer supports search, filters, sorting, grid/list views, match candidates,
  track lists, and links to Discogs, Spotify, and Qobuz searches.
- `make serve` builds `dist/` and serves on localhost:8000. The UI was started
  and opened on 2026-11-12; the browser displayed all 741 releases. A server's
  continued availability must be checked when resuming.
- GitHub Actions definitions cover tests and GitHub Pages deployment. README
  lists public URLs; live deployment availability has not been verified here.

## Limitations

- No Qobuz matcher exists. The imported documentation reports HTTP 403;
  access has not been rechecked in this session. Unchecked does not mean absent.
- Match classifications are algorithmic results, not a completed manual audit.
- The test suite has not been run in this session. Existing CI expectations
  pin the offline Spotify totals to 255 / 276 / 210.

## Active work and next action

Project documentation was established at the user's request on 2026-11-12.
No application implementation task is currently agreed or in progress.

Recommended next action: select a bounded sample for the proposed
[AD-001 match-quality audit](backlog.md#ad-001--audit-spotify-match-quality).
The backlog entries are suggestions, not authorization to execute them.

## References

- [Backlog](backlog.md)
- [Decisions](decisions.md)
- [History](history.md)
- [Implementation plans](../plans/README.md)
