# Backlog

Updated: 2026-11-13, Europe/Amsterdam

AD-005 (UI redesign), AD-002 (Qobuz investigation) and AD-003 (deployment
verification), AD-006 (initial Qobuz matching preparation) and AD-007 (full Qobuz candidate search) are complete; see history and context.
The entries below remain proposals. IDs remain stable when reordered. Promote an entry to
agreed work only when the user requests it; record completion in [history](history.md).

## AD-001 — Audit Spotify match quality

Status: proposed. Recommended first.

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

Status: user-authorized bounded offline pilot and integration complete. Further
expansion proposed. See [pilot and review](../plans/2026-11-13-qobuz-coverage-pilot.md).
Ten additional Probable releases integrated through recomputed credit/completeness
checks and a fixed candidate scope; alias/split-movement cases withheld. Next
recommended step is retrospective completeness review of the v1 baseline before
another bounded offline discovery sample. AD-006 initial preparation is complete;
see [audit](../plans/2026-11-13-qobuz-audit.md). User requested committing the bounded expansion checkpoint, then auditing the
original 66 matches offline. No push, merge or deployment requested.

Investigate verified catalogue aliases, multilingual works/performers, movement
completeness and recording-session identity. Broaden the 370 empty first-pass
queries in separately authorized slow batches. Keep unresolved cases distinct
from confirmed absence and preserve independent reviewed overrides.

Done when: a broader independently labelled sample supports improved rules and
coverage without regressing known wrong-orchestra/incomplete-programme controls.
