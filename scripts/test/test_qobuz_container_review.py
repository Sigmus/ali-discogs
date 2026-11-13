import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_container_review import assess_containers
from qobuz_lead_review import ROOT, fingerprint, reviewed_candidate
from qobuz_snapshot import load_snapshot


class ContainerHeadingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='6678433')
        cls.album = load_snapshot()['albums']['uoihym7lfe48a']
        cls.review = json.loads((ROOT/'data/qobuz_container_reviews.json').read_text())['releases'][0]

    def test_heading_is_not_a_piece_and_every_track_is_required(self):
        candidate = reviewed_candidate(self.row, self.album, self.review)
        self.assertEqual((candidate['status'], candidate['confidence']), ('probable', .85))
        self.assertEqual(len(candidate['programme']), 13)
        self.assertEqual([len(p['track_ids']) for p in candidate['programme']], [1]*13)
        self.assertIn('chopin-10-mazurkas-arturo-benedetti-michelangeli', candidate['url'])
        self.assertNotIn('Mazurkas', [p['target'] for p in candidate['programme']])
        review = copy.deepcopy(self.review)
        review['container_titles'] = []
        with self.assertRaises(ValueError):
            assess_containers(self.row, self.album, review)
        review = copy.deepcopy(self.review)
        review['container_titles'] = ['Mazurkas', 'Op. 67 No. 2: Cantabile']
        with self.assertRaises(ValueError):
            assess_containers(self.row, self.album, review)

    def test_removing_a_piece_or_the_pianist_does_not_pass(self):
        album = copy.deepcopy(self.album)
        album['tracks']['items'].pop()
        with self.assertRaises(ValueError):
            assess_containers(self.row, album, dict(self.review, album_sha256=fingerprint(album)))
        album = copy.deepcopy(self.album)
        album['tracks']['items'][0]['performers'] = 'Another Pianist, Piano'
        with self.assertRaises(ValueError):
            assess_containers(self.row, album, dict(self.review, album_sha256=fingerprint(album)))
