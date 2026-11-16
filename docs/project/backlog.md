# Backlog

Updated: 2026-11-16, Europe/Amsterdam

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
All16full-support leads reviewed:9Probable/7holds. All38partial-support leads now
reviewed:6Probable/32holds ([latest batch](../plans/2026-11-16-qobuz-partial38.md)).
All104zero-current-rule cases reviewed:3Probable/101explicit holds
([results](../plans/2026-11-16-qobuz-zero104.md)). The frozen160lead cohort is
complete:20accepted families,140reviewed holds,0open. Each hold retains specific
prerequisites for reopening, not an automatic return to the work queue.
Final two supported cached leads reviewed:9283162Probable;15660391held.
[Results and grouping](../plans/2026-11-16-qobuz-final-cached-leads.md).
The diverse12credit-support sample is now reviewed:Reiner1896362Probable,
11explicit holds. [Diagnostic/results](../plans/2026-11-16-qobuz-credit171.md).
All11work-field gains are reviewed, including the [nine-case follow-up](../plans/2026-11-16-qobuz-work-context9.md):2HeifetzProbable/7holds.
Current unreviewed split:150credit-support,170work/title,6no cached candidate and
5completeness cases. Vocal-role diagnostic complete: no candidate status/confidence changes or new
complete source-unit support; live normalization deferred ([results](../plans/2026-11-16-qobuz-vocal-role-diagnostic.md)).
Title179diagnostic’s leading9recording reviews complete:6Probable/3explicit holds
([results](../plans/2026-11-16-qobuz-title9.md)). Frozen queue now19pending:
13full-support needing completeness,6partial. Next recommended batch:the13
completeness cases, retaining source bands and all positive musician requirements.
No global work-field/alias policy or automated promotion adopted. The broader
323work/credit inventory remains separate. Zero support needs source/
lead/rule investigation, not automatic API retrieval. Revisit explicit holds only
with new evidence or a validated scoped rule; partial source support is triage,
not confidence. No new retrieval or broad policy change follows from completion.
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


## AD-010 — Audit musical source-role coverage

Status: suggested after the current bounded reviews; not implementation approval.

Raw source roles for harp, viola and drums can be omitted by current normalized
requirements (Ellis, Farulli and earlier MiltonBananaexamples). Design an offline
whole-collection diagnostic comparing raw musical roles to normalized requirements,
including work scopes and nonperformer exclusions. Do not add generic ensemble-
member, associated-performer or missing-credit waivers. Existing holds persist.

Done when: reproducible bounded discrepancy inventory and regression scope exist;
any normalization change has separate validated publication-impact review.
