import copy
import gzip
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import reviewed_candidate,fingerprint,ROOT

class TrialRecordingTests(unittest.TestCase):
    def test_klemperer_requires_all_movements_and_overture(self):
        row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='14934969')
        review=json.loads((ROOT/'data/qobuz_trial_recording_reviews.json').read_text())['releases'][0]
        album=next(x['album'] for x in json.loads(gzip.decompress((ROOT/'data/qobuz_query_trial_metadata.json.gz').read_bytes()))['metadata'] if x['task']['discogs_id']=='14934969')
        self.assertEqual(reviewed_candidate(row,album,review)['status'],'probable')
        for i in range(6):
            altered=copy.deepcopy(album);altered['tracks']['items'].pop(i)
            amended=dict(review,album_sha256=fingerprint(altered))
            self.assertIsNone(reviewed_candidate(row,altered,amended))
        altered=copy.deepcopy(album);altered['tracks']['items'][-1]['title']='Leonore Overture No. 2, Op.72'
        amended=dict(review,album_sha256=fingerprint(altered))
        self.assertIsNone(reviewed_candidate(row,altered,amended))
