# Qobuz work grouping and performer-role evidence

Date: 2026-11-13, Europe/Amsterdam. User authorized implementing the baseline
audit recommendations. Entirely offline; no new Qobuz requests.

## Implemented rules

`qobuz-work-groups-v1+reviewed-expansion-v2` is now the publication matcher.
`evaluate_v1` and `credits_v1` preserve the original policy for reproducible
historical baseline auditing. Current `evaluate` delegates to
`scripts/qobuz_work_groups.py`:

- Shared opus identities across target works on multi-composer releases require
  explicit composer-role membership plus distinctive target work-name evidence.
  This separates Grieg Peer Gynt Op.46 and Sibelius Pelléas Op.46. Ambiguous
  generic headings cannot pass that route. Outside this collision case, the old
  composer-name evidence policy is preserved: incomplete album-level composer
  lists and spelling differences do not alone trigger new downgrades. Full
  target-level composer disambiguation across all generic works remains limited.
- Abbreviated numbered movement titles can inherit a preceding explicit work
  prefix only along a consecutive sequence with unchanged composer-role identity
  and target conductor/ensemble support on every track. Disc/track-number changes,
  incompatible structured work fields, changed anchors/composer or a new explicit
  work terminate context. Structured-work formatting variants require equal
  catalogue identities and corroborating name words. Original cached metadata is
  never edited; inherited title parent IDs are recorded in evidence.
- Current credit parsing recognizes explicit vocal and choir/chorus roles as
  performance evidence, retaining the old role parser for historical replay.
- Group-level performer coverage is allowed only within a contiguous work run,
  with conductor/ensemble anchors on every track, one consistent explicit
  composer-role identity, no repeated titles or numbered movement restarts/gaps,
  and each required performer evidenced somewhere in that run. Unknown extra
  musical main artists/soloists block repair, including publisher metadata
  incorrectly labelled MainArtist. Multiple qualifying performances do not get
  merged. No general fuzzy person matching or new name aliases were enabled.
- Group-assisted results are capped at Probable 85%. Newly qualifying first-pass
  candidates also require programme completeness before publication promotion.
  Otherwise they stay Unchecked with the new evidence and a review explanation.
  The existing ten-release cache expansion still uses its fixed reviewed scope
  and recomputes credit/completeness checks.

These are conservative metadata groups, not independently verified sessions.
An unmarked alternate take or audio cut can still evade catalogue metadata checks.
Existing Probable work headings retain their documented completeness limitations;
this implementation does not retroactively validate every unresolved structure.

## Reaudit and observed results

`uv run python scripts/qobuz_group_audit.py` writes
`data/qobuz_group_audit.json`, comparing original v1 and current evidence for the
66 frozen baseline selections plus ten reviewed expansion releases. Inputs are
fingerprinted. The separate original-baseline audit remains frozen to v1.

All 76 selected statuses remain unchanged; no shared target-track assignments
remain in this audit. Five programme mappings change:

| Discogs ID | Before | Current evidence |
| --- | --- | --- |
| 2559625 | Monteux/Vienna Berlioz: one supported movement | Five; four abbreviated titles inherit the explicit first work prefix. |
| 3958148 | Same 13 tracks assigned to both Grieg and Sibelius Op.46 headings | Separate 4-track Peer Gynt I, 4-track Peer Gynt II and 9-track Pelléas groups. |
| 4685996 | Winterreise: 23 credited songs | 24; explicit baritone credit is recognized, without inventing a missing singer credit. |
| 14338491 | Pergolesi Stabat Mater: seven fully co-credited sections | All 12 supported across one conservative role-aware group; alternating soloist participation is retained. |
| 1469965 | Some raw title hits included another composer's material | Nonmatching composer title hits filtered; the same three supported Wagner transcriptions retained. |

The strict coverage checker supports 17 of these 76 (seven original + ten
expansion cases), with one incomplete-credit and 58 unknown results. Thus better
mapping does not imply that more entire programmes have independently passed.

Two previously unresolved release leads have stronger performer evidence:
6381208 (Klemperer Missa Solemnis) and 6599326 (Dvořák Requiem). They remain
Unchecked because the current completeness inventory cannot establish the full
programme. No confidence is published for these withheld leads.

Mutter/Karajan remains partially credited: extra publisher names tagged as
MainArtist make group repair ambiguous. Kiril/Kirill remains unresolved without
a verified alias. Complex Mozart Requiem subsections, grouped/unnumbered works
and other session-identification gaps still require review.

All 740 unique-release classifications are identical to checkpoint c1857a7:
12 Found / 64 Probable / 664 unchecked; collection copies 12 / 64 / 665.
No thresholds lowered, no automatic commit/push/merge/deployment.

## Validation

All 43 Qobuz mocked/offline tests pass, including new controls for alternating
roles, wrong orchestra, extra soloist, repeated/disjoint performances, context
boundaries, real Grieg/Sibelius and Berlioz fixes, withheld new leads and all 76
reviewed selections. Historical original-66 audit still reproduces 12/54 exactly.
UI normalization/overlay/sort tests, JS syntax, static build and diff checks pass.
Browser verified `12 tracks supported by recording-group credits` in Stabat Mater
and the four inherited movement-title explanations in Berlioz details.

Repeated generation is checked for identical output. No credentials or raw caches
are needed by these commands, and no retrieval inputs were modified. Research
reports and inventories stay outside the Pages artifact; published sidecar contains
only the relevant catalogue evidence and explanations.

Next proposed step: independently establish programme completeness for the two
withheld choral leads, then verify a bounded set of explicit name aliases. Broader
searches or general credit inheritance remain separate work.
