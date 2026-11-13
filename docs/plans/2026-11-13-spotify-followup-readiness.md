# Spotify follow-up audit and branch readiness

User authorized all three suggested stages in order on 2026-11-13,
Europe/Amsterdam: Dvorak replacements, broader bounded Spotify audit, then review
for merge/deployment. This authorizes the investigation and readiness review;
actual merge/push/deployment is not part of the wording of the proposed third step.

## 1. Dvorak alternatives

No existing track cache for the two alternatives. Retrieved both complete albums,
39 and62 tracks, with >=15-second spacing through the existing sp login. No API
warnings/retries. A local output-variable bug affected final checkpoint writing;
fixed and finalized from saved albums offline, with no repeated network requests.
Original ten-album pilot archive remains byte-identical. New scope, portable
tracks and audit are `data/spotify_dvorak_{scope.json,tracks.json.gz,audit.json}`.

Both contain Sixth I–IV and My Home Op.62 with Dvorak/Kertesz/LSO on all five
selected tracks. My Home576.9 seconds versus target575. The selected39-track
alternative becomes Probable85 through a separate explicit hash-bound positive
review, not an automatic runner-up fallback. Existing partial candidate remains
rejected and recorded. Exact take/mastering and artist-role identity remain
unverified. Public sources: [Decca cycle](https://shop.deccarecordsus.com/products/london-symphony-orchestra-dvorak-complete-symphonies-tone-poems-overtures-requiem)
and [Eloquence session documentation](https://www.eloquenceclassics.com/releases-archive/dvorak-overtures-tone-poems/).
These identify the Decca/LSO/Kertesz cycle and My Home's December1965 recording;
no exact Spotify barcode match or individual-take proof is claimed.

## 2. Broader sample — complete

`data/spotify_broader_scope.json` fixes eight new releases: four Found and four
Probable, evenly spaced by release ID within each status after filtering for
multi-item target programmes and candidate albums of2–40 tracks. Excludes all
original ten pilot releases. Deliberately targets programme-risk cases, not a
random/representative sample or service accuracy measurement. No search expansion.

Worker retains the same >=15-second spacing, 120-second rest per50 attempts,
STOP/lock, atomic saved pages and first-warning/no-retry policy. Each bounded
scope uses a separate ignored output folder and portable archive. Never overwrite
the original pilot evidence or negative review fingerprints. Up to12 explicitly
listed albums per custom scope; original default ten-case behaviour retained.

## 3. Merge/deployment review — complete

Inspect the entire feature branch against main, required CI coverage, evidence
publication boundary, credential exclusion, offline reproduction, build, local UI,
and mergeability against current remote main. Record material unresolved risks
and a concrete readiness decision. Do not claim remote CI or deployment success
without evidence. No automatic merge or deployment in a readiness review.

## Final findings and corrections

All eight albums fetched successfully (140 tracks) without service warnings. Two
Dvorak alternatives add101 tracks; total follow-up241 tracks, original227-track
pilot archive unchanged. No Qobuz calls. Full portable sources and hash-bound
manual findings are shared; `scripts/spotify_followup_verify.py` checks them offline.

| Release | Initial label | Finding / action |
| --- | --- | --- |
| 1010200 Bach Brandenburgs | Found | Six concertos represented, 19 tracks. Retained; recording identity unresolved. |
| 4067901 Chopin14Waltzes | Found | Fourteen opus/subnumber/title correspondences. Retained; recording identity unresolved. |
| 7577224 Pelleas | Found | ActsI–V represented. Heading support only; full scenes/text and recording unresolved. Retained. |
| 24278222 Dido | Found | Overture and ActsI–III represented; target ActII split across LP sides, plus two digital bonus tracks. Heading support only, recording unresolved. Retained. |
| 1252193 Greatest Jazz Concert | Probable | Different concert and all eight titles differ from the requested sixteen. Confirmed programme mismatch → Unchecked. |
| 5249935 Iberia/LaMer/Faun | Probable | Six tracks are Nocturnes/Daphnis Suite2; none of the requested three works. Confirmed programme mismatch → Unchecked. |
| 9458258 Scottish/Italian | Probable | Italian4 complete; Scottish3 missing, replaced by Reformation5. Confirmed partial → Unchecked. |
| 29719858 Dvorak cello | Probable | Three concerto movements and five arrangements represented. Grouping heading is not an extra composition. Retained; exact live performance/recording unresolved. |

The three new negative reviews use their own archive hashes in the existing guard.
Do not infer absent music from automatic title mapping; diagnostic mappings are
explicitly separate from these manual findings. Unknown replacements are not
promoted. UI distinguishes a programme mismatch from a partially covered programme.
Dvorak's positive replacement uses a separate required review ledger; source hashes,
selected tracks and required artist lists rechecked on every replay. It is capped
at Probable85, not an exact-session or mastering confirmation.

Current copies: Spotify **254 Found /273 Probable /210 Not found /4 Unchecked**.
Compared with3f5a2c6, only Dvorak6119238 and the three new rejected release objects
change labels. Brahms1012732 stays Unchecked; its review fingerprint/message updates.
Qobuz is unchanged at12/67/662 copies (12/67/661 unique); only collection fingerprint
updates when its generator replays after Spotify changes.

## Readiness evidence

- Fetched current `origin/main`:0847175; it is an ancestor of feature HEAD3f5a2c6.
  No merge conflict expected against that inspected main. Uncommitted follow-up
  changes still need committing before the complete result can be reviewed remotely.
- Reviewed feature branch files, publication inputs/boundary and CI. Fixed missing
  test discovery for programme guards. Added follow-up evidence verification in
  CI/Makefile. Pages now runs `make test` before uploading/deploying the artifact,
  preventing deployment when its validation step fails.
- Fresh prospective-checkout simulation contains tracked + new intended files,
  excludes `.env` and both ignored worker/cache trees, and uses no credentials.
  Nine pipeline/guard tests +66 script tests pass, portable audit verifies,
  Qobuz replay is byte-identical, UI normalization/sorting and JS syntax pass,
  and static build succeeds. Worker tests cover scoped export/checkpoint/offline
  reuse, first-warning STOP/no retry and duplicate track IDs.
- Original pilot and original Qobuz evidence/request archives are byte-identical.
  New track fields whitelisted; credential-value scan of prospective checkout
  passes. `dist/` has only index/app/style/.nojekyll and fixture, collection,
  summary, Qobuz overlay JSON. No review archives, credentials or worker state.
- Browser verified recovered Dvorak detail with85%Probable, four-result Spotify
  Unchecked filter, visible mismatch/partial explanations and retained Qobuz data.

**Decision:** locally ready for a PR, with explicit match-quality limitations.
Not a claim that all matches are verified or that remote CI passed. The feature
branch has four local commits plus this uncommitted follow-up; nothing pushed,
merged or deployed in this task. Next release action is commit/push and PR review,
then require green remote checks before merging. Main pushes trigger Pages with
its new validation gate; verify the live page after deployment, not before.

## Subsequent authorized release

User later authorized publication. PR2 passed remote tests and merged as02ec297
on2026-11-13. Merged-main tests and Pages deployment succeeded. Live static assets
and three publication JSON files match byte-for-byte; deployed Dvorak detail
verified. See [release history](../project/history.md) and
[live collection](https://sigmus.github.io/ali-discogs/). Earlier uncommitted/
unpublished statements above describe the readiness-stage checkpoint.
