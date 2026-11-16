import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_lead_review import ROOT
from qobuz_credit_role_audit import load_albums
from qobuz_musician21_audit import build


class MusicianTriageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.diagnostic = json.loads((ROOT/'data/qobuz_title151_diagnostic.json').read_text())
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.albums = load_albums()
        cls.saved = json.loads((ROOT/'data/qobuz_musician21_audit.json').read_text())

    def test_saved_evidence_reproduces_against_all_current_sources(self):
        self.assertEqual(build(self.diagnostic, self.rows, self.albums), self.saved)
        self.assertEqual(sum(self.saved['summary'].values()), 21)
        self.assertFalse(self.saved['publication_changed'])
        self.assertFalse(self.saved['policy_changed'])

    def test_scope_cannot_silently_drop_a_case(self):
        diagnostic = copy.deepcopy(self.diagnostic)
        diagnostic['entries'] = [e for e in diagnostic['entries'] if e['discogs_id'] != '11876845']
        with self.assertRaisesRegex(ValueError, 'Frozen musician scope changed'):
            build(diagnostic, self.rows, self.albums)

    def test_changed_candidate_credits_invalidate_saved_evidence(self):
        albums = dict(self.albums)
        aid = 'dds4ccexc73aa'
        albums[aid] = copy.deepcopy(albums[aid])
        albums[aid]['tracks']['items'][0]['performers'] = ''
        changed = build(self.diagnostic, self.rows, albums)
        old = next(e for e in self.saved['entries'] if e['discogs_id'] == '11876845')
        new = next(e for e in changed['entries'] if e['discogs_id'] == '11876845')
        oldc = next(c for c in old['candidates'] if c['album_id'] == aid)
        newc = next(c for c in new['candidates'] if c['album_id'] == aid)
        self.assertNotEqual(oldc['album_sha256'], newc['album_sha256'])
        self.assertNotEqual(oldc['track_manifest_sha256'], newc['track_manifest_sha256'])
