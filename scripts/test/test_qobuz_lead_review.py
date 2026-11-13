import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import load_reviews, assess, reviewed_candidate, fingerprint, target_fingerprint
from qobuz_completeness import movement_number

ROOT = Path(__file__).resolve().parents[2]


class PilotLeadReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reviews, cls.albums = load_reviews()
        cls.reviews = {r['discogs_id']: r for r in reviews}
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}

    def test_three_qualified_probables_and_wrong_cycle_excluded(self):
        for rid, review in self.reviews.items():
            result = reviewed_candidate(self.rows[rid], self.albums[review['album_id']], review)
            if rid == '3066447':
                self.assertIsNone(result)
            else:
                self.assertEqual((result['status'], result['confidence']), ('probable', .85))
                self.assertEqual(result['completeness']['status'], 'complete')

    def test_changed_target_or_album_requires_review(self):
        rid = '37312800'; review = self.reviews[rid]
        album = self.albums[review['album_id']]
        row = copy.deepcopy(self.rows[rid]); row['performers'] = ['Different Conductor']
        with self.assertRaises(ValueError): assess(row, album, review)
        broken = copy.deepcopy(album); broken['tracks']['items'].pop()
        with self.assertRaises(ValueError): assess(self.rows[rid], broken, review)

    def test_missing_or_wrong_credited_movement_cannot_be_promoted_even_if_rehashed(self):
        rid = '37312800'; review = self.reviews[rid]
        for change in ['remove', 'credits', 'repeat']:
            album = copy.deepcopy(self.albums[review['album_id']])
            track = next(t for t in album['tracks']['items'] if t['id'] == 41419222)
            if change == 'remove': album['tracks']['items'].remove(track)
            elif change == 'credits': track['performers'] = 'Different Orchestra, Orchestra - Different Conductor, Conductor'
            else: track['title'] = track['title'].replace(': 4.', ': 3.')
            amended = dict(review, album_sha256=fingerprint(album))
            self.assertIsNone(reviewed_candidate(self.rows[rid], album, amended), change)

    def test_joined_movement_permission_is_exact_and_not_global(self):
        review = self.reviews['4429613']; album = self.albums[review['album_id']]
        item = next(t for t in album['tracks']['items'] if t['id'] == 36924084)
        self.assertIsNone(movement_number(item['title']))
        result, _ = assess(self.rows['4429613'], album, review)
        self.assertEqual(result['completeness']['works'][2]['observed_movements'], [1,2,3,4])
        altered = copy.deepcopy(album)
        next(t for t in altered['tracks']['items'] if t['id'] == 36924084)['title'] += ' altered'
        amended = dict(review, album_sha256=fingerprint(altered))
        with self.assertRaises(ValueError): assess(self.rows['4429613'], altered, amended)

    def test_tenth_is_only_target_adagio_and_spotify_fields_are_independent(self):
        review = self.reviews['12130939']; row = copy.deepcopy(self.rows['12130939'])
        result, _ = assess(row, self.albums[review['album_id']], review)
        work = result['completeness']['works'][1]
        self.assertEqual(work['scope'], 'listed-target-excerpt')
        self.assertEqual(work['expected_movements'], [1])
        row['spotify'] = {'status': 'unchecked'}
        self.assertEqual(target_fingerprint(row), review['target_sha256'])
