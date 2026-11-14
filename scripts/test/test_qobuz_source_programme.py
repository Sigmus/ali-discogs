import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT
from qobuz_source_programme import validate_hold,withhold_candidates


class SourceProgrammeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='7971104')
        cls.raw=(ROOT/'raw/discogs/releases/7971104.json').read_bytes()
        cls.review=json.loads((ROOT/'data/qobuz_source_programme_reviews.json').read_text())['releases'][0]

    def test_known_missing_source_work_blocks_even_a_high_scoring_candidate(self):
        hold=validate_hold(self.row,self.raw,self.review)
        self.assertEqual((hold['saved_track_count'],hold['physical_track_count']),(13,14))
        candidates=[{'status':'found','confidence':.99,'coverage':1,'reasons':['All normalized source titles supported.']}]
        before=copy.deepcopy(candidates);result=withhold_candidates(candidates,hold)
        self.assertEqual(candidates,before)
        self.assertEqual(result[0]['status'],'unchecked');self.assertIsNone(result[0]['confidence'])
        self.assertIn('Sevillana',result[0]['reasons'][0])

    def test_stale_or_missing_source_evidence_cannot_silently_lift_the_hold(self):
        for field,value in [('source_sha256','0'*64),('missing_tracks',[]),('external_source_files',[]),('physical_track_count',13),('decision','accept')]:
            with self.assertRaises(ValueError):validate_hold(self.row,self.raw,{**self.review,field:value})
        bad=copy.deepcopy(self.review);bad['external_source_files'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):validate_hold(self.row,self.raw,bad)
        row=copy.deepcopy(self.row);row['tracklist'][0]['title']='Changed source'
        with self.assertRaises(ValueError):validate_hold(row,self.raw,self.review)
