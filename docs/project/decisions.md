# Decisions

## 2026-11-12 — Repo-local project documentation

Status: adopted by the user.

Keep current context, backlog, history, and durable decisions in `docs/project/`.
Use `AGENTS.md` to require reading context before work and maintaining it after
meaningful results. Use dated plans in `docs/plans/` only for substantial changes.

This combines CulturaFM's automatic upkeep with Sonoteque's separation of
current state and history. Keep context short; do not accumulate old handoffs.
The existing README remains the home for setup, commands, and architecture.
No separate roadmap or custom project skill is needed at this stage.

Backlog suggestions remain proposals until requested. Documentation upkeep does
not authorize implementation, commits, pushes, or external changes.

## 2026-11-12 — Sonoteque-style UI replacement

Status: adopted by the user.

Use Sonoteque's actual visual conventions. Table only, equal emphasis on browsing
and Spotify match review, dedicated detail views. Retain search, composer, label,
genre/style, decade and sorting. Qobuz is a search link in details; omit its
unchecked counts and filters from the main view. Feature parity with the previous
UI is not required. Work lives on `codex/sonoteque-ui`.

## 2026-11-12 — Preserve Qobuz enrichment as a resumable local PoC

Status: adopted for the user-requested PoC and handoff; production scoring and
collection writes remain proposed follow-up.

Use a local Qobuz user token and a pinned Sei969/qobuz-dl checkout for app-ID
discovery only. Share a catalogue-only adapter between single-query and batch
scripts; do not initialize the downloader or request audio/app secrets. Cache
successful responses outside Git with explicit offline/refresh modes. Persist
review evidence and distinguish recording/programme candidates from confirmed
album matches. Document token setup in .env.example without any real values.
The legacy Python client remains available for comparison, not the working path.

## 2026-11-12 — Show Qobuz search evidence in the explorer

Status: adopted by user request; supersedes the earlier search-link-only UI scope.

Show a Qobuz column and detailed cached candidates without treating search hits
as accepted matches. Use a minimal build-time sidecar keyed by Discogs release
ID so duplicate copies share evidence and Spotify rescoring cannot erase it.
Keep raw caches and credentials ignored; publication of review evidence is not
part of this local UI change.

## 2026-11-13 — Independent Qobuz publication overlay and cautious evidence levels

Status: adopted implementation of the user's matching/deployment-preparation request.

Keep versioned sanitized Qobuz output separate from generated Spotify collection
JSON, keyed by Discogs release ID. Build copies it without local caches/token.
Found/Probable scores are documented heuristic evidence levels, not calibrated
probabilities. Empty/inconclusive searches stay unchecked. Future reviewed manual
overrides must be separate, validated and take precedence over generated scores;
none have been accepted yet. Do not infer recording-session certainty from titles.

## 2026-11-13 — Commit portable Qobuz evidence for offline collaboration

Status: adopted by explicit user request so Ali can check out and work offline.

Version a deterministic compressed JSON snapshot of whitelisted catalogue fields,
complete searches/tracks/credits and provenance. Matcher reads it by default.
Keep raw request duplicates, third-party checkout, credentials, logs, locks and
STOP markers ignored. Publication builds copy only the UI match file, not the
research snapshot. Export updated evidence explicitly after authorized retrieval.

## 2026-11-13 — Share raw successful request caches too

Status: adopted by explicit follow-up user request, extending the portable snapshot.

Commit a deterministic archive of all successful request-cache JSON responses,
not merely selected evidence fields. Scan for credential values/sensitive keys;
exclude machine state, credentials and third-party source. Validated restoration
must preserve existing conflicting responses. Mutable local caches remain ignored,
and archives stay outside the Pages artifact. No network refresh implied.

## 2026-11-13 — Bounded offline coverage expansion

Status: adopted implementation of the user's continued matching-improvement request.

Reuse the shared snapshot before new API calls. A fixed reviewed candidate scope
limits publication expansion; it never overrides original credits or the new
completeness checks. Store independently sourced work expectations separately and
fingerprint both inputs in generated output. Expansion is capped at Probable 85%.
Do not enable experimental performer aliases or infer completeness from a sequence
starting at I. Explicit target movements and timed standalone tracks describe the
requested programme, not independently verified whole works or recording sessions.
The existing v1 baseline remains unchanged pending a separate retrospective audit.

## 2026-11-13 — Work-aware evidence without broad credit inheritance

Status: adopted implementation of the user's request to improve audited grouping.

Use explicit composer/work and contiguous movement context for the audited failure
modes. Group-based soloist participation requires stable conductor/ensemble support,
one explicit composer identity and no unknown extra musical main artists or mixed
performance runs. Recognize explicit vocal/chorus roles; do not invent missing
credits or enable general fuzzy aliases. Preserve the historical v1 evaluator for
comparison. Newly qualifying candidates require independent programme-completeness
evidence before promotion and are capped at Probable 85%. Metadata groups do not
establish session identity; unresolved old structures remain documented limitations.

## 2026-11-13 — Positive target scopes and shared sp authentication

Status: adopted implementation of user-requested query/credit/cache refinement.

Use only explicit cached Discogs work/position credits to specialize requirements;
retain unscoped, unparseable or ambiguous global actors. Candidate evidence must
not choose which target artists to discard. Preserve historical v1 target units
while current units recognize parent headings without losing standalone pieces.
Query relevance scores are discovery ranking, not accepted match confidence.

Reuse the existing sp PKCE login for bounded Spotify catalogue metadata rather
than copying secrets to this repo. Keep tokens in its subprocess/config cache,
refresh once with no retries, preserve credentials on failure and stop on warnings.
Share only whitelisted complete tracks, never tokens or audio/preview URLs.
Confirmed partial-programme observations remain separate from scoring changes;
no automatic correction or accuracy-rate claim from the ten-case sample.

## 2026-11-13 — Hash-bound pilot recording reviews

Status: adopted in the user-authorized four-lead validation.

Keep specific recording/programme judgements separate from general matching rules.
Portable review ledger hashes bind target inputs and full candidate metadata;
changed evidence requires re-review. Current work/credit checks and exact movement
coverage still run. One exact joined Schnabel track and one target-only Tennstedt
Adagio excerpt are permitted without globally loosening joined-movement parsing.
Three accepted leads remain Probable85%, with edition/session limitations visible.
Barenboim's conflicting recording cycle is recorded as rejected. See the
[four-lead review](../plans/2026-11-13-qobuz-lead-validation.md).

## 2026-11-13 — Withhold reviewed partial Spotify albums

Status: adopted in the user-authorized Spotify programme safeguard.

An explicit, hash-bound incomplete-programme finding takes precedence over album
similarity. Return Unchecked with no accepted album/public confidence; retain raw
signals, reviewed candidate, alternatives and missing-work explanation. Do not
silently promote an unaudited replacement or interpret this as catalogue absence.
Scope is the exact reviewed target/candidate pair; absence of a negative review
is not completeness approval. Changed evidence requires re-review. This supersedes
the earlier decision to leave the two pilot findings outside scoring.

## 2026-11-13 — Explicit replacements, broader negative reviews and Pages gate

Status: adopted in the user-authorized follow-up/readiness review.

A rejected Spotify candidate can be replaced only by a separate explicit positive
review with full portable track/source hashes and required-artist checks; cap
Dvorak's reviewed replacement at Probable85, with recording limitations. Negative
reviews may bind a separate bounded archive; never overwrite the original pilot
or infer programme absence from parser misses. Distinguish wrong programme from
partial programme in details. Unreviewed alternatives remain unaccepted.

Include programme-guard tests and portable follow-up verification in CI. Pages
must run local validation successfully before artifact upload and deployment;
separate test workflows alone do not gate its deploy job.

## 2026-11-13 — Preserve canonical Qobuz routes separately

Status: adopted in the user-requested link correction.

Use provider-supplied locale/slug album URLs from a separate shared offline index;
never synthesize bare www.qobuz.com/album/ID links. Keep matching evidence and
recording-review hashes immutable for presentation-only URL corrections. Validate
exact HTTPS host/path/album ID; absent URL evidence gets a search fallback.

## 2026-11-13 — Bound named-section and malformed-title reviews

Status: adopted in user-authorized Qobuz round2.

Exact target/candidate/track hashes may support reviewed named liturgical sections
without globally weakening movement parsing. A reviewed malformed work heading
may be interpreted canonically only inside that source-bound review, preserving
original text and original work-credit assignment keys. Recompute all required
performers and complete non-overlapping sections; cap additions at Probable85.
Conflicting catalogue/key information remains unresolved until specifically
reviewed; search recovery and correct musicians alone do not authorize a match.

## 2026-11-13 — Compare query strategies before broad expansion

Status: adopted for the authorized ten-release trial.

Use headline ensemble credits ahead of supporting individual players in new
queries. Compare paired performer/composer and catalogue-qualified queries on a
fixed disjoint scope; measure top-five search yield separately from validated
matches. Multi-composer mapping remains outside this trial. Preserve old query
manifests. Richter's source catalogue/key corrections are supported by Warner's
publisher documentation and hash-bound to one target/candidate pair; preserve
original work-credit lookup and require all3+5 movements. Cap at Probable85.

## 2026-11-13 — Cross-service validation standards must be disclosed

Status: documented limitation; shared replacement status model remains proposed.

Retained legacy Spotify album-level labels and stricter reviewed Qobuz labels
are not directly comparable coverage or accuracy measurements. Do not explain
count differences as catalogue/search superiority alone. Tristan2996680 shows a
Spotify Probable without full-edition confirmation. A later same-day Qobuz review
accepts the main three acts only; raw target includes rehearsal material.
Distinguish actual matcher blockers,
review observations and unverified Spotify track coverage. See
[validation gap](../plans/2026-11-13-cross-service-validation-gap.md).

## 2026-11-13 — Opera roles, ensemble names and act coverage stay source-bound

Status: adopted for the continued unmatched-release review.

A hash-bound opera review may equate two ensemble names only when the review
states the recording-specific reason. Chorus master is not director. Every
cached musical credit, including secondary singers, must remain in the review;
omitting one fails closed. Act labels can support a main-opera Probable85.
Scenes stay unresolved when the candidate uses incipits, and that limit must be
visible. A rehearsal or bonus side listed on the raw release stays an explicit
edition gap: Tristan's side J does not block the three acts and does not make
the LP box complete. A conflicting ensemble credit, a missing named singer, or
an unlabelled required scene withholds the album. No general alias table.

## 2026-11-13 — Prelude and fugue pairs stay hash-bound

Status: adopted for the Gould Well-Tempered Clavier review.

A container heading is not a separate work only when the review lists every such
heading from the cached source. Each remaining BWV needs its own prelude and
fugue, in source order, with the required pianist on both tracks. A title that
says only "Prelude" is accepted solely for a reviewed track immediately before
the fugue of that BWV. Cap at Probable85. A later recording cycle is not the
earlier one: EMI Barenboim volume 9866861 stays unmatched to DG 4631272.

## 2026-11-13 — A heading is a container only when every numbered piece remains

Status: adopted for the Michelangeli Chopin recital review.

A hash-bound review may treat source headings as containers when those headings
are exactly the units with no credited track. A title that carries an opus, BWV
or work number cannot be a container. Every other unit needs exactly one track,
those tracks must partition the album, and the required performer must be
credited on each. Losing a piece or the performer fails closed. Cap at
Probable85. Same label and programme do not prove the same mastering.

## 2026-11-13 — Eight cached near-misses are one pass

Status: adopted.

Review Kempff, Rubinstein, Davis/Sibelius, Haebler, Time Out, Jazz Samba,
Dutoit and Ellington before reporting. A title pairing is per review. A named
piece absent from the cached album stays unpublished. See
[eight cached near-misses](../plans/2026-11-13-qobuz-eight-cached.md).

## 2026-11-13 — Bound tracks need an explicit catalogue exception

Status: adopted for the eight-album pass.

A review may move or add a track only when the title still contains the cited
text. A conflicting catalogue number is accepted only as a suffix letter, a
posthumous token, a bare subnumber already present in the source title, or the
same stated sonata number. KV 322 is not another Köchel number. Extra tracks,
including a short bonus take, stay outside the programme. Cap at Probable85.

## 2026-11-13 — A recorded withhold is not an open inventory lead

Status: adopted.

The unmatched inventory follows the published matches. A release whose cached
album has a withhold decision is `reviewed_withheld`, including Tannhäuser,
Haebler, Time Out and Saint-Saëns Op. 50. That category does not publish a
match and does not queue the same gap again. Barenboim9866861 remains the one
completeness caution and stays unpublished against DG 4631272.

## 2026-11-13 — A heading may cover works that already have their tracks

Status: adopted for the Menuhin Paganini review.

When the only unmatched source unit is a heading, a hash-bound review may keep
the other units’ existing multi-track assignments. Those tracks must partition
the album, movement numbers must run in order, and every required performer
must be credited on every used track. A heading that carries an opus, BWV or
work number is not a container. This does not relax the one-track rule used
for numbered pieces under a heading. Cap at Probable 85. A source key name and
a later digital file do not prove the same mastering.

## 2026-11-13 — Bitches Brew’s missing credit is an open case

Status: proposal. Not a match rule and not a UI change.

Discogs 7609610 is the 2015 Columbia/Legacy double LP. Its six titles are the
1970 album. Larry Young is required on Pharaoh’s Dance, Spanish Key, John
McLaughlin, and Miles Runs the Voodoo Down. Cached Qobuz editions
0886443874428 and 0074646577424 name him only on the first two. The six-track
file also names Joe Zawinul on John McLaughlin, where this copy does not.
Feio is an extra on the seven-track file. The release stays unchecked at 4/6.
Session knowledge does not fill a credit the file omits. How this may affect
matching, and which of these facts the explorer should show, is
[Bitches Brew credits](../plans/2026-11-13-bitches-brew-credits.md).
