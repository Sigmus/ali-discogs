import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_match import expanded_candidate
from qobuz_snapshot import load_snapshot

ROOT = Path(__file__).resolve().parents[2]


class ReviewedExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.albums = load_snapshot()['albums']
        cls.inventory = json.loads((ROOT/'data/qobuz_work_inventory.json').read_text())

    def test_all_bounded_candidates_recompute_as_probable(self):
        scope = json.loads((ROOT/'data/qobuz_expansion_scope.json').read_text())['releases']
        self.assertEqual(len(scope), 10)
        for rid, ids in scope.items():
            for aid in ids:
                result = expanded_candidate(self.rows[rid], self.albums[aid], self.inventory)
                self.assertIsNotNone(result, (rid, aid))
                self.assertEqual(result['status'], 'probable')
                self.assertEqual(result['confidence'], .85)
                self.assertEqual(result['completeness']['status'], 'complete')

    def test_scope_cannot_override_wrong_missing_or_experimental_evidence(self):
        for rid, aid in [('1093216', '0002894778168'), ('1093216', '0002894805871'),
                         ('15282801', 'ezfmmvuhlu4uc'), ('2712474', 'd4y2z1shovo2a'),
                         ('3699703', '0002894791673')]:
            self.assertIsNone(expanded_candidate(self.rows[rid], self.albums[aid], self.inventory), (rid, aid))
        row = dict(self.rows['890111'], performers=['Different Pianist'])
        self.assertIsNone(expanded_candidate(row, self.albums['0002894776360'], self.inventory))
        self.assertIsNone(expanded_candidate(self.rows['890111'], self.albums['0002894776360'], {'works': []}))
