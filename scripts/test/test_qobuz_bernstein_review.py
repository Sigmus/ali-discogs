import copy
import gzip
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint,reviewed_candidate

class BernsteinReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='3956949')
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='3956949')
        cls.album=next(r['album'] for r in json.loads(gzip.decompress((ROOT/'data/qobuz_metadata_followup_2026_11_15.json.gz').read_bytes()))['metadata'] if r['album']['id']==cls.review['album_id'])

    def test_both_complete_live_symphonies_probable_only(self):
        c=reviewed_candidate(self.row,self.album,self.review)
        self.assertEqual((c['status'],c['confidence']),('probable',.85))
        self.assertEqual([w['track_ids'] for w in c['completeness']['works']],[list(range(46290798,46290802)),list(range(46290802,46290806))])

    def test_changed_recording_or_incomplete_programme_rejected_even_if_rehashed(self):
        for change in ['orchestra','conductor','live','isrc','timing','missing']:
            a=copy.deepcopy(self.album)
            if change=='missing':a['tracks']['items'].pop()
            elif change in ['orchestra','conductor']:
                for t in a['tracks']['items']:
                    t['performers']=t['performers'].replace('Israel Philharmonic Orchestra','New York Philharmonic') if change=='orchestra' else t['performers'].replace('Leonard Bernstein','Another Conductor')
            elif change=='live':a['tracks']['items'][0]['version']='Studio'
            elif change=='isrc':a['tracks']['items'][0]['isrc']='OTHER'
            else:a['tracks']['items'][0]['duration']+=90
            try:result=assess(self.row,a,{**self.review,'album_sha256':fingerprint(a)})[0]
            except ValueError:continue
            self.assertFalse(result['eligible'],change)
