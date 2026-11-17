import copy
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_credit150_triage import inspect_candidate


class Credit150TriageTests(unittest.TestCase):
    def candidate(self, track_credit, other_credit=''):
        row = {'discogs_id': 1}
        album = {'id': 'x', 'title': 'test', 'tracks': {'items': [
            {'id': 1, 'title': 'wanted', 'performers': track_credit},
            {'id': 2, 'title': 'other', 'performers': other_credit}]}}
        original = copy.deepcopy(album)
        evidence = {'required_performers': ['Paul Kuen'], 'coverage': 0,
                    'programme': [{'target': 'wanted'}]}
        with patch('qobuz_credit150_triage.evaluate', return_value=evidence), \
             patch('qobuz_credit150_triage.contextual_tracks', side_effect=lambda row, tracks: tracks), \
             patch('qobuz_credit150_triage.target_work_matches', side_effect=lambda row, target, track: track['title'] == target):
            result = inspect_candidate(row, album)
        self.assertEqual(album, original)
        return result

    def test_other_work_cannot_supply_credit(self):
        r = self.candidate('Someone Else, Piano', 'Paul Kuen, MainArtist')
        self.assertIn('positive_only_on_other_work', r['flags'])
        self.assertEqual(r['units'][0]['name_evidence'][0]['positive_work_track_ids'], [])

    def test_similar_name_is_not_an_identity(self):
        self.assertIn('required_name_not_declared', self.candidate('Paul Kuentz, MainArtist')['flags'])

    def test_composer_and_associated_roles_are_not_recommended_as_instruments(self):
        self.assertIn('roleless_or_composer_only', self.candidate('Paul Kuen, Composer')['flags'])
        self.assertIn('associated_role_unresolved', self.candidate('Paul Kuen, AssociatedPerformer')['flags'])

    def test_explicit_unaccepted_instrument_is_diagnostic_only(self):
        r = self.candidate('Paul Kuen, Guitar')
        self.assertEqual(r['coverage'], 0)
        self.assertIn('explicit_unaccepted_role', r['flags'])
        self.assertNotIn('status', r)
