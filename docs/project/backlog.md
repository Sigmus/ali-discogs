# Backlog

Updated: 2026-11-15, Europe/Amsterdam

Only active work and proposals belong here. IDs stay stable. Completed work is
in [history](history.md); previous detailed case notes and plan links are preserved
in the [14 November archive](../plans/2026-11-14-backlog-detail-archive.md).

## AD-008 — Qobuz evidence and matching refinement

Status: agreed priority; candidate cache integrated, offline recording reviews next.

Use the [offline follow-up](../plans/2026-11-14-qobuz-offline-followup.md) and
[source-credit review plan](../plans/2026-11-15-qobuz-source-credit-reviews.md).
Completed cases and validations are in history; current counts in context.
The12+305pass and prior metadata follow-ups are validated/shared. User now authorizes
caching all936uncached saved-hit albums for160metadata-needed releases before
ranking; retrieval and offline ranking are now complete. [Scope/run plan](../plans/2026-11-15-qobuz-uncached160.md). No new searches.

The [fourteen-case batch](../plans/2026-11-15-qobuz-priority14-batch.md) is complete:
2 Probable recording-family matches, 12 explicit holds. Complete review does not
mean complete match. Evidence, frozen IDs, alternatives and next actions are in
`data/qobuz_priority14_batch_audit.json`; completed outcomes belong in history.

All26secondary recording reviews are complete:7Probable,18withheld and1specific
wrong-recording rejection, including the [final23batch](../plans/2026-11-15-qobuz-secondary23.md).
The earlier priority/secondary batches are complete. New936album cache is
validated/shared and160leads ranked:2supported complete,16full support needing
completeness,38partial,104zero-current-rule support. Both complete Brahms leads
are now reviewed/Probable ([results](../plans/2026-11-16-qobuz-brahms2.md)).
All16full-support leads now reviewed:9Probable/7holds
([batch results](../plans/2026-11-16-qobuz-fullsupport16.md)). Next38partial-support
leads: inspect complete programme/credit gaps and only then choose bounded reviews.
104zero-current-rule cases follow. Current
whole-inventory work/credit queue:13priority,27secondary,454zero-current-support
and3known constraints. Zero support needs source/lead/rule investigation,
not automatic API retrieval. Revisit explicit holds only with new evidence or a
validated scoped rule; partial source support is triage, not confidence.
Source N°/opus members and separate digital work fields remain recurring parsing
gaps; a global rule would need a bounded collection diff and false-positive tests.
Continue verified cached enrichment and commits autonomously within agreed scope.

Prêtre original-image named-credit gaps and Reiner associated-role uncertainty
remain holds. [Associated-role review](../plans/2026-11-15-qobuz-associated-credit-roles.md)
is proposed: provider-specific semantics and bounded sample needed before any role
normalization or bulk label change. No generic performer waiver. Casals/Gieseking
transfer provenance remains unresolved; Rubinstein7971104source14versus13work
hold and Gilels15221307composer guard remain. No bulk source/results refresh.

Done when: bounded evidence is validated/shared, justified matching rules pass
checks, remaining gaps have explicit next actions. New retrieval needs concrete
scope; no automatic push/deployment or warning retry. Preserve all other source
musicians, empty results and recording uncertainty.

## AD-001 — Comparable Spotify evidence checks

Status: agreed direction after Qobuz; broader execution scope still to define.

Existing bounded track audits and programme safeguards are complete. Next, design
a risk-based sample using comparable programme/performer checks and document
status changes, including possible Found → Probable/Unchecked demotions. Do not
interpret missing metadata as proof of catalogue absence or claim a population
accuracy rate. [Validation gap](../plans/2026-11-13-cross-service-validation-gap.md).

Done when: bounded scope, evidence requirements and review outcomes are documented;
any wider retrieval/reclassification is explicitly scoped before execution.

## AD-004 — Collection refresh and manual corrections

Status: proposed, not active.

Define copy/release identity, new/removed items, cache freshness and reviewed
correction precedence so rescoring cannot erase decisions.

Done when: a linked design specifies reconciliation and validation; implementation
is a separate step.

## AD-009 — Bitches Brew credit gap

Status: proposed; no exception or UI change authorized.

Decide whether missing named credits permit any hash-bound Probable and how to
present the limitation. Keep the release unchecked meanwhile.
[Case evidence](../plans/2026-11-13-bitches-brew-credits.md).

Done when: the exception and wording are accepted or rejected in a decision.
