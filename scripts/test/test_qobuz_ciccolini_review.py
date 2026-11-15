import copy
import gzip
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint,reviewed_candidate

class CiccoliniReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='2236260')
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='2236260')
        cls.album=next(x['album'] for x in json.loads(gzip.decompress((ROOT/'data/qobuz_metadata_followup_2026_11_15.json.gz').read_bytes()))['metadata'] if x['album']['id']==cls.review['album_id'])

    def test_both_complete_source_side_programmes_probable_only(self):
        c=reviewed_candidate(self.row,self.album,self.review)
        self.assertEqual((c['status'],c['confidence']),('probable',.85))
        self.assertEqual([w['track_ids'] for w in c['completeness']['works']],[list(range(193451727,193451730)),list(range(193451730,193451733))])

    def test_rehashed_wrong_composer_role_or_recording_cannot_pass(self):
        for change in ['composer','role','conductor','orchestra','missing','timing','isrc']:
            a=copy.deepcopy(self.album)
            if change=='missing':a['tracks']['items'].pop()
            elif change=='timing':a['tracks']['items'][0]['duration']+=80
            elif change=='isrc':a['tracks']['items'][0]['isrc']='other'
            else:
                for t in a['tracks']['items']:
                    if change=='composer':t['performers']=t['performers'].replace('Pyotr Tchaikovsky','Sergei Rachmaninoff')
                    elif change=='role':t['performers']=t['performers'].replace(', Composer',', Producer')
                    elif change=='conductor':t['performers']=t['performers'].replace('Constantin Silvestri','Andre Cluytens')
                    else:t['performers']=t['performers'].replace('Orchestre National De France','Paris Conservatoire Orchestra')
            try:result=assess(self.row,a,{**self.review,'album_sha256':fingerprint(a)})[0]
            except ValueError:continue
            self.assertFalse(result['eligible'],change)
