import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_credit171_diagnostic import declared_gaps, explicit_work_copy


class CreditDiagnosticTests(unittest.TestCase):
    def test_work_context_is_a_copy_and_never_overwrites_full_titles(self):
        album = {'tracks': {'items': [
            {'id': 1, 'title': 'I. Allegro', 'work': 'Sonata Op. 1', 'performers': 'A, Piano'},
            {'id': 2, 'title': 'Another Sonata: II. Andante', 'work': 'Wrong work', 'performers': 'B, Piano'},
            {'id': 3, 'title': 'III. Presto', 'work': None, 'performers': 'C, Piano'}]}}
        before = copy.deepcopy(album)
        result, changes = explicit_work_copy(album)
        self.assertEqual(album, before)
        self.assertEqual(result['tracks']['items'][0]['title'], 'Sonata Op. 1: I. Allegro')
        self.assertEqual(result['tracks']['items'][1:], before['tracks']['items'][1:])
        self.assertEqual(changes, [{'track_id': 1, 'original_title': 'I. Allegro', 'work': 'Sonata Op. 1'}])
        self.assertEqual(result['tracks']['items'][0]['performers'], 'A, Piano')

    def test_role_gap_cannot_borrow_a_performance_from_another_track(self):
        gaps = declared_gaps(['A'], [
            {'id': 1, 'performers': 'A, Guitar'}, {'id': 2, 'performers': 'A, Piano'}])
        self.assertEqual(gaps, [{'required_name': 'A', 'declarations': [
            {'track_id': 1, 'name': 'A', 'roles': 'Guitar'}]}])

    def test_distinct_near_names_are_never_merged(self):
        self.assertEqual(declared_gaps(['Paul Kuen'], [{'id': 1, 'performers': 'Paul Kuentz, Composer'}]), [])

    def test_second_positive_declaration_on_same_track_prevents_false_gap(self):
        self.assertEqual(declared_gaps(['A'], [{'id': 1, 'performers': 'A, Guitar - A, MainArtist'}]), [])
