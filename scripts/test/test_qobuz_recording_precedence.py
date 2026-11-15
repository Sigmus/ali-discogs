import copy
import gzip
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,apply_recording_review
from qobuz_snapshot import load_snapshot

class RecordingPrecedenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews={r['discogs_id']:r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.albums=load_snapshot()['albums']
        cls.albums.update({r['album']['id']:r['album'] for r in json.loads(gzip.decompress((ROOT/'data/qobuz_comparison_evidence.json.gz').read_bytes()))['metadata']})

    def test_hold_or_rejection_overrides_even_a_found_candidate_without_mutation(self):
        for rid in ['7864758','9769609','9866788','9866861','9876728']:
            review=self.reviews[rid];album=self.albums[review['album_id']]
            source=[{'id':review['album_id'],'status':'found','confidence':.99,'coverage':1,'reasons':['Synthetic complete scorer support']},{'id':'other-recording','status':'probable','confidence':.85}]
            before=copy.deepcopy(source);result=apply_recording_review(self.rows[rid],album,review,source)
            self.assertEqual(source,before)
            self.assertEqual((result[0]['status'],result[0]['confidence']),('unchecked',None))
            self.assertEqual(result[0]['recording_review_decision'],review['decision'])
            self.assertEqual(result[1],source[1])

    def test_positive_review_replaces_instead_of_duplicating_scored_candidate(self):
        rid='14766559';r=self.reviews[rid]
        result=apply_recording_review(self.rows[rid],self.albums[r['album_id']],r,[{'id':r['album_id'],'status':'unchecked','confidence':None}])
        self.assertEqual(len(result),1)
        self.assertEqual((result[0]['status'],result[0]['confidence']),('probable',.85))

    def test_rejected_recording_still_requires_current_source_proof(self):
        rid='7864758';r=copy.deepcopy(self.reviews[rid]);r['source_sha256']='stale'
        with self.assertRaises(ValueError):apply_recording_review(self.rows[rid],self.albums[r['album_id']],r,[])
    def test_casals_programme_support_cannot_override_transfer_provenance_hold(self):
        rid='5838140'
        review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']==rid)
        album=next(r['album'] for r in json.loads(gzip.decompress((ROOT/'data/qobuz_metadata_followup_2026_11_15.json.gz').read_bytes()))['metadata'] if r['album']['id']==review['album_id'])
        result=apply_recording_review(self.rows[rid],album,review,[{'id':album['id'],'status':'found','confidence':.99,'coverage':1}])
        self.assertEqual((result[0]['status'],result[0]['confidence']),('unchecked',None))
