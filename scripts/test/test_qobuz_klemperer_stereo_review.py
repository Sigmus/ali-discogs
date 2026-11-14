import copy
import gzip
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint


class StereoLabelReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews={r['discogs_id']:r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.album=json.loads(gzip.decompress((ROOT/'data/qobuz_evidence.json.gz').read_bytes()))['albums']['vrg5q0y8vzvaa']

    def test_complete_programmes_require_positive_stereo_label_evidence(self):
        for rid,counts in [('24964822',[4,1,1]),('26149643',[4,1])]:
            review=self.reviews[rid];result,evidence=assess(self.rows[rid],self.album,review)
            self.assertTrue(result['eligible'])
            self.assertEqual([len(w['track_ids']) for w in result['completeness']['works']],counts)
            bad=copy.deepcopy(review);bad['external_source_files'][0]['sha256']='0'*64
            with self.assertRaises(ValueError):assess(self.rows[rid],self.album,bad)

    def test_later_orchestra_or_missing_overture_cannot_pass_after_rehash(self):
        review=self.reviews['26149643'];row=self.rows['26149643']
        a=copy.deepcopy(self.album)
        for t in a['tracks']['items']:t['performers']=t['performers'].replace('Philharmonia Orchestra','New Philharmonia Orchestra')
        with self.assertRaises(ValueError):assess(row,a,{**review,'album_sha256':fingerprint(a)})
        a=copy.deepcopy(self.album);a['tracks']['items']=[t for t in a['tracks']['items'] if t['id']!=353969779]
        with self.assertRaises(ValueError):assess(row,a,{**review,'album_sha256':fingerprint(a)})
