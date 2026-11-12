# Backlog

Updated: 2026-11-12, Europe/Amsterdam

AD-005 (UI redesign), AD-002 (Qobuz investigation) and AD-003 (deployment
verification) are complete; see history and context.
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

## AD-006 — Build reviewed Qobuz enrichment

Status: proposed follow-up; catalogue PoC is complete, production merging is not authorized yet.

Use [Qobuz setup and resume](../qobuz.md) and the
[six-release report](../plans/2026-11-12-qobuz-sample.md). Implement metadata
normalization and conservative programme/performer checks, distinguish album
matches from compilation subsets, and output reviewable candidates. Coordinate
manual override persistence with AD-004 before writing collection results.

Done when: a reviewed test sample demonstrates accepted/rejected candidates,
access failures remain unchecked, and reviewed Qobuz results survive Spotify
rescoring. Keep credentials and raw private-session caches out of publication.

## AD-007 — Full-collection Qobuz candidate search

Status: agreed and running locally (2026-11-12). All 740 distinct releases,
covering 741 copies, get a slow first-pass search. See docs/qobuz.md for progress,
stop/resume and pacing. Done when the manifest has a successful search response
for every release and a counts summary is recorded; zero hits remain unresolved.
This scope does not authorize automatic acceptance of matches or production writes.
