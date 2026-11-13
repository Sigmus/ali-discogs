# Backlog

Updated: 2026-11-13, Europe/Amsterdam

AD-005 (UI redesign), AD-002 (Qobuz investigation) and AD-003 (deployment
verification), AD-006 (initial Qobuz matching preparation) and AD-007 (full Qobuz candidate search) are complete; see history and context.
The entries below remain proposals. IDs remain stable when reordered. Promote an entry to
agreed work only when the user requests it; record completion in [history](history.md).

## AD-001 — Audit Spotify match quality

Status: user-authorized ten-album track caching/audit completed (227 tracks),
using existing sp PKCE login. See [refinement and findings](../plans/2026-11-13-query-credits-spotify-tracks.md).
Two partial programmes confirmed (1012732 and 6119238); eight recording validations
remain unresolved. Proposed next: a full-programme warning/scoring safeguard and
broader audit. No Spotify score changes or population error-rate claim yet.

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

Status: bounded offline improvement and 30-release comparison complete,
including twenty slow Qobuz fallback queries and eight album metadata inspections. See
[comparison plan](../plans/2026-11-13-service-comparison-pilot.md). Further expansion
remains proposed. See [pilot and review](../plans/2026-11-13-qobuz-coverage-pilot.md).
Ten additional Probable releases integrated through recomputed credit/completeness
checks and a fixed candidate scope; alias/split-movement cases withheld. Baseline completeness audit is now complete; see the
[audit and next recommendations](../plans/2026-11-13-qobuz-baseline-completeness-audit.md).
Work-aware context/opus disambiguation and conservative role-aware groups are
now implemented; see [implementation review](../plans/2026-11-13-qobuz-work-groups.md).
All 76 reviewed statuses unchanged, five mappings improved. Next proposed work:
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
