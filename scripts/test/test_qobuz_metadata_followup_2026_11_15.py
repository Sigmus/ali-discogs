import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
worker=importlib.import_module('qobuz_metadata_followup_2026_11_15')


class ProposedMetadataBatchTests(unittest.TestCase):
    def isolated(self,tmp):
        scope=json.loads(worker.SCOPE.read_text())
        scope['screen_sha256']=worker.digest(worker.ROOT/'data/qobuz_remaining_screen.json')
        path=Path(tmp)/'scope.json';path.write_text(json.dumps(scope))
        return path

    def test_default_prepares_seven_fixed_albums_without_network_and_freezes_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            scope=self.isolated(tmp)
            with patch.object(worker,'SCOPE',scope),patch.object(worker,'OUTPUT',Path(tmp)/'run'),patch.object(sys,'argv',['worker']),patch.object(worker.runner,'search',side_effect=AssertionError('network forbidden')):
                self.assertEqual(worker.main(),0)
                manifest=worker.prepare()
                self.assertEqual([t['album_id'] for t in manifest['entries']],worker.EXPECTED)
                data=json.loads(scope.read_text());data['entries'][0]['album_id']='outside-scope';scope.write_text(json.dumps(data))
                with self.assertRaises(ValueError):worker.prepare()

    def test_incomplete_metadata_exports_partial_checkpoint_but_duplicate_tracks_stop(self):
        with tempfile.TemporaryDirectory() as tmp:
            scope=self.isolated(tmp)
            with patch.object(worker,'SCOPE',scope),patch.object(worker,'OUTPUT',Path(tmp)/'run'),patch.object(worker,'ARCHIVE',Path(tmp)/'export.gz'):
                manifest=worker.prepare();payload=worker.export(manifest)
                self.assertEqual((payload['completed'],payload['total']),(0,7))
                task=manifest['entries'][0]
                record={'task':task,'saved_at':'fixture','album':{'id':task['album_id'],'tracks_count':2,'tracks':{'items':[{'id':1},{'id':1}]}}}
                (worker.OUTPUT/'metadata-00.json').write_text(json.dumps(record))
                with self.assertRaises(ValueError):worker.export(manifest)
                self.assertTrue((worker.OUTPUT/'STOP').exists())
