"""Offline screen must reject incomplete metadata and never change publication."""
import copy
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qobuz_remaining_screen import ROOT, screen, validate_album

class RemainingScreenTests(unittest.TestCase):
    def test_metadata_fails_closed(self):
        album={'id':'test','tracks_count':2,'tracks':{'items':[{'id':1},{'id':2}]}}
        validate_album(album)
        for tracks in [[{'id':1}], [{'id':1},{'id':1}]]:
            changed=copy.deepcopy(album);changed['tracks']['items']=tracks
            with self.assertRaises(ValueError):validate_album(changed)

    def test_screen_is_offline_and_preserves_published_matches(self):
        publication=ROOT/'data/qobuz_matches.json';before=publication.read_bytes()
        with patch('requests.sessions.Session.request',side_effect=AssertionError('Network forbidden')):
            report=screen()
        self.assertEqual(publication.read_bytes(),before)
        entries=report['entries']
        self.assertEqual(len(entries),len({(e['discogs_id'],e['album_id']) for e in entries}))
        self.assertTrue(all(e['cached_complete_metadata'] for e in entries if e['finding']=='needs_recording_review'))
        self.assertTrue(all(e['assessment']['status']!='unchecked' and e['completeness']['status']=='complete' for e in entries if e['finding']=='needs_recording_review'))
