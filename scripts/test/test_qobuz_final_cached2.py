import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_credit_role_audit import load_albums
from qobuz_lead_review import ROOT, assess
from qobuz_fullsupport16_audit import validate


class FinalCachedLeadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.albums = load_albums()
        cls.report = json.loads((ROOT/'data/qobuz_final_cached2_recording_audit.json').read_text())

    def test_two_decisions_and_high_score_hold_precedence(self):
        self.assertEqual(validate(self.report, self.rows, self.albums, self.reviews, expected_count=2),
                         {'reviewed': 2, 'probable': 1, 'withhold': 1})

    def test_source_typo_preserved_and_no_overture_can_disappear(self):
        review = copy.deepcopy(self.reviews['9283162'])
        self.assertIn('Luftschloss', review['source_leaves'][2]['title'])
        self.assertEqual(review['bindings'][2]['track_ids'], [527170])
        self.assertEqual(len(review['bindings']), 5)
        review['bindings'].pop()
        with self.assertRaises(ValueError):
            assess(self.rows['9283162'], self.albums[review['album_id']], review)
