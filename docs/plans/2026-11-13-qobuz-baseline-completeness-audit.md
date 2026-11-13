# Original Qobuz baseline: completeness audit

Date: 2026-11-13, Europe/Amsterdam. User requested committing the expansion,
then auditing the original 66 matches. Checkpoint: `c1857a7`. No push requested.

## Scope and reproducibility

Frozen scope `data/qobuz_baseline_audit_scope.json` is extracted from commit
`7ea8898f9fa97213f331ec0005c2f7d308170405`: the 12 Found and 54 Probable selected
albums before expansion. The ten newly added Probable releases are excluded.

Run `uv run python scripts/qobuz_baseline_audit.py`. It uses only the committed
snapshot, collection, frozen scope and 24-work inventory; no API requests, mutable
cache, credentials or Git history are needed at replay time. The research output
`data/qobuz_baseline_audit.json` records each original selection, recomputed v1
mapping, title-matched tracks, missing performer evidence, completeness checks,
diagnostic flags and input fingerprints. It never writes publication matches.

This is a programme/metadata audit, not a recording-session or audio-cut audit.
The full 66 target-to-credited-track mappings were inspected for counts, movement
labels and overlaps; all eleven releases with automatic diagnostic flags received
closer cached track/title/credit inspection. The output table below covers every
selection. There is no statistical precision/recall estimate.

## Results

- All 66 selections reproduce their original v1 status. All 12 Found selections
  retain their original one-to-one catalogue correspondences; that criterion is
  not an independent proof that an entire composition or recording is present.
- Seven meet the stricter movement/timed-target coverage check: three Found and
  four Probable. Their evidence is scoped to sourced works or listed timed tracks.
- One has incomplete **credited** movement coverage: Mutter/Karajan Mozart
  concertos, release 1026299. All six movements exist in the cached album; Mutter
  is absent from four track-credit records. Do not describe this as missing music.
- 58 remain unresolved under the stricter checker: nine Found and 49 Probable.
  Limited inventory, absent LP timings, unnumbered/grouped tracks, missing work
  context or partial credits prevent automatic verification. Unknown is not a
  confirmed wrong match and is not evidence of catalogue absence.
- No confirmed missing-music conclusion is established by this audit. Several
  apparently partial v1 mappings are explained by metadata/rule limitations.
  This is not a clean bill of health: the unresolved programmes still need work.
- Publication stays 12 Found / 64 Probable / 664 unchecked unique releases,
  including the separately reviewed expansion. No automatic reclassification.

Eight releases have title matches without full required credits, four have a
single credited track under at least one work heading, and one has shared track
assignments. Groups overlap: eleven distinct releases flagged. Flags are diagnostic
leads; the Polonaises and excluded alternate-orchestra performances show why a
flag cannot itself justify a downgrade.

## Closer inspection of every flagged release

| Discogs ID | Evidence and conclusion | Follow-up |
| --- | --- | --- |
| 1026299 | K.216 I–III and K.219 I–III all appear. Only K.216 II (13277660) and K.219 III (13277671) list Mutter in parsed credits; Karajan/Berlin are present on all six. Credit evidence incomplete; no missing-music claim. | Require explicit recording-group evidence before filling missing soloist credits. |
| 2559625 | Monteux/Vienna Symphonie fantastique: first title includes Op.14/work context, next four titles are bare numbered movements 2–5. All five carry the expected composer/conductor/orchestra. v1 maps only the first because it checks titles independently. | Reconstruct explicit album/work context without crossing into the following Mendelssohn works. |
| 2949124 | Three Polonaises each map to one named track; the accompanying Sonata has four mapped movements. A single track per work heading is normal here, not itself an error. | Add sourced structure or timing evidence; retain unknown meanwhile. |
| 3958148 | Grieg Peer Gynt I and Sibelius Pelléas both use Op.46. v1 assigns the same 13 tracks to each heading because it accepts the shared opus and any listed composer. The album actually contains separate four-track Grieg and nine-track Sibelius groups. No confirmed absent programme, but the mapping is misleading. | Bind composer and work identity per target group, not album-wide composer membership. |
| 4685996 | Winterreise lists Nos.1–24. No.5 (1037506) lacks Fischer-Dieskau in parsed credits; v1 counts only 23 supporting songs. | Distinguish missing credits from absent tracks; independently review recording-group continuity. |
| 8418209 | Mozart Requiem has 14 named sections. v1 supports only two because it requires chorus and all target soloists together on every supporting track. Other sections list different subsets of those performers. | Role-aware, group-level soloist evidence; do not assume every soloist sings every section. |
| 9932715 | Schumann anthology includes more than one Fourth Symphony. Four title hits lack the target Berlin orchestra; a separate fully credited group supplies all four target movements. | Preserve exclusion of the other-orchestra group; do not infer a missing programme from rejected distractors. |
| 12774826 | Berlioz Te Deum has six named sections. Four lack Alexander Young in parsed credits, leaving only two fully credited supports. | Role-aware recording groups, with missing-credit versus participation uncertainty retained. |
| 14338491 | Pergolesi Stabat Mater has 12 numbered sections in the album; alternating soloist credits leave only seven supporting tracks. Additional Scarlatti Stabat Mater sections are also title hits but fail target credits. | Associate composer/work first, then review role-specific participation. |
| 15282801 | The Decca anthology includes Vienna and Concertgebouw Eroica groups. The wrong-orchestra group is excluded; a separate Concertgebouw I–IV group passes completeness. | Keep this negative control when changing group/credit rules. |
| 18770818 | Shostakovich Fourth has I–III with the target orchestra. First movement credits Kiril Kondrashin; II/III use Kirill, so v1 maps only I. | Verify the explicit alias before adoption; do not apply general fuzzy conductor matching. |

Other reviewed grouping limitations include split Berlioz III (6913643), joined
Cherubini Requiem sections across two tracks (4197603), grouped Liszt movements
(1855288) and complex sonata joins in the complete Beethoven set (7678883).
They remain unresolved; no movement-count guesses were introduced in this audit.

## Recommended next work — proposed, not implemented

Prioritise an offline recording/work-group model before another discovery batch:

1. Bind each target work to a composer plus catalogue identity and preserve title
   distinctions. Prevent shared opus numbers from merging unrelated works.
2. Carry explicit work context into abbreviated movement titles only inside
   supported boundaries. Do not spill into adjacent works or recordings.
3. Separate conductor/ensemble identity from role-specific soloist participation.
   Require evidence across a coherent recording group; never fill credits from
   album-wide membership alone or combine different performances to make coverage.
4. Add verified explicit spelling aliases and broader sourced structures; retain
   unknown for unresolved splits/joins or recording-session identity.

Use the eleven reviewed cases, wrong-orchestra controls, partial Kleiber albums,
Part II A/B/C and opus subdivisions as regression controls. Reaudit all 66 plus
the ten expansion cases before changing publication status or adding candidates.
Any new catalogue search remains a separately authorized slow operation.

Validation: all 36 Qobuz mocked/offline tests pass, including three audit tests
for frozen-scope exclusion, original-score replay, present movements with missing
credits and overlapping work assignments. Publication file is unchanged from the
checkpoint; repeated audit generation is byte-identical. No API calls, push,
merge or deployment. Audit artifacts/docs are left uncommitted after the checkpoint.

## Complete selection table

`Supported` below means the stricter metadata coverage gate passed. `Credit gap`
means all expected movement titles are present but full required track credits
are not. `Unresolved` is not a failed or absent recording.

| Discogs ID | Original status | Completeness audit | Target |
| --- | --- | --- | --- |
| 1026299 | Probable | Credit gap | Violinkonzerte = Violin Concertos (No.3 G-dur = G Major KV 216 · No.5 A-dur = A Major KV 219) |
| 1445439 | Found | Unresolved | Glenn Gould Plays Music Of William Byrd And Orlando Gibbons |
| 1477603 | Found | Unresolved | Back To Back (Duke Ellington And Johnny Hodges Play The Blues) |
| 1607240 | Probable | Unresolved | 12 Etudes D'Exécution Transcendante / 3 Etudes De Concert |
| 1855288 | Probable | Unresolved | Piano Concerto No. 1 / Piano Concerto No. 2 |
| 2151729 | Probable | Unresolved | Concerto In D, Op. 35 |
| 2207158 | Probable | Supported | The Chopin Ballades |
| 2208689 | Probable | Unresolved | Concerto No. 1 |
| 2218786 | Probable | Unresolved | Piano Concerto |
| 2279849 | Found | Supported | Les Ballades |
| 2559625 | Probable | Unresolved | Symphonie Fantastique |
| 2799449 | Found | Unresolved | Sings The Blues |
| 2939272 | Found | Supported | Sketches Of Spain |
| 2949124 | Probable | Unresolved | Sonate No.3 / Polonaises Nos. 3 · 4 · 6 |
| 2955185 | Probable | Unresolved | L'Oiseau De Feu - Le Chant Du Rossignol |
| 3097437 | Probable | Unresolved | Concerto No. 1 |
| 3154926 | Probable | Unresolved | Piano Concerto No. 2 |
| 3417675 | Probable | Unresolved | Cello Concerto |
| 3507687 | Probable | Unresolved | Symphonie No. 4 |
| 3622476 | Probable | Unresolved | Dvořák Cello Concerto |
| 3759065 | Found | Supported | The Köln Concert |
| 3773687 | Probable | Unresolved | Symphonie Fantastique |
| 3958148 | Probable | Unresolved | Peer Gynt Suites 1 & 2 / Pelléas Et Mélisande |
| 4197603 | Probable | Unresolved | Requiem Mass In C Minor |
| 4226783 | Probable | Unresolved | Violin Concerto |
| 4305503 | Probable | Unresolved | Mein Herze Schwimmt Im Blut / Jauchzet Gott In Allen Landen |
| 4478666 | Found | Unresolved | Disney Songs The Satchmo Way |
| 4540319 | Probable | Unresolved | Symphony No.5 / Hussite Overture |
| 4685996 | Probable | Unresolved | Winterreise |
| 4719816 | Found | Unresolved | The Chopin Scherzos |
| 5286520 | Probable | Unresolved | Concerto In D Major |
| 6115834 | Probable | Unresolved | Symphony No. 2 |
| 6115836 | Probable | Unresolved | Symphony No.4 / Overture: In Nature's Realm |
| 6118529 | Probable | Unresolved | Symphony No. 3 / Symphonic Variations, Op. 78 |
| 6119238 | Probable | Unresolved | Symphony No. 6 / Overture 'My Home' |
| 6175022 | Probable | Unresolved | Sonaten (No. 15 »Pastorale« ∙ No. 3) |
| 6426884 | Probable | Unresolved | Symphony No. 8 |
| 6575638 | Probable | Unresolved | Symphony No. 7 In D Minor |
| 6913643 | Probable | Unresolved | Symphonie Fantastique |
| 6919420 | Probable | Unresolved | Eroica-Variationen / Piano Sonata No.7 |
| 7001990 | Found | Unresolved | Four Suites For Orchestra |
| 7159852 | Probable | Unresolved | Études Op. 10 Et Op. 25 |
| 7678883 | Probable | Unresolved | The Piano Sonatas |
| 7871589 | Probable | Supported | "Carnival" Overture; Scherzo Capriccioso; The Golden Spinning Wheel |
| 7888645 | Probable | Unresolved | Piano Concerto No.1 / Piano Concerto No.2 |
| 8316658 | Found | Unresolved | Preludes Book I |
| 8418209 | Probable | Unresolved | Requiem |
| 8597411 | Found | Unresolved | Satchmo Sings |
| 9387170 | Probable | Unresolved | The Piano Concertos |
| 9521183 | Found | Unresolved | Les Scherzos Les Impromptus |
| 9932637 | Probable | Unresolved | 9 Symphonies |
| 9932715 | Probable | Unresolved | 4 Symphonies |
| 10480488 | Probable | Unresolved | Symphony No.7 |
| 12122769 | Probable | Unresolved | Concerto No. 2, In B Flat Major For Piano And Orchestra |
| 12189169 | Probable | Unresolved | Cello Concerto No.2 / Chant Du Ménestrel |
| 12774826 | Probable | Unresolved | Te Deum |
| 13509145 | Probable | Unresolved | Symphony No.2 |
| 14338491 | Probable | Unresolved | Stabat Mater |
| 14448160 | Probable | Unresolved | Pictures At An Exhibition |
| 15282801 | Probable | Supported | Symphony No. 3 In E Flat Major Opus 55 "Eroica" |
| 15390424 | Probable | Unresolved | Sinfonia N.º 2 |
| 18770818 | Probable | Unresolved | Symphony No. 4 |
| 23695508 | Probable | Unresolved | Symphony No. 6 "Pathetique" |
| 28133197 | Probable | Unresolved | Symphonie No. 1 / Karelia Suite |
| 28220854 | Probable | Unresolved | Sonaten No. 17 »Der Sturm/The Tempest« • No. 18 |
| 34875983 | Probable | Supported | Symphony No. 5 In C Minor Op. 67 |
