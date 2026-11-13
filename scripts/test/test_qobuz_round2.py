import copy
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_snapshot import load_snapshot
from qobuz_lead_review import reviewed_candidate,fingerprint
from qobuz_round2 import prepare,main

ROOT=Path(__file__).resolve().parents[2]


class RoundTwoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.albums=load_snapshot()['albums']
        import gzip
        for record in json.loads(gzip.decompress((ROOT/'data/qobuz_round2_metadata.json.gz').read_bytes()))['metadata']:
            cls.albums[str(record['album']['id'])]=record['album']
        cls.reviews=json.loads((ROOT/'data/qobuz_round2_reviews.json').read_text())['releases']

    def test_two_cached_leads_require_all_reviewed_sections(self):
        for r in self.reviews:
            row=self.rows[r['discogs_id']];album=self.albums[r['album_id']]
            candidate=reviewed_candidate(row,album,r)
            self.assertEqual((candidate['status'],candidate['confidence']),('probable',.85))
            self.assertEqual(candidate['completeness']['status'],'complete')
            altered=copy.deepcopy(album);altered['tracks']['items'].pop()
            amended=dict(r,album_sha256=fingerprint(altered))
            self.assertIsNone(reviewed_candidate(row,altered,amended))

    def test_section_permissions_are_hash_bound_not_generic_aliases(self):
        for r in self.reviews:
            altered=copy.deepcopy(self.albums[r['album_id']]);altered['tracks']['items'][0]['title']+=' different version'
            with self.assertRaises(ValueError):reviewed_candidate(self.rows[r['discogs_id']],altered,r)
            amended=dict(r,album_sha256=fingerprint(altered))
            with self.assertRaises(ValueError):reviewed_candidate(self.rows[r['discogs_id']],altered,amended)

    def test_fixed_twenty_empty_cases_and_offline_default(self):
        scope,_,manifest=prepare()
        self.assertEqual(len(scope['entries']),20)
        self.assertEqual(len(manifest['entries']),40)
        prior={e['discogs_id'] for e in json.loads((ROOT/'data/qobuz_comparison_scope.json').read_text())['entries']}
        self.assertFalse(prior.intersection(e['discogs_id'] for e in scope['entries']))
        with patch('sys.argv',['worker']),patch('qobuz_round2.runner.search') as call:
            self.assertEqual(main(),0);call.assert_not_called()

    def test_metadata_scope_cannot_expand_silently(self):
        import tempfile
        from qobuz_round2 import metadata
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'data').mkdir()
            (root/'data/qobuz_round2_metadata_scope.json').write_text(json.dumps({'schema_version':1,'entries':[{}, {}, {}]}))
            with patch('qobuz_round2.ROOT',root),patch('qobuz_round2.runner.search') as call:
                with self.assertRaises(ValueError):metadata()
                call.assert_not_called()

    def test_reviewed_title_cleanup_preserves_original_work_credit_scope(self):
        from qobuz_target_credits import requirements
        row=copy.deepcopy(self.rows['3667210'])
        title='Piano Concerto No. 2, Sz.95'
        row['_reviewed_title_sources']={title:'Piano Concerto No.2, Sz83#'}
        effective,required,scope=requirements(row,title,row['performers'])
        self.assertIn('Orchestre De Paris',required)
        self.assertNotIn('London Symphony Orchestra',required)
        self.assertIn('Sviatoslav Richter',required)
        self.assertEqual(scope['positions'],['A1','A2','A3'])
