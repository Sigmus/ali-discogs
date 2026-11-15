# Associated-performer credit semantics

15 November 2026, Europe/Amsterdam. Proposed AD-008 follow-up; no credit-policy
change or provider retrieval authorized by this document.

## Observed evidence

Reiner2463301/td12jypyopyqb has complete diagnostic5+8work bindings. Chinese
March279922682names Chicago Symphony Orchestra solely as `AssociatedPerformer`.
The other sections have accepted performer roles. The exact candidate remains
Unchecked under an explicit hold; borrowing another section’s credit is forbidden.

`scripts/qobuz_credit_role_audit.py` reproduces the offline census across1164cached
albums.775associated-only declarations:540spaced and235compact.540names are
accepted solely via their associated declaration; five more are recognized through
another declaration on the same track.288declarations reference required names in
saved candidate records. These are declaration/candidate counts, not false matches,
unique recordings or an accuracy estimate. Per-track hashes and references saved
in `data/qobuz_credit_role_audit.json`; inspect current output before using counts.

The current token parser accepts the spaced form via its `performer` token but
not the compact form. This inconsistency is observed behaviour, not an adopted
semantic distinction. Legacy scorer/parser remain unchanged.

[DDEX’s role definition](https://service.ddex.net/dd/DD-AVS-CURRENT/dd/avs_ContributorRole_RDR.html)
describes work-identification association. Whether Qobuz’s track field guarantees
recording participation is unresolved; the standard alone does not establish
Qobuz’s implementation contract.

## Recommended bounded next step

Keep current publication stable and Reiner held. Inspect a risk-based sample of
spaced-only accepted candidates and compact-only blocked candidates using actual
source/track/recording evidence. Seek primary provider documentation for the field.
Do not globally recognize compact roles merely to increase coverage, or demote all
spaced cases merely because the parser differs. No accuracy calibration follows
from this census.

Any adopted interpretation must specify recording versus work identity, source
musician requirements, exact role normalization, negative producer/composer cases,
existing-review precedence and the affected publication diff. Cross-track credit
borrowing and invented instrument roles remain forbidden. Wider provider retrieval
or bulk relabelling requires a separate concrete scope. This is a proposal, not a
new exception or a blocker to independent cached reviews.
