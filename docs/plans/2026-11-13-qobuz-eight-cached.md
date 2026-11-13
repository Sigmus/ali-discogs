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

## Result

Reviewed together on 13 November 2026. No new catalogue calls. Copies are now
12 Found / 83 Probable / 646 Unchecked; unique 12/83/645.

Probable 85:

- Kempff11562013. All 32 sonatas. Op. 81 A is Op. 81a. The Sonata No. 12 scherzo
  is tagged Op. 22 and is pulled back by its sonata number. The Waldstein
  introduction shares the rondo track. Heritage 2018 is not the 1964 mono box.
- Rubinstein3475547 and11168177. All 19 nocturnes. Op. Posth. 72 No. 1 is the
  posthumous nocturne. The 51 mazurka tracks stay outside the LP.
- Davis/Sibelius6029612. The seven symphonies, Finlandia, Swan of Tuonela and
  Tapiola, with Davis and Boston on those tracks. Symphony 7 is split into five
  tracks. Nine other tracks stay outside, including the London Symphony violin
  concerto.
- Jazz Samba5177097. Baia is the track spelled Bahia. The 2:03 second
  Desafinado stays outside. Bahia’s duration differs from the LP.
- Ellington7525022. Take 1 is the 5:47 Shepherd track and take 2 is the 6:32
  track. The digital titles do not print the take numbers.

Withheld:

- Haebler4641786. “Sonate F-Dur” and “Sonate F-Dur, KV 322” do not identify
  K. 332 or K. 533/494. KV 322 is not relabelled.
- Time Out2383925. Audrey, the 1954 bonus, is absent from the Legacy Edition.
- Saint-Saëns10102576. *La Jeunesse d’Hercule*, Op. 50, is absent. The five
  concertos do not replace it.
