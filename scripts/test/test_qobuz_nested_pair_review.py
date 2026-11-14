import copy
import gzip
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint


class NestedPairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='1458083')
        cls.album=next(x['album'] for x in json.loads(gzip.decompress((ROOT/'data/qobuz_remaining_followup_metadata.json.gz').read_bytes()))['metadata'] if str(x['album']['id'])=='0886444299039')
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='1458083')

    def test_all_fifteen_source_pairs_cover_thirty_distinct_tracks(self):
        result,evidence=assess(self.row,self.album,self.review)
        self.assertTrue(result['eligible']);self.assertEqual(evidence['covered'],15)
        self.assertEqual([i for p in evidence['programme'] for i in p['track_ids']],[t['id'] for t in self.album['tracks']['items']])

    def test_wrong_bwv_pianist_missing_and_swapped_pair_rejected_even_with_fresh_hashes(self):
        variants=[]
        a=copy.deepcopy(self.album);a['tracks']['items'][0]['title']=a['tracks']['items'][0]['title'].replace('772','773');variants.append(a)
        a=copy.deepcopy(self.album);a['tracks']['items'][0]['performers']='Another Pianist';variants.append(a)
        a=copy.deepcopy(self.album);a['tracks']['items'].pop();variants.append(a)
        a=copy.deepcopy(self.album);a['tracks']['items'][:2]=a['tracks']['items'][1::-1];variants.append(a)
        for a in variants:
            review={**self.review,'album_sha256':fingerprint(a),'track_sha256':[fingerprint(t) for t in a['tracks']['items']]}
            with self.assertRaises(ValueError):assess(self.row,a,review)

    def test_changed_source_binding_rejected(self):
        review={**self.review,'source_sha256':'0'*64}
        with self.assertRaises(ValueError):assess(self.row,self.album,review)
