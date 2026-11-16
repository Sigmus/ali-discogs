import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT, assess, fingerprint
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate


class WorkContextBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.albums = load_albums()
        cls.report = json.loads((ROOT/'data/qobuz_work_context9_recording_audit.json').read_text())

    def test_all9_decisions_and_hold_precedence(self):
        self.assertEqual(validate(self.report, self.rows, self.albums, self.reviews, expected_count=9),
                         {'reviewed': 9, 'withhold': 7, 'probable': 2})
        for rid in ['2636984', '3000291', '6681884', '6820841', '9703869']:
            self.assertEqual(self.reviews[rid]['decision'], 'withhold')

    def test_heifetz_conductors_stay_scoped_to_their_own_work(self):
        review = self.reviews['4259729']
        self.assertEqual(len(review['bindings']), 6)
        first, last = review['bindings'][0], review['bindings'][-1]
        self.assertIn('Walter Hendl', first['required_performers'])
        self.assertNotIn('Charles Munch', first['required_performers'])
        self.assertIn('Charles Munch', last['required_performers'])
        self.assertNotIn('Walter Hendl', last['required_performers'])
        self.assertEqual(first['composer'], 'Jean Sibelius')
        self.assertEqual(last['composer'], 'Sergei Prokofiev')
        self.assertEqual(review['album_id'], '0090266177929')
        selected = {i for b in review['bindings'] for i in b['track_ids']}
        self.assertTrue(all('Associated' not in t['performers'] for t in self.albums[review['album_id']]['tracks']['items'] if t['id'] in selected))

    def test_source_orchestra_cannot_be_removed_even_with_refreshed_hashes(self):
        review = copy.deepcopy(self.reviews['10851475'])
        album = copy.deepcopy(self.albums[review['album_id']])
        for track in album['tracks']['items']:
            track['performers'] = ' - '.join(part for part in track['performers'].split(' - ')
                                           if not part.startswith('Chicago Symphony Orchestra,'))
        review['album_sha256'] = fingerprint(album)
        by_id = {t['id']: t for t in album['tracks']['items']}
        for binding in review['bindings']:
            binding['track_sha256'] = [fingerprint(by_id[i]) for i in binding['track_ids']]
        review['selected_track_fingerprints'] = {str(i): fingerprint(by_id[i]) for b in review['bindings'] for i in b['track_ids']}
        self.assertFalse(assess(self.rows['10851475'], album, review)[0]['eligible'])
