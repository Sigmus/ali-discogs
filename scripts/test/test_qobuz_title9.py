import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT, assess, fingerprint
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate


class TitleNineReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.albums = load_albums()
        cls.report = json.loads((ROOT/'data/qobuz_title9_recording_audit.json').read_text())

    def test_entire_scope_and_future_hold_precedence(self):
        self.assertEqual(validate(self.report, self.rows, self.albums, self.reviews, expected_count=9),
                         {'reviewed': 9, 'withhold': 3, 'probable': 6})

    def test_lp_excerpts_do_not_become_complete_ninths(self):
        tail, first = self.reviews['11883662'], self.reviews['11885637']
        self.assertEqual([b['track_ids'] for b in tail['bindings']], [[196450], [196451], [196452]])
        self.assertIn(196449, tail['extra_track_ids'])
        self.assertEqual(first['bindings'][-1]['track_ids'], [196449])
        self.assertTrue({196450, 196451, 196452}.issubset(first['extra_track_ids']))
        for review in [tail, first]:
            result, _ = assess(self.rows[review['discogs_id']], self.albums[review['album_id']], review)
            self.assertTrue(all(w['scope'] == 'reviewed-complete-source-band' for w in result['completeness']['works']))

    def test_diagnostic_best_does_not_override_recording_or_positive_credit_evidence(self):
        self.assertEqual(self.reviews['11887204']['album_id'], '0828765570220')
        self.assertEqual(self.reviews['8567942']['bindings'][2]['track_ids'], [196434, 196435])
        self.assertEqual(self.reviews['2845131']['decision'], 'withhold')
        # Busoni occurs on Op.15, not the accepted Op.73 tracks of the same album.
        review = self.reviews['16996626']
        self.assertEqual([b['track_ids'] for b in review['bindings']], [[191161], [191162], [191163]])

    def test_extra_composer_still_blocks_even_after_refreshing_hashes(self):
        review = copy.deepcopy(self.reviews['16996626'])
        album = copy.deepcopy(self.albums[review['album_id']])
        selected = {i for b in review['bindings'] for i in b['track_ids']}
        for t in album['tracks']['items']:
            if t['id'] in selected:
                t['performers'] += ' - Busoni, Composer'
        by_id = {t['id']: t for t in album['tracks']['items']}
        review['album_sha256'] = fingerprint(album)
        for b in review['bindings']:
            b['track_sha256'] = [fingerprint(by_id[i]) for i in b['track_ids']]
        review['selected_track_fingerprints'] = {str(i): fingerprint(by_id[i]) for i in selected}
        result, _ = assess(self.rows['16996626'], album, review)
        self.assertFalse(result['eligible'])
        self.assertIn('composer', result['blockers'])
