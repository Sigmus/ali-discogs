import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint,reviewed_candidate
from qobuz_snapshot import load_snapshot

class GilelsWaldsteinTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='13655367')
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='13655367')
        cls.album=load_snapshot()['albums'][cls.review['album_id']]

    def test_source_coda_is_included_once_in_complete_finale(self):
        c=reviewed_candidate(self.row,self.album,self.review)
        self.assertEqual((c['status'],c['confidence']),('probable',.85))
        works=c['completeness']['works']
        self.assertEqual([len(w['track_ids']) for w in works],[3,4])
        self.assertEqual(len({i for w in works for i in w['track_ids']}),7)
        self.assertEqual(self.review['target_unit_groups'][0]['source_titles'][1],'Attacca Prestissimo')
        self.assertEqual(works[0]['track_ids'][-1],610583)

    def test_rehashed_missing_coda_movement_or_wrong_pianist_cannot_pass(self):
        for change in ['coda','movement','pianist']:
            a=copy.deepcopy(self.album)
            if change=='coda':
                t=next(t for t in a['tracks']['items'] if t['id']==610583)
                t['title']=t['title'].replace(' – Prestissimo','')
            elif change=='movement':a['tracks']['items']=[t for t in a['tracks']['items'] if t['id']!=610540]
            else:
                for t in a['tracks']['items']:t['performers']=t['performers'].replace('Emil Gilels','Sviatoslav Richter')
            try:result=assess(self.row,a,{**self.review,'album_sha256':fingerprint(a)})[0]
            except ValueError:continue
            self.assertFalse(result['eligible'],change)
