"""Reviewed exact full-name composer identities; never performer/surname aliases."""
from ali_discogs.text import norm

# Library of Congress authority n79139515 and its linked biography identify
# Felix Mendelssohn / Felix Mendelssohn-Bartholdy as the same composer.
# https://www.loc.gov/item/n79139515/felix-mendelssohn-bartholdy-1809-1847/
FELIX_NAMES = frozenset({'felix mendelssohn', 'felix mendelssohn bartholdy'})

def composer_key(name):
    key = norm(name)
    return 'felix mendelssohn' if key in FELIX_NAMES else key


def reviewed_equivalence(declared, credited):
    """Require positive Composer roles and exact reviewed full-name variants."""
    return any(norm(a) in FELIX_NAMES and norm(b) in FELIX_NAMES
               for a in declared for b in credited)
