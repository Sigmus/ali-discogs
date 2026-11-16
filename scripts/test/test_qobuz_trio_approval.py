import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint
from qobuz_credit_role_audit import load_albums
from qobuz_source_leaf_review import collective_members,collective_credited

class TrioApprovalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='8535848')
        cls.raw=json.loads((ROOT/'raw/discogs/releases/8535848.json').read_text())
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='8535848')
        cls.album=load_albums()[cls.review['album_id']]

    def test_approved_complete_programme(self):
        result,evidence=assess(self.row,self.album,self.review)
        self.assertTrue(result['eligible']);self.assertEqual(evidence['covered'],8)
        self.assertEqual([b['source_path'] for b in self.review['bindings']],[[g,m] for g in range(2) for m in range(4)])
        self.assertTrue(all(w['status']=='complete' for w in result['completeness']['works']))

    def test_collective_never_substitutes_for_any_missing_member_or_instrument(self):
        spec=self.review['source_collective_members'];required=self.review['bindings'][0]['required_performers'];original=self.album['tracks']['items'][0]
        for member in spec['members']:
            for replacement in ['',member['name']+', Associated Performer',member['name']+', MainArtist']:
                track=copy.deepcopy(original)
                track['performers']=' - '.join(replacement if p.startswith(member['name']+',') else p for p in track['performers'].split(' - '))
                self.assertFalse(collective_credited(spec,required,track))
        with self.assertRaisesRegex(ValueError,'requirement was omitted'):
            collective_credited(spec,required[1:],original)

    def test_approval_cannot_move_or_change_lineup(self):
        r=copy.deepcopy(self.review);r['discogs_id']='123'
        with self.assertRaisesRegex(ValueError,'exact trio'):collective_members(self.raw,r)
        raw=copy.deepcopy(self.raw);next(a for a in raw['extraartists'] if a['name']=='Leonard Rose')['id']=1
        with self.assertRaisesRegex(ValueError,'lineup changed'):collective_members(raw,self.review)
        r=copy.deepcopy(self.review);r['external_source_files']=r['external_source_files'][:1]
        with self.assertRaisesRegex(ValueError,'saved user approval'):collective_members(self.raw,r)

    def test_original_collective_gate_is_retained_without_approval_spec(self):
        r=copy.deepcopy(self.review);del r['source_collective_members']
        result,_=assess(self.row,self.album,r)
        self.assertFalse(result['eligible']);self.assertIn('performer',result['blockers'])

    def test_approval_does_not_waive_timing_or_missing_bands(self):
        r=copy.deepcopy(self.review);r['bindings'].pop()
        with self.assertRaisesRegex(ValueError,'omitted'):assess(self.row,self.album,r)
        # Keep the exact approval hashes; changing any cached timing is rejected before acceptance.
        album=copy.deepcopy(self.album);album['tracks']['items'][0]['duration']+=120
        with self.assertRaisesRegex(ValueError,'evidence changed'):assess(self.row,album,self.review)
