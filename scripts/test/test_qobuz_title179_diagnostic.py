import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_title179_diagnostic import rank, review_queue


class TitleDiagnosticRankingTests(unittest.TestCase):
    def test_completeness_breaks_tie_without_overriding_coverage(self):
        def candidate(aid, coverage, complete):
            return {'album_id': aid, 'baseline_coverage': 0, 'experimental_coverage': coverage,
                    'experimental_completeness': {'status': complete}}
        entries = [
            {'discogs_id': '1', 'title': 'Full', 'candidates': [candidate('a', 1, 'unknown'), candidate('b', 1, 'complete')]},
            {'discogs_id': '2', 'title': 'Partial', 'candidates': [candidate('c', .5, 'complete')]},
            {'discogs_id': '3', 'title': 'No gain', 'candidates': [candidate('d', 0, 'unknown')]}]
        result = rank(entries)
        self.assertEqual([e['discogs_id'] for e in result], ['1', '2'])
        self.assertEqual(result[0]['best_album_id'], 'b')
        self.assertEqual(result[0]['bucket'], 'full_support_complete_programme')
        self.assertEqual(result[1]['bucket'], 'partial_support')

    def test_saved_holds_and_accepted_results_do_not_return_to_pending(self):
        entries = [{'discogs_id': str(i), 'title': 'Example', 'candidates': [
            {'album_id': 'a', 'baseline_coverage': 0, 'experimental_coverage': 1,
             'experimental_completeness': {'status': 'complete'}}]} for i in range(3)]
        pending, resolved, held = review_queue(entries, {
            '0': {'status': 'unchecked'}, '1': {'status': 'probable'},
            '2': {'status': 'unchecked', 'review': {'reason': 'Transfer unresolved.'}}})
        self.assertEqual([e['discogs_id'] for e in pending], ['0'])
        self.assertEqual([e['discogs_id'] for e in resolved], ['1'])
        self.assertEqual([e['discogs_id'] for e in held], ['2'])
