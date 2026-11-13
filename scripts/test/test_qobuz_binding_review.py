import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_binding_review import allowed, assess_bindings
from qobuz_lead_review import ROOT, reviewed_candidate
from qobuz_snapshot import load_snapshot


class BindingReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.albums = load_snapshot()['albums']
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_binding_reviews.json').read_text())['releases']}

    def review(self, discogs_id):
        review = self.reviews[discogs_id]
        return self.rows[discogs_id], self.albums[review['album_id']], review

    def test_saved_decisions_publish_only_complete_bindings(self):
        published = []
        for discogs_id, review in self.reviews.items():
            row, album, review = self.review(discogs_id)
            candidate = reviewed_candidate(row, album, review)
            if review['decision'] == 'probable':
                self.assertEqual((candidate['status'], candidate['confidence']), ('probable', .85))
                self.assertEqual(candidate['covered'], candidate['target_count'])
                self.assertTrue(all(item['credited_tracks'] for item in candidate['programme']))
                published.append(discogs_id)
            else:
                self.assertIsNone(candidate)
        self.assertEqual(published, ['11562013', '3475547', '11168177', '6029612', '5177097', '7525022', '4483876', '7119504', '6472687'])

    def test_a_mislabelled_scherzo_or_a_wrong_koechel_number_cannot_be_forced(self):
        row, album, review = self.review('11562013')
        broken = copy.deepcopy(review)
        broken['pulls'] = []
        with self.assertRaises(ValueError):
            assess_bindings(row, album, broken)
        row, album, review = self.review('4641786')
        forced = copy.deepcopy(review)
        forced['decision'] = 'probable'
        forced['required_performers'] = ['Ingrid Haebler']
        forced['adds'] = [{'track_id': 179323471, 'target': 'Sonate F-Dur, KV 322',
                           'title_contains': 'K. 332', 'catalogue_exception': 'suffix-letter',
                           'reason': 'Trying to treat KV 322 as the F-major sonata K. 332.'}]
        with self.assertRaises(ValueError):
            assess_bindings(row, album, forced)

    def test_an_absent_bonus_and_a_short_extra_take_stay_out(self):
        row, album, review = self.review('2383925')
        forced = copy.deepcopy(review)
        forced['adds'] = [{'track_id': album['tracks']['items'][0]['id'], 'target': 'Audrey',
                           'title_contains': 'Blue', 'reason': 'Using another Time Out track in place of Audrey.'}]
        with self.assertRaises(ValueError):
            assess_bindings(row, album, forced)
        row, album, review = self.review('5177097')
        kept = copy.deepcopy(review)
        kept['exclusions'] = []
        with self.assertRaises(ValueError):
            assess_bindings(row, album, kept)

    def test_the_violin_original_cannot_replace_the_arranged_concerto(self):
        target = 'Concerto En Ut Mineur, BWV 1062 Pour Deux Pianos (Transcription Du Concerto Pour Deux Violons, BWV 1043)'
        self.assertTrue(allowed('transcription-bwv', target, 'Concerto for Two Pianos in C Minor, BWV 1062: I.'))
        self.assertFalse(allowed('transcription-bwv', target, 'Concerto for Two Violins, BWV 1043'))
