# Backlog

Updated: 2026-11-14, Europe/Amsterdam

Only active work and proposals belong here. IDs stay stable. Completed work is
in [history](history.md); previous detailed case notes and plan links are preserved
in the [14 November archive](../plans/2026-11-14-backlog-detail-archive.md).

## AD-008 — Qobuz evidence and matching refinement

Status: agreed priority; retrieval and first offline screen/audit complete.
[Offline follow-up](../plans/2026-11-14-qobuz-offline-followup.md): recording review
now includes twenty-one new Probables and shared inventory/parser fixes. Nine-album
follow-up complete216tracks:7Probables/4withheld release leads after further
reviews. Next:
Toscanini10757120 RCA recording-family/source audit against cached1952lead.
Three further Katchen LPs now Probable: key discrepancy disclosed, joined band
verified from original label, session versus issue year reconciled. Saved source
images/hash checks support offline reuse;149script tests pass. Nabucco/Mozart
credit/catalogue gaps remain unresolved.
170remaining metadata-needed releases are not a fetch mandate. Follow the
[retrieval and follow-up plan](../plans/2026-11-14-qobuz-remaining-retrieval.md).

Order: finish/validate/export 83 metadata albums and 603 searches across the
12 + 305 release groups; rank and match offline; audit promising/uncertain cases;
improve reusable rules with false-positive regressions; regenerate UI data and
verify details/build. Fetching search results is discovery, not match acceptance.
Additional full metadata for new hits needs a bounded follow-up scope.

Done when: fixed-scope retrieval is validated and shared portably, follow-up audit
findings are recorded, justified rules/data pass checks, and unresolved gaps have
an explicit next action. No automatic push/deployment or warning retry.

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
