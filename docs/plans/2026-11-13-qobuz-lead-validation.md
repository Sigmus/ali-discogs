# Four Qobuz pilot leads: programme and recording review

Reviewed 2026-11-13, Europe/Amsterdam. User authorized proceeding with the strongest
four cached leads. No new Qobuz/Spotify requests, commit, push or deployment.

## Result

Three bounded candidates qualify as **Probable (85% heuristic)**. One is rejected
for conflicting recording provenance. These are programme/credit and documentary
recording reviews, not listening verification or calibrated probabilities.

| Discogs release | Result | Evidence and limits |
| --- | --- | --- |
| 3066447 Barenboim | Excluded | Target EMI notes specify 1966–1969. Selected DG catalogue 4631272 is a later Paris cycle: [catalogue track dates](https://www.prestomusic.com/classical/products/7924312--beethoven-complete-piano-sonatas). Eight matching work headings and the same pianist would give a false positive. Do not conclude the EMI performances are absent from Qobuz. |
| 4429613 Schnabel | Probable | All seven sonatas (11–17), 25 movements in 24 digital tracks. [Warner's exact barcode](https://www.warnerclassics.com/release/beethoven-complete-piano-sonatas-3) identifies the 1932–1938 historical cycle. [DCML work/movement corpus](https://dcmlab.github.io/beethoven_piano_sonatas/) supports movement inventories. Op.27/1 III–IV share track36924084; only that hash-bound track gets a joined-movement exception. Remastered superset, not identical Seraphim LP edition. |
| 12130939 Tennstedt | Probable | Fifth I–V plus **Tenth Adagio only**. Raw target nested tracklist explicitly requests the excerpt, though normalization loses that qualifier in the work heading. [Warner exact digital barcode](https://wmg.jp/klaus-tennstedt/discography/31233) specifies studio Fifth and Adagio recorded in 1978 at Abbey Road. Distinguish the later live Fifth. Exact LP mastering remains unverified. |
| 37312800 Kubelik | Probable | All four Brahms Fourth movements with Vienna/Kubelik credits. [Decca/Eloquence](https://www.eloquenceclassics.com/releases-archive/brahms-symphonies-nos-1-4/) identifies the Vienna cycle and March1956 Fourth sessions, consistent with the target Decca LXT5214. Candidate production personnel agree. Publisher's physical companion barcode differs from the digital barcode; mono LP versus digital remaster is not identical-edition proof. |

Schnabel whole-work LP timing totals versus digital seconds, in sonata order:
1470/1473, 1330/1343, 945/926, 825/828, 1290/1320, 1460/1453, 1389/1377.
All are within3%, but Tempest first/second movement annotations differ materially
(593/447 versus530/500 seconds). Total timing supports programme correspondence;
it does not resolve individual take or LP timing-allocation uncertainty. This is
preserved in publication reasons and remains a limit on the Probable judgement.

## Reproducible, bounded integration

`data/qobuz_lead_reviews.json` records decisions, source URLs, selected raw target
notes/labels/nested programme, and canonical hashes of the normalized matching
inputs and complete portable candidate metadata. It includes the rejected lead.
It contains no account data or credentials. Raw target source hashes preserve
provenance; replay uses the portable review and existing comparison archive.

`scripts/qobuz_lead_review.py` runs offline and writes
`data/qobuz_lead_audit.json`. Every accepted candidate must still pass the current
work/performer matcher, all reviewed movements in order, full credited coverage
and non-overlapping track assignments. A source hash change raises an error
requiring re-review. Spotify scores are excluded from target hashes, preserving
independent Qobuz enrichment. Movement-join permission is exact-track/hash scoped;
there is no global relaxation for joins, excerpts or aliases.

The publication generator adds these three candidates from the existing portable
comparison archive, with ledger/archive fingerprints and review reasons. Original
snapshot and ten-release expansion scope are unchanged, preserving the historical
66+10 audit. Existing publication labels are retained; only these three previously
unchecked releases change. Unique totals: **12 Found /67 Probable /661 Unchecked**;
741 copies: **12/67/662**. Unchecked is not confirmed absence. Spotify unchanged.

Reproduce without credentials or `.qobuz-poc/`:

```sh
uv run python scripts/qobuz_lead_review.py
uv run python scripts/qobuz_match.py
make build
```

Validation: 63 offline/mocked regression tests, UI normalization/overlay/sorting,
JS syntax and static build. Repeated generation must be byte-identical; compare
all740 old statuses to verify only the three intended changes. Local details
retain source/session limitations and the Tenth excerpt warning. No raw archives
or review ledgers are copied into the deployed static bundle.

## Next proposed work

Add a Spotify full-programme safeguard for the two confirmed partial matches
before publication. Separately search for Barenboim's actual EMI cycle in a bounded,
explicitly authorized slow batch. Neither proposal is implemented by this review.
