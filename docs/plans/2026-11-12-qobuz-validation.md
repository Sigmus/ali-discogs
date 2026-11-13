# Small Qobuz validation sample

Date: 2026-11-12, Europe/Amsterdam. User-authorized metadata review only.

## Scope and method

Four new album/get records, chosen from existing first-pass search results,
plus two cached controls. No searches repeated. New network requests (including
app-ID discovery) spaced at least 15 seconds apart; no retries. All four album
responses succeeded with complete advertised track lists: 8, 10, 20 and 50 tracks.
Evidence is preserved in ignored `.qobuz-poc/validation-small/` and the shared
request cache. Reproduce/resume with `uv run scripts/qobuz_validation_sample.py`.
A STOP marker blocks new requests; remove only after user direction if a warning
occurs. The script does not accept matches or write collection results.

Compared Discogs work headings and performer/conductor/orchestra credits against
full Qobuz track titles and role-labelled credits. These six deliberately chosen
cases test failure modes; they do not measure collection-wide accuracy. Review
is catalogue evidence, not listening or independent recording-session verification.

## Evidence and outcomes

| Discogs release | Qobuz candidate | Review outcome |
| --- | --- | --- |
| 1855288 — Liszt, Kempff/Fistoulari, concertos 1 & 2 | zccb3oe0za3sb | Strong programme/performer candidate: both concertos, S.124 and S.125, across eight digital tracks; every track credits Kempff, Fistoulari and London Symphony Orchestra. Discogs has two work headings rather than eight movements. Different reissue label does not by itself reject a match. Recording-session identity remains unverified. |
| 7001990 — Bach, Klemperer, Four Suites | 3610154955247 | Reject as a complete-album match: only suites 3/4 (BWV1068/1069), ten tracks, though Klemperer and Philharmonia credits agree. Missing suites 1/2. This rejects this candidate, not every search candidate or the release's availability. |
| 8121703 — Landowska, Twenty Harpsichord Sonatas | ujhzfrl46gycc | Unresolved: twenty tracks and Landowska/Scarlatti credits agree, but Discogs groups pieces under Longo L. numbers while Qobuz uses Kirkpatrick K. numbers and a different order. Require a verified catalogue concordance and complete programme comparison; equal count/title/artist is insufficient. No correspondence inferred from number similarity. |
| 5820114 — Gilels/Szell, Five Piano Concertos | v97lzb7cicexb | Strong programme/performer candidate: all five concertos (Op.15/19/37/58/73), plus three variation sets matching the descriptions, in 50 tracks. Concerto tracks credit Gilels, Szell and Cleveland Orchestra; solo variation tracks credit Gilels. Discogs uses older G.182/G.191 designations for two sets while Qobuz uses WoO71/80; descriptions agree but catalogue equivalence is not independently established here. Treat as probable programme match pending catalogue/session confirmation. |
| 15282801 — Kleiber/Concertgebouw, Eroica (cached negative control) | ezfmmvuhlu4uc | Reject: track credits name Wiener Philharmoniker rather than Concertgebouw, despite matching conductor and work. |
| 1445439 — Gould, Byrd/Gibbons (cached positive control) | 0886445075762 | Strong programme match: all eight named pieces in the same order and Gould credited on every track, despite different digital album title. Recording-session identity remains unverified. |

No Found/100% scores assigned: this sample provides three strong candidates,
two candidate rejections and one unresolved case, not calibrated percentages.
Raw metadata may contain additional useful identifiers, but Discogs evidence
must also support recording identity before claiming certainty.

## Rules supported by this sample

- Compare programme coverage at work/movement level; LP headings and digital
  tracks differ in granularity. Track-count equality is neither required nor sufficient.
- Require relevant performer, conductor and orchestra agreement on the matched
  tracks; separate solo items from orchestral tracks and ignore producer credits.
- Distinguish missing works from extra material on a reissue/compilation.
- Normalize catalogue aliases only with verified mappings; unresolved aliases
  must not produce an automatic acceptance.
- Preserve candidate rejection separately from release-level Not found. Empty
  searches and failed API requests cannot establish catalogue absence.

## Next bounded step

Implement an offline evidence normalizer and repeatable checks against these
cases before expanding metadata retrieval. Keep unresolved cases visible and
reviewed evidence separate from generated Spotify results. Broader scoring,
full-collection metadata retrieval and production publication remain future work.
