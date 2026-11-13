import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_baseline_audit import audit
from qobuz_snapshot import load_snapshot

ROOT = Path(__file__).resolve().parents[2]


class BaselineAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scope = json.loads((ROOT/'data/qobuz_baseline_audit_scope.json').read_text())
        rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.report = audit(cls.scope, rows, load_snapshot(), json.loads((ROOT/'data/qobuz_work_inventory.json').read_text()))
        cls.results = {r['discogs_id']: r for r in cls.report['releases']}

    def test_frozen_baseline_excludes_ten_expansions_and_reproduces_original_scores(self):
        scope = {e['discogs_id'] for e in self.scope['entries']}
        expanded = set(json.loads((ROOT/'data/qobuz_expansion_scope.json').read_text())['releases'])
        self.assertEqual(len(scope), 66)
        self.assertFalse(scope & expanded)
        self.assertEqual(self.report['summary']['original_statuses'], {'probable': 54, 'found': 12})
        self.assertEqual(self.report['summary']['v1_status_disagreements'], 0)
        self.assertEqual(self.report['summary']['one_to_one_catalogue_correspondences'], 12)

    def test_present_movements_with_missing_credits_not_claimed_absent(self):
        r = self.results['1026299']
        self.assertEqual(r['audit_status'], 'insufficient_track_credit_evidence')
        for p in r['programme']:
            self.assertEqual([t['movement'] for t in p['title_matched_tracks']], [1, 2, 3])
            self.assertEqual(p['credited_tracks'], 1)
        self.assertEqual(self.report['summary']['audit_statuses'], {
            'supported': 7, 'unresolved': 58, 'insufficient_track_credit_evidence': 1})

    def test_overlap_is_traceable_but_not_automatically_a_missing_programme(self):
        r = self.results['3958148']
        self.assertIn('shared_track_assignments', r['diagnostic_flags'])
        self.assertEqual(r['audit_status'], 'unresolved')
        first, _, third = r['programme']
        self.assertEqual(first['track_ids'], third['track_ids'])
        # An unlabelled target with no inventory remains unknown, not failed.
        self.assertEqual(self.results['1445439']['audit_status'], 'unresolved')
        # Wrong-orchestra distractors do not defeat a complete credited version.
        self.assertEqual(self.results['15282801']['audit_status'], 'supported')
