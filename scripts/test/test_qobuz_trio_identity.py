import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT
from qobuz_credit_role_audit import load_albums
from qobuz_trio_identity_diagnostic import inspect, RID, AID, MEMBERS

class TrioIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])==RID)
        cls.raw=json.loads((ROOT/f'raw/discogs/releases/{RID}.json').read_text())
        cls.album=load_albums()[AID]

    def test_eight_positive_member_and_timing_checks(self):
        result=inspect(self.row,self.raw,self.album)
        self.assertEqual(result['summary'],{'source_leaves':8,'candidate_tracks':8,'all_members_positively_credited':True,'all_composer_checks_pass':True,'all_source_timings_pass':True,'collective_declarations':0})
        self.assertFalse(result['publication_changed'])
        self.assertEqual(result['proposal_status'],'not_adopted')

    def test_each_individual_member_remains_required(self):
        for name in MEMBERS:
            a=copy.deepcopy(self.album)
            a['tracks']['items'][0]['performers']=' - '.join(p for p in a['tracks']['items'][0]['performers'].split(' - ') if not p.startswith(name+','))
            result=inspect(self.row,self.raw,a)
            self.assertFalse(result['summary']['all_members_positively_credited'])
            self.assertEqual(result['bindings'][0]['missing_members'],[name])

    def test_incomplete_programme_rejected(self):
        a=copy.deepcopy(self.album);a['tracks']['items'].pop()
        with self.assertRaisesRegex(ValueError,'eight-movement'):inspect(self.row,self.raw,a)

    def test_duration_discrepancy_does_not_get_consensus_waiver(self):
        a=copy.deepcopy(self.album);a['tracks']['items'][0]['duration']+=120
        self.assertFalse(inspect(self.row,self.raw,a)['summary']['all_source_timings_pass'])
