import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_credit_role_audit import load_albums
from qobuz_lead_review import ROOT, assess, fingerprint, target_fingerprint


class SecondaryReviewsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.albums = load_albums()
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}

    def test_frozen_26_screen_is_not_26_recording_approvals(self):
        report = json.loads((ROOT/'data/qobuz_secondary26_audit.json').read_text())
        ids = [e['discogs_id'] for e in report['entries']]
        self.assertEqual(ids, [e['discogs_id'] for e in report['frozen_entries']])
        self.assertEqual(len(set(ids)), 26)
        self.assertEqual(sum(e['stage'] == 'recording_review_complete' for e in report['entries']), 3)
        for entry in report['entries']:
            rid = entry['discogs_id']
            self.assertEqual(entry['target_sha256'], target_fingerprint(self.rows[rid]))
            self.assertEqual(entry['source_sha256'], hashlib.sha256((ROOT/f'raw/discogs/releases/{rid}.json').read_bytes()).hexdigest())
            for candidate in entry['cached_candidates']:
                self.assertEqual(candidate['album_sha256'], fingerprint(self.albums[candidate['album_id']]))

    def test_two_waltz_programmes_are_complete_and_distinct(self):
        for rid in ['1704535', '4067901']:
            review = self.reviews[rid]
            result, _ = assess(self.rows[rid], self.albums[review['album_id']], review)
            self.assertTrue(result['eligible'])
            works = result['completeness']['works']
            self.assertEqual(len(works), 14)
            self.assertEqual(len({i for w in works for i in w['track_ids']}), 14)

    def test_wrong_waltz_member_or_composer_cannot_inherit_correction(self):
        for rid in ['1704535', '4067901']:
            review = self.reviews[rid]
            original = self.albums[review['album_id']]
            for field, text in [('title', 'Waltz in A-Flat Major, Op. 34 No. 2'), ('performers', 'Dinu Lipatti, MainArtist - Erik Satie, Composer')]:
                album = copy.deepcopy(original)
                album['tracks']['items'][0][field] = text
                changed = {**review, 'album_sha256': fingerprint(album)}
                try:
                    result, _ = assess(self.rows[rid], album, changed)
                except ValueError:
                    continue
                self.assertFalse(result['eligible'])

    def test_missing_waltz_is_not_replaced_by_a_bonus_track(self):
        review = self.reviews['1704535']
        album = copy.deepcopy(self.albums[review['album_id']])
        album['tracks']['items'].pop(5)
        result, _ = assess(self.rows['1704535'], album, {**review, 'album_sha256': fingerprint(album)})
        self.assertFalse(result['eligible'])

    def test_bruckner_cycle_requires_35_movements_and_berlin_orchestra(self):
        review = self.reviews['7860979']
        original = self.albums[review['album_id']]
        result, _ = assess(self.rows['7860979'], original, review)
        self.assertTrue(result['eligible'])
        self.assertEqual([len(w['track_ids']) for w in result['completeness']['works']], [4]*8+[3])
        album = copy.deepcopy(original)
        for track in album['tracks']['items']:
            track['performers'] = track['performers'].replace('Berliner Philharmoniker', 'Wiener Philharmoniker')
        self.assertFalse(assess(self.rows['7860979'], album, {**review, 'album_sha256': fingerprint(album)})[0]['eligible'])

    def test_bruckner_tempo_alone_does_not_identify_a_symphony(self):
        review = self.reviews['7860979']
        album = copy.deepcopy(self.albums[review['album_id']])
        album['tracks']['items'][0]['work'] = 'Symphony No. 2 in C minor'
        with self.assertRaises(ValueError):
            assess(self.rows['7860979'], album, {**review, 'album_sha256': fingerprint(album)})
