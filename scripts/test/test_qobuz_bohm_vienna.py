import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint,reviewed_candidate
from qobuz_snapshot import load_snapshot

class BohmViennaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='6810640')
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='6810640')
        cls.album=load_snapshot()['albums'][cls.review['album_id']]

    def test_two_plus_four_movements_with_explicit_work_and_live_marker(self):
        c=reviewed_candidate(self.row,self.album,self.review)
        self.assertEqual((c['status'],c['confidence']),('probable',.85))
        works=c['completeness']['works']
        self.assertEqual([len(w['track_ids']) for w in works],[2,4])
        ids={i for w in works for i in w['track_ids']}
        self.assertEqual(len(ids),6)
        self.assertTrue(ids.isdisjoint(self.review['extra_track_ids']))
        self.assertEqual(len(self.review['extra_track_ids']),8)

    def test_rehashed_wrong_work_session_orchestra_composer_or_missing_movement_fails(self):
        for change in ['work','session','orchestra','composer','missing']:
            a=copy.deepcopy(self.album);t=a['tracks']['items'][0]
            if change=='work':t['work']='Symphony No. 5 In B Flat, D.485'
            elif change=='session':t['version']='Studio Berlin / 1966'
            elif change=='orchestra':t['performers']=t['performers'].replace('Wiener Philharmoniker','Berliner Philharmoniker')
            elif change=='composer':t['performers']=t['performers'].replace('Franz Schubert','Anton Bruckner')
            else:a['tracks']['items'].remove(t)
            try:result=assess(self.row,a,{**self.review,'album_sha256':fingerprint(a)})[0]
            except ValueError:continue
            self.assertFalse(result['eligible'],change)
