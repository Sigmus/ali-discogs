import json
import os
import unittest

from ali_discogs.paths import data_dir, repo_root
from ali_discogs.pipeline import run_match
from ali_discogs.spotify import cache_path


class OfflineMatchTest(unittest.TestCase):
    def test_cache_key_matches_checked_in_file(self):
        spotify = os.path.join(repo_root(), "raw", "spotify")
        name = next(n for n in os.listdir(spotify) if n.endswith(".json"))
        with open(os.path.join(spotify, name), encoding="utf-8") as fh:
            query = json.load(fh)["q"]
        self.assertEqual(os.path.basename(cache_path(query)), name)

    def test_offline_rerun_reproduces_committed_results(self):
        rows, summary = run_match(offline=True, write=False)
        with open(os.path.join(data_dir(), "collection_matches.json"), encoding="utf-8") as fh:
            committed = json.load(fh)
        self.assertEqual(len(rows), 741)
        self.assertEqual(summary["spotify"], {"not_found": 210, "found": 254, "probable": 273, "unchecked": 4})
        self.assertEqual(summary["qobuz"], {"unchecked": 741})
        self.assertEqual(rows, committed)


if __name__ == "__main__":
    unittest.main()
