# Multi-select picker prototypes

14November2026. User requested interactive UI options before choosing an approach.
Local comparison: /prototypes/multi-select.html. Prototype only, no main-filter
behaviour or URL-state changes. Build includes prototypes for reproducible review.

A: compact immediate checklist, summary in field. B: searchable immediate checklist
with removable selection chips. C: side panel with draft selections, cancel and
apply, plus draft result count. All six filters: Spotify/Qobuz status, composer,
label, genre/style, decade. Search and sort remain separate/single purpose.
All use real741-copy data. OR within a filter, AND across filters; no selections
means any value. Counts show global frequencies, not faceted remaining counts.
No persistence in these prototypes. Each option has independent state.

Starting recommendation A for short status/decade lists; searchable B-style
interaction for long composer/label/genre lists. User has not selected a design.
Keyboard uses native buttons/checkboxes, Escape dismissal and panel focus trap;
production implementation needs complete accessibility/responsive review.

Verified in browser: A Found+Probable=527copies, B Brahms search/selection=43,
C draftFound=254 and apply updates preview. Screenshot saved locally. Node syntax,
existing explorer normalization and make build pass. Qobuz worker unchanged.
Next: user chooses preferred interaction; implement shared multi-select filtering
and URL state only after that choice, preserving existing single-value links.

## Option B selected and implemented

User selected searchable pickers plus removable chips for all six filters.
Production implementation `explorer/multi-picker.js` uses native checkboxes,
search, clear-per-filter, outside-click/Escape dismissal, focus return, and
viewport-positioned menus. Scoped checkbox dimensions fix the prototype's global
input-width/label-style collision. Menus live outside the grid to avoid clipping.

Filter state uses arrays; query keeps legacy scalar compatibility. URLs use
repeated parameters, e.g. `#sp=found&sp=probable`; existing single-value URLs work.
OR within and AND across filters. Clear preserves layout. Frequency ordering
remains active; global option counts and selection chips preserved when reordered.
Search and sorting remain single-purpose controls. No service/matching changes.

Validated: Node normalization plus OR/AND/empty/legacy regression checks, JS syntax
and build pass. Browser real-data527Found+Probable,29withBrahms,527afterchip removal;
search and Escape dismissal exercised. Page reload preserves repeated URL values.
Prototype remains available for reference; production main filters now use B.
No commit, push or deployment requested. Qobuz retrieval left running separately.

## Per-picker order controls prototyped

User requested pushing6a48d70 (completed) and comparing replacements for the
single frequency switch. Local `/prototypes/picker-order.html` shows three open
composer pickers: A segmented Most frequent/A–Z, B Alphabetical checkbox,
C explicit Order select. All default frequency; selection and search survive
reorder, independent per picker. Real case-deduplicated composer counts.
Browser verified each alphabetical mode, A Beethoven selection retained, and
B remained frequency while only A changed. Build passes. Screenshot saved.
Recommendation A for explicit/discoverable choice. No option chosen yet; main
frequency toggle unchanged. No commit/push of these new prototypes requested.


## Footer ordering selected and implemented

User chose ordering optionB with checkbox between selected count and clear.
All six production picker footers now show count / Alphabetical / Clear selection.
Unchecked defaults to frequency; checked uses locale-aware case-insensitive
alphabetical order, numeric comparison. Each picker remembers its own order
while the page stays open, including closing/reopening; reload defaults frequency.
Selection and search survive reordering. The general toggle is removed.
Browser verified Composer A–Z retains Beethoven while Qobuz independently stays
frequency; reopening Composer retains A–Z. Global toggle absent. Node existing
filter regressions, syntax and build pass. No commit/push requested.
