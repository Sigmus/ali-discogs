import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint
from qobuz_match import catalogue,evaluate
from qobuz_credit_role_audit import load_albums
from qobuz_catalogue40_audit import notation_copy,related,clues
from qobuz_fullsupport16_audit import validate

class CatalogueFortyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews={r['discogs_id']:r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.albums=load_albums();cls.report=json.loads((ROOT/'data/qobuz_catalogue40_recording_audit.json').read_text())

    def test_all_forty_decisions_and_future_hold_precedence(self):
        self.assertEqual(validate(self.report,self.rows,self.albums,self.reviews,40),{'reviewed':40,'withhold':38,'probable':2})
        self.assertEqual(sum(len(e['cached_alternative_checks']) for e in self.report['entries']),82)
        self.assertEqual(set(self.report['accepted_release_ids']),{'2383222','28448206'})

    def test_parent_clue_never_equates_different_members(self):
        self.assertTrue(related({('op','10','')},{('op','10','3')}))
        self.assertFalse(related({('op','10','1')},{('op','10','2')}))
        self.assertFalse(related({('op','10','')},{('op','25','1')}))
        self.assertFalse(related({('l','104','')},{('k','159','')}))

    def test_copy_notation_preserves_numeric_lists(self):
        self.assertEqual(catalogue(notation_copy('Hob. XXII:14, "Harmoniemesse"')),{('hob','22','14')})
        self.assertIn('XXII:14, 15',notation_copy('Hob. XXII:14, 15'))
        self.assertIn('XXII:14-16',notation_copy('Hob. XXII:14-16'))
        self.assertEqual(catalogue(notation_copy('BWV 1.066')),{('bwv','1066','')})

    def test_parent_number_cannot_supply_another_composer_or_missing_player(self):
        row={'composers':['Frédéric Chopin']}
        a={'tracks':{'items':[{'id':1,'title':'Etude Op.10 No.1','performers':'Nikolai Medtner, Composer - Other Person, Piano'}]}}
        result=clues(row,a,[{'target':'Etudes Opus 10','required_performers':['François-René Duchâble']}])
        self.assertFalse(result[0]['tracks'][0]['composer_positive'])
        self.assertEqual(result[0]['tracks'][0]['missing_required_musicians'],['François-René Duchâble'])

    def test_opus_sets_remain_all_twenty_four_source_leaves(self):
        r=self.reviews['2383222'];a=self.albums[r['album_id']]
        self.assertEqual([catalogue(t['title']) for t in a['tracks']['items']],[{('op',op,str(i))} for op in ['10','25'] for i in range(1,13)])
        self.assertEqual(len(r['bindings']),24)
        r=copy.deepcopy(r);r['bindings'].pop()
        with self.assertRaisesRegex(ValueError,'omitted'):assess(self.rows['2383222'],a,r)
        self.assertEqual(evaluate(self.rows['2383222'],a)['status'],'unchecked')

    def test_accepted_cases_cannot_lose_positive_credits_even_after_rebinding(self):
        for rid in ['2383222','28448206']:
            r=copy.deepcopy(self.reviews[rid]);a=copy.deepcopy(self.albums[r['album_id']]);t=a['tracks']['items'][0]
            t['performers']='Hector Berlioz, Composer' if rid=='28448206' else 'Frederic Chopin, Composer'
            r['album_sha256']=fingerprint(a);r['bindings'][0]['track_sha256']=[fingerprint(t)];r['selected_track_fingerprints'][str(t['id'])]=fingerprint(t)
            result,_=assess(self.rows[rid],a,r)
            self.assertFalse(result['eligible']);self.assertIn('performer',result['blockers'])

    def test_ozawa_source_discrepancy_and_timing_guard_remain(self):
        r=copy.deepcopy(self.reviews['28448206']);a=copy.deepcopy(self.albums[r['album_id']])
        self.assertEqual(r['source_leaves'][0]['source_work'],'Symphonie Fantastique Op. 24')
        self.assertEqual(len(r['bindings']),5)
        a['tracks']['items'][0]['duration']+=100;t=a['tracks']['items'][0]
        r['album_sha256']=fingerprint(a);r['bindings'][0]['track_sha256']=[fingerprint(t)];r['selected_track_fingerprints'][str(t['id'])]=fingerprint(t)
        result,_=assess(self.rows['28448206'],a,r)
        self.assertFalse(result['eligible']);self.assertIn('source-band-duration',result['blockers'])
