import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT, assess, fingerprint
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate


class EnsembleNameReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.albums = load_albums()
        cls.report = json.loads((ROOT/'data/qobuz_name2_recording_audit.json').read_text())

    def test_both_decisions_and_raw_movement_order(self):
        self.assertEqual(validate(self.report, self.rows, self.albums, self.reviews, 2), {'reviewed':2, 'probable':2})
        for rid in self.report['frozen_release_ids']:
            r = self.reviews[rid]
            raw = json.loads((ROOT/f'raw/discogs/releases/{rid}.json').read_text())
            self.assertEqual([b['position'] for b in r['source_band_bindings']], [s['position'] for s in raw['tracklist'][0]['sub_tracks']])
            self.assertEqual([b['title'] for b in r['source_band_bindings']], [s['title'] for s in raw['tracklist'][0]['sub_tracks']])
            self.assertEqual([b['track_ids'][0] for b in r['source_band_bindings']], list(r['expected'].values())[0])

    def test_without_scoped_alias_neither_recording_passes(self):
        for rid in self.report['frozen_release_ids']:
            r = copy.deepcopy(self.reviews[rid]);r.pop('performer_aliases')
            result,_ = assess(self.rows[rid], self.albums[r['album_id']], r)
            self.assertFalse(result['eligible']);self.assertIn('performer',result['blockers'])

    def test_names_do_not_waive_soloist_conductor_or_orchestra_roles(self):
        for rid in self.report['frozen_release_ids']:
            for omitted in ['Conductor', 'Orchestra', 'Violin' if rid=='11876845' else 'Piano']:
                r = copy.deepcopy(self.reviews[rid]);a = copy.deepcopy(self.albums[r['album_id']])
                track = a['tracks']['items'][0]
                track['performers'] = ' - '.join(p for p in track['performers'].split(' - ') if omitted not in p)
                r['album_sha256'] = fingerprint(a)
                result,_ = assess(self.rows[rid], a, r)
                self.assertFalse(result['eligible'],(rid,omitted));self.assertIn('performer',result['blockers'])

    def test_publisher_timing_change_requires_review(self):
        r = copy.deepcopy(self.reviews['21490438']);a = copy.deepcopy(self.albums[r['album_id']])
        a['tracks']['items'][0]['duration'] += 120
        r['album_sha256'] = fingerprint(a)
        # Even deliberately rebinding an add cannot waive the independent publisher mark.
        r['adds'][0]['duration_seconds'] += 120
        result,_ = assess(self.rows['21490438'],a,r)
        self.assertFalse(result['eligible']);self.assertIn('reference-duration',result['blockers'])
