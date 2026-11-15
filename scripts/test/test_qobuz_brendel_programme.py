import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint,reviewed_candidate
from qobuz_brendel_audit import audit
from qobuz_snapshot import load_snapshot

class BrendelProgrammeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='5403356')
        cls.raw=json.loads((ROOT/'raw/discogs/releases/5403356.json').read_text())
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='5403356')
        cls.album=load_snapshot()['albums'][cls.review['album_id']]

    def test_all_sonatas_and_andante_complete_without_source_rewrite(self):
        before=copy.deepcopy(self.row)
        c=reviewed_candidate(self.row,self.album,self.review)
        self.assertEqual((c['status'],c['confidence']),('probable',.85))
        works=c['completeness']['works']
        self.assertEqual(len(works),33)
        ids={i for w in works for i in w['track_ids']}
        self.assertEqual(len(ids),103)
        self.assertIn(3033548,ids)
        source='Sonate Nr. 9 E-dur op. 14,2'
        self.assertIn(source,[t['title'] for t in self.row['tracklist']])
        self.assertEqual(self.review['target_title_corrections'][source],'Piano Sonata No. 9 in E Major, Op. 14 No. 1')
        self.assertEqual(self.row,before)

    def test_rehashed_wrong_sonata_pianist_composer_or_missing_andante_fails(self):
        for change in ['sonata','pianist','composer','andante']:
            a=copy.deepcopy(self.album)
            t=next(t for t in a['tracks']['items'] if t['id']==3033475)
            if change=='sonata':t['title']=t['title'].replace('No. 9 in E Major, Op. 14 No. 1','No. 10 in G Major, Op. 14 No. 2')
            elif change=='pianist':t['performers']=t['performers'].replace('Alfred Brendel','Wilhelm Kempff')
            elif change=='composer':t['performers']=t['performers'].replace('Ludwig van Beethoven','Johannes Brahms')
            else:a['tracks']['items']=[t for t in a['tracks']['items'] if t['id']!=3033548]
            try:result=assess(self.row,a,{**self.review,'album_sha256':fingerprint(a)})[0]
            except ValueError:continue
            self.assertFalse(result['eligible'],change)

    def test_joint_timing_fields_cover_each_position_once_and_keep_small_differences(self):
        d=audit(self.row,self.raw,self.album,self.review)
        self.assertEqual(len(d['timing_groups']),86)
        positions=[p for g in d['timing_groups'] for p in g['positions']]
        self.assertEqual(len(positions),103)
        self.assertEqual(len(set(positions)),103)
        first=next(g for g in d['timing_groups'] if g['positions']==['Q1','Q2'])
        self.assertEqual(first['duration_field_position'],'Q1')
        self.assertEqual(first['source_seconds'],624)
        self.assertTrue(first['image_verified'])
        self.assertEqual(max(abs(g['difference_seconds']) for g in d['timing_groups']),15)
        self.assertEqual(next(g['difference_seconds'] for g in d['timing_groups'] if g['positions']==['U4']),9)
        review=copy.deepcopy(self.review);review['source_timing_groups'][0]['positions'].append('A1')
        with self.assertRaises(ValueError):audit(self.row,self.raw,self.album,review)
