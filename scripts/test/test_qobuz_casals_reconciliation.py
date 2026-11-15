import copy
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT
from qobuz_source_reconciliation import reconcile,suite_positions
from qobuz_casals_audit import audit

class CasalsReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='6628473')
        cls.review=json.loads((ROOT/'data/qobuz_casals_source_audit.json').read_text())
        cls.flat=json.loads((ROOT/'raw/discogs/releases/23950082.json').read_text())

    def test_exact_correction_is_copy_only_and_excludes_only_documented_liner_author(self):
        original=copy.deepcopy(self.row);fixed=reconcile(self.row,self.review)
        self.assertEqual(self.row,original)
        self.assertIn('BWV.1009',fixed['tracklist'][0]['title'])
        self.assertIn('BWV.1008',self.row['tracklist'][0]['title'])
        self.assertEqual(fixed['performers'],['Pablo Casals'])

    def test_stale_or_missing_source_proof_and_principal_exclusion_fail_closed(self):
        for change in ['target','source','photo','missing','credit']:
            r=copy.deepcopy(self.review)
            if change=='target':r['target_sha256']='stale'
            elif change=='source':r['source_sha256']='stale'
            elif change=='photo':r['source_evidence'][0]['sha256']='stale'
            elif change=='missing':r['source_evidence']=[]
            else:r['nonperforming_source_credit']={'name':'Pablo Casals','role':'Cello'}
            with self.assertRaises(ValueError):reconcile(self.row,r)

    def test_flat_suite_context_rejects_cross_suite_or_missing_movements(self):
        self.assertEqual([g['suite_number'] for g in suite_positions(self.flat)],[5,6])
        for change in ['missing','reorder','side','header']:
            raw=copy.deepcopy(self.flat)
            if change=='missing':raw['tracklist'].pop(2)
            elif change=='reorder':raw['tracklist'][1],raw['tracklist'][2]=raw['tracklist'][2],raw['tracklist'][1]
            elif change=='side':raw['tracklist'][6]['position']='A1'
            else:raw['tracklist'][6]['title']='1st Movement: Prélude'
            with self.assertRaises(ValueError):suite_positions(raw)

    def test_diagnostic_cannot_fetch_or_change_publication(self):
        publication=ROOT/'data/qobuz_matches.json';before=publication.read_bytes()
        with patch('urllib.request.urlopen',side_effect=AssertionError('network forbidden')):
            report=audit()
        self.assertEqual(publication.read_bytes(),before)
        self.assertTrue(all(r['decision']=='programme_supported_recording_unresolved' for r in report['releases']))
        self.assertEqual(len({i for r in report['releases'] for w in r['programme'] for i in w['track_ids']}),24)
