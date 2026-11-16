import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT, assess, fingerprint
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate


class FullSupportBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.albums = load_albums()
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.report = json.loads((ROOT/'data/qobuz_fullsupport16_recording_audit.json').read_text())

    def accepted(self, rid, mutate):
        review = copy.deepcopy(self.reviews[rid])
        album = copy.deepcopy(self.albums[review['album_id']])
        mutate(album)
        review['album_sha256'] = fingerprint(album)
        try:
            return assess(self.rows[rid], album, review)[0]['eligible']
        except ValueError:
            return False

    def test_all16_frozen_decisions_and_hold_precedence(self):
        self.assertEqual(validate(self.report, self.rows, self.albums, self.reviews),
                         {'reviewed': 16, 'probable': 9, 'withhold': 7})
        missing = copy.deepcopy(self.report)
        missing['entries'].pop()
        with self.assertRaises(ValueError):
            validate(missing, self.rows, self.albums, self.reviews)

    def test_every_accepted_programme_needs_all_selected_tracks(self):
        for rid in self.report['accepted_release_ids']:
            review = self.reviews[rid]
            self.assertTrue(assess(self.rows[rid], self.albums[review['album_id']], review)[0]['eligible'])
            def remove_selected(a):
                result, evidence = assess(self.rows[rid], self.albums[review['album_id']], review)
                selected = evidence['programme'][0]['track_ids'][0]
                a['tracks']['items'] = [t for t in a['tracks']['items'] if t['id'] != selected]
            self.assertFalse(self.accepted(rid, remove_selected), rid)

    def test_kempff_cannot_borrow_soloist_from_another_recording(self):
        review = self.reviews['10583401']
        ids = set(next(iter(review['expected_recording_groups'].values()))['track_ids'])
        def remove_group_soloist(a):
            for t in a['tracks']['items']:
                if t['id'] in ids:
                    t['performers'] = ' - '.join(p for p in t['performers'].split(' - ') if not p.startswith('Wilhelm Kempff,'))
        self.assertFalse(self.accepted('10583401', remove_group_soloist))
        changed = copy.deepcopy(review)
        next(iter(changed['expected_recording_groups'].values()))['track_ids'][0] = -1
        with self.assertRaises(ValueError):
            assess(self.rows['10583401'], self.albums[review['album_id']], changed)

    def test_battle_is_required_on_her_source_piece(self):
        def remove_battle(a):
            for t in a['tracks']['items']:
                t['performers'] = ' - '.join(p for p in t['performers'].split(' - ') if not p.startswith('Kathleen Battle,'))
        self.assertFalse(self.accepted('3675625', remove_battle))

    def test_leonhardt_discrepancies_and_krips_join_are_preserved(self):
        entries = {e['discogs_id']: e for e in self.report['entries']}
        for rid in ['7077802', '7467218']:
            self.assertEqual(entries[rid]['outcome'], 'withhold')
            self.assertIn('BWV828', entries[rid]['finding'])
        self.assertIn('do not claim the finale is missing', entries['10552903']['finding'])
        self.assertIn('RudolfScholz', entries['2831179']['finding'])
