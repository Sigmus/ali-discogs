# Eight cached near-misses, one pass

13 November 2026, Europe/Amsterdam. After Michelangeli, eight cached Qobuz
albums remain within two programme units of an unchecked release. The user
asked to review all eight in one pass, without pausing between them, and to
report only when the pass is finished. This document is that authorization.
No new catalogue or API calls.

Nine Discogs releases, eight albums:

| Discogs | Gap | Cached album | Named gap |
|---|---|---|---|
| 11562013 | 31/32 | `nrkspj3p5zasa` | Kempff sonata Op. 81a |
| 3475547, 11168177 | 18/19 | `5099973025054` | Rubinstein nocturne Op. posth. 72 No. 1 |
| 6029612 | 9/10 | `0002894783696` | Davis, *Der Schwan von Tuonela* |
| 4641786 | 17/19 | `zcagbe356rypb` | Haebler, two F-major sonatas; one is labelled KV 322 |
| 2383925 | 7/8 | `0884977171662` | Brubeck, Audrey |
| 5177097 | 6/7 | `xw3ecebytz0xa` | Getz/Byrd, Baia |
| 10102576 | 5/6 | `x8we8ykf2exc9` | Dutoit, *La Jeunesse d’Hercule* |
| 7525022 | 8/10 | `0002521867172` | Ellington, The Shepherd, both takes |

Rubinstein is one album on two Discogs releases. The Warner set is a nocturnes
and mazurkas superset of RCA LSC-7050. Extra works stay visible and do not fill
a missing nocturne.

## Rules for every release

- Hash-bind the collection row, the cached album and the raw Discogs file.
  Changed evidence requires the review to be written again.
- Probable stays capped at 85%. That is programme and credit support, not a
  verified take or mastering.
- A title may be paired with one cached track only when the review names both
  titles and the rest of the programme still matches with the required
  performer. No general alias table.
- A heading is a container only under the existing container-heading rule.
- A piece, take or singer that is absent from the cached album stays absent.
  KV 322 is not relabelled to a different Mozart sonata unless the source title
  and the cached track identify the same work.
- Movement completeness still has to be shown. A translated title does not
  prove that every movement is present.
- Each release ends as Probable 85 or stays Unchecked, with the reason kept
  visible. Withheld pairs are recorded so the same gap is not treated as open.
- Regenerate `data/qobuz_matches.json` after all eight reviews exist. Update
  context, history, decisions and the backlog with the outcomes together.
- Verify any newly published detail in the local explorer. Do not commit the
  implementation as part of this plan.

## Done when

All eight albums have a recorded decision, the match file is regenerated, and
the eight results are reported together.
