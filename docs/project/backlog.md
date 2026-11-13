# Backlog

Updated: 2026-11-13, Europe/Amsterdam

AD-005 (UI redesign), AD-002 (Qobuz investigation) and AD-003 (deployment
verification), AD-006 (initial Qobuz matching preparation) and AD-007 (full Qobuz candidate search) are complete; see history and context.
The entries below remain proposals. IDs remain stable when reordered. Promote an entry to
agreed work only when the user requests it; record completion in [history](history.md).

## AD-001 — Audit Spotify match quality

Status: user-authorized ten-album track caching/audit completed (227 tracks),
using existing sp PKCE login. See [refinement and findings](../plans/2026-11-13-query-credits-spotify-tracks.md).
Two partial programmes confirmed (1012732 and 6119238); user-authorized
[programme safeguard](../plans/2026-11-13-spotify-programme-safeguard.md) now withholds
them as Unchecked with visible findings and no automatic alternate promotion.
User-authorized [Dvorak alternatives, eight-album broader audit and branch
readiness review](../plans/2026-11-13-spotify-followup-readiness.md) completed in order.
Dvorak recovered as Probable85; three additional bad programmes withheld.
Five broader labels retained with programme/act-heading support but recording
identity unresolved. Original eight recording validations also remain unresolved.
No population error-rate claim. Proposed next: a broader independently reviewed
sample and further bounded replacement checks; no automatic collection-wide run.

Review a bounded sample across found, probable, and not-found results, comparing
the work and actual performers/recording identity. Identify false positives and
missed matches before proposing scoring changes.

Done when: sample scope, evidence, error types, and recommended follow-ups are
documented. This investigation does not require changing thresholds or data.

## AD-004 — Define collection refresh and manual corrections

Status: proposed.

Design how new/removed collection copies are reconciled and how reviewed match
corrections survive rescoring. Account for duplicate copies and cache freshness.

Done when: identity, refresh, correction precedence, and validation rules are
documented in a linked plan. Implementation is a separate step.

## AD-008 — Improve Qobuz coverage beyond conservative v1

Status: user-authorized [round2](../plans/2026-11-13-qobuz-round2.md) complete:
3new bounded Probables (Klemperer,Ancerl,deVito),40slow searches for20empty
releases recover hits for18;2selected metadata fetches (15tracks), no warnings.
Richter pair remains unresolved for source catalogue/key conflicts. Further work
is proposed: verify that bounded correction, shorten title queries and improve
explicit role/composer normalization. No broad run, push or deployment authorized. Prior bounded offline improvement and30-release comparison complete,
including twenty slow Qobuz fallback queries and eight album metadata inspections. See
[comparison plan](../plans/2026-11-13-service-comparison-pilot.md). Further expansion
remains proposed. See [pilot and review](../plans/2026-11-13-qobuz-coverage-pilot.md).
Ten additional Probable releases integrated through recomputed credit/completeness
checks and a fixed candidate scope; alias/split-movement cases withheld. Baseline completeness audit is now complete; see the
[audit and next recommendations](../plans/2026-11-13-qobuz-baseline-completeness-audit.md).
Work-aware context/opus disambiguation and conservative role-aware groups are
now implemented; see [implementation review](../plans/2026-11-13-qobuz-work-groups.md).
Historical76 reviewed statuses unchanged, five mappings improved. Latest user-authorized
[four-lead review](../plans/2026-11-13-qobuz-lead-validation.md) adds three Probable
candidates with hash-bound programme/recording evidence and excludes Barenboim’s
conflicting cycle. No further catalogue calls. Next proposed work:
query relevance and explicit work/position credit handling implemented; see
[refinement](../plans/2026-11-13-query-credits-spotify-tracks.md). Two corrected queries
validated without warnings; target source archive covers 128 releases. Remaining
proposals: source completeness and verify aliases in bounded reviewed cases. No collection-wide
fallback run is authorized by the completed pilot. AD-006 initial preparation is complete;
see [audit](../plans/2026-11-13-qobuz-audit.md). Bounded expansion checkpoint committed as c1857a7; subsequent audit/grouping work
is included in the user-requested follow-up commit. No push, merge or deployment requested.

Investigate verified catalogue aliases, multilingual works/performers, movement
completeness and recording-session identity. Broaden the 370 empty first-pass
queries in separately authorized slow batches. Keep unresolved cases distinct
from confirmed absence and preserve independent reviewed overrides.

Done when: a broader independently labelled sample supports improved rules and
coverage without regressing known wrong-orchestra/incomplete-programme controls.
