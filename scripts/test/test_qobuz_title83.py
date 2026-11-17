import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT, assess, fingerprint
from qobuz_credit_role_audit import load_albums
from qobuz_title83_audit import validate_title83, ACCEPTED


class Title83Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.albums = load_albums()
        cls.report = json.loads((ROOT/'data/qobuz_title83_recording_audit.json').read_text())
        cls.diagnostic = json.loads((ROOT/'data/qobuz_title151_diagnostic.json').read_text())

    def test_all_83_and_263_comparisons_with_saved_hold_precedence(self):
        self.assertEqual(validate_title83(self.report, self.diagnostic, self.rows, self.albums, self.reviews),
                         {'reviewed': 83, 'withhold': 78, 'probable': 5})
        self.assertEqual(sum(len(e['cached_alternative_checks']) for e in self.report['entries']), 263)

    def test_source_scope_and_alternatives_cannot_be_removed(self):
        report = copy.deepcopy(self.report)
        report['entries'][0]['cached_alternative_checks'].pop()
        with self.assertRaisesRegex(ValueError, 'candidate scope'):
            validate_title83(report, self.diagnostic, self.rows, self.albums, self.reviews)

    def test_complete_source_programmes_and_no_timing_exceptions(self):
        for rid, counts in zip(ACCEPTED, [[1]*3, [1]*12, [1]*5, [1]*4, [7, 5, 6]]):
            r = self.reviews[rid]
            self.assertEqual([len(b['track_ids']) for b in r['bindings']], counts)
            self.assertFalse(r.get('source_duration_notes'))
            self.assertTrue(assess(self.rows[rid], self.albums[r['album_id']], r)[0]['eligible'])

    def altered_track(self, rid, transform):
        r = copy.deepcopy(self.reviews[rid]); a = copy.deepcopy(self.albums[r['album_id']])
        tid = r['bindings'][0]['track_ids'][0]
        t = next(t for t in a['tracks']['items'] if t['id'] == tid)
        transform(t)
        r['album_sha256'] = fingerprint(a)
        r['bindings'][0]['track_sha256'][0] = fingerprint(t)
        r['selected_track_fingerprints'][str(tid)] = fingerprint(t)
        return assess(self.rows[rid], a, r)[0]

    def test_missing_musician_or_wrong_composer_cannot_borrow_album_credit(self):
        for text, blocker in [('Leonard Bernstein, Conductor, MainArtist', 'performer'),
                              ('Bela Bartok, Composer', 'composer')]:
            result = self.altered_track('3103644', lambda t: t.update(performers=t['performers'].replace(text, 'Unrelated Person, MainArtist')))
            self.assertFalse(result['eligible']); self.assertIn(blocker, result['blockers'])

    def test_joined_lesson_cannot_drop_a_section(self):
        r = copy.deepcopy(self.reviews['12561696']); r['bindings'][0]['track_ids'].pop()
        with self.assertRaises(ValueError):
            assess(self.rows['12561696'], self.albums[r['album_id']], r)

    def test_changed_ravel_timing_remains_blocked(self):
        result = self.altered_track('6900724', lambda t: t.update(duration=t['duration']+100))
        self.assertFalse(result['eligible']); self.assertIn('source-band-duration', result['blockers'])

    def test_boston_pastorale_is_not_a_new_timing_waiver(self):
        r = copy.deepcopy(self.reviews['4286791']); r['decision'] = 'probable'
        result, _ = assess(self.rows['4286791'], self.albums[r['album_id']], r)
        self.assertFalse(result['eligible']); self.assertIn('source-band-duration', result['blockers'])
        work = result['completeness']['works'][3]
        self.assertEqual((work['source_duration_seconds'], work['digital_duration_seconds']), (170, 179))
