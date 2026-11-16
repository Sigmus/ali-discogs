import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT, assess
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate


class CreditSampleRecordingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.albums = load_albums()
        cls.report = json.loads((ROOT/'data/qobuz_credit12_recording_audit.json').read_text())

    def test_all12_outcomes_and_high_score_hold_precedence(self):
        self.assertEqual(validate(self.report, self.rows, self.albums, self.reviews, expected_count=12),
                         {'reviewed': 12, 'withhold': 11, 'probable': 1})
        self.assertEqual(self.reviews['1723557']['decision'], 'withhold')
        self.assertEqual(self.reviews['1180104']['decision'], 'withhold')

    def test_reiner_all_four_movements_and_explicit_positive_credits(self):
        review = copy.deepcopy(self.reviews['1896362'])
        self.assertEqual([b['track_ids'] for b in review['bindings']], [[192486], [192487], [192488], [192489]])
        self.assertTrue(assess(self.rows['1896362'], self.albums[review['album_id']], review)[0]['eligible'])
        review['bindings'].pop()
        with self.assertRaises(ValueError):
            assess(self.rows['1896362'], self.albums[review['album_id']], review)
