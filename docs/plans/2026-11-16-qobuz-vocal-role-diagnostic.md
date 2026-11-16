# Compact vocal-role semantic and impact diagnostic

16November2026, Europe/Amsterdam. User authorized continuing the proposed bounded
vocal-role diagnostic. This is not live policy adoption or automatic promotion.
No Qobuz requests, shared cache/source rewrites, fuzzy identities or role waivers.

Current parser recognizes Soprano/Tenor/etc tokens but not their compact provider
Vocalist spellings. Experimental exact whole-role mappings are isolated in
`scripts/qobuz_vocal_role_diagnostic.py`, never imported by matching code. It
rewrites temporary copies only, preserves names/other roles, scans the2100album
cache and joins saved publication/unmatched candidate references across740targets.
Measure both gains and regressions, complete programme diagnostics, accepted
results and existing holds. Candidate improvement is not recording acceptance.

Primary inspection: DDEX current RDR defines Vocalist as vocal performance, with
SopranoVoice separately in its index. The inspected current dictionary/index did
not contain SopranoVocalist or TenorVocalist. Do not represent the provider's exact
compact spelling as a verified DDEX contract. Composer, producer, generic Artist,
associated roles and substring guesses remain excluded. Provider/raw-source
semantic corroboration and negative cases are needed before any live change.

## Results

Across2100cached albums,178contain4990tracks with10550exact compact vocal-role
declarations covered by the hypothesis. Most names already have another accepted
role or are not required by a source; declaration totals are not blocked matches.
The saved-reference universe is2597candidate/release pairs across740targets;
259pairs on157unique releases reference affected albums.

Only1989694/4268630gain source-unit coverage, both previously held Solti
Rheingold releases. Gains are partial:1→3of31units and0→2of22. Neither programme
is complete. Both retain PaulKuen/PaulKuentz and source/programme blockers.
No candidate status/confidence changes, no new complete unit support and no
coverage regressions in this bounded experiment. This is not a population
accuracy estimate. Production roles and all publication/workflow labels remain
unchanged. Defer live vocal normalization as an enrichment priority.

`data/qobuz_vocal_role_diagnostic.json` preserves the census, track fingerprints,
exact role substitutions, baseline/experimental programme and completeness
results, source hashes and caveats. Primary-standard observation is under
`data/review_sources/vocal-role-semantics/`. Reproduce with
`uv run --with requests python scripts/qobuz_vocal_role_diagnostic.py`.
Five regression tests cover exact fields, names, technical/associated exclusions,
copy immutability, whitespace and reference scope. Full281script tests pass.
No provider, source/cache, matcher, score, publication or UI changes.

## Higher-yield next direction

The explicit work-field hypothesis was then tested on the separate179unreviewed
work/title cases; see [frozen title179 diagnostic](2026-11-16-qobuz-title179.md).
It yields28leads for source-bound recording review. The role experiment itself
makes no promotions or new review decisions.
