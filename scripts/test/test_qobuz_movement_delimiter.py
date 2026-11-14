import copy
import gzip
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_completeness import movement_number,check_programme
from qobuz_match import ROOT,evaluate

class MovementDelimiterTests(unittest.TestCase):
    def test_explicit_catalogue_comma_roman_only(self):
        self.assertEqual(movement_number('Symphony No.6 in F, Op.68, IV. Allegro'),4)
        self.assertIsNone(movement_number('Symphony, IV. Allegro'))
        self.assertIsNone(movement_number('Op.68, 4. Alternate take'))
        self.assertIsNone(movement_number('Op.68, II/III. Joined'))
        self.assertIsNone(movement_number('Op.68, II. Andante: III. Allegro'))
        self.assertIsNone(movement_number('Op.68, IVa. Excerpt'))

    def test_cached_pastoral_requires_all_five_movements_and_credits(self):
        rows=json.loads((ROOT/'data/collection_matches.json').read_text())
        row=next(r for r in rows if r['discogs_id']==10757120)
        album=None
        for path in (ROOT/'data').glob('qobuz*.json.gz'):
            d=json.loads(gzip.decompress(path.read_bytes()))
            if not isinstance(d,dict):continue
            candidates=list(d.get('albums',{}).values()) if isinstance(d.get('albums'),dict) else []
            candidates += [x['album'] for x in d.get('metadata',[])]
            album=next((a for a in candidates if a['id']=='lbd4bwo8ommnb'),album)
        inventory=json.loads((ROOT/'data/qobuz_work_inventory.json').read_text())
        self.assertEqual(check_programme(row,album,evaluate(row,album),inventory)['status'],'complete')
        altered=copy.deepcopy(album);altered['tracks']['items'].pop(2)
        self.assertNotEqual(check_programme(row,altered,evaluate(row,altered),inventory)['status'],'complete')
        altered=copy.deepcopy(album)
        for t in altered['tracks']['items']:t['performers']=t['performers'].replace('NBC Symphony Orchestra','Another Orchestra')
        self.assertNotEqual(check_programme(row,altered,evaluate(row,altered),inventory)['status'],'complete')
