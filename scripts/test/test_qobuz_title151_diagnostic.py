import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_title151_diagnostic import catalogue_text, work_copy, target_copy, family
from qobuz_match import catalogue, work_match


class RemainingTitleDiagnosticTests(unittest.TestCase):
    def test_hob_section_and_work_number_never_collapse(self):
        self.assertEqual(catalogue(catalogue_text('Hoboken XVI/42')), {('hob', '16', '42')})
        self.assertEqual(catalogue_text('Hob. XVI:42'), 'Hob 16 No 42')
        self.assertNotEqual(catalogue_text('Hob XVI/42'), catalogue_text('Hob XVIII/42'))
        self.assertFalse(work_match(catalogue_text('Hob XVI/42'), catalogue_text('Hob XVI/48')))
        self.assertEqual(catalogue_text('Hob XXVIIb/1'), 'Hob XXVIIb/1')

    def test_opus_subdivision_preserved_and_ranges_not_truncated(self):
        self.assertEqual(catalogue_text('Op. 9/1'), 'Op 9 No 1')
        self.assertEqual(catalogue_text('Op. 26 N°1'), 'Op 26 No 1')
        self.assertFalse(work_match(catalogue_text('Op9/1'), 'Op.9 No.2'))
        for title in ['Op.9/1-3', 'Op.9/1/2', 'Hob XVI/42–48', 'Op9/1,2']:
            self.assertEqual(catalogue_text(title), title)

    def test_work_field_copy_does_not_change_credits_or_original(self):
        album = {'tracks': {'items': [{'id': 1, 'title': 'Allegro (excerpt, piano arrangement)',
                  'work': 'Violin Sonata K.378', 'performers': 'A, AssociatedPerformer', 'duration': 99}]}}
        original = copy.deepcopy(album)
        transformed, changes = work_copy(album)
        self.assertEqual(album, original)
        self.assertIn('excerpt, piano arrangement', transformed['tracks']['items'][0]['title'])
        self.assertEqual(transformed['tracks']['items'][0]['performers'], 'A, AssociatedPerformer')
        self.assertEqual(transformed['tracks']['items'][0]['duration'], 99)
        self.assertEqual(changes[0]['original_title'], original['tracks']['items'][0]['title'])

    def test_explicit_existing_catalogue_cannot_be_overwritten(self):
        album = {'tracks': {'items': [{'id': 1, 'title': 'Sonata K.454', 'work': 'Sonata K.378'}]}}
        transformed, changes = work_copy(album)
        self.assertEqual(transformed, album)
        self.assertEqual(changes, [])

    def test_source_scopes_preserved_and_colliding_titles_rejected(self):
        row = {'tracklist': [{'title': 'Sonata Hoboken XVI/42', 'type': 'index'}], 'performers': ['A']}
        result, mapping = target_copy(row)
        self.assertEqual(mapping, {'Sonata Hob 16 No 42': 'Sonata Hoboken XVI/42'})
        self.assertEqual(result['_reviewed_title_sources'], mapping)
        self.assertEqual(row['tracklist'][0]['title'], 'Sonata Hoboken XVI/42')
        with self.assertRaises(ValueError):
            target_copy({'tracklist': [{'title': 'Op.9/1'}, {'title': 'Op 9 No 1'}]})

    def test_family_distinguishes_credit_and_composer_gaps(self):
        def candidate(coverage, title, composer, shared):
            return {'formatted_evidence': {'coverage': coverage}, 'observations': [{
                'title_match_track_ids': title, 'composer_guard_pass_track_ids': composer,
                'shared_catalogue_track_ids': shared, 'catalogue': [('op', '1', '')]}]}
        self.assertEqual(family([candidate(0,[1],[1],[1])]), 'work_title_support_but_musician_gap')
        self.assertEqual(family([candidate(0,[1],[],[1])]), 'title_similarity_rejected_by_composer_guards')
        self.assertEqual(family([candidate(0,[],[],[1])]), 'shared_catalogue_but_unresolved_title_structure')
        self.assertEqual(family([candidate(0,[],[],[])]), 'no_shared_catalogue_in_saved_candidates')
        self.assertEqual(family([candidate(1,[1],[1],[1])]), 'experimental_full_unit_support')
