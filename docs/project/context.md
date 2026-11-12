# Ali Discogs

Updated: 2026-11-12, Europe/Amsterdam

Match Ali's Discogs collection (`ajozi`) against Spotify and browse the results
in a static explorer. See [README](../../README.md) for setup and matching rules.

## Current state

- Redesign developed on `codex/sonoteque-ui`, based on documentation commit `3c2d393`.
  User authorized merging to main and pushing on 2026-11-12.
  Application baseline: `99589fb`.
  Inspect Git for subsequent changes and publication status.
- Committed dataset generated 2026-11-11: 741 collection copies; Spotify has
  255 found, 276 probable, and 210 not found. Qobuz has 741 unchecked.
  Source: `data/summary.json`; these are saved results, not a fresh match run.
- Explorer now uses a Sonoteque-style table and dedicated details, with search,
  filters, sorting, match candidates,
  track lists, and links to Discogs, Spotify, and Qobuz searches.
- `make serve` builds `dist/` and serves on localhost:8000. The UI was started
  and opened on 2026-11-12; the browser displayed all 741 releases. A server's
  continued availability must be checked when resuming.
- GitHub Pages now uses the GitHub Actions source (`build_type: workflow`).
  Live site verified on 2026-11-12: album UI loads all 741 rows, without status
  tabs or status hyperlinks. Deployment run `43231078310` succeeded.

## Limitations

- No Qobuz matcher exists. The imported documentation reports HTTP 403;
  access has not been rechecked in this session. Unchecked does not mean absent.
- Match classifications are algorithmic results, not a completed manual audit.
- Full offline Python matcher and UI normalization/query tests pass on
  2026-11-12, along with the static build. Existing CI expectations
  pin the offline Spotify totals to 255 / 276 / 210.

## Active work and next action

Implemented AD-005 locally: table only, equal browsing/Spotify-review emphasis,
dedicated details, all requested filters retained, Qobuz search link in details.
Sonoteque theme tokens and component measurements are used in standalone CSS.
The main container is capped at 80% of the viewport per user preference.
Browser verified filtering, details/return, empty state, mobile and both themes;
loader/query tests and build pass. No application data changed.
Dropdowns now use Sonoteque’s exact `.view-select` CSS and SVG chevrons,
verified in both themes. Filters use equal-width grid columns, Clear follows
Sort, and the A to Z button is removed. All named table headers now toggle
ascending/descending sorting with Sonoteque’s triangle indicators; the Sort
selector stays synchronized. Spotify sorts by status then confidence. Spotify cells display confidence and status inline, e.g. `100% (Found)`.
Status tabs have been removed; Spotify filtering remains in the dropdown.
Table metadata/status are plain text; title and cover open details. Static
detail labels use neutral colors so they do not resemble hyperlinks.
Redesign committed as `c0ed7a3`, fast-forwarded into main and pushed to origin.
Follow-up UI commit `8e9f638` is pushed and deployed. The previous branch-root
Pages source served the README; switching to Actions fixed publication.
[Plan and validation](../plans/2026-11-12-sonoteque-ui.md).

## References

- [Backlog](backlog.md)
- [Decisions](decisions.md)
- [History](history.md)
- [Implementation plans](../plans/README.md)
