# Ali Discogs

Updated: 2026-11-13, Europe/Amsterdam

Match Ali's Discogs collection (`ajozi`) against Spotify and browse a static
explorer. [README](../../README.md) owns setup/architecture; project history and
plans preserve dated evidence and prior handoffs.

## Current state

- Active branch `codex/qobuz-coverage-round2`, based on deployed main1735ab7.
  User authorized cached near-match validation, then a slow20-release fallback
  batch. Local changes uncommitted; no push/merge/deploy requested.
- Current collection:741 copies /740 unique releases. Spotify254Found /273Probable
  /210NotFound /4Unchecked copies. Retained labels are not independent full
  recording confirmations. Qobuz figures below are independent enrichment.
- Qobuz overlay: 12 Found / 70 Probable / 659 unchecked copies; unique12/70/658 locally.
  Separate `data/qobuz_matches.json` survives Spotify rescoring; original pipeline
  Qobuz fields stay unchecked. Empty/inconclusive queries are not confirmed absence.
- Sonoteque table/details, 80% main width, column sorting (Year ascending default),
  Spotify/Qobuz filters and frequency-order switch. Qobuz details show evidence.
- Live site: https://sigmus.github.io/ali-discogs/ . Main Pages workflow validates
  before publishing. Release02ec297 test/Pages runs passed; live asset bytes match.

## Preserved catalogue evidence

- Original search: 740 queries, 370 nonempty / 370 empty, 1,217 candidate entries /
  1,036 unique Qobuz albums. Full metadata completed 2026-11-13 01:15 Amsterdam:
  27,770 tracks, album IDs/counts/unique track IDs verified. One 500/730-track
  response was recovered with user-authorized strict pagination. Monitors deleted.
- Shared `data/qobuz_evidence.json.gz` preserves original whitelisted evidence.
  Raw request archive now has1,829 responses (41 added in round2);
  original member payloads preserved. Credentials/run state remain ignored.
- Comparison pilot adds portable `data/qobuz_comparison_evidence.json.gz`: twenty
  fallback queries and eight complete selected albums (seven new/one reused).
  Two corrected-query validations are separately preserved. No audio requested.
- Shared evidence supports offline collaboration; [Qobuz guide](../qobuz.md) owns
  export/restore/replay commands. No automatic refresh or warning retry permitted.

## Matching, audits and refinement

- Current work-group-v2 matcher uses bounded inherited movement titles, explicit
  vocal roles, conservative recording-group support and shared-opus work guards.
  Found 95% / Probable 85% are heuristic levels, not calibrated probabilities or
  independent recording-session verification. Ambiguous aliases remain unresolved.
- Original-66 audit reproduced v1 scores: seven strict-coverage supports, one
  incomplete-credit case with music present and 58 unresolved. Later comparison
  across 66+10 selected matches fixes five evidence mappings, no shared track
  assignments. All existing publication status labels remain unchanged.
- Explicit target-credit archive derives positive work/position assignments for
  128 releases from cached Discogs, with source hashes. Unknown/unscoped actors
  stay required globally; cross-side ranges and parent/child units handled with
  fail-closed guards. Candidate credits do not determine target requirements.
- Query planner selects album leads instead of supporting players and fixes
  compound composer query names. Relevance ranking is not match confidence.
  Corrected Coltrane query finds actual A Love Supreme editions; live variant
  flagged. Only two validation queries run, not a collection-wide expansion.
- Thirty-release pilot: fallback hits for all ten originally empty releases,
  three initial programme/performer leads. Credit/hierarchy changes
  improve Barenboim target mapping from 23/31 flattened items to 8/8 work units.
  Subsequent bounded review promotes Schnabel, Tennstedt and Kubelik to Probable,
  with complete movement/credit checks and documented recording-cycle support.
  Barenboim is excluded: target EMI1966–69 versus later DG cycle. Hash-bound
  review permits one exact Schnabel joined track and Tennstedt Adagio excerpt.
  Blank source credit assignments and other completeness/session gaps remain open.

## Spotify track evidence

- Existing sp PKCE login reused; tokens stay outside the repo. Original ten albums
  (227tracks) are shared portably; local state ignored, no playback/library calls.
- Five negative candidate reviews: original Brahms whole collection/Symphony1
  and Dvorak Sixth/MyHome, plus new wrong jazz concert, unrelated Debussy/Ravel
  programme and Mendelssohn missing Scottish3. Known bad albums cannot be accepted
  by similarity scores; preserve candidates and explain missing/mismatched works.
- Dvorak replacement explicitly reviewed: both alternatives cover Sixth I–IV and
  MyHome with required artists; selected39-track set Probable85. Original partial
  remains rejected. Positive review has source hashes; exact take/mastering unverified.
- Eight new risk-selected albums cached (140tracks); two Dvorak alternatives add
  101tracks. Shared separate archives; original227-track archive unchanged.
  Broader audit:2programme mismatches,1partial,3listed-programme supports and
  2opera act-heading supports. Five retained labels still recording-unverified.
  No population accuracy estimate; no title-gap-to-absence inference.

## Validation and next action

- Current round2 checks:9pipeline/guard +75script tests, offline audit/replay,
  canonical URLs, UI/JS/build pass. Prior fresh-checkout validation remains recorded.
  Credential scan/whitelist/build-boundary checks pass; browser UI verified.
- Deployed main1735ab7 remains12/67/662Qobuz copies; round2 is local/uncommitted.
  Next proposal: verify Richter catalogue conflicts, then shorter work queries
  and explicit role/composer normalization. No further batch/publication authorized.
- Round2 complete: Klemperer Missa, Ancerl Requiem and deVito/Fischer Sonatas1/3
  now Probable85 with bounded evidence/source-title review. Search40queries:
  18/20releases have hits,107pairs;2selected albums15tracks fetched without warnings.
  Richter pair withheld for source catalogue/key conflicts. No active retrieval.
- [Active round2 scope and findings](../plans/2026-11-13-qobuz-round2.md).
- [Follow-up findings and readiness](../plans/2026-11-13-spotify-followup-readiness.md).
- [Spotify safeguard](../plans/2026-11-13-spotify-programme-safeguard.md) records scope and checks.
- Latest review: [four Qobuz leads](../plans/2026-11-13-qobuz-lead-validation.md).
- [Backlog](backlog.md), [decisions](decisions.md), [history](history.md).
