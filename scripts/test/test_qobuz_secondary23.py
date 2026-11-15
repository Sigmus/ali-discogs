import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_credit_role_audit import load_albums
from qobuz_lead_review import ROOT, assess, fingerprint, apply_recording_review
from qobuz_secondary23_audit import validate
from qobuz_vocal_programme_review import source_groups


class FinishSecondaryReviewsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.albums = load_albums()
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.report = json.loads((ROOT/'data/qobuz_secondary23_recording_audit.json').read_text())

    def altered(self, rid, change, rebind_tracks=False):
        review = self.reviews[rid]
        album = copy.deepcopy(self.albums[review['album_id']])
        change(album)
        review = {**review, 'album_sha256': fingerprint(album)}
        if rebind_tracks:
            review['track_fingerprints'] = {str(t['id']): fingerprint(t) for t in album['tracks']['items']}
        try:
            return assess(self.rows[rid], album, review)[0]['eligible']
        except ValueError:
            return False

    def test_all23_have_complete_frozen_decisions(self):
        self.assertEqual(validate(self.report, self.rows, self.albums, self.reviews),
                         {'reviewed': 23, 'probable': 4, 'withheld': 18, 'rejected_recording': 1})
        incomplete = copy.deepcopy(self.report)
        incomplete['entries'].pop()
        with self.assertRaises(ValueError):
            validate(incomplete, self.rows, self.albums, self.reviews)

    def test_janis_keeps_all12pieces_and_three_pinto_movements(self):
        r = self.reviews['34776194']
        result, evidence = assess(self.rows['34776194'], self.albums[r['album_id']], r)
        self.assertTrue(result['eligible'])
        self.assertEqual(len(result['completeness']['works']), 12)
        self.assertEqual(len({i for w in result['completeness']['works'] for i in w['track_ids']}), 14)
        self.assertEqual([len(w['track_ids']) for w in result['completeness']['works']][-1], 3)
        self.assertNotIn('Franz Liszt', [p['target'] for p in evidence['programme']])
        self.assertFalse(self.altered('34776194', lambda a: a['tracks']['items'].pop()))

    def test_group_display_cannot_introduce_an_unlisted_piece(self):
        review = copy.deepcopy(self.reviews['34776194'])
        review['target_unit_groups'][0]['display_source_title'] = 'A piece absent from this source'
        with self.assertRaises(ValueError):
            assess(self.rows['34776194'], self.albums[review['album_id']], review)

    def test_klemperer_needs_every_named_selection(self):
        r = self.reviews['2808874']
        self.assertTrue(assess(self.rows['2808874'], self.albums[r['album_id']], r)[0]['eligible'])
        def remove_tristan(album):
            album['tracks']['items'] = [t for t in album['tracks']['items'] if t['id'] != 2319848]
        self.assertFalse(self.altered('2808874', remove_tristan))

    def test_passion_keeps_raw_source_soloists_missing_from_normalized_principals(self):
        review = self.reviews['25537708']
        self.assertIn('Christa Ludwig', review['required_performers'])
        self.assertIn('Walter Berry', review['required_performers'])
        for name in ['Christa Ludwig', 'Walter Berry']:
            def remove_credit(album):
                for t in album['tracks']['items']:
                    t['performers'] = ' - '.join(p for p in t.get('performers', '').split(' - ') if not p.startswith(name+','))
            self.assertFalse(self.altered('25537708', remove_credit, rebind_tracks=True))

    def test_passion_source_ranges_are_not_modern_number_labels_or_optional_sides(self):
        r = self.reviews['25537708']
        row = copy.deepcopy(self.rows['25537708'])
        raw = json.loads((ROOT/'raw/discogs/releases/25537708.json').read_text())
        album = self.albums[r['album_id']]
        groups = source_groups(row, raw, album['tracks']['items'], r)
        self.assertEqual([len(g['track_ids']) for g in groups], [10,11,8,6,11,9,9,8,6])
        # Tenth old section is modern No.6; literal number equality would be false.
        self.assertIn('No. 6,', album['tracks']['items'][9]['title'])
        raw['tracklist'][1]['title'] = 'Part 1 Nos. 2 To 10 Inclusive'
        row['tracklist'][1]['title'] = raw['tracklist'][1]['title']
        changed = {**r, 'source_projection': row['tracklist']}
        with self.assertRaises(ValueError):
            source_groups(row, raw, album['tracks']['items'], changed)

    def test_otello_has_four_acts_without_invented_part_boundaries(self):
        r = self.reviews['7095769']
        result, _ = assess(self.rows['7095769'], self.albums[r['album_id']], r)
        self.assertTrue(result['eligible'])
        work = result['completeness']['works'][0]
        self.assertEqual(len(work['track_ids']), 45)
        self.assertFalse(work['source_side_boundaries_verified'])
        self.assertEqual([g['source_act'] for g in work['source_groups']], [1,2,3,4])
        self.assertFalse(self.altered('7095769', lambda a: a['tracks']['items'].pop()))

    def test_otello_wrong_edition_cannot_pass_on_three_shared_principal_singers(self):
        def wrong_conductor(album):
            for t in album['tracks']['items']:
                t['performers'] = t['performers'].replace('Herbert Von Karajan', 'Alberto Erede')
        self.assertFalse(self.altered('7095769', wrong_conductor, rebind_tracks=True))
        def wrong_composer(album):
            for t in album['tracks']['items']:
                t['performers'] = t['performers'].replace('Giuseppe Verdi, Composer', 'Richard Wagner, Composer')
        self.assertFalse(self.altered('7095769', wrong_composer, rebind_tracks=True))

    def test_wrong_vivaldi_file_stays_rejected_even_after_a_future_high_score(self):
        r = self.reviews['17623039']
        self.assertEqual(r['decision'], 'reject-recording')
        held = apply_recording_review(self.rows['17623039'], self.albums[r['album_id']], r,
                                     [{'id': r['album_id'], 'status': 'found', 'confidence': .99}])
        self.assertEqual(held[0]['status'], 'unchecked')

    def test_source_proof_and_full_vocal_manifest_are_mandatory(self):
        for rid in ['25537708', '7095769']:
            review = copy.deepcopy(self.reviews[rid])
            review['external_source_files'][0]['sha256'] = '0'*64
            with self.assertRaises(ValueError):
                assess(self.rows[rid], self.albums[review['album_id']], review)
