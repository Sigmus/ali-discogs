import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_coverage_pilot import discover


class CoveragePilotTests(unittest.TestCase):
    def test_cache_cross_search_and_alias_are_separate_from_baseline(self):
        row = {'title': 'Concerto', 'performers': ['David Oistrach'],
               'composers': ['Beethoven'], 'tracklist': [{'title': 'Concerto Op.61', 'type': 'track'}]}
        album = {'id': 'a', 'title': 'Concerto', 'tracks': {'items': [
            {'id': 1, 'title': 'Concerto Op.61', 'performers': 'David Oistrakh, Violin - Beethoven, Composer'}]}}
        result = discover({'1': row}, {'1': {'status': 'unchecked', 'candidates': []}},
                          {'albums': {'a': album}, 'metadata_completed_at': 'test'})
        c = result['proposals'][0]['candidates'][0]
        self.assertFalse(c['original_search_candidate'])
        self.assertEqual(c['unmodified_rules_status'], 'unchecked')
        self.assertTrue(c['requires_experimental_alias'])
        self.assertEqual(row['performers'], ['David Oistrach'])
        self.assertIn('Oistrakh', album['tracks']['items'][0]['performers'])

    def test_wrong_orchestra_and_incomplete_programme_remain_blocked(self):
        row = {'title': 'Concertos', 'performers': ['Alice'], 'ensembles': ['London Orchestra'],
               'tracklist': [{'title': 'Concerto Op.61'}, {'title': 'Concerto Op.62'}]}
        album = {'id': 'a', 'title': 'Concerto', 'tracks': {'items': [
            {'id': 1, 'title': 'Concerto Op.61', 'performers': 'Alice, Piano - Vienna Orchestra, Orchestra'}]}}
        prior = {'1': {'status': 'unchecked', 'candidates': []}}
        snap = {'albums': {'a': album}, 'metadata_completed_at': 'test'}
        self.assertEqual(discover({'1': row}, prior, snap)['proposals'], [])
        album['tracks']['items'][0]['performers'] = 'Alice, Piano - London Orchestra, Orchestra'
        self.assertEqual(discover({'1': row}, prior, snap)['proposals'], [])
