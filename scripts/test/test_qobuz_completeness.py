import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_completeness import check_programme, movement_number, inventory_work
from qobuz_match import evaluate
from qobuz_snapshot import load_snapshot

ROOT = Path(__file__).resolve().parents[2]
INVENTORY = json.loads((ROOT/'data/qobuz_work_inventory.json').read_text())


def target(composer='Ludwig van Beethoven', title='Symphony Op.67'):
    return {'performers': ['Alice'], 'composers': [composer],
            'tracklist': [{'title': title, 'type': 'index'}]}


def album(numbers=(1, 2, 3, 4)):
    return {'tracks': {'items': [
        {'id': i, 'title': f'Symphony Op.67: {n}. Allegro',
         'performers': 'Alice, Conductor - Ludwig van Beethoven, Composer'}
        for i, n in enumerate(numbers)]}}


def check(row, recording):
    return check_programme(row, recording, evaluate(row, recording), INVENTORY)


class CompletenessTests(unittest.TestCase):
    def test_requires_inventory_and_every_movement(self):
        self.assertEqual(check(target(), album())['status'], 'complete')
        self.assertEqual(check(target(), album((1,)))['status'], 'incomplete')
        self.assertEqual(check(target(), album((1, 2, 4)))['status'], 'incomplete')
        self.assertEqual(check(target(title='Symphony Op.999'), album())['status'], 'unknown')
        self.assertIsNone(inventory_work(target(composer='Someone Else'), 'Symphony Op.67', INVENTORY))
        self.assertIsNone(inventory_work(target(title='Sonata Op.67 No.2'), 'Sonata Op.67 No.2', INVENTORY))

    def test_no_automatic_split_joined_duplicate_or_order_guesses(self):
        for label in ['Work: IVa-b. Finale', 'Work: II/III. Andante',
                      'Work: II. Andante / III. Rondo', 'Work: Allegro con brio']:
            self.assertIsNone(movement_number(label))
        self.assertEqual(movement_number('Work Op.67: IV. Allegro'), 4)
        self.assertEqual(check(target(), album((1, 2, 3, 4, 4)))['status'], 'unknown')
        self.assertEqual(check(target(), album((2, 1, 3, 4)))['status'], 'unknown')
        a = album()
        a['tracks']['items'][3]['title'] = 'Symphony Op.67: IVa-b. Finale'
        self.assertEqual(check(target(), a)['status'], 'unknown')

    def test_credits_and_explicit_movement_targets_not_bypassed(self):
        a = album()
        a['tracks']['items'][2]['performers'] = 'Bob, Conductor - Ludwig van Beethoven, Composer'
        self.assertEqual(check(target(), a)['status'], 'incomplete')
        self.assertEqual(check(target(title='Symphony Op.67: I. Allegro'), album())['status'], 'unknown')

    def test_real_kleiber_negative_controls_and_full_work_controls(self):
        snapshot = load_snapshot()
        rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        row = rows['1093216']
        for aid in ['0002894778168', '0002894805871']:
            result = check(row, snapshot['albums'][aid])
            self.assertNotEqual(result['status'], 'complete', aid)
        for aid in ['0002894791000', 'y7nd66idm247a']:
            self.assertEqual(check(row, snapshot['albums'][aid])['status'], 'complete', aid)
        # Existing wrong-orchestra control remains blocked even with work titles.
        row = rows['15282801']
        evidence = evaluate(row, snapshot['albums']['ezfmmvuhlu4uc'])
        self.assertEqual(evidence['status'], 'unchecked')
        self.assertNotEqual(check_programme(row, snapshot['albums']['ezfmmvuhlu4uc'], evidence, INVENTORY)['status'], 'complete')

    def test_numbered_target_children_without_inventory(self):
        row = target(title='Symphony Op.999')
        row['tracklist'] += [{'title': t, 'type': 'track'} for t in ['I. Allegro', 'II. Andante', 'III. Presto']]
        a = album((1, 2, 3))
        for t in a['tracks']['items']:
            t['title'] = t['title'].replace('Op.67', 'Op.999')
        result = check(row, a)
        self.assertEqual(result['status'], 'complete')
        self.assertEqual(result['works'][0]['scope'], 'listed-target-movements')
        a['tracks']['items'].pop()
        self.assertEqual(check(row, a)['status'], 'incomplete')
        row['tracklist'][-1]['title'] = 'Unnumbered Finale'
        self.assertEqual(check(row, a)['status'], 'unknown')

    def test_timed_explicit_tracks_and_overlapping_targets(self):
        row = target(title='A Distinctive Prelude')
        row['tracklist'][0].update(type='track', duration='10:00')
        a = {'tracks': {'items': [{'id': 1, 'title': 'A Distinctive Prelude', 'duration': 610,
              'performers': 'Alice, Piano - Ludwig van Beethoven, Composer'}]}}
        self.assertEqual(check(row, a)['status'], 'complete')
        a['tracks']['items'][0]['duration'] = 300
        self.assertEqual(check(row, a)['status'], 'unknown')
        a['tracks']['items'][0]['duration'] = 610
        row['tracklist'].append({'title': 'Another Prelude', 'type': 'track', 'duration': '10:00'})
        # Direct evidence control: even apparently matching titles/timings must
        # not allow reuse of the same recording track for different target items.
        evidence = {'status': 'probable', 'programme': [
            {'target': t['title'], 'track_ids': [1]} for t in row['tracklist']]}
        self.assertEqual(check_programme(row, a, evidence, INVENTORY)['status'], 'unknown')

    def test_fixed_pilot_scope_and_alias_not_promoted(self):
        from qobuz_completeness import check_pilot
        rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
        report = check_pilot(json.loads((ROOT/'data/qobuz_coverage_pilot.json').read_text()),
                             rows, load_snapshot()['albums'], INVENTORY)
        self.assertEqual(report['summary']['releases_with_complete_candidate'], 11)
        self.assertEqual(report['summary']['releases_ready_for_probable_integration'], 10)
        cases = {r['discogs_id']: r for r in report['releases']}
        self.assertFalse(cases['2712474']['candidates'][0]['ready_for_probable_integration'])
        self.assertEqual(cases['3699703']['candidates'][0]['status'], 'unknown')
