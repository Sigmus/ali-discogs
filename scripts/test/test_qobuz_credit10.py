import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT, assess, fingerprint
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate
from qobuz_credit10_audit import IDS


class CreditTenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
        cls.report = json.loads((ROOT/'data/qobuz_credit10_recording_audit.json').read_text())
        cls.albums = load_albums()

    def test_complete_batch_and_hold_precedence(self):
        self.assertEqual(self.report['frozen_release_ids'], IDS)
        self.assertEqual(validate(self.report, self.rows, self.albums, self.reviews, 10),
                         {'reviewed': 10, 'withhold': 9, 'probable': 1})
        self.assertEqual(sum(len(e['cached_alternative_checks']) for e in self.report['entries']), 30)

    def test_dupre_requires_all_four_source_works(self):
        r = copy.deepcopy(self.reviews['4079723'])
        self.assertEqual([b['track_ids'] for b in r['bindings']], [[27578140], [27578142], [27578144], [27578146]])
        r['bindings'].pop()
        with self.assertRaisesRegex(ValueError, 'omitted'):
            assess(self.rows['4079723'], self.albums[r['album_id']], r)

    def changed_credit(self, change):
        r = copy.deepcopy(self.reviews['4079723']); a = copy.deepcopy(self.albums[r['album_id']])
        t = a['tracks']['items'][0]; t['performers'] = change(t['performers'])
        r['album_sha256'] = fingerprint(a); r['bindings'][0]['track_sha256'][0] = fingerprint(t)
        r['selected_track_fingerprints'][str(t['id'])] = fingerprint(t)
        return assess(self.rows['4079723'], a, r)[0]

    def test_associated_alone_cannot_replace_positive_main_artist(self):
        result = self.changed_credit(lambda text: text.replace('Marcel Dupre, MainArtist, AssociatedPerformer', 'Marcel Dupre, AssociatedPerformer'))
        self.assertFalse(result['eligible']); self.assertIn('performer', result['blockers'])

    def test_source_misclassified_organist_cannot_replace_correct_composer(self):
        result = self.changed_credit(lambda text: text.replace('Cesar Franck, Composer', 'Marcel Dupre, Composer'))
        self.assertFalse(result['eligible']); self.assertIn('composer', result['blockers'])

    def test_full_jazz_source_lineup_is_retained_despite_empty_parser_gap(self):
        entry = next(e for e in self.report['entries'] if e['discogs_id'] == '5085113')
        self.assertEqual(entry['outcome'], 'withhold')
        names = {c['name'] for c in entry['source_credits']}
        self.assertTrue({'Ben Van Gelder', 'Maarten Hogenhuis', 'Sean Fasciani', 'Mark Schilders'} <= names)
        self.assertIn('underrepresents saxophone/bass/drums', entry['finding'])
