import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint,reviewed_candidate
from qobuz_snapshot import load_snapshot

class SayReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='14766559')
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='14766559')
        cls.album=load_snapshot()['albums'][cls.review['album_id']]

    def test_four_complete_sonatas_only_and_technician_not_required(self):
        c=reviewed_candidate(self.row,self.album,self.review)
        self.assertEqual((c['status'],c['confidence']),('probable',.85))
        ids=[i for w in c['completeness']['works'] for i in w['track_ids']]
        self.assertEqual([len(w['track_ids']) for w in c['completeness']['works']],[3,3,3,3])
        self.assertEqual(len(set(ids)),12)
        self.assertEqual(len(self.review['extra_track_ids']),101)
        self.assertFalse(set(ids)&set(self.review['extra_track_ids']))
        self.assertEqual(c['required_performers'],['Fazıl Say'])

    def test_wrong_work_pianist_or_incomplete_movement_cannot_pass_after_rehash(self):
        for change in ['work','pianist','missing','timing']:
            a=copy.deepcopy(self.album);t=next(t for t in a['tracks']['items'] if t['id']==84954353)
            if change=='work':t['work']='Piano Sonata No. 1 in F Minor, Op. 2 No. 1'
            elif change=='pianist':t['performers']=t['performers'].replace('Fazil Say','Another Pianist')
            elif change=='timing':t['duration']+=60
            else:a['tracks']['items'].remove(t)
            try:result=assess(self.row,a,{**self.review,'album_sha256':fingerprint(a)})[0]
            except ValueError:continue
            self.assertFalse(result['eligible'],change)

    def test_real_pianist_cannot_be_excluded_as_technician(self):
        r=copy.deepcopy(self.review)
        r['source_credit_reconciliation']['nonperformers']=[{'name':'Fazıl Say','role':'Piano'}]
        with self.assertRaises(ValueError):assess(self.row,self.album,r)
