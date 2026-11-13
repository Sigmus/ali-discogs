import copy
import gzip
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_query_trial import strategies, prepare, ROOT
from qobuz_lead_review import reviewed_candidate, fingerprint

class QueryTrialTests(unittest.TestCase):
    def test_ensemble_headline_precedes_supporting_musician(self):
        row = {'artists': ['Antonín Dvořák', 'Prague String Quartet'], 'ensembles': ['Prague String Quartet'], 'key_performers': ['Jan Šírc'], 'composers': ['Antonín Dvořák'], 'tracklist': [{'title': 'Quartet Op.51', 'type': 'index'}]}
        queries = strategies(row)
        self.assertEqual(queries[0]['query'], 'prague string quartet dvorak')
        self.assertEqual(queries[1]['query'], 'prague string quartet dvorak op 51')
        row['composers'].append('Johannes Brahms')
        self.assertEqual(strategies(row), [])

    def test_trial_scope_disjoint_and_offline(self):
        from unittest.mock import patch
        with patch('qobuz_query_trial.runner.search', side_effect=AssertionError('Network forbidden')):
            scope, _, _, manifest = prepare()
        self.assertEqual(len(scope['entries']), 10)
        self.assertEqual(len(manifest['entries']), 20)

    def test_richter_correction_preserves_complete_work_credit_guards(self):
        rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        review = json.loads((ROOT/'data/qobuz_richter_review.json').read_text())['review']
        albums = json.loads(gzip.decompress((ROOT/'data/qobuz_round2_metadata.json.gz').read_bytes()))['metadata']
        album = next(e['album'] for e in albums if e['task']['album_id'] == review['album_id'])
        candidate = reviewed_candidate(rows['3667210'], album, review)
        self.assertEqual(candidate['status'], 'probable')
        self.assertEqual(candidate['completeness']['status'], 'complete')
        altered = copy.deepcopy(album)
        altered['tracks']['items'].pop()
        amended = dict(review, album_sha256=fingerprint(altered))
        self.assertIsNone(reviewed_candidate(rows['3667210'], altered, amended))
