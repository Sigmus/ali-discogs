# Backlog

Updated: 2026-11-12, Europe/Amsterdam

AD-005 is implemented locally and awaiting visual review; see history and context.
The entries below remain proposals. IDs remain stable when reordered. Promote an entry to
agreed work only when the user requests it; record completion in [history](history.md).

## AD-001 — Audit Spotify match quality

Status: proposed. Recommended first.

Review a bounded sample across found, probable, and not-found results, comparing
the work and actual performers/recording identity. Identify false positives and
missed matches before proposing scoring changes.

Done when: sample scope, evidence, error types, and recommended follow-ups are
documented. This investigation does not require changing thresholds or data.

## AD-002 — Decide the Qobuz approach

Status: proposed.

Recheck supported access options and decide whether to retain search links,
support manual verification, or implement matching. Preserve unchecked as a
separate state from not found.

Done when: a feasible approach and its limitations are recorded as a decision;
any implementation is scoped separately.

## AD-003 — Verify public deployment

Status: proposed.

Check the documented GitHub Pages URL, workflow status, and loading of scripts,
styles, and collection data under the repository prefix.

Done when: the current deployment is verified with dated evidence, or a concrete
blocker and remedy are documented. Deployment/settings changes require task scope.

## AD-004 — Define collection refresh and manual corrections

Status: proposed.

Design how new/removed collection copies are reconciled and how reviewed match
corrections survive rescoring. Account for duplicate copies and cache freshness.

Done when: identity, refresh, correction precedence, and validation rules are
documented in a linked plan. Implementation is a separate step.
