import copy
import gzip
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint,reviewed_candidate
from qobuz_snapshot import load_snapshot

class KarajanMendelssohnTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='7064777')
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='7064777')
        cls.album=load_snapshot()['albums'][cls.review['album_id']]

    def test_all_five_symphonies_and_each_split_sinfonia_band_are_accounted_for(self):
        c=reviewed_candidate(self.row,self.album,self.review)
        self.assertEqual((c['status'],c['confidence']),('probable',.85))
        self.assertEqual([len(w['track_ids']) for w in c['completeness']['works']],[4,12,4,4,4])
        self.assertEqual(len({i for w in c['completeness']['works'] for i in w['track_ids']}),28)
        self.assertEqual(c['completeness']['works'][1]['observed_movements'],[1,1,1,2,3,4,5,6,7,8,9,10])

    def test_rehashed_missing_band_repeated_part_or_wrong_orchestra_cannot_pass(self):
        for change in ['missing','repeat','orchestra']:
            a=copy.deepcopy(self.album)
            if change=='missing':a['tracks']['items'].pop(9)
            elif change=='repeat':a['tracks']['items'][9]['title']=a['tracks']['items'][8]['title']
            else:
                for t in a['tracks']['items']:t['performers']=t['performers'].replace('Berliner Philharmoniker','Vienna Philharmonic')
            try:result=assess(self.row,a,{**self.review,'album_sha256':fingerprint(a)})[0]
            except ValueError:continue
            self.assertFalse(result['eligible'],change)
