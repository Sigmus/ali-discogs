import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_blocker_groups import build


class BlockerGroupingTests(unittest.TestCase):
    def test_work_and_credit_diagnostics_are_not_review_decisions(self):
        entries = [{'discogs_id': str(i), 'title': 'Example', 'uncached_hits': 0,
                    'cached_candidates': [{'programme': [p]}]} for i, p in enumerate([
                        {'work_tracks': 0, 'credited_tracks': 0},
                        {'work_tracks': 3, 'credited_tracks': 0},
                        {'work_tracks': 3, 'credited_tracks': 2}])]
        result = build({'entries': entries}, {'releases': {str(i): {'status': 'unchecked'} for i in range(3)}}, {})
        self.assertEqual(result['review_state_counts'], {'no_saved_decision': 3})
        self.assertEqual([e['group'] for e in result['entries']], [
            'work_title_or_catalogue_mapping_unresolved', 'credit_support_unresolved',
            'partial_programme_or_completeness'])

    def test_saved_hold_wins_even_with_no_search_candidate(self):
        result = build({'entries': [{'discogs_id': '1', 'title': 'Held', 'uncached_hits': 2,
                                    'cached_candidates': []}]},
                       {'releases': {'1': {'status': 'unchecked', 'review': {
                           'decision': 'withhold', 'reason': 'Unknown transfer.'}}}}, {})
        self.assertEqual(result['entries'][0]['group'], 'saved:withhold')
        self.assertEqual(result['review_state_counts'], {'reviewed_unresolved': 1})

    def test_stale_inventory_fails_closed(self):
        with self.assertRaises(ValueError):
            build({'entries': [{'discogs_id': '1'}]}, {'releases': {'1': {'status': 'probable'}}}, {})
