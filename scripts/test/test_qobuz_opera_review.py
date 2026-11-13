import copy
import gzip
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT, fingerprint, reviewed_candidate
from qobuz_opera_review import assess_opera


class OperaSourceRoleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.albums = {x['task']['discogs_id']: x['album'] for x in json.loads(gzip.decompress((ROOT/'data/qobuz_unmatched_metadata.json.gz').read_bytes()))['metadata']}
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_opera_recording_reviews.json').read_text())['releases']}

    def review(self, rid):
        return copy.deepcopy(self.reviews[rid])

    def test_tristan_is_probable_only_with_every_track_and_named_singer(self):
        row, album, review = self.rows['2996680'], self.albums['2996680'], self.review('2996680')
        candidate = reviewed_candidate(row, album, review)
        self.assertEqual((candidate['status'], candidate['confidence']), ('probable', .85))
        self.assertEqual(candidate['programme'][0]['opera_acts'], {1: 7, 2: 11, 3: 11})
        self.assertEqual(len(candidate['programme'][0]['track_ids']), 29)
        self.assertNotIn('unresolved', ' '.join(candidate['reasons']))
        self.assertIn('scene alignment is not claimed', ' '.join(candidate['reasons']))
        self.assertIn('not the complete LP box', ' '.join(candidate['reasons']))
        self.assertIn('orchester-der-bayreuther-festspiele-karl-bohm', candidate['url'])
        shortened = copy.deepcopy(album)
        shortened['tracks']['items'].pop(0)
        self.assertIsNone(reviewed_candidate(row, shortened, dict(review, album_sha256=fingerprint(shortened))))
        review['source_roles'] = [e for e in review['source_roles'] if e['name'] != 'Wolfgang Windgassen']
        with self.assertRaises(ValueError):
            assess_opera(row, album, review)

    def test_voice_conflicts_and_bonus_sides_cannot_be_silent(self):
        row, album = self.rows['2996680'], self.albums['2996680']
        review = self.review('2996680')
        for entry in review['source_roles']:
            entry.pop('voice_conflict', None)
        with self.assertRaises(ValueError):
            assess_opera(row, album, review)
        review = self.review('2996680')
        changed = copy.deepcopy(album)
        changed['tracks']['items'][0]['title'] += ' Probe'
        amended = dict(review, album_sha256=fingerprint(changed))
        with self.assertRaises(ValueError):
            assess_opera(row, changed, amended)
        review['edition_gaps'] = []
        with self.assertRaises(ValueError):
            assess_opera(row, album, review)

    def test_tannhauser_blocks_missing_pages_wrong_role_and_other_orchestra(self):
        row, album, review = self.rows['4365080'], self.albums['4365080'], self.review('4365080')
        self.assertIsNone(reviewed_candidate(row, album, review))
        review['decision'] = 'probable'
        result, _ = assess_opera(row, album, review)
        self.assertFalse(result['eligible'])
        self.assertIn('absent:Arnold Schremm', result['blockers'])
        self.assertIn('role-mismatch:Karl Schmidt (2)', result['blockers'])
        self.assertTrue(any(item.startswith('conflicting-ensemble:') for item in result['blockers']))
        self.assertIn('missing-scenes-3', result['blockers'])
        review = self.review('4365080')
        review['source_roles'] = [e for e in review['source_roles'] if 'Edelknaben' not in e['role']]
        with self.assertRaises(ValueError):
            assess_opera(row, album, review)
        review = self.review('4365080')
        review['source_roles'][5]['equate_director'] = True
        with self.assertRaises(ValueError):
            assess_opera(row, album, review)

    def test_ensemble_alias_is_explicit_and_recording_specific(self):
        row, album = self.rows['2996680'], self.albums['2996680']
        review = self.review('2996680')
        orchestra = next(e for e in review['source_roles'] if e['kind'] == 'orchestra')
        orchestra.pop('alias_reason')
        with self.assertRaises(ValueError):
            assess_opera(row, album, review)
        review = self.review('2996680')
        orchestra = next(e for e in review['source_roles'] if e['kind'] == 'orchestra')
        orchestra['candidate_name'] = 'Los Angeles Philharmonic'
        orchestra['alias_reason'] = 'This substitution is intentionally not the Bayreuth orchestra.'
        result, _ = assess_opera(row, album, review)
        self.assertFalse(result['eligible'])
        self.assertTrue(any('Los Angeles' in item or item.startswith('missing-orchestra') or item.startswith('conflicting-ensemble') for item in result['blockers']))
