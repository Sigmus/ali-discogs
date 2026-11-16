import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_match import review_progress


class ReviewProgressTests(unittest.TestCase):
    def test_explicit_holds_and_rejections_are_reviewed_even_without_candidates(self):
        for decision in ['withhold', 'reject-recording']:
            review = {'decision': decision, 'recording_review': 'Named pianist unresolved.',
                      'limitations': ['Other recordings may exist.']}
            result = review_progress('unchecked', review)
            self.assertEqual(result['state'], 'reviewed_unresolved')
            self.assertEqual(result['reason'], review['recording_review'])

    def test_no_decision_is_not_claimed_reviewed(self):
        self.assertIsNone(review_progress('unchecked'))
        self.assertIsNone(review_progress('unchecked', {'decision': 'probable'}))

    def test_accepted_matches_keep_their_status(self):
        for status in ['found', 'probable']:
            self.assertIsNone(review_progress(status, {'decision': 'withhold'}))

    def test_explicit_source_programme_hold_is_reviewed(self):
        self.assertEqual(review_progress('unchecked', source_hold={'reason': 'Source incomplete.'})['decision'],
                         'source-programme-hold')
