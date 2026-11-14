import copy
import gzip
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint


class SchnabelSideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='4352998')
        cls.album=next(x['album'] for x in json.loads(gzip.decompress((ROOT/'data/qobuz_comparison_evidence.json.gz').read_bytes()))['metadata'] if str(x['album']['id'])=='0190295866983')
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='4352998')

    def test_side_split_does_not_duplicate_a_sonata(self):
        result,evidence=assess(self.row,self.album,self.review)
        self.assertTrue(result['eligible'])
        works=result['completeness']['works']
        split=[w for w in works if 'Op. 54' in w['target']]
        self.assertEqual([w['track_ids'] for w in split],[[36924113],[36924114]])
        used=[i for w in works for i in w['track_ids']]
        self.assertEqual(len(used),26);self.assertEqual(len(set(used)),26)

    def test_missing_conclusion_rejected(self):
        a=copy.deepcopy(self.album);a['tracks']['items']=[t for t in a['tracks']['items'] if t['id']!=36924114]
        with self.assertRaises(ValueError):assess(self.row,a,{**self.review,'album_sha256':fingerprint(a)})

    def test_side_movement_order_and_pianist_required(self):
        a=copy.deepcopy(self.album)
        for t in a['tracks']['items']:
            if t['id']==36924114:t['title']=t['title'].replace('II.','I.')
        r=copy.deepcopy(self.review);r['album_sha256']=fingerprint(a)
        # Even after rebinding exact title guards, movement II remains required.
        altered=next(t for t in a['tracks']['items'] if t['id']==36924114)['title']
        for entry in r['exclusions']+r['marks']:
            if entry['track_id']==36924114:
                if 'title_contains' in entry:entry['title_contains']=altered
                if 'text' in entry:entry['text']=altered
        self.assertFalse(assess(self.row,a,r)[0]['eligible'])
        a=copy.deepcopy(self.album)
        for t in a['tracks']['items']:t['performers']=t['performers'].replace('Artur Schnabel','Another Pianist')
        with self.assertRaises(ValueError):assess(self.row,a,{**self.review,'album_sha256':fingerprint(a)})
