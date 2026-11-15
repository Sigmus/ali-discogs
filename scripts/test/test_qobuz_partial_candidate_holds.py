import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,apply_recording_review
from qobuz_credit_role_audit import load_albums
from qobuz_match import catalogue,credits,agrees

class PartialCandidateHoldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews={r['discogs_id']:r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.albums=load_albums()

    def test_missing_works_and_wrong_recordings_are_real_cached_gaps(self):
        for rid,identity in [('9792325',('k','333','')),('11938919',('op','58','')),('2666680',('k','595',''))]:
            album=self.albums[self.reviews[rid]['album_id']]
            self.assertFalse(any(identity in catalogue(t['title']+' '+(t.get('work') or '')) for t in album['tracks']['items']),rid)
        concerto=self.albums[self.reviews['2700887']['album_id']]['tracks']['items'][:3]
        self.assertTrue(all(agrees('Eugene Ormandy',credits(t)) and not agrees('Alfred Wallenstein',credits(t)) for t in concerto))
        mozart=self.albums[self.reviews['5065978']['album_id']]
        fortieth=[t for t in mozart['tracks']['items'] if ('k','550','') in catalogue(t['title']+' '+(t.get('work') or ''))]
        self.assertEqual(len(fortieth),4)
        self.assertTrue(all(agrees('Leonard Bernstein',credits(t)) and not agrees('Karl Böhm',credits(t)) for t in fortieth))

    def test_complete_scorer_support_cannot_erase_six_explicit_holds(self):
        for rid in ['2463301','9792325','11938919','2700887','5065978','2666680']:
            review=self.reviews[rid];album=self.albums[review['album_id']]
            result=apply_recording_review(self.rows[rid],album,review,[{'id':album['id'],'status':'found','confidence':.99,'coverage':1}, {'id':'other','status':'probable','confidence':.85}])
            self.assertEqual((result[0]['status'],result[0]['confidence']),('unchecked',None),rid)
            self.assertEqual(result[1]['id'],'other')
