import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT, assess, fingerprint
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate


class TitleThreeReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.albums = load_albums()
        cls.report = json.loads((ROOT/'data/qobuz_title3_recording_audit.json').read_text())

    def test_all_three_decisions_and_future_hold_precedence(self):
        self.assertEqual(validate(self.report, self.rows, self.albums, self.reviews, expected_count=3),
                         {'reviewed': 3, 'withhold': 2, 'probable': 1})

    def test_full_haydn_titles_do_not_waive_source_timings(self):
        review = self.reviews['2548602']
        result, _ = assess(self.rows['2548602'], self.albums[review['album_id']], review)
        self.assertFalse(result['eligible'])
        self.assertIn('source-band-duration', result['blockers'])
        work = next(w for w in result['completeness']['works'] if w['source_path'] == [4, 1])
        self.assertEqual((work['source_duration_seconds'], work['digital_duration_seconds']), (207, 142))
        self.assertEqual(len(review['bindings']), 15)
        self.assertFalse(review.get('source_duration_notes'))

    def test_heifetz_complete_movements_cannot_omit_source_pianist(self):
        review = copy.deepcopy(self.reviews['7065721'])
        album = copy.deepcopy(self.albums[review['album_id']])
        self.assertEqual([b['track_ids'] for b in review['bindings']], [[i] for i in range(7847932, 7847938)])
        selected = {i for b in review['bindings'] for i in b['track_ids']}
        for track in album['tracks']['items']:
            if track['id'] in selected:
                track['performers'] = ' - '.join(p for p in track['performers'].split(' - ') if not p.startswith('Brooks Smith,'))
        byid = {t['id']: t for t in album['tracks']['items']}
        review['album_sha256'] = fingerprint(album)
        for binding in review['bindings']:
            binding['track_sha256'] = [fingerprint(byid[i]) for i in binding['track_ids']]
        review['selected_track_fingerprints'] = {str(i): fingerprint(byid[i]) for i in selected}
        result, _ = assess(self.rows['7065721'], album, review)
        self.assertFalse(result['eligible'])
        self.assertIn('performer', result['blockers'])

    def test_dido_hold_keeps_all_source_sides_and_all_alternatives(self):
        entry = next(e for e in self.report['entries'] if e['discogs_id'] == '24278222')
        self.assertEqual([t['position'] for t in entry['source_programme']], ['A1', 'A2', 'B1', 'B2'])
        self.assertEqual(len(entry['cached_alternative_checks']), 5)
        self.assertEqual(self.reviews['24278222']['decision'], 'withhold')
        self.assertNotIn('review_kind', self.reviews['24278222'])
