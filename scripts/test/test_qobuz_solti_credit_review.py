import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint,reviewed_candidate
from qobuz_snapshot import load_snapshot

class SoltiCreditReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='5972183')
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='5972183')
        cls.album=load_snapshot()['albums'][cls.review['album_id']]

    def test_minton_required_only_on_songs_and_liner_author_never_required(self):
        c=reviewed_candidate(self.row,self.album,self.review)
        self.assertEqual((c['status'],c['confidence']),('probable',.85))
        self.assertEqual([len(w['track_ids']) for w in c['completeness']['works']],[4,4])
        self.assertNotIn('Roger Dettmer',c['required_performers'])
        self.assertNotIn('Yvonne Minton',c['programme'][0]['required_performers'])
        self.assertIn('Yvonne Minton',c['programme'][1]['required_performers'])

    def test_missing_singer_or_orchestra_and_wrong_composer_cannot_pass_after_rehash(self):
        for change in ['singer','orchestra','composer','missing']:
            a=copy.deepcopy(self.album)
            if change=='missing':a['tracks']['items'].pop()
            else:
                for t in a['tracks']['items']:
                    if change=='singer':t['performers']=t['performers'].replace('Yvonne Minton','Another Singer')
                    elif change=='orchestra':t['performers']=t['performers'].replace('Chicago Symphony Orchestra','London Symphony Orchestra')
                    else:t['performers']=t['performers'].replace('Gustav Mahler','Another Composer')
            try:result=assess(self.row,a,{**self.review,'album_sha256':fingerprint(a)})[0]
            except ValueError:continue
            self.assertFalse(result['eligible'],change)

    def test_source_scope_or_credit_omission_requires_review(self):
        for change in ['scope','principal','omission']:
            r=copy.deepcopy(self.review);spec=r['source_credit_reconciliation']
            if change=='scope':spec['work_scopes'][0]['targets']=[next(iter(r['expected']))]
            elif change=='principal':spec['nonperformers'][0]={'name':'Georg Solti','role':'Conductor'}
            else:spec['expected_required_performers'][spec['work_scopes'][0]['targets'][0]].remove('Yvonne Minton')
            with self.assertRaises(ValueError):assess(self.row,self.album,r)
    def test_fifth_stays_withheld_when_orchestra_is_present_but_named_soloists_are_not(self):
        from qobuz_match import credits,agrees
        row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='3386012')
        review=next(r for r in json.loads((ROOT/'data/qobuz_binding_reviews.json').read_text())['releases'] if r['discogs_id']=='3386012')
        album=load_snapshot()['albums'][review['album_id']]
        self.assertTrue(all(agrees('Chicago Symphony Orchestra',credits(t)) for t in album['tracks']['items']))
        self.assertTrue(all(not agrees(n,credits(t)) for n in ['Dale Clevenger','Adolph Herseth'] for t in album['tracks']['items']))
        self.assertIsNone(reviewed_candidate(row,album,review))

    def test_liner_author_with_any_real_work_solo_credit_cannot_be_excluded(self):
        from qobuz_source_reconciliation import validate_nonperforming_credit
        raw=json.loads((ROOT/'raw/discogs/releases/5972183.json').read_text())
        credit=self.review['source_credit_reconciliation']['nonperformers'][0]
        for scope in ['global','nested']:
            altered=copy.deepcopy(raw)
            target=altered['extraartists'] if scope=='global' else altered['tracklist'][0]['sub_tracks'][0].setdefault('extraartists',[])
            target.append({'name':'Roger Dettmer','role':'Horn [Solo]'})
            with self.assertRaises(ValueError):validate_nonperforming_credit(self.row,altered,credit)
