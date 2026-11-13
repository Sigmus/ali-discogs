import sys
from pathlib import Path
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_target_credits import derive,requirements
from qobuz_query_plan import lead,propose,relevance
from qobuz_match import units,units_v1


class TargetCreditQueryTests(unittest.TestCase):
    def test_position_scope_does_not_spill_and_unscoped_names_stay_required(self):
        raw={'tracklist':[{'title':'Work A','position':'A','type_':'track'},{'title':'Work B','position':'B','type_':'track'}],
             'extraartists':[{'name':'Alice','role':'Piano','tracks':'A'},{'name':'Technician','role':'Piano Technician','tracks':'A'}]}
        model=derive(raw)
        self.assertEqual([p['name'] for p in model[0]['performers']],['Alice'])
        row={'discogs_id':1,'ensembles':['Shared Orchestra'],'conductor':'Conductor'}
        with patch('qobuz_target_credits.load',return_value={'1':model}):
            _,a,_=requirements(row,'Work A',['Alice','Conductor','Unknown Global Artist'])
            _,b,_=requirements(row,'Work B',['Alice','Conductor','Unknown Global Artist'])
        self.assertIn('Alice',a);self.assertNotIn('Alice',b)
        self.assertIn('Unknown Global Artist',b)

    def test_nested_positive_credit_added_only_to_its_work(self):
        raw={'tracklist':[{'title':'Concerto','type_':'index','sub_tracks':[{'position':'A1'}],'extraartists':[{'name':'Alice','role':'Oboe, Soloist'}]},
                          {'title':'Sonata','position':'B1','type_':'track'}], 'extraartists':[{'name':'Bob','role':'Violin','tracks':'AA1'}]}
        model=derive(raw)
        self.assertEqual(len(model),1)
        self.assertEqual(model[0]['performers'][0]['name'],'Alice')

    def test_parent_headings_preserve_standalone_items_and_legacy(self):
        row={'tracklist':[{'type':'heading','title':'Sonata Op.27 No.2'}, {'type':'track','title':'I: Adagio sostenuto'},
                          {'type':'track','title':'II: Allegretto'},{'type':'track','title':'Ballade Op.23'}]}
        self.assertEqual(len(units_v1(row)),4)
        self.assertEqual(units(row),['Sonata Op.27 No.2','Ballade Op.23'])

    def test_query_uses_album_lead_not_supporting_pianist_and_compound_composer(self):
        row={'artists':['John Coltrane'],'key_performers':['McCoy Tyner'],'composers':['John Coltrane'],'title':'A Love Supreme'}
        self.assertEqual(lead(row),'John Coltrane')
        self.assertIn('john coltrane a love supreme',propose(row))
        row={'artists':['Felix Mendelssohn-Bartholdy','Alfred Cortot'],'composers':['Felix Mendelssohn-Bartholdy'],'title':'Piano Trio'}
        self.assertEqual(propose(row)[0],'alfred cortot mendelssohn')

    def test_search_ranking_is_not_acceptance_and_downranks_other_lead(self):
        row={'artists':['John Coltrane'],'title':'A Love Supreme'}
        good=relevance(row,{'title':'A Love Supreme','artist':{'name':'John Coltrane'}})
        other=relevance(row,{'title':'Plays John Coltrane','artist':{'name':'McCoy Tyner'}})
        self.assertGreater(good['score'],other['score'])
        self.assertNotIn('status',good)

    def test_cross_side_ranges_and_unparseable_scopes_never_drop_requirements(self):
        from qobuz_target_credits import selectors
        positions=['A','B','C1','C2','D1','D2']
        self.assertEqual(selectors('A to C1, D2',positions),{'A','B','C1','D2'})
        self.assertEqual(selectors('A, C1 to D1',positions),{'A','C1','C2','D1'})
        self.assertIsNone(selectors('unsupported description, D2',positions))
        raw={'tracklist':[{'title':'A work','position':'A','type_':'track'},{'title':'B work','position':'B','type_':'track'}],
             'extraartists':[{'name':'Alice','role':'Violin','tracks':'A'},{'name':'Alice','role':'Piano','tracks':''}]}
        with patch('qobuz_target_credits.load',return_value={'1':derive(raw)}):
            _,required,_=requirements({'discogs_id':1},'B work',['Alice'])
        self.assertIn('Alice',required)

    def test_real_bitches_brew_cross_side_credits_are_not_partially_parsed(self):
        import json
        raw=json.loads((Path(__file__).resolve().parents[2]/'raw/discogs/releases/7609610.json').read_text())
        model=derive(raw)
        row={'discogs_id':7609610}
        with patch('qobuz_target_credits.load',return_value={'7609610':model}):
            _,spanish,_=requirements(row,'Spanish Key',['Joe Zawinul','Larry Young','Miles Davis'])
            _,sanctuary,_=requirements(row,'Sanctuary',['Joe Zawinul','Larry Young','Miles Davis'])
        self.assertIn('Joe Zawinul',spanish);self.assertIn('Larry Young',spanish)
        self.assertIn('Joe Zawinul',sanctuary);self.assertNotIn('Larry Young',sanctuary)
