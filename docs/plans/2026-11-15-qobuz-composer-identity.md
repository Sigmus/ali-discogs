# Reviewed composer identity: Felix Mendelssohn

15 November 2026, Europe/Amsterdam. Offline refinement under AD-008.

Library of Congress authority n79139515 explicitly uses Felix Mendelssohn-Bartholdy
and Felix Mendelssohn for the composer:
https://www.loc.gov/item/n79139515/felix-mendelssohn-bartholdy-1809-1847/
The Mendelssohn Gesellschaft biography corroborates the family-name context:
https://mendelssohn-gesellschaft.de/en/mendelssohns/biografien/felix-mendelssohn-bartholdy

Adopted exact normalized full-name equivalence only in grouped Composer-role
identity. No surname-only or initial expansion, no Fanny/Moses alias, no changes
to performer matching or legacy score. Source-bound composer scopes, collision
checks and contiguous-group composer boundaries use the same canonical identity.
The baseline surname policy remains outside this exact exception. Bare structured
composer fields or producer credits do not activate the exception.

Two tests cover exact names, unrelated family members, Bernstein's two four-track
programmes and wrong composer/role/orchestra controls. Composer equivalence is not
completeness, recording-family proof or publication authorization.

Collection contains32copies naming Mendelssohn among composers. That is potential
scope, not a claim of32affected matches. Current cached candidate diff is recorded
in data/qobuz_composer_identity_audit.json after regeneration.


## Validated outcome

164script tests pass, including wrong family member, non-Composer role and wrong
orchestra controls. Full publication regeneration changes evidence for4releases
6686688/4009817/7064777/2877518, with no status changes. All other release records
unchanged, including both reviewed bindings. UI normalization/static build pass.

Screen2227pairs:8changed;6pairs gain coverage (Bernstein3956949 and5alternatives
for8962178),2gain possible work tracks but no credited coverage (3476755/19183792).
All remain unresolved by completeness/credits, not automatically accepted.
Inventory605unchecked unique:423work/credit,160metadata,8completeness,7withheld,
6empty,1source hold. Counts12Found/123Probable/606Unchecked copies unchanged.

Initial regression correctly rejected duplicate manual adds now naturally matched
by the new rule. Re-reviewed6472687joined Op64track and10757104eight symphony
movements; removed9redundant adds only. Exact reviewed assignments, source/album
hashes, required credits, programme/timing/version checks remain unchanged. No
generic idempotency bypass or weakened binding validator. Repeat suite passes.
No provider calls, push/deployment. Next Bernstein's eight movements need reviewed
inventories and recording-family evidence before any publication decision.
