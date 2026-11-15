import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src'))
from ali_discogs.model import build_item,credit_role_text
ROOT=Path(__file__).resolve().parents[2]

class DiscogsCreditRoleTests(unittest.TestCase):
    def test_annotations_do_not_create_performance_or_composition_roles(self):
        for role in ['Liner Notes [The Violoncello Before 1720]','Photography [Conductor at the Piano]','Liner Notes [Written By the Composer [Cello]]']:
            self.assertFalse(any(k in credit_role_text(role) for k in ['cello','conductor','piano','written','composed']))
        self.assertEqual(credit_role_text('Cello [Baroque], Liner Notes [The Piano]'),'cello , liner notes ')
        self.assertEqual(credit_role_text('Conductor [Guest]'),'conductor ')

    def test_casals_liner_author_is_not_required_performer_on_new_normalization(self):
        raw=json.loads((ROOT/'raw/discogs/releases/6628473.json').read_text())
        basic={'id':6628473,'title':raw['title'],'artists':raw['artists']}
        with patch('ali_discogs.model.raw_dir',return_value=str(ROOT/'raw')):
            item=build_item({'basic_information':basic})
        self.assertEqual(item['performers'],['Pablo Casals'])
        self.assertEqual(item['key_performers'],['Pablo Casals'])
        self.assertIn('Johann Sebastian Bach',item['composers'])
        self.assertNotIn('Guglielmo Barblan',item['performers'])

    def test_vocal_roles_still_retain_real_singers_after_annotations_removed(self):
        for rid,names in [('1640528',['Rosl Schwaiger','Theo Altmeyer']),('2906025',['Betty Van Den Berghe','Josep Cabré'])]:
            raw=json.loads((ROOT/f'raw/discogs/releases/{rid}.json').read_text())
            with patch('ali_discogs.model.raw_dir',return_value=str(ROOT/'raw')):
                item=build_item({'basic_information':{'id':int(rid),'title':raw['title'],'artists':raw['artists']}})
            for name in names:self.assertIn(name,item['performers'])
