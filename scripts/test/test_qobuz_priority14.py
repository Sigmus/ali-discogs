import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_credit_role_audit import load_albums
from qobuz_lead_review import ROOT, assess, fingerprint, apply_recording_review
from qobuz_priority14_audit import validate
from qobuz_cached_review_queue import build


class PriorityBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.albums = load_albums()
        cls.report = json.loads((ROOT/'data/qobuz_priority14_batch_audit.json').read_text())

    def test_every_frozen_case_and_alternative_remains_bound(self):
        self.assertEqual(validate(self.report, self.rows, self.albums, self.reviews), {'reviewed': 14, 'probable': 2, 'withheld': 12})
        incomplete = copy.deepcopy(self.report)
        incomplete['entries'].pop()
        with self.assertRaises(ValueError):
            validate(incomplete, self.rows, self.albums, self.reviews)

    def test_stern_requires_both_composers_and_correct_soloist(self):
        review = self.reviews['6686688']
        original = self.albums[review['album_id']]
        for old, new in [('Isaac Stern', 'Albert Spalding'), ('Pyotr Ilyich Tchaikovsky', 'Nikolai Rimsky-Korsakov')]:
            album = copy.deepcopy(original)
            for track in album['tracks']['items']:
                track['performers'] = track.get('performers', '').replace(old, new)
            self.assertFalse(assess(self.rows['6686688'], album, {**review, 'album_sha256': fingerprint(album)})[0]['eligible'])

    def test_stern_bare_tempo_cannot_change_work_or_omit_finale(self):
        review = self.reviews['6686688']
        for remove in [False, True]:
            album = copy.deepcopy(self.albums[review['album_id']])
            if remove:
                album['tracks']['items'] = [t for t in album['tracks']['items'] if t['id'] != 67018862]
            else:
                next(t for t in album['tracks']['items'] if t['id'] == 67018860)['work'] = 'Scheherazade, Op. 35'
            with self.assertRaises(ValueError):
                assess(self.rows['6686688'], album, {**review, 'album_sha256': fingerprint(album)})

    def test_fidelio_is_not_leonore_three_despite_source_opus(self):
        review = self.reviews['7002243']
        result, _ = assess(self.rows['7002243'], self.albums[review['album_id']], review)
        self.assertEqual(result['completeness']['works'][1]['track_ids'], [353969812])
        uncorrected = copy.deepcopy(review)
        uncorrected.pop('target_title_corrections')
        self.assertFalse(assess(self.rows['7002243'], self.albums[review['album_id']], uncorrected)[0]['eligible'])

    def test_holds_survive_an_improved_future_score(self):
        for entry in self.report['entries']:
            if entry['outcome'] != 'withhold':
                continue
            review = self.reviews[entry['discogs_id']]
            candidate = {'id': review['album_id'], 'status': 'found', 'confidence': .99}
            held = apply_recording_review(self.rows[entry['discogs_id']], self.albums[review['album_id']], review, [candidate])[0]
            self.assertEqual(held['status'], 'unchecked')

    def test_reviewed_blocker_is_not_requeued_by_an_alternative(self):
        entry = {'discogs_id': '1656511', 'title': 'du Pre', 'category': 'work_or_credit_unresolved', 'uncached_hits': 0,
                 'cached_candidates': [{'album_id': 'other', 'coverage': 1, 'reviewed_withheld': False, 'reviewed_rejected': False}]}
        reviewed = {e['discogs_id']: e for e in self.report['entries']}
        self.assertEqual(build({'entries': [entry]}, reviewed)['entries'][0]['queue'], 'reviewed_blocker')
