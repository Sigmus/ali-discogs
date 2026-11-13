import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_match import evaluate, evaluate_v1
from qobuz_work_groups import contextual_tracks
from qobuz_snapshot import load_snapshot

ROOT = Path(__file__).resolve().parents[2]


def target():
    return {'composers': ['Example Composer'], 'performers': ['Alice', 'Bob'],
            'ensembles': ['Target Orchestra'], 'conductor': 'Target Conductor',
            'tracklist': [{'title': 'Cantata Op.123', 'type': 'index'}]}


def recording():
    return {'tracks': {'items': [
        {'id': 1, 'title': 'Cantata Op.123: I. Allegro', 'performers': 'Alice, Soprano - Target Orchestra, Orchestra - Target Conductor, Conductor - Example Composer, Composer'},
        {'id': 2, 'title': 'Cantata Op.123: II. Andante', 'performers': 'Bob, Tenor - Target Orchestra, Orchestra - Target Conductor, Conductor - Example Composer, Composer'}]}}


class WorkGroupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        cls.albums = load_snapshot()['albums']

    def test_role_specific_participation_requires_coherent_group(self):
        row, album = target(), recording()
        self.assertEqual(evaluate_v1(row, album)['status'], 'unchecked')
        result = evaluate(row, album)
        self.assertEqual(result['status'], 'probable')
        self.assertEqual(result['programme'][0]['track_ids'], [1, 2])
        self.assertIn('recording_group', result['programme'][0])
        self.assertNotIn('recording_group', evaluate_v1(row, album)['programme'][0])

    def test_never_borrow_from_wrong_orchestra_extra_soloist_or_repeated_take(self):
        for alteration in ['orchestra', 'soloist', 'restart', 'separate']:
            a = recording()
            if alteration == 'orchestra':
                a['tracks']['items'][1]['performers'] = a['tracks']['items'][1]['performers'].replace('Target Orchestra', 'Wrong Orchestra')
            elif alteration == 'soloist':
                a['tracks']['items'][1]['performers'] += ' - Charlie, MainArtist, Tenor'
            elif alteration == 'restart':
                a['tracks']['items'][1]['title'] = 'Cantata Op.123: I. Different take'
            else:
                a['tracks']['items'].insert(1, {'id': 3, 'title': 'Other Work Op.124', 'performers': 'Example Composer, Composer'})
            self.assertEqual(evaluate(target(), a)['status'], 'unchecked', alteration)

    def test_context_stops_at_changed_composer_anchor_or_sequence(self):
        original = recording()['tracks']['items']
        original[1]['title'] = '2. Andante'
        before = copy.deepcopy(original)
        result = contextual_tracks(target(), original)
        self.assertIn('Op.123', result[1]['title'])
        self.assertEqual(result[1]['context_parent_track_id'], 1)
        self.assertEqual(original, before)
        for field, replacement in [('title', '3. Andante'),
                                    ('performers', original[1]['performers'].replace('Example Composer', 'Other Composer')),
                                    ('performers', original[1]['performers'].replace('Target Orchestra', 'Wrong Orchestra'))]:
            changed = copy.deepcopy(original)
            changed[1][field] = replacement
            self.assertNotIn('context_parent_track_id', contextual_tracks(target(), changed)[1])
        for field, before, after in [('media_number', 1, 2), ('track_number', 1, 3), ('work', 'One work', 'Other work')]:
            changed = copy.deepcopy(original)
            changed[0][field], changed[1][field] = before, after
            self.assertNotIn('context_parent_track_id', contextual_tracks(target(), changed)[1])

    def test_cached_work_collision_and_shortened_titles(self):
        r = evaluate(self.rows['3958148'], self.albums['0002894742692'])
        self.assertEqual([p['credited_tracks'] for p in r['programme']], [4, 4, 9])
        self.assertFalse(set(r['programme'][0]['track_ids']) & set(r['programme'][2]['track_ids']))
        r = evaluate(self.rows['2559625'], self.albums['0002894808892'])
        self.assertEqual(r['programme'][0]['credited_tracks'], 5)
        self.assertEqual(len(r['programme'][0]['inherited_title_context']), 4)
        r = evaluate(self.rows['14338491'], self.albums['0002894594542'])
        self.assertEqual(r['programme'][0]['credited_tracks'], 12)
        self.assertEqual(r['status'], 'probable')

    def test_uncertain_alias_and_dirty_main_artist_credits_not_invented(self):
        r = evaluate(self.rows['18770818'], self.albums['pfc4fflitmbpa'])
        self.assertEqual(r['programme'][0]['credited_tracks'], 1)
        r = evaluate(self.rows['1026299'], self.albums['0002894802866'])
        self.assertEqual([p['credited_tracks'] for p in r['programme']], [1, 1])

    def test_new_group_leads_need_completeness_before_publication(self):
        from qobuz_match import publication_evidence
        for rid, aid in [('6381208', 'kno5hz96hygbc'), ('6599326', 'tzrc8oc3d248a')]:
            row, album = self.rows[rid], self.albums[aid]
            self.assertEqual(evaluate(row, album)['status'], 'probable')
            result = publication_evidence(row, album, {'works': []})
            self.assertEqual(result['status'], 'unchecked')
            self.assertIsNone(result['confidence'])
            self.assertEqual(result['promotion_review']['status'], 'unknown')

    def test_reaudit_of_original_66_and_ten_expansions(self):
        from qobuz_group_audit import audit
        report = audit(self.rows, {'albums': self.albums},
            json.loads((ROOT/'data/qobuz_baseline_audit_scope.json').read_text()),
            json.loads((ROOT/'data/qobuz_expansion_scope.json').read_text()),
            json.loads((ROOT/'data/qobuz_work_inventory.json').read_text()))
        self.assertEqual(report['summary']['releases'], 76)
        self.assertEqual(report['summary']['status_changes'], 0)
        self.assertEqual(report['summary']['shared_track_assignment_releases'], 0)
