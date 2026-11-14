import json,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_remaining_retrieval import prepare,SCOPE,BASE

class RemainingRetrievalTests(unittest.TestCase):
    def test_fixed_scope_is_offline_and_resume_manifests_are_stable(self):
        before=SCOPE.read_bytes()
        with patch('qobuz_remaining_retrieval.runner.search',side_effect=AssertionError('API forbidden')):
            scope=prepare();prepare()
        self.assertEqual(SCOPE.read_bytes(),before)
        self.assertEqual(len(scope['metadata_release_ids']),12)
        self.assertEqual(len(set(scope['empty_release_ids'])),305)
        self.assertEqual(len(scope['metadata']),83)
        self.assertEqual(len({e['album_id'] for e in scope['metadata']}),83)
        self.assertEqual(len(scope['search']),603)
        self.assertEqual({e['discogs_id'] for e in scope['search']},set(scope['empty_release_ids']))
        for phase in ['metadata','search']:
            manifest=json.loads((BASE/phase/'manifest.json').read_text())
            self.assertEqual(len(manifest['entries']),len(scope[phase]))
