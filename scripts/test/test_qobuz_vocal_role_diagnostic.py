import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_vocal_role_diagnostic import experimental_text, experimental_album, references


class VocalRoleDiagnosticTests(unittest.TestCase):
    def test_exact_role_fields_only_and_names_stay_unchanged(self):
        original = 'SopranoVocalist Person, Producer - Singer, SopranoVocalist, MainArtist'
        value, changes = experimental_text(original)
        self.assertEqual(value, 'SopranoVocalist Person, Producer - Singer, Soprano, MainArtist')
        self.assertEqual(changes, [{'name': 'Singer', 'role': 'SopranoVocalist', 'experimental_role': 'Soprano'}])

    def test_technical_generic_and_associated_roles_are_not_added(self):
        original = 'A, VocalProducer - B, Composer - C, Artist - D, AssociatedPerformer - E, NotSopranoVocalist'
        self.assertEqual(experimental_text(original), (original, []))

    def test_copy_preserves_original_album_and_all_nonrole_fields(self):
        album = {'id': 'a', 'tracks': {'items': [{'id': 1, 'title': 'Movement', 'duration': 61,
                 'work': 'Work', 'performers': 'Singer, TenorVocalist - Composer, Composer'}]}}
        before = copy.deepcopy(album)
        result, changes = experimental_album(album)
        self.assertEqual(album, before)
        self.assertEqual(result['tracks']['items'][0]['performers'], 'Singer, Tenor - Composer, Composer')
        for key in ['id', 'title', 'duration', 'work']:
            self.assertEqual(result['tracks']['items'][0][key], before['tracks']['items'][0][key])
        self.assertNotEqual(changes[0]['original_track_sha256'], changes[0]['experimental_track_sha256'])

    def test_whitespace_case_and_nontext_are_bounded(self):
        self.assertEqual(experimental_text('Singer,\tBASSVOCALIST\r')[0], 'Singer,\tBass\r')
        self.assertEqual(experimental_text('Singer, Soprano Vocalist'), ('Singer, Soprano Vocalist', []))
        self.assertEqual(experimental_text(None), (None, []))

    def test_references_include_held_candidates_and_deduplicate(self):
        result = references({'releases': {'1': {'candidates': [{'id': 'a'}]}}},
                            {'entries': [{'discogs_id': '1', 'cached_candidates': [{'album_id': 'a'}, {'album_id': 'b'}]}]})
        self.assertEqual(result, {'1': {'a', 'b'}})
