import copy
import gzip
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess
from qobuz_match import evaluate
from qobuz_completeness import check_programme

class YepesReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='2857544')
        cls.album=next(x['album'] for x in json.loads(gzip.decompress((ROOT/'data/qobuz_metadata_followup_2026_11_15.json.gz').read_bytes()))['metadata'] if x['album']['id']=='0002894457132')
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_binding_reviews.json').read_text())['releases'] if r['discogs_id']=='2857544')

    def test_equal_track_count_cannot_override_recorded_withhold(self):
        raw=json.loads((ROOT/'raw/discogs/releases/2857544.json').read_text())
        self.assertEqual(sum(len(t['sub_tracks']) for t in raw['tracklist']),len(self.album['tracks']['items']))
        self.assertFalse(assess(self.row,self.album,self.review)[0]['eligible'])

    def test_suffix_fix_does_not_supply_missing_gigue(self):
        row=copy.deepcopy(self.row)
        for t in row['tracklist']:
            if t['title']=='Suite E-Dur BWV 1006 a':t['title']='Suite E-Dur BWV 1006a'
        evidence=evaluate(row,self.album)
        self.assertEqual(evidence['coverage'],1)
        inventory={'works':[{'composer':'Johann Sebastian Bach','catalogue':['bwv','1006a',''],'movements':[1,2,3,4,5,6],'source':'reviewed source suite order'}]}
        checked=check_programme(row,self.album,evidence,inventory)
        suite=checked['works'][-1]
        self.assertNotEqual(suite['status'],'complete')
        self.assertEqual(suite['observed_movements'],[1,2,3,4,4,5])
        self.assertIn(6,suite['missing_movements'])
