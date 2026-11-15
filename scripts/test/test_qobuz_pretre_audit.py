import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess
from qobuz_pretre_audit import audit
from qobuz_snapshot import load_snapshot

class PretreAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec=json.loads((ROOT/'data/qobuz_pretre_band_review.json').read_text())
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])==cls.spec['discogs_id'])
        cls.raw=json.loads((ROOT/'raw/discogs/releases/13671866.json').read_text())
        cls.album=load_snapshot()['albums'][cls.spec['album_id']]
        cls.hold=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='13671866')

    def test_all_combined_bands_accounted_for_but_equal_side_total_is_not_identity(self):
        before=copy.deepcopy(self.row)
        d=audit(self.row,self.raw,self.album,self.spec)
        self.assertEqual((d['source_bands'],d['digital_sections']),(13,20))
        self.assertEqual(d['side_totals']['B'],{'source_seconds':1280,'digital_seconds':1280})
        self.assertTrue(next(b for b in d['bands'] if b['position']=='B3')['timing_discrepancy'])
        self.assertTrue(next(b for b in d['bands'] if b['position']=='B4')['timing_discrepancy'])
        self.assertFalse(d['recording_identity_verified'])
        self.assertFalse(d['publication_change'])
        self.assertEqual(before,self.row)
        missing=[c['name'] for c in d['source_image_credit_mentions'] if not c['surname_mentioned_on_track_ids']]
        self.assertEqual(missing,['M. Cazauran','M. Debost'])

    def test_reused_or_missing_digital_section_and_changed_source_band_rejected(self):
        for change in ['reuse','missing','source']:
            spec=copy.deepcopy(self.spec);raw=copy.deepcopy(self.raw)
            if change=='reuse':spec['bands'][1]['candidate_track_ids'][1]=spec['bands'][1]['candidate_track_ids'][0]
            elif change=='missing':spec['bands'].pop()
            else:raw['tracklist'][1]['title']='Another source section'
            with self.assertRaises(ValueError):audit(self.row,raw,self.album,spec)

    def test_default_withhold_validates_images_before_returning_ineligible(self):
        self.assertFalse(assess(self.row,self.album,self.hold)[0]['eligible'])
        for change in ['hash','outside']:
            hold=copy.deepcopy(self.hold)
            if change=='hash':hold['external_source_files'][0]['sha256']='0'*64
            else:hold['external_source_files'][0]['path']='README.md'
            with self.assertRaises(ValueError):assess(self.row,self.album,hold)
