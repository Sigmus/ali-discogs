import copy
import gzip
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_match import ROOT
from qobuz_lead_review import assess,fingerprint

class FollowupReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews={r['discogs_id']:r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.albums={str(x['album']['id']):x['album'] for x in json.loads(gzip.decompress((ROOT/'data/qobuz_remaining_followup_metadata.json.gz').read_bytes()))['metadata']}

    def test_lipatti_has_every_waltz_and_excludes_three_bonus_pieces(self):
        review=self.reviews['7194998'];album=self.albums[review['album_id']]
        result,evidence=assess(self.rows['7194998'],album,review)
        self.assertTrue(result['eligible']);self.assertEqual(evidence['covered'],14)
        self.assertEqual([i for w in result['completeness']['works'] for i in w['track_ids']],[t['id'] for t in album['tracks']['items'][:14]])
        self.assertEqual(review['extra_track_ids'],[t['id'] for t in album['tracks']['items'][14:]])
        altered=copy.deepcopy(album);altered['tracks']['items'].pop(3)
        with self.assertRaises(ValueError):assess(self.rows['7194998'],altered,{**review,'album_sha256':fingerprint(altered)})

    def test_lipatti_does_not_accept_wrong_pianist(self):
        review=self.reviews['7194998'];album=copy.deepcopy(self.albums[review['album_id']])
        for t in album['tracks']['items']:t['performers']=t['performers'].replace('Dinu Lipatti','Another Pianist')
        changed={**review,'album_sha256':fingerprint(album)}
        with self.assertRaises(ValueError):assess(self.rows['7194998'],album,changed)

    def test_kreisler_requires_all_movements_and_the_right_orchestra(self):
        review=self.reviews['10175959'];album=self.albums[review['album_id']];row=self.rows['10175959']
        self.assertTrue(assess(row,album,review)[0]['eligible'])
        altered=copy.deepcopy(album);altered['tracks']['items'].pop(1)
        self.assertFalse(assess(row,altered,{**review,'album_sha256':fingerprint(altered)})[0]['eligible'])
        altered=copy.deepcopy(album)
        for t in altered['tracks']['items']:t['performers']=t['performers'].replace('London Philharmonic Orchestra','Berlin State Opera Orchestra')
        self.assertFalse(assess(row,altered,{**review,'album_sha256':fingerprint(altered)})[0]['eligible'])
