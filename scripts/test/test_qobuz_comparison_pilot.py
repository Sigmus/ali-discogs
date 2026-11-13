import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch, Mock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import qobuz_comparison_pilot as pilot
from qobuz_catalog import CatalogError


class ComparisonPilotTests(unittest.TestCase):
    def test_stop_marker_blocks_any_connection(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(pilot,'OUTPUT',Path(tmp)), patch.object(pilot,'Catalog') as catalog:
            (Path(tmp)/'STOP').touch()
            self.assertEqual(pilot.search({'entries':[]}),1)
            catalog.assert_not_called()

    def test_first_api_warning_stops_without_retry_and_preserves_saved_searches(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(pilot,'OUTPUT',Path(tmp)), patch.object(pilot,'Catalog') as factory:
            client=Mock();factory.return_value=client
            client.fetch.side_effect=CatalogError('catalog/search: HTTP 429; no matches classified.')
            self.assertEqual(pilot.search({'entries':[{'discogs_id':'1','query':'one'},{'discogs_id':'2','query':'two'}]}),1)
            self.assertEqual(client.fetch.call_count,1)
            self.assertTrue((Path(tmp)/'STOP').exists())
            state=json.loads((Path(tmp)/'progress.json').read_text())
            self.assertEqual(state['status'],'failed');self.assertEqual(state['completed'],0)
            self.assertFalse((Path(tmp)/'search-00.json').exists())

    def test_saved_search_is_reused_without_network(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(pilot,'OUTPUT',Path(tmp)), patch.object(pilot,'Catalog') as factory:
            task={'discogs_id':'1','query':'one'}
            (Path(tmp)/'search-00.json').write_text(json.dumps({'task':task,'search':{'albums':{'items':[]}}}))
            self.assertEqual(pilot.search({'entries':[task]}),0)
            factory.return_value.fetch.assert_not_called()
            self.assertEqual(json.loads((Path(tmp)/'progress.json').read_text())['status'],'complete')

    def test_portable_export_is_whitelisted_and_rejects_mismatched_album(self):
        import gzip
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'data').mkdir();out=root/'local';out.mkdir()
            scope=root/'data/qobuz_comparison_scope.json';scope.write_text('{}')
            task={'discogs_id':'1','album_id':'abc'}
            (root/'data/qobuz_comparison_metadata_scope.json').write_text(json.dumps({'entries':[task]}))
            (out/'search-00.json').write_text(json.dumps({'task':{'query':'one'},'saved_at':'test','search':{'albums':{'items':[]}}}))
            album={'id':'abc','title':'Example','tracks_count':1,'account_token':'SENSITIVE',
                   'tracks':{'items':[{'id':1,'title':'Example','file_url':'SENSITIVE'}]}}
            p=out/'metadata-00.json';p.write_text(json.dumps({'task':task,'saved_at':'test','album':album}))
            with patch.object(pilot,'ROOT',root),patch.object(pilot,'OUTPUT',out),patch.object(pilot,'SCOPE',scope):
                manifest={'entries':[{'query':'one'}]};pilot.export_evidence(manifest)
                with gzip.open(root/'data/qobuz_comparison_evidence.json.gz','rt') as f:text=f.read()
                self.assertNotIn('SENSITIVE',text)
                album['id']='different';p.write_text(json.dumps({'task':task,'saved_at':'test','album':album}))
                with self.assertRaises(ValueError):pilot.export_evidence(manifest)
