import copy
import gzip
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT, reviewed_candidate
from qobuz_side_range_review import assess_ranges


class SideRangeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='8176289')
        cls.review = json.loads((ROOT/'data/qobuz_side_range_reviews.json').read_text())['releases'][0]
        albums = json.loads(gzip.decompress((ROOT/'data/qobuz_empty_search_metadata.json.gz').read_bytes()))
        cls.album = next(record['album'] for record in albums['metadata'] if record['album']['id']==cls.review['album_id'])

    def test_two_sides_cover_fifteen_numbers_without_dropping_a_singer(self):
        candidate = reviewed_candidate(self.row, self.album, self.review)
        self.assertEqual((candidate['status'], candidate['confidence'], candidate['covered']), ('probable', .85, 2))
        self.assertEqual([len(item['track_ids']) for item in candidate['programme']], [7, 8])
        self.assertNotIn('Dramma', ' '.join(item['target'] for item in candidate['programme']))
        self.assertIn('Theo Adam', self.review['somewhere'])
        self.assertIn('Eva Fleischer', self.review['somewhere'])

    def test_a_missing_singer_or_a_miscounted_side_cannot_be_forced(self):
        dropped = copy.deepcopy(self.review)
        dropped['somewhere'] = [name for name in dropped['somewhere'] if name != 'Theo Adam']
        with self.assertRaises(ValueError):
            assess_ranges(self.row, self.album, dropped)
        swapped = copy.deepcopy(self.review)
        moved = swapped['ranges'][0]['tracks'].pop()
        swapped['ranges'][1]['tracks'].insert(0, moved)
        with self.assertRaises(ValueError):
            assess_ranges(self.row, self.album, swapped)
        quiet = copy.deepcopy(self.album)
        last = quiet['tracks']['items'][-1]
        last['performers'] = last['performers'].replace('Thomanerchor', 'Choir')
        result, _ = assess_ranges(self.row, quiet, self.review)
        self.assertFalse(result['eligible'])
        self.assertIn('performer', result['blockers'])
