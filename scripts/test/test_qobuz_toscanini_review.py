import copy
import gzip
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint


class ToscaniniReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='10757120')
        cls.album=json.loads(gzip.decompress((ROOT/'data/qobuz_evidence.json.gz').read_bytes()))['albums']['lbd4bwo8ommnb']
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='10757120')

    def test_all_five_movements_and_source_photo(self):
        result,evidence=assess(self.row,self.album,self.review)
        self.assertTrue(result['eligible']);self.assertEqual(len(result['completeness']['works'][0]['track_ids']),5)
        bad=copy.deepcopy(self.review);bad['external_source_files'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):assess(self.row,self.album,bad)

    def test_changed_year_timing_or_orchestra_is_not_accepted_after_rehash(self):
        a=copy.deepcopy(self.album);a['version']='Album of1951'
        with self.assertRaises(ValueError):assess(self.row,a,{**self.review,'album_sha256':fingerprint(a)})
        a=copy.deepcopy(self.album);a['tracks']['items'][0]['duration']+=180
        self.assertFalse(assess(self.row,a,{**self.review,'album_sha256':fingerprint(a)})[0]['eligible'])
        a=copy.deepcopy(self.album)
        for t in a['tracks']['items']:t['performers']=t['performers'].replace('NBC Symphony Orchestra','BBC Symphony Orchestra')
        with self.assertRaises(ValueError):assess(self.row,a,{**self.review,'album_sha256':fingerprint(a)})
