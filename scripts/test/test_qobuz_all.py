from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_all_poc import manifest, Pace, StopRequested


class FullSearchTests(unittest.TestCase):
    def test_duplicate_copies_share_one_query(self):
        row = {'discogs_id': 123, 'title': 'Symphony No. 3',
               'composers': ['Ludwig van Beethoven'], 'key_performers': ['Erich Kleiber']}
        plan = manifest([row, dict(row)])
        self.assertEqual(len(plan), 1)
        self.assertEqual(plan[0]['copies'], 2)
        self.assertEqual(plan[0]['query'], 'erich kleiber beethoven symphony no 3')

    def test_requests_are_spaced(self):
        pace = Pace(15, Path('/tmp/nonexistent-qobuz-unit-test-stop'))
        with patch('qobuz_all_poc.time.monotonic', side_effect=[100, 105, 115]), patch.object(pace, 'wait') as wait:
            pace()
            pace()
        wait.assert_called_once_with(10)
        self.assertEqual(pace.requests, 2)

    def test_stop_marker_prevents_request(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / 'STOP'
            marker.touch()
            pace = Pace(15, marker)
            with self.assertRaises(StopRequested):
                pace()
            self.assertEqual(pace.requests, 0)
