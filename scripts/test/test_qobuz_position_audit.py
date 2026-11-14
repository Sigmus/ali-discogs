import copy
import gzip
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_position_audit import ROOT, audit


class PositionAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id']) == '11412875')
        cls.album = next(x['album'] for x in json.loads(gzip.decompress((ROOT/'data/qobuz_remaining_followup_metadata.json.gz').read_bytes()))['metadata'] if str(x['album']['id']) == 'v96ulyegxutlc')

    def test_repeated_allegros_remain_distinct(self):
        result = audit(self.row, self.album)
        mapping = result['positional_mapping']
        self.assertEqual([x['source_position'] for x in mapping], ['Aa','Ab','Ba','Bb'])
        self.assertNotEqual(mapping[0]['track_id'], mapping[3]['track_id'])
        self.assertFalse(result['publication_changed'])

    def test_reordered_missing_duplicate_wrong_work_and_wrong_artist_rejected(self):
        mutations = []
        a = copy.deepcopy(self.album); a['tracks']['items'].reverse(); mutations.append(a)
        a = copy.deepcopy(self.album); a['tracks']['items'].pop(); mutations.append(a)
        a = copy.deepcopy(self.album); a['tracks']['items'][3] = copy.deepcopy(a['tracks']['items'][0]); mutations.append(a)
        a = copy.deepcopy(self.album); a['tracks']['items'][0]['title'] = a['tracks']['items'][0]['title'].replace('Op. 29','Op. 27'); mutations.append(a)
        a = copy.deepcopy(self.album); a['tracks']['items'][0]['performers'] = 'Another Orchestra'; mutations.append(a)
        for album in mutations:
            with self.subTest(album=album['tracks']['items'][0]['id']):
                with self.assertRaises(ValueError): audit(self.row, album)

    def test_source_side_order_is_required(self):
        row = copy.deepcopy(self.row)
        row['tracklist'][0]['position'], row['tracklist'][3]['position'] = 'Bb', 'Aa'
        with self.assertRaises(ValueError): audit(row, self.album)

    def test_publication_review_is_hash_bound_and_keeps_both_allegros(self):
        from qobuz_lead_review import assess, fingerprint
        review = next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id'] == '11412875')
        result, evidence = assess(self.row, self.album, review)
        self.assertTrue(result['eligible'])
        self.assertEqual(evidence['covered'], 4)
        self.assertEqual(len({p['target'] for p in evidence['programme']}), 4)
        bad = copy.deepcopy(review); bad['mapping'][3]['track_id'] = bad['mapping'][0]['track_id']
        with self.assertRaises(ValueError): assess(self.row, self.album, bad)
        bad = copy.deepcopy(review); bad['source_sha256'] = '0'*64
        with self.assertRaises(ValueError): assess(self.row, self.album, bad)
        album = copy.deepcopy(self.album); album['tracks']['items'].reverse()
        with self.assertRaises(ValueError): assess(self.row, album, {**review,'album_sha256':fingerprint(album)})
