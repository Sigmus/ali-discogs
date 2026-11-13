import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_cache_archive import export, restore
from qobuz_catalog import Catalog, DEFAULT_SOURCE


class CacheArchiveTests(unittest.TestCase):
    def test_restored_cache_replays_without_network_and_preserves_conflicts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root/'source'; source.mkdir()
            request = {'endpoint': 'album/get', 'params': {'album_id': 'example'}}
            name = hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest()+'.json'
            (source/name).write_text(json.dumps({'request': request, 'response': {'id': 'example'}}))
            archive = root/'cache.tar.gz'
            export(source, archive)
            target = root/'restored'
            restore(archive, target)
            client = Catalog(DEFAULT_SOURCE, offline=True, cache=target)
            try:
                self.assertEqual(client.fetch('album/get', album_id='example'), {'id': 'example'})
            finally:
                client.close()
            (target/name).write_text('preserve me')
            with self.assertRaises(ValueError):
                restore(archive, target)
            self.assertEqual((target/name).read_text(), 'preserve me')

    def test_path_traversal_members_are_rejected_without_extraction(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); archive = root/'bad.tar.gz'
            with tarfile.open(archive, 'w:gz') as tar:
                member = tarfile.TarInfo('../outside.json');member.size = 2
                tar.addfile(member, io.BytesIO(b'{}'))
            with self.assertRaises(ValueError):
                restore(archive, root/'target')
            self.assertFalse((root/'outside.json').exists())
