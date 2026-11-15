import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,reviewed_candidate
from qobuz_snapshot import load_snapshot
from qobuz_match import agrees,credits

class PhotographerWithholdTests(unittest.TestCase):
    def test_five_gap_reviews_never_promote_from_album_or_ensemble_credit(self):
        rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        reviews={r['discogs_id']:r for r in json.loads((ROOT/'data/qobuz_binding_reviews.json').read_text())['releases']};albums=load_snapshot()['albums']
        for rid in ['14398300','13708175','1638548','29719858','5987607']:
            review=reviews[rid];self.assertIsNone(reviewed_candidate(rows[rid],albums[review['album_id']],review))
        album=albums['0002894637382']
        self.assertTrue(any('Kubelik' in a['name'] for a in album['artists']))
        self.assertTrue(all(not agrees('Rafael Kubelik',credits(t)) for t in album['tracks']['items']))
        prok=next(t for t in albums['0002894805871']['tracks']['items'] if 'Prokofiev' in t['title'])
        self.assertTrue(agrees('Boston Symphony Orchestra',credits(prok)))
        self.assertFalse(agrees('San Francisco Symphony',credits(prok)))
