import copy
import gzip
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,target_fingerprint
from qobuz_match import evaluate,evaluate_v1
from qobuz_source_composer import validate_scope
from qobuz_work_groups import target_work_matches


class SourceComposerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='15221307')
        cls.album=json.loads(gzip.decompress((ROOT/'data/qobuz_evidence.json.gz').read_bytes()))['albums']['0002894776360']
        cls.review=json.loads((ROOT/'data/qobuz_source_composer_reviews.json').read_text())['releases'][0]
        cls.raw=(ROOT/'raw/discogs/releases/15221307.json').read_bytes()

    def test_medtners_opus_is_not_a_beethoven_work_even_with_empty_album_composers(self):
        self.assertEqual(self.row['composers'],[])
        self.assertEqual(evaluate_v1(self.row,self.album)['coverage'],1)
        result=evaluate(self.row,self.album)
        self.assertEqual(result['coverage'],.8)
        self.assertEqual(result['programme'][-1]['track_ids'],[])
        self.assertEqual(result['status'],'unchecked')
        self.assertEqual(evaluate_v1(self.row,self.album)['coverage'],1)  # legacy remains independent

    def test_scope_cannot_drop_or_reassign_a_source_attribution(self):
        self.assertEqual(len(validate_scope(self.row,self.raw,self.review)),5)
        for field,value in [('source_sha256','0'*64),('targets',self.review['targets'][:-1])]:
            with self.assertRaises(ValueError):validate_scope(self.row,self.raw,{**self.review,field:value})
        bad=copy.deepcopy(self.review);bad['targets'][-1]['composer']='Ludwig van Beethoven'
        with self.assertRaises(ValueError):validate_scope(self.row,self.raw,bad)
        from qobuz_source_composer import required_composer
        with self.assertRaises(ValueError):required_composer(self.row,'Unreviewed target')
        changed=copy.deepcopy(self.row);changed['title']='Changed release'
        with self.assertRaises(ValueError):validate_scope(changed,self.raw,self.review)

    def test_positive_candidate_composer_required_only_for_reviewed_scope(self):
        title=self.row['tracklist'][-1]['title']
        track={'title':'Piano Sonata in G Minor, Op.22','performers':'Emil Gilels, MainArtist - Nikolai Medtner, Composer'}
        self.assertTrue(target_work_matches(self.row,title,track))
        track['performers']='Emil Gilels, MainArtist - Ludwig van Beethoven, Composer'
        self.assertFalse(target_work_matches(self.row,title,track))
        track['performers']='Emil Gilels, MainArtist'
        self.assertFalse(target_work_matches(self.row,title,track))
        row={**self.row,'discogs_id':0}
        self.assertTrue(target_work_matches(row,title,track))  # no inferred global composer policy
