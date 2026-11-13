import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import load_reviews, reviewed_candidate, fingerprint, ROOT

class SchnabelLateReviewTests(unittest.TestCase):
    def test_complete_late_sonatas_and_missing_join_fail_closed(self):
        row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='2966855')
        review=json.loads((ROOT/'data/qobuz_schnabel_late_review.json').read_text())['review']
        _,albums=load_reviews();album=albums[review['album_id']]
        candidate=reviewed_candidate(row,album,review)
        self.assertEqual(candidate['status'],'probable')
        self.assertEqual(len(candidate['completeness']['works']),5)
        for tid in [36924128,36924140,36924142]:
            altered=copy.deepcopy(album)
            altered['tracks']['items']=[t for t in altered['tracks']['items'] if t['id']!=tid]
            amended=dict(review,album_sha256=fingerprint(altered))
            self.assertIsNone(reviewed_candidate(row,altered,amended))
        altered=copy.deepcopy(album)
        next(t for t in altered['tracks']['items'] if t['id']==36924128)['title']='Unrelated track'
        amended=dict(review,album_sha256=fingerprint(altered))
        self.assertIsNone(reviewed_candidate(row,altered,amended))
