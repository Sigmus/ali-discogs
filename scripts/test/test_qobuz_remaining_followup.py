import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import qobuz_remaining_followup as worker

class RemainingFollowupTests(unittest.TestCase):
    def test_prepare_is_offline_and_manifest_changes_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(worker,'OUTPUT',Path(temp)), patch.object(worker.runner,'search',side_effect=AssertionError('API forbidden')):
            scope=json.loads(worker.SCOPE.read_text());scope['screen_sha256']=worker.digest(worker.ROOT/'data/qobuz_remaining_screen.json')
            scope_path=Path(temp)/'scope.json';scope_path.write_text(json.dumps(scope))
            with patch.object(worker,'SCOPE',scope_path):
                one=worker.prepare();two=worker.prepare()
            self.assertEqual(one,two)
            self.assertEqual(len(one['entries']),9)
            path=Path(temp)/'manifest.json';changed=copy.deepcopy(one);changed['entries'][0]['album_id']='different';path.write_text(json.dumps(changed))
            with patch.object(worker,'SCOPE',scope_path), self.assertRaises(ValueError):worker.prepare()

    def test_export_preserves_partial_evidence_but_rejects_duplicate_tracks(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(worker,'OUTPUT',Path(temp)), patch.object(worker,'ARCHIVE',Path(temp)/'portable.json.gz'):
            task={'discogs_id':'3167056','album_id':'0002894133212'}
            album={'id':task['album_id'],'title':'test','tracks_count':2,'tracks':{'items':[{'id':1,'title':'one'},{'id':2,'title':'two'}]}}
            record={'task':task,'saved_at':'2026-11-14','album':album};path=Path(temp)/'metadata-00.json';path.write_text(json.dumps(record))
            result=worker.export({'entries':[task]});self.assertEqual(result['completed'],1);self.assertEqual(result['total'],9)
            record['album']['tracks']['items'][1]['id']=1;path.write_text(json.dumps(record))
            with self.assertRaises(ValueError):worker.export({'entries':[task]})
            self.assertTrue((Path(temp)/'STOP').exists())
