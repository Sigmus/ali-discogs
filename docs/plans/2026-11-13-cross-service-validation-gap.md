# Spotify and Qobuz labels use different evidence standards

Recorded13November2026, Europe/Amsterdam, at the user's explicit request.

## Material limitation

Current Found/Probable counts are not an apples-to-apples measure of service
catalogue coverage. Most retained Spotify labels come from legacy album-level
search similarity (title, lead artists, conductor and other signals). Only a
bounded subset has been independently reviewed against track programmes.
Qobuz additions currently face stricter work/movement/credit and completeness
reviews before publication. A lower Qobuz count therefore reflects validation
policy and metadata/parser limitations as well as discovery/catalogue differences.
The percentages are heuristic scores, not comparable calibrated probabilities.

## Tristan example: Discogs2996680

- Target: Bohm/Bayreuth1966 Tristan, five-LP DG box. Raw Discogs source includes
  sideJ, `Karl Böhm Bei Der Probe: III. Aufzug: Vorspiel & 1. Auftritt`,29:20.
- Retained Spotify candidate0q781kMYrvKGeeCHRXrHcI is Probable0.737 with29tracks,
  selected by legacy album-level scoring. That label is not proof of the complete
  box programme or rehearsal-side coverage. Its full tracks have not been
  independently validated in this audit; equal track count alone proves nothing.
- Qobuz0002894497722 has29cached tracks spanning the main opera, no track labelled
  as that rehearsal side. This is strong evidence of the same main recording
  family, not an accepted complete-edition match. Chorus/orchestra alias and
  opera-context interpretation remain unresolved too.

The assistant previously described the rehearsal gap as the sole reason Qobuz
was withheld, and implied the same omission was verified on Spotify. That was
too strong: current Qobuz evaluation already fails work/credit grouping, and the
normalized target loses nested side detail. Full-release completeness has not
been established by that evaluator. Raw-source review exposes an additional
rehearsal requirement; Spotify track-level omission still needs verification.
Keep these observations separate from the implemented matcher behaviour.

## Follow-up proposal (not an adopted status-model change)

Use equivalent independently reviewed criteria across services. Distinguish:
main recording supported; full edition supported; partial programme/bonus gap;
unresolved; and confirmed incompatible recording. Preserve legacy labels and
make their evidence/validation stage visible until audited; do not silently
reinterpret every legacy Spotify Probable as full-programme confirmation.
Start with a paired Tristan audit including Spotify tracks and the rehearsal,
then design shared UI/status semantics. No label, score, matching logic or UI
changes are authorized merely by recording this limitation.
