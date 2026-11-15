import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT,assess,fingerprint,reviewed_candidate
from qobuz_heading_movements_review import grouped_row
from qobuz_snapshot import load_snapshot

class HeadingMovementsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])=='4694861')
        cls.raw=json.loads((ROOT/'raw/discogs/releases/4694861.json').read_text())
        cls.review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='4694861')
        import gzip
        data=json.loads(gzip.decompress((ROOT/'data/qobuz_comparison_evidence.json.gz').read_bytes()))
        cls.album=next(x['album'] for x in data['metadata'] if str(x['album']['id'])==cls.review['album_id'])

    def test_all_source_bands_stay_under_ten_headings_without_mutation(self):
        before=copy.deepcopy(self.row)
        c=reviewed_candidate(self.row,self.album,self.review)
        self.assertEqual((c['status'],c['confidence']),('probable',.85))
        works=c['completeness']['works']
        self.assertEqual([len(w['track_ids']) for w in works],[4,4,4,4,3,3,4,3,3,3])
        self.assertEqual(len({i for w in works for i in w['track_ids']}),35)
        self.assertEqual(sum(len(w['source_movements']) for w in works),35)
        self.assertEqual(self.row,before)
        # Repeated Allegretto labels belong to separate source positions/works.
        self.assertEqual([b['position'] for w in works for b in w['source_movements'] if b['title']=='Allegretto'],['E5','H1'])

    def test_source_missing_band_duplicate_position_or_unattached_band_rejected(self):
        for change in ['missing','duplicate','unattached']:
            raw=copy.deepcopy(self.raw)
            if change=='missing':raw['tracklist'].pop(3)
            elif change=='duplicate':raw['tracklist'][2]['position']=raw['tracklist'][1]['position']
            else:raw['tracklist'].insert(0,raw['tracklist'].pop(1))
            with self.assertRaises(ValueError):grouped_row(self.row,raw,self.review)

    def test_cross_work_borrowing_or_wrong_pianist_cannot_pass_even_after_rehash(self):
        for change in ['work','movement','pianist']:
            a=copy.deepcopy(self.album)
            t=next(t for t in a['tracks']['items'] if t['id']==36924043)
            if change=='work':t['title']=t['title'].replace('No. 1 in F Minor, Op. 2 No. 1','No. 2 in A Major, Op. 2 No. 2')
            elif change=='movement':a['tracks']['items'].remove(t)
            else:t['performers']=t['performers'].replace('Artur Schnabel','Wilhelm Kempff')
            review=copy.deepcopy(self.review);review['album_sha256']=fingerprint(a)
            # Movement/credit gates must still fail if a future review rebinds hashes.
            review['track_fingerprints'].update({str(t['id']):fingerprint(t) for t in a['tracks']['items'] if str(t['id']) in review['track_fingerprints']})
            try:result=assess(self.row,a,review)[0]
            except ValueError:continue
            self.assertFalse(result['eligible'],change)
