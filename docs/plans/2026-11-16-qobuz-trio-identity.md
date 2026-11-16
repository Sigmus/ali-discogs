# Istomin/Stern/Rose collective identity

16November2026, Europe/Amsterdam. Diagnostic complete; adoption proposed only.
Release8535848/candidatewtgrq4n06qkbb, Mendelssohn Op49/66, eight movements.

All eight source leaves have ordered cached counterparts. Source/digital seconds:
558/557,396/396,223/223,495/494,621/622,424/424,225/225,475/477.
Every pair passes the existing max5second/3%tolerance, with no exception needed.
Every candidate track positively credits Istomin piano, Stern violin, Rose cello
and the source composer spelling. No track declares the collective source name.
Source notes distinguish1966/1980label dates; artist site describes the Op66
session inJuly1979. Do not infer exact sessions from label dates or ISRC years.

Istomin's own1990account identifies all three collective members. The artist-site
recording history corroborates the later Mendelssohn session. Reviewer paraphrases
and exact URLs are saved under `data/review_sources/trio-8535848/`; no audio used.
Reproduce `data/qobuz_trio_identity_diagnostic.json` with
`python scripts/qobuz_trio_identity_diagnostic.py` in the project environment.
Four targeted tests pass: positive eight-band checks, each member indispensable,
incomplete programme rejection, no majority waiver for a timing discrepancy.
No publication/ledger/global matcher changes. No Qobuz calls or push/deployment.

## Proposed bounded rule — not adopted

Represent this exact source collective as all three positively instrument-credited
members on every bound track, retaining the collective in displayed provenance.
Require exact raw source collective ID2593786, all three source member IDs/roles,
full source/target/album/track/external evidence hashes, two complete four-movement
work groups and unchanged source timing/composer checks. Never map collective to
one member, infer arbitrary ensemble membership, or waive any declared musician.
A future implementation should reject missing/substituted members, associated-only
roles, wrong instruments, wrong work/composer, changed source lineups, incomplete
bands and altered timings. Test full collection publication diff before adoption.

Current one-to-one `performer_aliases` cannot express this conjunction. The source
leaf adapter also deliberately preserves the collective requirement. No existing
review kind was stretched to bypass it. AGENTS.md allows autonomous continuation
only until a new review kind or open proposal is needed; this is that boundary.
Next action: user adoption of this narrowly scoped collective decomposition, then
implement/test the source-bound adapter and reassess8535848. Until then it remains
Unchecked with no recording decision; diagnostic evidence is not a published hold.

## User adoption and implementation

User inspected both album links and explicitly confirmed: “it's the same album,
it's correct, go ahead”. Proposal adopted for8535848/wtgrq4n06qkbbonly. Approval
is frozen with raw-source/target/album hashes and the exact collective/member
specification in `data/review_sources/trio-8535848/approval.json`. Earlier diagnostic
remains dated pre-adoption evidence, unchanged.

Source-leaf adapter now accepts this collective only as all3exact named instrument
credits on each bound track. It validates source collective ID2593786and all3raw
member IDs/roles, requires approval/external evidence, retains original collective
and member requirements in the programme, and leaves all existing composer,
source-band, timing and selected-track checks intact. No generic inference or
missing-member waiver. Onlythispublication record changes toProbable85.
`data/qobuz_trio_recording_audit.json` freezes the completed review.

Normalization/build pass; loaded local detail showsProbable85and8/8supported bands
with the approved limitation text. Browser reports existingfavicon404and cached
Qobuzthumbnail404; no metadata/search/auth/rate-limit warning, no API retrieval.
No exact pressing/take/transfer claim. No push/deploy.

All320script tests pass, including exact user approval/source lineup constraints,
all3member/instrument checks, missing-band rejection, unchanged old collective
gate when approval spec is absent, and timing/hash tamper rejection. Fixture429/STOP
output is simulated. Source/cache/Spotify data and global matching thresholds
unchanged. Next cached investigation:7956843RobinHoodDell/RCA recording identity.
