import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import Mock

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_catalog import Catalog, CatalogError


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.catalog = Catalog(cache=Path(self.temp.name))
        self.catalog.app_id = "test-app-id"
        self.catalog.session.headers["X-User-Auth-Token"] = "test-private-token"
        self.response = Mock()
        self.response.json.return_value = {"albums": {"items": []}}
        self.catalog.session.get = Mock(return_value=self.response)

    def tearDown(self):
        self.catalog.close()
        self.temp.cleanup()

    def test_cache_resumes_offline_without_credentials(self):
        expected = self.catalog.fetch("catalog/search", query="Gould", type="albums", limit=5)
        saved = next(Path(self.temp.name).glob('*.json')).read_text()
        self.assertNotIn("test-private-token", saved)
        self.assertNotIn("test-app-id", saved)
        self.assertIn("fetched_at", json.loads(saved))
        self.catalog.app_id = None
        self.catalog.offline = True
        self.assertEqual(self.catalog.fetch("catalog/search", query="Gould", type="albums", limit=5), expected)
        self.catalog.session.get.assert_called_once()
        with self.assertRaisesRegex(CatalogError, "Offline cache miss"):
            self.catalog.fetch("catalog/search", query="different", type="albums", limit=5)

    def test_http_error_not_cached_and_does_not_expose_url(self):
        failure = Mock(status_code=401)
        self.response.raise_for_status.side_effect = requests.HTTPError(
            "secret URL", response=failure
        )
        with self.assertRaisesRegex(CatalogError, "HTTP 401") as caught:
            self.catalog.fetch("catalog/search", query="Gould")
        self.assertNotIn("secret URL", str(caught.exception))
        self.assertEqual(list(Path(self.temp.name).iterdir()), [])

    def test_malformed_search_is_not_empty_result(self):
        self.response.json.return_value = {"message": "not an album response"}
        with self.assertRaises(CatalogError):
            self.catalog.fetch("catalog/search", query="Gould")
        self.assertEqual(list(Path(self.temp.name).iterdir()), [])

    def test_audio_endpoints_are_disallowed(self):
        with self.assertRaises(CatalogError):
            self.catalog.fetch("track/getFileUrl", track_id=1)
        self.catalog.session.get.assert_not_called()

    def test_refresh_refetches_and_failed_album_does_not_replace_cache(self):
        first = self.catalog.fetch("catalog/search", query="Gould")
        self.catalog.refresh = True
        self.response.json.return_value = {"albums": {"items": [{"id": "42"}]}}
        self.assertNotEqual(first, self.catalog.fetch("catalog/search", query="Gould"))
        self.assertEqual(self.catalog.session.get.call_count, 2)
        self.response.json.return_value = {"id": "wrong-album"}
        with self.assertRaises(CatalogError):
            self.catalog.fetch("album/get", album_id="42")
        self.assertEqual(len(list(Path(self.temp.name).glob('*.json'))), 1)


if __name__ == '__main__':
    unittest.main()
