import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint,reviewed_candidate
from qobuz_snapshot import load_snapshot

class CampanellaRhapsodiesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='10100439')
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='10100439')
        cls.album=load_snapshot()['albums'][cls.review['album_id']]

    def test_all_nineteen_members_are_distinct_and_source_key_is_preserved(self):
        c=reviewed_candidate(self.row,self.album,self.review)
        self.assertEqual((c['status'],c['confidence']),('probable',.85))
        self.assertEqual(len(c['completeness']['works']),19)
        self.assertTrue(all(len(w['track_ids'])==1 for w in c['completeness']['works']))
        self.assertEqual(len({i for w in c['completeness']['works'] for i in w['track_ids']}),19)
        self.assertEqual(len(self.review['adds']),9)
        self.assertIn('No.12 In C Sharp Major',self.review['expected'])

    def test_rehashed_wrong_number_composer_pianist_or_missing_member_cannot_pass(self):
        for change in ['number','composer','pianist','missing']:
            a=copy.deepcopy(self.album)
            t=next(t for t in a['tracks']['items'] if t['id']==4131551)
            if change=='number':t['title']=t['title'].replace('No. 11','No. 1')
            elif change=='composer':t['performers']=t['performers'].replace('Franz Liszt','Johannes Brahms')
            elif change=='pianist':t['performers']=t['performers'].replace('Michele Campanella','Roberto Szidon')
            else:a['tracks']['items'].remove(t)
            try:result=assess(self.row,a,{**self.review,'album_sha256':fingerprint(a)})[0]
            except ValueError:continue
            self.assertFalse(result['eligible'],change)
