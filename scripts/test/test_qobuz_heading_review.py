import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_heading_review import assess_headings
from qobuz_lead_review import ROOT, reviewed_candidate
from qobuz_snapshot import load_snapshot


class HeadingGroupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='2527568')
        cls.review = json.loads((ROOT/'data/qobuz_heading_reviews.json').read_text())['releases'][0]
        cls.album = load_snapshot()['albums'][cls.review['album_id']]

    def test_the_heading_is_not_a_third_concerto(self):
        candidate = reviewed_candidate(self.row, self.album, self.review)
        self.assertEqual((candidate['status'], candidate['confidence'], candidate['covered']), ('probable', .85, 2))
        self.assertEqual(sorted(len(item['track_ids']) for item in candidate['programme']), [3, 3])
        self.assertNotIn('Les Deux Concertos', ' '.join(item['target'] for item in candidate['programme']))

    def test_a_numbered_concerto_cannot_become_the_heading(self):
        review = copy.deepcopy(self.review)
        review['container_titles'] = ['Concerto N°1 En Ré Majeur, Op.6']
        with self.assertRaises(ValueError):
            assess_headings(self.row, self.album, review)
        album = copy.deepcopy(self.album)
        album['tracks']['items'].pop()
        with self.assertRaises(ValueError):
            assess_headings(self.row, album, self.review)
