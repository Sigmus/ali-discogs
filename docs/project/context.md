# Ali Discogs

Updated: 2026-11-13, Europe/Amsterdam

Match Ali's Discogs collection (`ajozi`) against Spotify and browse a static
explorer. [README](../../README.md) owns setup/architecture; project history and
plans preserve dated evidence and prior handoffs.

## Current state

- Branch `codex/qobuz-poc`; user requested committing the four-lead Qobuz
  validation and Spotify programme safeguard checkpoint. Prior three commits are
  local/unpushed. No push, merge or deployment requested.
- Current collection: 741 copies / 740 unique releases. Spotify labels now
  254 Found / 275 Probable / 210 Not found / 2 Unchecked copies. The two reviewed
  partial programmes are withheld; other labels are not independently verified.
- Qobuz overlay: 12 Found / 67 Probable / 662 unchecked copies; unique 12/67/661.
  Separate `data/qobuz_matches.json` survives Spotify rescoring; original pipeline
  Qobuz fields stay unchecked. Empty/inconclusive queries are not confirmed absence.
- Sonoteque table/details, 80% main width, column sorting (Year ascending default),
  Spotify/Qobuz filters and frequency-order switch. Qobuz details show evidence.
- Pages uses Actions on main. Last recorded live verification was 2026-11-12;
  inspect current Actions/live page before claiming subsequent deployment status.

## Preserved catalogue evidence

- Original search: 740 queries, 370 nonempty / 370 empty, 1,217 candidate entries /
  1,036 unique Qobuz albums. Full metadata completed 2026-11-13 01:15 Amsterdam:
  27,770 tracks, album IDs/counts/unique track IDs verified. One 500/730-track
  response was recovered with user-authorized strict pagination. Monitors deleted.
- Shared `data/qobuz_evidence.json.gz` preserves original whitelisted evidence.
  Raw request archive now has 1,788 responses (29 added in later bounded pilots);
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

- User requested .env placeholders; added without exposing/overwriting Qobuz
  settings. Existing sp PKCE login was reused instead: config/client ID and tokens
  remain under ~/.config/sp; no client secret required or copied into the repo.
- Ten selected albums cached successfully (227 tracks), with slow spacing,
  pagination and first-warning STOP/no retry. Shared whitelisted archive restores
  offline; local state ignored under `.spotify-poc/`. No playback/library calls.
- Two confirmed partial programmes: 1012732 Brahms whole collection maps to only
  Symphony No.1; 6119238 Dvorak Sixth/My Home maps to an album missing My Home.
  Other eight recording validations unresolved; artist lists lack role credits.
- User-authorized candidate-specific guard now withholds those two partial albums
  as Unchecked, preserves similarity signals/candidates and explains missing works
  in details. No silent alternate promotion. Hash changes require re-review.
  No population accuracy/catalogue-size claim from this selected sample.

## Validation and next action

- Seven pipeline/guard tests and 63 mocked/offline script tests, UI normalization,
  JS syntax and build pass. Only two intended Spotify objects change; prior three
  Qobuz promotions remain intact.
  No Qobuz/Spotify calls, push or deployment during this validation.
- Next recommendation: audit Dvorak complete-cycle alternatives, cache first;
  any new fetching remains proposed. No push, merge or deployment requested.
- [Spotify safeguard](../plans/2026-11-13-spotify-programme-safeguard.md) records scope and checks.
- Latest review: [four Qobuz leads](../plans/2026-11-13-qobuz-lead-validation.md).
- Details: [refinement and Spotify audit](../plans/2026-11-13-query-credits-spotify-tracks.md),
  [comparison pilot](../plans/2026-11-13-service-comparison-pilot.md),
  [backlog](backlog.md), [decisions](decisions.md), [history](history.md).
