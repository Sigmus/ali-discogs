# Fourteen cached priority reviews

15 November 2026, Europe/Amsterdam. User authorized all14as one batch, without
routine confirmation. Freeze the14priority IDs from qobuz_cached_review_queue.json;
counting/triage changes from the preceding turn are included in this work.

Use complete shared metadata, raw Discogs source and existing recording reviews.
Review best leads and cached alternatives; public source/publisher research may
corroborate programme/recording identity. No new Qobuz requests, downloads, credit
policy exemptions, source rewrites, push or deployment. Unresolved policy or
provenance keeps its case held while independent cases continue.

Every case receives a saved target/source/album-bound outcome, complete source and
candidate programme/credit diagnostic, explicit blocker or accepted-recording
rationale, limitations and next action. Threshold-based ranking never establishes
acceptance. Retain source discrepancies and require the whole source programme.

After all14: validate the combined reviews, regenerate publication/inventory/UI
and caches-only queue, verify accepted-status changes are limited to reviewed
cases, run meaningful false-positive tests and existing UI/build checks, update
project context/backlog/history and commit this single batch. Do not expand to
26secondary leads until this batch is reported complete.

## Review outcomes

All 14 cases have been inspected in one batch. Two recording-family matches are
eligible for Probable 85; twelve remain unresolved. A completed review is not a
completed match. No Qobuz requests or global credit-policy changes were needed.

| Release | Outcome | Finding |
| --- | --- | --- |
| 5820114 Gilels/Szell | Hold | Five concertos and three solo cycles present; exact solo/orchestral source scopes and old variation catalogue labels need reconciliation. |
| 2628957 Schwarzkopf | Hold | One Warner track lacks credits; complete Casta Diva alternative has unresolved transfer provenance. |
| 1656511 du Pré | Hold | Silent Woods is missing despite the matching album title. |
| 3408094 Bernstein | Hold | DG cycle has different orchestras from the CBS/New York source cycle. |
| 5038376 Kurtz | Hold | Complete ballet alternatives found, including a 1947-version marker; original side boundaries and transfer remain unverified. |
| 6686688 Stern/Ormandy | Probable | Both concertos found in cached Sony Original Jacket Collection; six exact work-field bindings, positive performers and per-work composers. |
| 7002243 Klemperer | Probable | Four Eroica movements plus Fidelio in cached Warner cycle; source Op72b corrected only inside this frozen review, excluding Leonore III. |
| 7248321 Barenboim | Hold | Sampler lacks K550 and has only K467 Andante; other candidate still lacks K550. |
| 8252155 Flämig | Hold | Both masses present; globally listed soprano needs verified source work-level scope. |
| 12690141 Klemperer | Hold | Original lead is Karajan; full cached Klemperer alternative has an unexplained Prometheus 336s versus source 254s. |
| 18963583 Walter | Hold | Brahms overture present, Dvorak 8 absent. |
| 20066470 Kurtz | Hold | All ten marches mapped; stereo/mono alternatives distinguished, transfer and arrangements unresolved. |
| 20588539 Klemperer/Nilsson | Hold | Full listed programme present; source soprano scope unresolved. |
| 22222342 Gould | Hold | Forty Partita movements and seven Toccatas mapped diagnostically; validate source containers and the two BWV914 versions before publication. |

Machine-readable evidence: `data/qobuz_priority14_batch_audit.json`. Each case
preserves source programme, source/target/album hashes, cached alternatives,
manual track diagnostics, blocker and next action. Recording decisions are in
the existing `qobuz_remaining_recording_reviews.json` ledger. A hold there applies
to its exact candidate; the report does not globally reject alternate editions.

The Warner publisher page corroborates the Klemperer stereo-cycle family, while
the original cover, positive per-track credits and close source timings support
the bounded inference. Exact pressing, take and mastering remain unverified.
Source durations were not silently rewritten. The Gould official discography
corroborates the late Toccatas Vol. II programme, not the exact source box/take.

Public Discogs image and original-ad PDF retrievals returned 403; their missing
visual proof is recorded. The Columbia ad was available only as indexed text,
not an inspected image. These were public research failures, not Qobuz API calls
or a resumed provider warning. Existing inspected images are saved/hash-bound.

## Reproduction and next action

Run `uv run python scripts/qobuz_priority14_audit.py` to validate all frozen
reviews and diagnostic track hashes. After regenerating matches and the unmatched
inventory, `uv run python scripts/qobuz_cached_review_queue.py` refreshes triage.
It keeps reviewed blockers out of the open priority list even if another partial
candidate still has a high automatic source-unit fraction.

Next: reassess the 26 secondary partial leads as a separate bounded queue. Do not
cycle through these twelve blockers again without new source evidence or an
adopted, tested rule. The 354 zero-support cases and 160 metadata-needed cases
are separate work populations, not authorization for new provider calls.

## Combined validation

215 script tests pass. All 14 source/review/track-hash checks, the regenerated
unmatched inventory and role census, UI normalization and static build pass.
The frozen publication diff has exactly two accepted-status changes: 6686688 and
7002243, both Unchecked → Probable. Collection and Spotify data are unchanged.
Copy totals: 12 Found / 135 Probable / 594 Unchecked. Current workflow queue:
0 priority, 26 secondary, 354 zero-current-support, 3 known constraints.
No provider calls, push or deployment. Mock 429/STOP output came from test fixtures.

Primary publisher references: [Warner stereo-cycle description](https://www.warnerclassics.com/release/beethoven-9-symphonies-overtures-remastered)
and [Gould Toccatas Vol. II discography](https://glenngould.com/music/bach-toccatas-vol-2/).
