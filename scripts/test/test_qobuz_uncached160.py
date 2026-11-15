import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_uncached160 import SCOPE, validate_record


class UncachedMetadataScopeTests(unittest.TestCase):
    def test_scope_is_deduplicated_and_covers_all160(self):
        scope = json.loads(SCOPE.read_text())
        self.assertEqual(len(scope['release_ids']), 160)
        self.assertEqual(len(scope['entries']), 936)
        self.assertEqual(len({e['album_id'] for e in scope['entries']}), 936)
        self.assertEqual({r for e in scope['entries'] for r in e['discogs_ids']}, set(scope['release_ids']))

    def test_mismatched_incomplete_or_duplicate_track_checkpoints_fail(self):
        task = {'discogs_id': '1', 'album_id': 'abc'}
        record = {'task': task, 'album': {'id': 'abc', 'tracks_count': 2,
                  'tracks': {'items': [{'id': 1}, {'id': 2}]}}}
        self.assertEqual(validate_record(record, task)['id'], 'abc')
        for mutate in [lambda r: r['album'].update(id='wrong'),
                       lambda r: r['album'].update(tracks_count=3),
                       lambda r: r['album']['tracks']['items'][1].update(id=1),
                       lambda r: r.update(task={'discogs_id': '2', 'album_id': 'abc'})]:
            broken = copy.deepcopy(record)
            mutate(broken)
            with self.assertRaises(ValueError):
                validate_record(broken, task)
