# Bitches Brew credit gap

Updated: 2026-11-13, Europe/Amsterdam

Status: proposal. Discogs `7609610` stays unchecked. No matcher or UI change
is authorized by this note.

## What is saved

Ali’s copy is a 2015 Columbia / Sony / Legacy 180 g double LP of *Bitches Brew*,
© 1970, 2015, recorded 19–21 August 1969. The six titles are the original
programme.

Discogs names Larry Young, electric piano, on A, C1 to D1: Pharaoh’s Dance,
Spanish Key, John McLaughlin, and Miles Runs the Voodoo Down. Joe Zawinul,
electric piano, is named on A to C1 and on Sanctuary (D2). Young is absent from
Bitches Brew and Sanctuary. Zawinul is absent from John McLaughlin and Miles
Runs the Voodoo Down.

Two cached Qobuz editions carry the six titles and credit Young on Pharaoh’s
Dance and Spanish Key only:

- `0886443874428`, Columbia/Legacy, six tracks, dated 1970-03-30. John
  McLaughlin is track `38359946`. Miles Runs the Voodoo Down is `38359947`.
  The John McLaughlin credit string names Joe Zawinul.
- `0074646577424`, Columbia-Legacy, seven tracks. The same two titles omit
  Young. Feio, track `2344857`, is not on this LP.

The matcher reports 4/6. Those two titles match as works and fail the required
credit. The release stays unchecked. Outside knowledge of the 1969 sessions
agrees that Young belongs on those four titles; that knowledge is not a credit
in the Qobuz file.

## Matching questions

These are not rules yet.

- Whether a hash-bound review may accept the six titles when the missing name
  appears on other tracks of the same file.
- Whether a contradictory name blocks that review. Here the digital John
  McLaughlin credit includes Zawinul, and this Discogs copy does not put him
  on C2.
- Whether session knowledge may supply a player the file does not name.
- Whether Feio stays an extra if the six titles are accepted.
- Whether any acceptance stays one release, capped at Probable 85, with the
  2015 vinyl and the digital file left as different masterings.
- A Love Supreme `594243` has the same shape: the programme is the known album,
  and a required player, McCoy Tyner, is absent from the credit string. A rule
  for one does not automatically cover the other.

## UI questions

The explorer already shows each Qobuz candidate as unchecked, with `4/6` and
the line “required credits not supported” on the two titles. It does not name
Young or Zawinul in that line.

Still to decide, before any change:

- Whether the album row may say that the six titles identify *Bitches Brew*
  while the credit check failed.
- Whether the missing player and the contradictory Zawinul credit are named in
  the programme evidence.
- Whether Feio is shown as a track outside the LP.
- Whether a score, a Probable label, or a selected album appears before a
  review decision.
- Which of those facts stay in the detail disclosure rather than the album row
  or the status filter.

Done when: the matching exception and the UI wording are chosen, or explicitly
rejected. Implementation is a separate step.
