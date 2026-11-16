import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT, assess, fingerprint
from qobuz_credit_role_audit import load_albums
from qobuz_zero104_audit import validate


class ZeroSupportBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.albums = load_albums()
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.report = json.loads((ROOT/'data/qobuz_zero104_recording_audit.json').read_text())

    def test_complete_scope_and_high_score_holds(self):
        self.assertEqual(validate(self.report, self.rows, self.albums, self.reviews),
                         {'reviewed': 104, 'withhold': 101, 'probable': 3})
        changed = copy.deepcopy(self.report)
        changed['entries'].pop()
        with self.assertRaises(ValueError):
            validate(changed, self.rows, self.albums, self.reviews)
        changed = copy.deepcopy(self.report)
        changed['entries'][0]['cached_alternative_checks'].pop()
        with self.assertRaises(ValueError):
            validate(changed, self.rows, self.albums, self.reviews)

    def test_raw_credits_and_alternative_titles_cannot_disappear(self):
        changed = copy.deepcopy(self.report)
        changed['entries'][0]['source_credits'] = []
        with self.assertRaises(ValueError):
            validate(changed, self.rows, self.albums, self.reviews)
        changed = copy.deepcopy(self.report)
        changed['entries'][0]['cached_alternative_checks'][0]['track_titles'].pop()
        with self.assertRaises(ValueError):
            validate(changed, self.rows, self.albums, self.reviews)

    def test_heifetz_complete_split_variations_cannot_be_truncated(self):
        review = copy.deepcopy(self.reviews['8923384'])
        self.assertEqual(len(review['bindings'][-1]['track_ids']), 7)
        review['bindings'][-1]['track_ids'].pop()
        with self.assertRaises(ValueError):
            assess(self.rows['8923384'], self.albums[review['album_id']], review)

    def test_missing_bay_credit_still_blocks_rehashed_mapping(self):
        review = copy.deepcopy(self.reviews['8923384'])
        album = copy.deepcopy(self.albums[review['album_id']])
        track = album['tracks']['items'][0]
        track['performers'] = track['performers'].replace('Emanuel Bay, Piano', '')
        review['album_sha256'] = fingerprint(album)
        review['bindings'][0]['track_sha256'] = [fingerprint(track)]
        review['selected_track_fingerprints'][str(track['id'])] = fingerprint(track)
        self.assertFalse(assess(self.rows['8923384'], album, review)[0]['eligible'])

    def test_schuricht_uses_warner_boundaries_not_bad_bnf_split(self):
        review = self.reviews['36163426']
        self.assertEqual(review['album_id'], 'btegd89k63vxa')
        self.assertEqual([b['track_ids'] for b in review['bindings']],
                         [[277256531], [277256532], [277256533]])
        self.assertTrue(assess(self.rows['36163426'], self.albums[review['album_id']], review)[0]['eligible'])

    def test_prokofiev_spelling_is_local_and_every_excerpt_retained(self):
        review = copy.deepcopy(self.reviews['6544574'])
        self.assertEqual(len(review['bindings']), 9)
        self.assertTrue(assess(self.rows['6544574'], self.albums[review['album_id']], review)[0]['eligible'])
        review.pop('source_composer_spellings')
        with self.assertRaises(ValueError):
            assess(self.rows['6544574'], self.albums[review['album_id']], review)
