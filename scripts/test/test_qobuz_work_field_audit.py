import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from qobuz_work_field_audit import with_work_context


class WorkFieldAuditTests(unittest.TestCase):
    def test_uses_explicit_work_without_mutating_source(self):
        album={'tracks':{'items':[{'title':'1. Allegro','work':'Piano Sonata Op.5','performers':'Julius Katchen, MainArtist','composer':{'name':'Johannes Brahms'}}]}}
        before=copy.deepcopy(album)
        out=with_work_context(album,'Julius Katchen','Johannes Brahms')
        self.assertEqual(out['tracks']['items'][0]['title'],'Piano Sonata Op.5: 1. Allegro')
        self.assertEqual(album,before)

    def test_no_work_guessing_or_artist_credit_repair(self):
        base={'title':'1. Allegro','work':'Piano Sonata Op.5','performers':'Julius Katchen, MainArtist','composer':{'name':'Johannes Brahms'}}
        for changes in [{'work':None},{'work':'Piano Sonata'},{'performers':'Another Pianist, MainArtist'},{'composer':{'name':'Another Composer'}},{'title':'1. Allegro Op.1'}]:
            track={**base,**changes};album={'tracks':{'items':[track]}}
            self.assertEqual(with_work_context(album,'Julius Katchen','Johannes Brahms'),album)
