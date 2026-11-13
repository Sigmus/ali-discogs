# Backlog

Updated: 2026-11-13, Europe/Amsterdam

AD-005 (UI redesign), AD-002 (Qobuz investigation) and AD-003 (deployment
verification), AD-006 (initial Qobuz matching preparation) and AD-007 (full Qobuz candidate search) are complete; see history and context.
The entries below remain proposals. IDs remain stable when reordered. Promote an entry to
agreed work only when the user requests it; record completion in [history](history.md).

## AD-001 — Audit Spotify match quality

Major documented gap: [cross-service validation standards](../plans/2026-11-13-cross-service-validation-gap.md).
Proposed next paired audit: Tristan2996680 main opera versus rehearsal-side
coverage on both services; then shared evidence/status semantics. Documentation
requested; implementation and Spotify retrieval are separate work.

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

The [eight cached near-misses](../plans/2026-11-13-qobuz-eight-cached.md) are
reviewed. Probable85: Kempff, both Rubinstein nocturne releases, Davis/Sibelius,
Jazz Samba and Ellington. Withheld: Haebler’s two F-major titles, Time Out’s
Audrey and Saint-Saëns Op. 50. Prior triage:
[remaining-release offline triage](../plans/2026-11-13-qobuz-unmatched-audit.md).
Source-role, ensemble-alias and act review is implemented and hash-bound.
Tristan2996680 is Probable85 for the main three acts, with the rehearsal side
kept visible. Gould2175684 is Probable85 for BWV 846–893 prelude/fugue pairs.
Michelangeli6678433 is Probable85: the heading Mazurkas is a container and the
13 numbered pieces each have one track. Tannhäuser4365080 stays withheld.
Barenboim9866861 stays unmatched to the later DG cycle.
Wrong-orchestra Nevsky stays excluded. The stored triage file was refreshed
2026-11-13: 324 no saved hits, 10 metadata-needed, 306 work/credit unresolved,
4 reviewed withholds, and Barenboim9866861 as the one completeness caution.

Status: user-authorized [round2](../plans/2026-11-13-qobuz-round2.md) complete:
3new bounded Probables (Klemperer,Ancerl,deVito),40slow searches for20empty
releases recover hits for18;2selected metadata fetches (15tracks), no warnings.
Round2 committed877bc5a. Follow-up authorized: Richter publisher/credit audit passes
with bounded source correction; [ten-release query trial](../plans/2026-11-13-qobuz-query-strategy-trial.md)
compares short performer/composer versus catalogue queries, preserving headline
ensembles. Trial complete:10/10broad,9/10catalogue queries nonempty;31additional
candidate pairs, no automatic acceptance. Offline screening completed81pairs:19cached/62uncached, none fully verified.
Cached Schnabel late-sonata review complete: one Probable with bounded joined
sections and recording-family evidence. Two-album metadata fetch complete77tracks without warnings. Klemperer programme/
credits and bounded recording/overture review complete: one new Probable. Dvorak individual
member credits and No.8 work disambiguation unresolved; no promotion. No broad run, push or deployment authorized. Prior bounded offline improvement and30-release comparison complete,
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
