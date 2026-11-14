import copy
import gzip
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_match import ROOT,evaluate
from qobuz_lead_review import assess,fingerprint
from qobuz_completeness import check_programme,inventory_work

class RemainingReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if r['discogs_id']==4491358)
        cls.review=json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'][0]
        records=json.loads(gzip.decompress((ROOT/'data/qobuz_remaining_metadata.json.gz').read_bytes()))['metadata']
        cls.album=next(x['album'] for x in records if x['album']['id']==cls.review['album_id'])
        cls.inventory=json.loads((ROOT/'data/qobuz_work_inventory.json').read_text())

    def test_review_requires_complete_programme_and_bound_source(self):
        result,_=assess(self.row,self.album,self.review)
        self.assertTrue(result['eligible'])
        album=copy.deepcopy(self.album);album['tracks']['items'].pop();album['tracks_count']-=1
        with self.assertRaises(ValueError):assess(self.row,album,self.review)
        review={**self.review,'album_sha256':fingerprint(album)}
        self.assertFalse(assess(self.row,album,review)[0]['eligible'])

    def test_wrong_or_missing_recording_credit_is_withheld(self):
        album=copy.deepcopy(self.album)
        for t in album['tracks']['items']:t['performers']=t['performers'].replace('Wiener Symphoniker','London Symphony Orchestra')
        review={**self.review,'album_sha256':fingerprint(album)}
        self.assertFalse(assess(self.row,album,review)[0]['eligible'])

    def test_inventory_keeps_opus_subnumbers_distinct(self):
        row={'composers':['Ludwig van Beethoven']}
        first=inventory_work(row,'Sonata Op.49 No.1',self.inventory)
        second=inventory_work(row,'Sonata Op.49 No.2',self.inventory)
        self.assertNotEqual(first['catalogue'],second['catalogue'])
        self.assertIsNone(inventory_work(row,'Sonata Op.49 No.3',self.inventory))
        self.assertIsNone(inventory_work(row,'Sonata Op.81',self.inventory))
        self.assertEqual(inventory_work(row,'Sonata Op.81a',self.inventory)['movements'],[1,2,3])

    def test_klemperer_reviews_remain_complete_and_ambiguous_versions_unreviewed(self):
        from qobuz_snapshot import load_snapshot
        rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        reviews=json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']
        album=load_snapshot()['albums']['vrg5q0y8vzvaa']
        self.assertFalse({'24964822','26149643'} & {r['discogs_id'] for r in reviews})
        for review in reviews:
            if review['album_id'] != album['id']:continue
            self.assertTrue(assess(rows[review['discogs_id']],album,review)[0]['eligible'])
            altered=copy.deepcopy(album)
            used=assess(rows[review['discogs_id']],album,review)[0]['completeness']['works'][0]['track_ids'][0]
            altered['tracks']['items']=[t for t in altered['tracks']['items'] if t['id']!=used]
            changed={**review,'album_sha256':fingerprint(altered)}
            self.assertFalse(assess(rows[review['discogs_id']],altered,changed)[0]['eligible'])
