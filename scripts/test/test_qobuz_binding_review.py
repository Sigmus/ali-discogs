import copy
import gzip
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
        cls.albums = dict(load_snapshot()['albums'])
        extra = json.loads(gzip.decompress((ROOT/'data/qobuz_empty_search_metadata.json.gz').read_bytes()))
        for record in extra['metadata']:
            cls.albums[str(record['album']['id'])] = record['album']
        follow = json.loads(gzip.decompress((ROOT/'data/qobuz_empty_search_follow_metadata.json.gz').read_bytes()))
        for record in follow['metadata']:
            cls.albums[str(record['album']['id'])] = record['album']
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
        self.assertEqual(published, ['11562013', '3475547', '11168177', '6029612', '5177097', '7525022', '4483876', '7119504', '6472687', '10757104', '15980846', '4395895', '8291074', '11938972', '9739139', '9343746'])

    def test_an_ensemble_alias_needs_a_reason_and_still_names_the_source_ensemble(self):
        row, album, review = self.review('15980846')
        short = copy.deepcopy(review)
        short['performer_aliases'][0]['reason'] = 'same group'
        with self.assertRaises(ValueError):
            assess_bindings(row, album, short)
        plain = copy.deepcopy(review)
        plain['performer_aliases'] = []
        result, _ = assess_bindings(row, album, plain)
        self.assertFalse(result['eligible'])
        self.assertIn('performer', result['blockers'])

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

    def test_pink_panther_keeps_the_twelve_cues_and_leaves_galway_out(self):
        row, album, review = self.review('11938972')
        candidate = reviewed_candidate(row, album, review)
        ids = [track_id for item in candidate['programme'] for track_id in item['track_ids']]
        self.assertEqual(len(ids), 12)
        self.assertNotIn(21590198, ids)
        self.assertIn('instrumental', ' '.join(candidate['reasons']))
        self.assertIn('0886445007398', candidate['url'])
        dropped = copy.deepcopy(review)
        dropped['performer_aliases'] = [a for a in dropped['performer_aliases'] if 'Chorus' not in a['file']]
        result, _ = assess_bindings(row, album, dropped)
        self.assertFalse(result['eligible'])
        self.assertIn('performer', result['blockers'])

    def test_new_world_keeps_kondrashin_under_the_file_spelling(self):
        row, album, review = self.review('9739139')
        candidate = reviewed_candidate(row, album, review)
        self.assertEqual(len(candidate['programme'][0]['track_ids']), 4)
        self.assertIn('Kirill', ' '.join(candidate['reasons']))
        self.assertIn('jox1pt5atqcga', candidate['url'])
        plain = copy.deepcopy(review)
        plain['performer_aliases'] = []
        result, _ = assess_bindings(row, album, plain)
        self.assertFalse(result['eligible'])
        self.assertIn('performer', result['blockers'])

    def test_four_concertos_keep_the_storm_in_the_third_place(self):
        row, album, review = self.review('9343746')
        candidate = reviewed_candidate(row, album, review)
        titles = [item['target'] for item in candidate['programme']]
        self.assertEqual(titles[2], 'Concerto Mi Bémol Majeur la Tempête En Mer')
        self.assertEqual(sum(len(item['track_ids']) for item in candidate['programme']), 12)
        self.assertIn('3614595584943', candidate['url'])
        plain = copy.deepcopy(review)
        plain['performer_aliases'] = []
        result, _ = assess_bindings(row, album, plain)
        self.assertFalse(result['eligible'])
        self.assertIn('performer', result['blockers'])

    def test_a_printed_numero_counts_as_that_subnumber_only(self):
        target = 'Valse En La Mineur Op 34 N°2'
        self.assertTrue(allowed('bare-subnumber', target, 'Op. 34: No. 2 in A Minor'))
        self.assertFalse(allowed('bare-subnumber', target, 'Op. 34: No. 3 in F Major'))
        self.assertFalse(allowed('bare-subnumber', 'Valse Op 34', 'Op. 34: No. 2 in A Minor'))

    def test_the_violin_original_cannot_replace_the_arranged_concerto(self):
        target = 'Concerto En Ut Mineur, BWV 1062 Pour Deux Pianos (Transcription Du Concerto Pour Deux Violons, BWV 1043)'
        self.assertTrue(allowed('transcription-bwv', target, 'Concerto for Two Pianos in C Minor, BWV 1062: I.'))
        self.assertFalse(allowed('transcription-bwv', target, 'Concerto for Two Violins, BWV 1043'))
