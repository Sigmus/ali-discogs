import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate
from qobuz_match import recording_review_album

class MusicianEighteenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews={r['discogs_id']:r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.albums=load_albums()
        cls.report=json.loads((ROOT/'data/qobuz_musician18_recording_audit.json').read_text())

    def test_complete_scope_and_no_future_score_bypass(self):
        self.assertEqual(validate(self.report,self.rows,self.albums,self.reviews,18),{'reviewed':18,'withhold':18})
        triage=json.loads((ROOT/'data/qobuz_musician21_audit.json').read_text())
        expected=set(triage['frozen_release_ids'])-{'11876845','21490438','8535848'}
        self.assertEqual(set(self.report['frozen_release_ids']),expected)
        self.assertEqual(sum(len(e['cached_alternative_checks']) for e in self.report['entries']),37)
        self.assertTrue(all(c['copy_only_work_context_evidence']['status']=='unchecked' for e in self.report['entries'] for c in e['candidate_rechecks']))

    def test_changed_alternative_is_not_silently_ignored(self):
        albums=dict(self.albums);aid='pt8g5qypj4bxa';albums[aid]=copy.deepcopy(albums[aid])
        albums[aid]['tracks']['items'][0]['performers']='Different orchestra, Orchestra'
        with self.assertRaisesRegex(ValueError,'alternative changed'):
            validate(self.report,self.rows,albums,self.reviews,18)

    def test_dropped_release_cannot_report_complete(self):
        report=copy.deepcopy(self.report);report['entries'].pop()
        with self.assertRaisesRegex(ValueError,'scope changed'):
            validate(report,self.rows,self.albums,self.reviews,18)


class RecordingReviewCacheTests(unittest.TestCase):
    def test_original_snapshot_is_available_without_expanding_candidates(self):
        a={'id':'old','tracks_count':1,'tracks':{'items':[{'id':1}]}}
        self.assertIs(recording_review_album('old',{}, {'old':a}),a)
        self.assertIs(recording_review_album('old',{'old':a}, {'old':a}),a)

    def test_conflicting_or_absent_caches_fail_closed(self):
        a={'id':'old','tracks_count':1,'tracks':{'items':[{'id':1}]}}
        b=copy.deepcopy(a);b['title']='conflict'
        with self.assertRaisesRegex(ValueError,'Conflicting'):
            recording_review_album('old',{'old':b},{'old':a})
        with self.assertRaisesRegex(ValueError,'missing'):
            recording_review_album('old',{}, {})

    def test_partial_duplicate_or_mismatched_metadata_rejected(self):
        for a in [{'id':'old','tracks_count':2,'tracks':{'items':[{'id':1}]}},
                  {'id':'old','tracks_count':2,'tracks':{'items':[{'id':1},{'id':1}]}},
                  {'id':'wrong','tracks_count':1,'tracks':{'items':[{'id':1}]}}]:
            with self.assertRaisesRegex(ValueError,'mismatched'):
                recording_review_album('old',{}, {'old':a})
