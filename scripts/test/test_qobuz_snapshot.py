import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_snapshot import album_fields, load_snapshot


class SnapshotTests(unittest.TestCase):
    def test_export_whitelist_excludes_unknown_and_account_fields(self):
        album = album_fields({'id': 'x', 'title': 'Album', 'token': 'secret',
                              'artist': {'id': 1, 'name': 'Artist', 'email': 'private'},
                              'image': {'small': 'https://static.qobuz.com/cover.jpg', 'session': 'secret'}})
        self.assertNotIn('token', album)
        self.assertNotIn('email', album['artist'])
        self.assertNotIn('session', album['image'])

    def test_portable_evidence_contains_all_manifest_candidates(self):
        data = load_snapshot()
        self.assertEqual(len(data['searches']), 740)
        self.assertEqual(len(data['albums']), 1036)
        ids = {str(a['id']) for s in data['searches'].values() for a in s['search']['albums']['items']}
        self.assertEqual(ids, set(data['albums']))
        self.assertEqual(sum(len(a['tracks']['items']) for a in data['albums'].values()), 27770)
