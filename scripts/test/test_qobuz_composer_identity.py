import copy
import gzip
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_match import ROOT,evaluate,evaluate_v1
from qobuz_composer_identity import composer_key,reviewed_equivalence

class ComposerIdentityTests(unittest.TestCase):
    def test_exact_full_names_only(self):
        self.assertEqual(composer_key('Felix Mendelssohn-Bartholdy'),composer_key('Felix Mendelssohn'))
        for name in ['Fanny Mendelssohn','Moses Mendelssohn','Mendelssohn','F. Mendelssohn','Felix Mendelssohn Bartholdy the Younger']:
            self.assertNotEqual(composer_key(name),composer_key('Felix Mendelssohn'))
        self.assertFalse(reviewed_equivalence(['Fanny Mendelssohn'],['Felix Mendelssohn']))

    def test_bernstein_support_requires_positive_composer_and_performer_credits(self):
        row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='3956949')
        album=next(r['album'] for r in json.loads(gzip.decompress((ROOT/'data/qobuz_metadata_followup_2026_11_15.json.gz').read_bytes()))['metadata'] if r['album']['id']=='cxg5qouu14c6b')
        self.assertEqual(evaluate_v1(row,album)['covered'],0)
        result=evaluate(row,album)
        self.assertEqual(result['covered'],2)
        self.assertEqual([len(p['track_ids']) for p in result['programme']],[4,4])
        for change in ['composer','role','orchestra']:
            a=copy.deepcopy(album)
            for t in a['tracks']['items']:
                if change=='composer':t['performers']=t['performers'].replace('Felix Mendelssohn','Fanny Hensel')
                if change=='role':t['performers']=t['performers'].replace('Felix Mendelssohn, Composer','Felix Mendelssohn, Producer')
                if change=='orchestra':t['performers']=t['performers'].replace('Israel Philharmonic Orchestra','Different Orchestra')
            self.assertEqual(evaluate(row,a)['covered'],0)
