import copy,gzip,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,reviewed_candidate,fingerprint

class KarajanGroupingTests(unittest.TestCase):
    def test_grouping_is_complete_and_cannot_drop_source_or_candidate_sections(self):
        row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='10738828')
        review=json.loads((ROOT/'data/qobuz_unmatched_recording_reviews.json').read_text())['releases'][0]
        album=next(x['album'] for x in json.loads(gzip.decompress((ROOT/'data/qobuz_unmatched_metadata.json.gz').read_bytes()))['metadata'] if x['task']['discogs_id']=='10738828')
        candidate=reviewed_candidate(row,album,review)
        self.assertEqual(candidate['status'],'probable')
        self.assertEqual(len(candidate['completeness']['works']),2)
        altered=copy.deepcopy(review);altered['target_unit_groups'][1]['source_titles'].pop()
        with self.assertRaises(ValueError):reviewed_candidate(row,album,altered)
        for i in range(9):
            modified=copy.deepcopy(album);modified['tracks']['items'].pop(i)
            amended=dict(review,album_sha256=fingerprint(modified))
            self.assertIsNone(reviewed_candidate(row,modified,amended))
