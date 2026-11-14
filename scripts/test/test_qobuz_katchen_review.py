import copy
import gzip
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint


class KatchenReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews={r['discogs_id']:r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.album=next(x['album'] for x in json.loads(gzip.decompress((ROOT/'data/qobuz_remaining_followup_metadata.json.gz').read_bytes()))['metadata'] if str(x['album']['id'])=='0002894552472')

    def test_complete_source_sonatas_and_scherzo_without_compilation_extras(self):
        for rid,counts in [('6264736',[5,1]),('7291398',[4,4])]:
            result,evidence=assess(self.rows[rid],self.album,self.reviews[rid])
            self.assertTrue(result['eligible'])
            self.assertEqual([len(w['track_ids']) for w in result['completeness']['works']],counts)

    def test_wrong_work_metadata_rejected_even_after_album_rehash(self):
        review=self.reviews['6264736'];a=copy.deepcopy(self.album)
        next(t for t in a['tracks']['items'] if t['id']==review['adds'][0]['track_id'])['work']='Piano Sonata Op.2'
        with self.assertRaises(ValueError):assess(self.rows['6264736'],a,{**review,'album_sha256':fingerprint(a)})

    def test_missing_movement_and_wrong_pianist_rejected(self):
        review=self.reviews['7291398'];a=copy.deepcopy(self.album)
        a['tracks']['items']=[t for t in a['tracks']['items'] if t['id']!=review['adds'][1]['track_id']]
        with self.assertRaises(ValueError):assess(self.rows['7291398'],a,{**review,'album_sha256':fingerprint(a)})
        a=copy.deepcopy(self.album)
        for t in a['tracks']['items']: t['performers']=t['performers'].replace('Julius Katchen','Another Pianist')
        self.assertFalse(assess(self.rows['7291398'],a,{**review,'album_sha256':fingerprint(a)})[0]['eligible'])

    def test_number_placement_and_collection_members_are_bounded(self):
        from qobuz_binding_review import allowed
        self.assertTrue(allowed('stated-rhapsody-number','Rhapsody Op.79 No.1','Rhapsody No.1 in B Minor Op.79'))
        self.assertFalse(allowed('stated-rhapsody-number','Rhapsody Op.79 No.1','Rhapsody No.2 in G Minor Op.79'))
        self.assertFalse(allowed('stated-rhapsody-number','Rhapsody Op.79 No.1','Rhapsody No.1 Op.119'))
        self.assertTrue(allowed('brahms-ballade-member','Ballades Op.10','4 Ballades Op.10 No.4'))
        self.assertFalse(allowed('brahms-ballade-member','Ballades Op.10','4 Ballades Op.10 No.5'))
        self.assertFalse(allowed('brahms-ballade-member','Ballades Op.10','Ballade Op.118 No.3'))
        result,evidence=assess(self.rows['6347314'],self.album,self.reviews['6347314'])
        self.assertTrue(result['eligible'])
        self.assertEqual([len(w['track_ids']) for w in result['completeness']['works']],[2,1,1,4])

    def test_volume_one_requires_every_listed_piece_and_discloses_source_key(self):
        review=self.reviews['6265501'];row=self.rows['6265501']
        result,evidence=assess(row,self.album,review)
        self.assertTrue(result['eligible'])
        self.assertEqual([len(w['track_ids']) for w in result['completeness']['works']],[3,4,6])
        a=copy.deepcopy(self.album);a['tracks']['items']=[t for t in a['tracks']['items'] if t['id']!=552025]
        with self.assertRaises(ValueError):assess(row,a,{**review,'album_sha256':fingerprint(a)})
        self.assertTrue(any('Intermezzo In G' in limitation and 'C major' in limitation for limitation in review['limitations']))

    def test_volume_two_joined_band_requires_saved_photo_and_all_fifteen_pieces(self):
        review=self.reviews['8836514'];row=self.rows['8836514']
        result,evidence=assess(row,self.album,review)
        self.assertTrue(result['eligible'])
        self.assertEqual([len(w['track_ids']) for w in result['completeness']['works']],[8,7])
        self.assertEqual(review['source_band_mapping']['B4'],[4,5])
        bad=copy.deepcopy(review);bad['external_source_files'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):assess(row,self.album,bad)
        bad=copy.deepcopy(review);bad['external_source_files'][0]['path']='data/collection_matches.json'
        with self.assertRaises(ValueError):assess(row,self.album,bad)
        a=copy.deepcopy(self.album)
        missing=review['expected']['Fantasias, Op. 116'][4]
        a['tracks']['items']=[t for t in a['tracks']['items'] if t['id']!=missing]
        with self.assertRaises(ValueError):assess(row,a,{**review,'album_sha256':fingerprint(a)})

    def test_joined_band_cannot_drop_a_piece_or_its_photo(self):
        review=copy.deepcopy(self.reviews['8836514']);row=self.rows['8836514']
        review['source_band_mapping']['B4']=[4]
        with self.assertRaises(ValueError):assess(row,self.album,review)
        review=copy.deepcopy(self.reviews['8836514']);review['external_source_files']=[]
        with self.assertRaises(ValueError):assess(row,self.album,review)

    def test_variation_books_and_later_version_markers_are_required(self):
        review=self.reviews['1697514'];row=self.rows['1697514']
        result,evidence=assess(row,self.album,review)
        self.assertTrue(result['eligible'])
        self.assertEqual([len(w['track_ids']) for w in result['completeness']['works']],[1,2])
        for field,value in [('version','1958 Recording'),('isrc','OTHER-RECORDING')]:
            a=copy.deepcopy(self.album)
            next(t for t in a['tracks']['items'] if t['id']==551958)[field]=value
            self.assertFalse(assess(row,a,{**review,'album_sha256':fingerprint(a)})[0]['eligible'])
        a=copy.deepcopy(self.album);a['tracks']['items']=[t for t in a['tracks']['items'] if t['id']!=551964]
        with self.assertRaises(ValueError):assess(row,a,{**review,'album_sha256':fingerprint(a)})
