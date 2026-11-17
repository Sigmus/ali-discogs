import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate

class FocusedFourTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews={r['discogs_id']:r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.albums=load_albums();cls.report=json.loads((ROOT/'data/qobuz_focused4_recording_audit.json').read_text())

    def test_all_four_decisions_and_hold_precedence(self):
        self.assertEqual(validate(self.report,self.rows,self.albums,self.reviews,4),{'reviewed':4,'probable':1,'withhold':3})
        self.assertEqual(sum(len(e['cached_alternative_checks']) for e in self.report['entries']),10)

    def test_two_source_sides_preserve_every_split_track_and_duration(self):
        r=self.reviews['5163525'];result,_=assess(self.rows['5163525'],self.albums[r['album_id']],r)
        self.assertEqual([b['track_ids'] for b in r['bindings']],[[36079973,36079975,36079977,36079979],[36079981,36079983,36079985,36079987]])
        self.assertTrue(result['eligible'])
        self.assertEqual([(w['source_duration_seconds'],w['digital_duration_seconds']) for w in result['completeness']['works']],[(1572,1610),(1288,1274)])
        self.assertFalse(r.get('source_duration_notes'))

    def test_composer_cannot_be_borrowed_from_other_source_side(self):
        r=copy.deepcopy(self.reviews['5163525']);a=copy.deepcopy(self.albums[r['album_id']]);t=a['tracks']['items'][0]
        t['performers']=t['performers'].replace('Franz Liszt, Composer','Franz Schubert, Composer')
        r['album_sha256']=fingerprint(a);r['bindings'][0]['track_sha256'][0]=fingerprint(t);r['selected_track_fingerprints'][str(t['id'])]=fingerprint(t)
        result,_=assess(self.rows['5163525'],a,r)
        self.assertFalse(result['eligible']);self.assertIn('composer',result['blockers'])

    def test_missing_side_or_reused_track_is_rejected(self):
        r=copy.deepcopy(self.reviews['5163525']);r['bindings'].pop()
        with self.assertRaisesRegex(ValueError,'omitted'):assess(self.rows['5163525'],self.albums[r['album_id']],r)
        r=copy.deepcopy(self.reviews['5163525']);r['bindings'][1]['track_ids'][0]=r['bindings'][0]['track_ids'][0]
        with self.assertRaisesRegex(ValueError,'reused'):assess(self.rows['5163525'],self.albums[r['album_id']],r)

    def test_changed_timing_cannot_use_a_global_consensus_waiver(self):
        r=copy.deepcopy(self.reviews['5163525']);a=copy.deepcopy(self.albums[r['album_id']]);t=a['tracks']['items'][0];t['duration']+=100
        r['album_sha256']=fingerprint(a);r['bindings'][0]['track_sha256'][0]=fingerprint(t);r['selected_track_fingerprints'][str(t['id'])]=fingerprint(t)
        result,_=assess(self.rows['5163525'],a,r)
        self.assertFalse(result['eligible']);self.assertIn('source-band-duration',result['blockers'])
