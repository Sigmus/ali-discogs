import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT, assess
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate


class TitleNineteenReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.albums = load_albums()
        cls.report = json.loads((ROOT/'data/qobuz_title19_recording_audit.json').read_text())

    def test_all19_and_future_high_score_hold_precedence(self):
        self.assertEqual(validate(self.report, self.rows, self.albums, self.reviews, expected_count=19),
                         {'reviewed': 19, 'withhold': 10, 'probable': 9})

    def test_all_french_suite_movements_and_physical_bands_retained(self):
        review = self.reviews['6268701']
        self.assertEqual(len(review['bindings']), 8)
        tracks = [i for b in review['bindings'] for i in b['track_ids']]
        self.assertEqual(len(tracks), 51)
        self.assertEqual(len(set(tracks)), 51)
        self.assertEqual([len(b['track_ids']) for b in review['bindings'][-2:]], [1, 10])
        missing_band = copy.deepcopy(review)
        missing_band['bindings'].pop()
        with self.assertRaises(ValueError):
            assess(self.rows['6268701'], self.albums[review['album_id']], missing_band)

    def test_bartok_and_prokofiev_musicians_stay_with_their_work(self):
        review = self.reviews['10598540']
        self.assertEqual(review['bindings'][1]['track_ids'], [175165, 175166])
        for b in review['bindings'][:2]:
            self.assertIn('George Szell', b['required_performers'])
            self.assertIn('Columbia Symphony Orchestra', b['required_performers'])
            self.assertNotIn('Eugene Ormandy', b['required_performers'])
        for b in review['bindings'][2:]:
            self.assertIn('Eugene Ormandy', b['required_performers'])
            self.assertIn('The Philadelphia Orchestra', b['required_performers'])
            self.assertNotIn('George Szell', b['required_performers'])
        altered = copy.deepcopy(review)
        altered['bindings'][0]['required_performers'].remove('George Szell')
        with self.assertRaises(ValueError):
            assess(self.rows['10598540'], self.albums[review['album_id']], altered)

    def test_birthday_annotations_are_explicit_and_source_bound(self):
        for rid in ['10598540', '23764721']:
            review = self.reviews[rid]
            self.assertTrue(review['source_composer_spellings'])
            altered = copy.deepcopy(review)
            del altered['source_composer_spellings']
            with self.assertRaises(ValueError):
                assess(self.rows[rid], self.albums[review['album_id']], altered)

    def test_bonus_and_source_discrepancies_remain_unresolved(self):
        for rid in ['5349319', '7946604', '6953193', '4046757', '8470218']:
            self.assertEqual(self.reviews[rid]['decision'], 'withhold')
        review = self.reviews['12524051']
        self.assertEqual(len(review['bindings']), 36)
        self.assertEqual(review['extra_track_ids'], [])
