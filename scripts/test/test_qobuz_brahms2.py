import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT, assess, fingerprint
from qobuz_credit_role_audit import load_albums


class BrahmsRecordingReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.albums = load_albums()
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}

    def test_complete_recording_families_and_missing_finales(self):
        for rid in ['6798013', '12803844']:
            review = self.reviews[rid]
            album = self.albums[review['album_id']]
            self.assertTrue(assess(self.rows[rid], album, review)[0]['eligible'])
            changed = copy.deepcopy(album)
            changed['tracks']['items'].pop()
            rebound = {**review, 'album_sha256': fingerprint(changed)}
            self.assertFalse(assess(self.rows[rid], changed, rebound)[0]['eligible'])

    def test_wrong_conductor_cannot_inherit_same_work_recording_acceptance(self):
        for rid in ['6798013', '12803844']:
            review = self.reviews[rid]
            album = copy.deepcopy(self.albums[review['album_id']])
            for track in album['tracks']['items']:
                track['performers'] = ' - '.join(p for p in track['performers'].split(' - ') if 'Conductor' not in p)
            rebound = {**review, 'album_sha256': fingerprint(album)}
            self.assertFalse(assess(self.rows[rid], album, rebound)[0]['eligible'])
