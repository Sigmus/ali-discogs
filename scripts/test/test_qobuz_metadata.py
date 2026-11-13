import json
from pathlib import Path
import tempfile
import unittest
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_metadata_poc import candidate_plan, validate_album, fetch_complete_album
from unittest.mock import Mock
from qobuz_catalog import CatalogError


class MetadataTests(unittest.TestCase):
    def test_duplicate_albums_are_requested_once_with_release_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'manifest.json').write_text(json.dumps({'entries': [{'discogs_id': 1}, {'discogs_id': 2}]}))
            for release in [1, 2]:
                (root / f'{release}.json').write_text(json.dumps({'search': {'albums': {'items': [{'id': 'shared'}]}}}))
            self.assertEqual(candidate_plan(root), [{'album_id': 'shared', 'discogs_ids': [1, 2]}])

    def test_incomplete_tracks_and_wrong_album_are_not_successes(self):
        for album in [{'id': 'x', 'tracks_count': 2, 'tracks': {'items': [{}]}},
                      {'id': 'wrong', 'tracks_count': 1, 'tracks': {'items': [{}]}}]:
            with self.assertRaises(CatalogError):
                validate_album(album, 'x')
        validate_album({'id': 'x', 'tracks_count': 1, 'tracks': {'items': [{}]}}, 'x')

    def test_pages_assembled_without_mutating_cached_first_page(self):
        first = {'id': 'x', 'tracks_count': 3, 'tracks': {'items': [{'id': 1}, {'id': 2}], 'offset': 0, 'total': 3}}
        second = {'id': 'x', 'tracks_count': 3, 'tracks': {'items': [{'id': 3}], 'offset': 2, 'total': 3}}
        catalog = Mock()
        catalog.fetch.side_effect = [first, second]
        result = fetch_complete_album(catalog, 'x')
        self.assertEqual([t['id'] for t in result['tracks']['items']], [1, 2, 3])
        self.assertEqual(len(first['tracks']['items']), 2)
        catalog.fetch.assert_called_with('album/get', album_id='x', offset=2, limit=500)

    def test_pagination_rejects_overlap_wrong_offset_and_empty_page(self):
        first = {'id': 'x', 'tracks_count': 2, 'tracks': {'items': [{'id': 1}], 'offset': 0, 'total': 2}}
        for items, offset in [([{'id': 1}], 1), ([{'id': 2}], 0), ([], 1)]:
            catalog = Mock()
            catalog.fetch.side_effect = [first, {'id': 'x', 'tracks_count': 2, 'tracks': {'items': items, 'offset': offset, 'total': 2}}]
            with self.assertRaises(CatalogError):
                fetch_complete_album(catalog, 'x')

    def test_pagination_failure_propagates_without_retry(self):
        catalog = Mock()
        catalog.fetch.side_effect = [
            {'id': 'x', 'tracks_count': 2, 'tracks': {'items': [{'id': 1}], 'offset': 0, 'total': 2}},
            CatalogError('HTTP 429')]
        with self.assertRaises(CatalogError):
            fetch_complete_album(catalog, 'x')
        self.assertEqual(catalog.fetch.call_count, 2)
