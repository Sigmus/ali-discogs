import copy
import gzip
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from ali_discogs.paths import data_dir
from ali_discogs.pipeline import match_spotify
from ali_discogs.spotify_programme import programme_review, target_fingerprint


class SpotifyProgrammeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(data_dir())
        cls.rows = {str(r['discogs_id']): r for r in json.loads((root/'collection_matches.json').read_text())}
        cls.ledger = json.loads((root/'spotify_programme_reviews.json').read_text())
        cls.archive = json.loads(gzip.decompress((root/'spotify_pilot_tracks.json.gz').read_bytes()))

    def candidate(self, review):
        return {'id': review['album_id'], 'name': review['album_name'],
                'total_tracks': review['total_tracks'], 'artists': []}

    def test_both_confirmed_partial_programmes_block_high_similarity(self):
        for review in self.ledger['entries']:
            item = self.rows[review['discogs_id']]
            album = self.candidate(review)
            self.assertEqual(programme_review(item, album)['status'], review['decision'])
            runner_up = dict(album, id='unreviewed-alternative')
            with patch('ali_discogs.pipeline.queries', return_value=['test']), \
                    patch('ali_discogs.pipeline.score', side_effect=lambda it,a: {'confidence': .99 if a['id']==album['id'] else .98}), \
                    patch('ali_discogs.pipeline.classify', return_value='found'):
                result = match_spotify(item, lambda q: {'albums': {'items': [album, runner_up]}})
            self.assertEqual(result['status'], 'unchecked')
            self.assertIsNone(result['confidence'])
            self.assertIsNone(result['album'])
            self.assertEqual(result['best_candidate']['id'], album['id'])
            self.assertEqual(result['alternates'][0]['id'], runner_up['id'])
            self.assertEqual(result['signals']['confidence'], .99)

    def test_different_candidate_or_target_is_not_a_rejection_or_approval(self):
        review = self.ledger['entries'][0]; item = self.rows[review['discogs_id']]
        self.assertIsNone(programme_review(item, dict(self.candidate(review), id='different')))
        self.assertIsNone(programme_review(dict(item, discogs_id=123456789), self.candidate(review)))

    def test_changed_target_and_album_fail_closed(self):
        review = self.ledger['entries'][0]; item = self.rows[review['discogs_id']]
        changed = copy.deepcopy(item); changed['tracklist'] = []
        with self.assertRaises(ValueError): programme_review(changed, self.candidate(review))
        with self.assertRaises(ValueError): programme_review(item, dict(self.candidate(review), total_tracks=999))
        with self.assertRaises(ValueError): programme_review(item, dict(self.candidate(review), name='New edition'))

    def test_missing_changed_or_incomplete_cache_cannot_be_used(self):
        review = self.ledger['entries'][0]; item = self.rows[review['discogs_id']]
        for mode in ['missing', 'changed', 'incomplete']:
            archive = copy.deepcopy(self.archive)
            matching = next(a for a in archive['albums'] if a['album_id']==review['album_id'])
            if mode=='missing': archive['albums'].remove(matching)
            elif mode=='changed': matching['tracks'][0]['name'] += ' changed'
            else: matching['tracks'].pop()
            with patch('ali_discogs.spotify_programme.gzip.decompress', return_value=json.dumps(archive).encode()):
                with self.assertRaises(ValueError): programme_review(item, self.candidate(review))

    def test_service_results_do_not_invalidate_target_hash(self):
        review = self.ledger['entries'][0]; item = copy.deepcopy(self.rows[review['discogs_id']])
        item['spotify'] = {}; item['qobuz'] = {}
        self.assertEqual(target_fingerprint(item), review['target_sha256'])

    def test_reviewed_dvorak_replacement_and_source_guards(self):
        from ali_discogs.spotify_programme import reviewed_replacement
        ledger = json.loads((Path(data_dir())/'spotify_replacement_reviews.json').read_text())
        review = ledger['entries'][0]; item = self.rows[review['discogs_id']]
        album = self.candidate(review)
        result = reviewed_replacement(item, [({'confidence': .99}, album)])
        self.assertEqual(result[2]['status'], 'reviewed_programme_supported')
        self.assertEqual(result[1]['id'], review['album_id'])
        self.assertIsNone(reviewed_replacement(item, []))
        changed = copy.deepcopy(item); changed['performers'] = ['Wrong Orchestra']
        with self.assertRaises(ValueError): reviewed_replacement(changed, [({}, album)])
        with self.assertRaises(ValueError): reviewed_replacement(item, [({}, dict(album, total_tracks=999))])
        with patch('ali_discogs.spotify_programme.gzip.decompress', return_value=b'{"schema_version":1,"albums":[]}'):
            with self.assertRaises(ValueError): reviewed_replacement(item, [({}, album)])

    def test_pipeline_positive_review_caps_and_preserves_rejection(self):
        review = json.loads((Path(data_dir())/'spotify_replacement_reviews.json').read_text())['entries'][0]
        item = self.rows[review['discogs_id']]
        negative = next(r for r in self.ledger['entries'] if r['discogs_id']==review['discogs_id'])
        bad = self.candidate(negative); good = self.candidate(review)
        with patch('ali_discogs.pipeline.queries', return_value=['test']), \
                patch('ali_discogs.pipeline.score', side_effect=lambda it,a: {'confidence': .99 if a['id']==bad['id'] else .98}), \
                patch('ali_discogs.pipeline.classify', return_value='found'):
            result = match_spotify(item, lambda q: {'albums': {'items': [bad, good]}})
        self.assertEqual((result['status'],result['confidence']), ('probable', .85))
        self.assertEqual(result['album']['id'], good['id'])
        self.assertEqual(result['rejected_candidates'][0]['album']['id'], bad['id'])
        self.assertNotIn(good['id'], [a['id'] for a in result['alternates']])
