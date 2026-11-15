import copy
import gzip
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint,reviewed_candidate

class SevenFollowupReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='1662708')
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='1662708')
        cls.album=next(r['album'] for r in json.loads(gzip.decompress((ROOT/'data/qobuz_metadata_followup_2026_11_15.json.gz').read_bytes()))['metadata'] if r['album']['id']==cls.review['album_id'])

    def test_complete_paris_programme_is_probable_only(self):
        c=reviewed_candidate(self.row,self.album,self.review)
        self.assertEqual((c['status'],c['confidence']),('probable',.85))
        self.assertEqual(c['completeness']['works'][0]['track_ids'],[43457314,43457315,43457316])

    def test_berlin_substitution_or_missing_movement_is_not_eligible(self):
        for change in ['orchestra','movement']:
            a=copy.deepcopy(self.album)
            if change=='movement':a['tracks']['items'].pop(1);a['tracks_count']-=1
            else:
                for t in a['tracks']['items']:
                    t['performers']=t['performers'].replace('Orchestre De Paris','Berliner Philharmoniker').replace('Orchestre de Paris','Berliner Philharmoniker')
                    t['performer']['name']=t['performer']['name'].replace('Orchestre de Paris','Berliner Philharmoniker')
            r={**self.review,'album_sha256':fingerprint(a)}
            self.assertFalse(assess(self.row,a,r)[0]['eligible'])
