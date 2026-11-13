import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_urls import album_url, export, load_urls, valid_album_url
from qobuz_match import public_album

ROOT = Path(__file__).resolve().parents[2]


class CanonicalQobuzURLTests(unittest.TestCase):
    def test_reported_album_uses_exact_cached_locale_and_slug(self):
        aid = '0002894786633'
        url = public_album({'id':aid, 'title':'Dvorak'})['url']
        self.assertEqual(url, load_urls()[aid])
        self.assertIn('/fr-fr/album/dvorak-complete-symphonies-', url)
        self.assertTrue(url.endswith('/'+aid))

    def test_untrusted_or_missing_url_never_creates_bare_album_route(self):
        good='https://www.qobuz.com/nl-en/album/real-slug/abc123'
        self.assertEqual(album_url({'id':'abc123','url':good}, {}), good)
        for bad in ['https://www.qobuz.com/album/abc123',
                    'https://www.qobuz.com.evil.test/nl-en/album/slug/abc123',
                    'https://user:password@www.qobuz.com/nl-en/album/slug/abc123',
                    good+'?token=private', good.replace('abc123','wrong'), 'javascript:alert(1)']:
            self.assertFalse(valid_album_url(bad,'abc123'),bad)
            self.assertEqual(album_url({'id':'abc123','title':'Title & Artist','url':bad}, {}),
                             'https://www.qobuz.com/nl-en/search?q=Title%20%26%20Artist')

    def test_publication_and_pilot_album_links_all_resolve_from_shared_index(self):
        urls=load_urls()
        self.assertGreaterEqual(len(urls),1043)
        def check(value):
            if isinstance(value,dict):
                if 'url' in value and 'id' in value:
                    self.assertEqual(value['url'],urls[str(value['id'])])
                for child in value.values():check(child)
            elif isinstance(value,list):
                for child in value:check(child)
        check(json.loads((ROOT/'data/qobuz_matches.json').read_text())['releases'])
        check(json.loads((ROOT/'data/qobuz_coverage_pilot.json').read_text()))

    def test_shared_archive_export_is_deterministic_and_offline(self):
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'urls.json'
            export(target=output)
            self.assertEqual(output.read_bytes(),(ROOT/'data/qobuz_album_urls.json').read_bytes())
