import copy
import gzip
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint
from qobuz_choral_finale_review import NINTH


class ChoralFinaleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.album=json.loads(gzip.decompress((ROOT/'data/qobuz_evidence.json.gz').read_bytes()))['albums']['vrg5q0y8vzvaa']
        cls.reviews={r['discogs_id']:r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}

    def rebound(self,album):
        review=copy.deepcopy(self.reviews['6119375']);review['album_sha256']=fingerprint(album)
        tracks={t['id']:t for t in album['tracks']['items']}
        review['track_sha256']=[fingerprint(tracks[i]) for i in review['selected_track_ids'] if i in tracks]
        return review

    def test_all_four_movements_and_both_overtures(self):
        for rid in ['6113868','6119375']:
            result,evidence=assess(self.rows[rid],self.album,self.reviews[rid])
            self.assertTrue(result['eligible']);self.assertEqual(evidence['covered'],3)
            self.assertEqual([len(g) for g in result['completeness']['works'][0]['movement_track_ids']],[1,1,1,5])
            self.assertEqual(len(set(i for w in result['completeness']['works'] for i in w['track_ids'])),10)

    def test_missing_reordered_or_repeated_finale_is_rejected(self):
        for action in ['missing','reorder','duplicate']:
            a=copy.deepcopy(self.album);tracks=a['tracks']['items'];i=next(i for i,t in enumerate(tracks) if t['id']==NINTH[4])
            if action=='missing':tracks.pop(i)
            elif action=='reorder':tracks[i],tracks[i+1]=tracks[i+1],tracks[i]
            else:tracks[i+1]=copy.deepcopy(tracks[i])
            with self.assertRaises(ValueError):assess(self.rows['6119375'],a,self.rebound(a))

    def test_positive_sung_credits_and_instrumental_anchors_required(self):
        for before,after in [('Hans Hotter','Other Bass'),('Philharmonia Chorus','Other Chorus'),('Philharmonia Orchestra','Other Orchestra'),('Otto Klemperer','Other Conductor')]:
            a=copy.deepcopy(self.album)
            for t in a['tracks']['items']:t['performers']=t['performers'].replace(before,after)
            with self.assertRaises(ValueError):assess(self.rows['6119375'],a,self.rebound(a))

    def test_voice_discrepancy_and_source_cannot_be_hidden(self):
        review=copy.deepcopy(self.reviews['6119375']);review['voice_metadata_discrepancy']={}
        with self.assertRaises(ValueError):assess(self.rows['6119375'],self.album,review)
        review=copy.deepcopy(self.reviews['6119375']);review['source_sha256']='0'*64
        with self.assertRaises(ValueError):assess(self.rows['6119375'],self.album,review)
