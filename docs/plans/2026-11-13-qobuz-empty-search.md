# Twenty searches for releases with no saved hit

2026-11-13, Europe/Amsterdam. User asked for more searches. The search itself published nothing.

`scripts/qobuz_empty_search.py` selects twenty releases from the 324 that had no
saved Qobuz hit, excluding the comparison, round-two and query-trial scopes.
The twenty are evenly spaced by release ID. Each gets two queries, at most five
albums, fifteen seconds between requests. Output is
`data/qobuz_empty_searches.json.gz` and `data/qobuz_empty_search_results.json`.
A hit is not an accepted match. An empty query is not confirmed absence.

A few queries were rewritten before the run because the planner named the wrong
person or the wrong work: Solti for Walküre, Klemperer for the Eroica, Barbirolli
for the two Mahler symphonies, BWV 201 for the cantata, and the named works for
Harasiewicz, Gieseking, Kubelik, the Hungarian Quartet, Cluytens and Janis.

Completed without a STOP file: 40 queries, 31 nonempty, 19 releases with hits,
126 pairs. Sellheim 7421796 returned nothing on both queries.

No album/get followed that search. A later read of the title-aligned hits
downloaded five albums, 37 tracks, into `data/qobuz_empty_search_metadata.json.gz`.
Harasiewicz 6534486 was left out: `0002894632942` is a 10-track recital, not the
Philips box.

Toscanini 10757104 / `3614591367922` is Probable 85. Both symphonies have four
movements, and Toscanini and the NBC Symphony are on every track. The link is
`https://www.qobuz.com/fr-fr/album/mendelssohn-symphonies-italienne-reformation-arturo-toscanini-nbc-symphony-orchestra/3614591367922`.
The BNF file is not verified as the 1980 RCA Victrola pressing.

BWV 201 `3610154303352` is Probable 85. The heading is not a third work.
Nr. 1–7 and Nr. 8–15 are the fifteen movements, in order. Kurt Thomas and the
Gewandhaus are on every track, the Thomanerchor is on both sides, and Günther
Leib, Theo Adam, Eva Fleischer, Adele Stolte, Rolf Apreck, and Hans-Joachim
Rotzsch each appear. The link is
`https://www.qobuz.com/fr-fr/album/bach-der-streit-zwischen-phoebus-und-pan-bwv-201-gewandhausorchester-leipzig-thomanerchor-kurt-thomas/3610154303352`.
The BNF file is not verified as Musique Royale 199 021. Barbirolli `5099943329052` is the Fifth with the
New Philharmonia, and `5099991872555` is the Ninth with the Berliner
Philharmoniker. Neither file contains both symphonies. Cluytens
`3614596892627` has Psyché and the Rédemption excerpt, and not Le Chasseur
maudit. None of those three releases is published.
