# Sonoteque-style explorer

Status: implemented; user requested main merge and publication.
Backlog: AD-005. Branch: `codex/sonoteque-ui`.

## Agreed scope

Replace the old card/grid UI with a compact table. Give collection browsing and
Spotify match review equal emphasis. Retain search, composer, label, genre/style,
decade, sorting and direction. Open dedicated album details containing full
credits, tracks, Spotify candidate/alternates, and external links. Show Qobuz only
as a search link in details. Keep the existing static build and data pipeline.

## Reference and implementation

Sonoteque's `src/sonoteque/web/templates/base.html`, `classical/index.html`,
`_album_cells.html`, and album detail template supply the visual reference:
paired theme colors, system font, 24px heading, slim sticky header, 48rem shell
expanding to 90rem at 1536px, 32px table covers, small muted metadata, thin rules,
4px controls, and violet accents. Implement those styles in local CSS without
adding Tailwind CDN or a framework dependency.

Reuse normalization/query logic. Replace cards with table rows and hash-routed
detail views. Preserve filters in detail links and on return. Identify collection
copies by release and instance ID, falling back to occurrence for missing instance
IDs. The fallback is stable for unchanged source ordering, not across refreshes
that reorder duplicate copies without instance IDs; AD-004 remains separate.
On small screens hide year/artists columns; all metadata remains in details.

## Validation

- JavaScript syntax check, existing 741-release normalization/query tests, build.
- Browser: 741 rows, Spotify missing filter (210), combined composer/label/style/
  decade filter (one result), sorting, detail navigation and preserved filters,
  empty search and clear action.
- Visually inspect table and detail views, mobile layout and both themes;
  inspect console errors. No scoring/data changes or full Python rerun needed.

## Remaining scope

Full offline matcher/UI tests and build pass before publication. No playback, manual match editing, or new matcher behavior.
