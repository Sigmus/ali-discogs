import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT, fingerprint, reviewed_candidate
from qobuz_pair_review import assess_pairs
from qobuz_snapshot import load_snapshot


class PreludeFugueReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='2175684')
        cls.album = load_snapshot()['albums']['0886443628625']
        cls.review = json.loads((ROOT/'data/qobuz_prelude_fugue_reviews.json').read_text())['releases'][0]

    def test_both_books_require_every_prelude_and_fugue(self):
        candidate = reviewed_candidate(self.row, self.album, self.review)
        self.assertEqual((candidate['status'], candidate['confidence']), ('probable', .85))
        self.assertEqual(len(candidate['programme']), 48)
        ids = [i for item in candidate['programme'] for i in item['track_ids']]
        self.assertEqual(len(ids), 96)
        self.assertEqual(len(set(ids)), 96)
        self.assertIn('glenn-gould-plays-bach-the-well-tempered-clavier', candidate['url'])
        self.assertIn('Volume headings are containers', ' '.join(candidate['reasons']))
        shortened = copy.deepcopy(self.album)
        shortened['tracks']['items'].pop()
        self.assertIsNone(reviewed_candidate(self.row, shortened, dict(self.review, album_sha256=fingerprint(shortened))))

    def test_container_headings_and_bare_preludes_cannot_be_reassigned(self):
        review = copy.deepcopy(self.review)
        review['container_titles'] = review['container_titles'][1:]
        with self.assertRaises(ValueError):
            assess_pairs(self.row, self.album, review)
        review = copy.deepcopy(self.review)
        review['bare_preludes'][0]['bwv'] = 846
        result, _ = assess_pairs(self.row, self.album, review)
        self.assertFalse(result['eligible'])
        self.assertTrue(any(item.startswith('bare-prelude') for item in result['blockers']))

    def test_missing_pianist_withholds_the_pair(self):
        album = copy.deepcopy(self.album)
        album['tracks']['items'][0]['performers'] = 'Another Pianist, Piano'
        review = dict(self.review, album_sha256=fingerprint(album))
        result, _ = assess_pairs(self.row, album, review)
        self.assertFalse(result['eligible'])
        self.assertIn('pair-846', result['blockers'])
