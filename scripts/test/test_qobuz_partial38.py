import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT, assess, fingerprint
from qobuz_credit_role_audit import load_albums
from qobuz_partial38_audit import validate


class PartialSupportBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.albums = load_albums()
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.report = json.loads((ROOT/'data/qobuz_partial38_recording_audit.json').read_text())

    def test_all38_decisions_and_high_score_holds(self):
        self.assertEqual(validate(self.report, self.rows, self.albums, self.reviews),
                         {'reviewed': 38, 'probable': 6, 'withhold': 32})
        changed = copy.deepcopy(self.report)
        changed['entries'].pop()
        with self.assertRaises(ValueError):
            validate(changed, self.rows, self.albums, self.reviews)

    def test_no_source_leaf_can_be_dropped_or_reused(self):
        for rid in self.report['accepted_release_ids']:
            review = copy.deepcopy(self.reviews[rid])
            album = self.albums[review['album_id']]
            self.assertTrue(assess(self.rows[rid], album, review)[0]['eligible'])
            review['bindings'].pop()
            with self.assertRaises(ValueError):
                assess(self.rows[rid], album, review)
            review = copy.deepcopy(self.reviews[rid])
            review['bindings'][1]['track_ids'] = review['bindings'][0]['track_ids']
            with self.assertRaises(ValueError):
                assess(self.rows[rid], album, review)

    def test_pires_all31pieces_and_source_headings_retained(self):
        r = self.reviews['5980586']
        result, evidence = assess(self.rows['5980586'], self.albums[r['album_id']], r)
        self.assertEqual(len(result['completeness']['works']), 31)
        self.assertEqual(len({i for p in evidence['programme'] for i in p['track_ids']}), 31)
        self.assertEqual(r['bindings'][-1]['track_ids'], [2679273])

    def test_baker_cannot_be_removed_from_source_songs(self):
        r = copy.deepcopy(self.reviews['6748142'])
        album = copy.deepcopy(self.albums[r['album_id']])
        for t in album['tracks']['items']:
            t['performers'] = ' - '.join(s for s in t['performers'].split(' - ') if not s.startswith('Janet Baker,'))
        r['album_sha256'] = fingerprint(album)
        for b in r['bindings']:
            t = next(t for t in album['tracks']['items'] if t['id'] == b['track_ids'][0])
            b['track_sha256'] = [fingerprint(t)]
            r['selected_track_fingerprints'][str(t['id'])] = fingerprint(t)
        self.assertFalse(assess(self.rows['6748142'], album, r)[0]['eligible'])
        self.assertNotIn('Janet Baker', r['bindings'][0]['required_performers'])
        self.assertIn('Janet Baker', r['bindings'][-1]['required_performers'])

    def test_wrong_source_composer_and_missing_gilels_finale_fail(self):
        r = copy.deepcopy(self.reviews['17748481'])
        r['bindings'][0]['composer'] = 'Nikolai Medtner'
        with self.assertRaises(ValueError):
            assess(self.rows['17748481'], self.albums[r['album_id']], r)
        album = copy.deepcopy(self.albums[r['album_id']])
        album['tracks']['items'] = [t for t in album['tracks']['items'] if t['id'] != 189468462]
        r = {**self.reviews['17748481'], 'album_sha256': fingerprint(album)}
        with self.assertRaises(ValueError):
            assess(self.rows['17748481'], album, r)

    def test_duration_discrepancy_is_explicit_and_frozen(self):
        r = copy.deepcopy(self.reviews['4031075'])
        self.assertEqual(r['source_duration_notes'][0]['digital_seconds']-r['source_duration_notes'][0]['source_seconds'], 6)
        r.pop('source_duration_notes')
        self.assertFalse(assess(self.rows['4031075'], self.albums[r['album_id']], r)[0]['eligible'])

    def test_wrong_moldau_and_raw_quartet_member_stay_held(self):
        entries = {e['discogs_id']: e for e in self.report['entries']}
        self.assertIn('ArthurFiedler/BostonPops', entries['6652276']['finding'])
        self.assertIn('PieroFarulli', entries['17256520']['finding'])
        self.assertEqual(entries['6652276']['outcome'], 'withhold')
        self.assertEqual(entries['17256520']['outcome'], 'withhold')

    def test_numbered_source_heading_cannot_disappear(self):
        r = copy.deepcopy(self.reviews['5980586'])
        self.assertIn('Op. 99', r['source_heading_groups'][0]['title'])
        r['source_heading_groups'] = []
        with self.assertRaises(ValueError):
            assess(self.rows['5980586'], self.albums[r['album_id']], r)
