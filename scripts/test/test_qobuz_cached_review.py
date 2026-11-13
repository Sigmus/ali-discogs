import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_cached_review import assess_labels, assess_opus_pieces
from qobuz_lead_review import ROOT, reviewed_candidate
from qobuz_snapshot import load_snapshot


class CachedHalfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.albums = load_snapshot()['albums']
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_cached_half_reviews.json').read_text())['releases']}

    def test_busch_keeps_three_concertos_and_rubinstein_keeps_every_mazurka(self):
        busch = self.reviews['8165012']
        candidate = reviewed_candidate(self.rows['8165012'], self.albums[busch['album_id']], busch)
        self.assertEqual((candidate['status'], candidate['covered']), ('probable', 3))
        self.assertNotIn('Affetuoso', [item['target'] for item in candidate['programme']])
        mazurkas = self.reviews['5939010']
        candidate = reviewed_candidate(self.rows['5939010'], self.albums[mazurkas['album_id']], mazurkas)
        self.assertEqual((candidate['status'], candidate['covered']), ('probable', 51))

    def test_a_changed_spelling_or_a_new_mode_conflict_fails(self):
        busch = copy.deepcopy(self.reviews['8165012'])
        busch['labels'][1]['title_contains'] = ['Affetuoso']
        with self.assertRaises(ValueError):
            assess_labels(self.rows['8165012'], self.albums[busch['album_id']], busch)
        mazurkas = copy.deepcopy(self.reviews['5939010'])
        mazurkas['mode_conflicts'] = []
        with self.assertRaises(ValueError):
            assess_opus_pieces(self.rows['5939010'], self.albums[mazurkas['album_id']], mazurkas)
