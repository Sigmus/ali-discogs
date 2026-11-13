import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_match import evaluate, work_match, units


def track(title, performer='Alice Pianist', composer='Ludwig van Beethoven', ident=1):
    return {'id': ident, 'title': title, 'performers': f'{performer}, MainArtist, Piano - {composer}, Composer'}


def row(titles):
    return {'tracklist': [{'title': t, 'type': 'track'} for t in titles],
            'performers': ['Alice Pianist'], 'composers': ['Ludwig van Beethoven']}


class MatchTests(unittest.TestCase):
    def test_wrong_orchestra_blocks_match(self):
        target = row(['Symphony No. 3 Op. 55'])
        target.update(performers=['Erich Kleiber'], ensembles=['Royal Concertgebouw Orchestra'])
        t = track('Symphony No. 3 Op. 55: I. Allegro', 'Erich Kleiber')
        t['performers'] += ' - Wiener Philharmoniker, Orchestra'
        result = evaluate(target, {'tracks': {'items': [t]}})
        self.assertEqual(result['status'], 'unchecked')
        self.assertEqual(result['covered'], 0)

    def test_missing_programme_not_accepted_and_superset_is_probable(self):
        target = row(['Piano Sonata Op. 31 No. 2', 'Piano Sonata Op. 31 No. 3'])
        album = {'tracks': {'items': [track('Piano Sonata Op. 31 No. 2', ident=1)]}}
        self.assertEqual(evaluate(target, album)['status'], 'unchecked')
        album['tracks']['items'] += [track('Piano Sonata Op. 31 No. 3', ident=2), track('Piano Sonata Op. 28', ident=3)]
        self.assertEqual(evaluate(target, album)['status'], 'probable')

    def test_subdivision_catalogue_alias_and_ordinal_are_not_guessed(self):
        self.assertFalse(work_match('Sonata Op.31 No.2', 'Sonata Op.31 No.3'))
        self.assertFalse(work_match('Sonata L.104', 'Sonata K.159'))
        self.assertFalse(work_match('First Pavan and Galliard', 'Sixth Pavan and Galliard'))
        self.assertFalse(work_match('Allegro', 'Allegro'))
        self.assertFalse(work_match('Koln Part II c', 'Koln Pt. II A'))
        self.assertTrue(work_match('Koln Part II c', 'Koln Pt. II C'))
        self.assertFalse(work_match('Symphony Op.55', 'Symphony Op.55 (Excerpt)'))

    def test_standalone_items_not_discarded_by_work_headings(self):
        target = {'tracklist': [{'title': 'Concerto No.1', 'type': 'index'},
                                {'title': 'Allegro', 'type': 'track'},
                                {'title': 'Ballade Op.23', 'type': 'track'}]}
        self.assertEqual(units(target), ['Concerto No.1', 'Ballade Op.23'])

    def test_all_performers_and_composer_required(self):
        target = row(['Piano Sonata Op. 31 No. 2'])
        self.assertEqual(evaluate(target, {'tracks': {'items': [track('Piano Sonata Op. 31 No. 2')]}})['status'], 'found')
        bad = track('Piano Sonata Op. 31 No. 2', composer='Johannes Brahms')
        self.assertEqual(evaluate(target, {'tracks': {'items': [bad]}})['status'], 'unchecked')
        target['performers'].append('Bob Violinist')
        self.assertEqual(evaluate(target, {'tracks': {'items': [track('Piano Sonata Op. 31 No. 2')]}})['status'], 'unchecked')
