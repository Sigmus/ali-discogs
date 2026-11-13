import sys
from pathlib import Path
import unittest
from unittest.mock import Mock,patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from spotify_pilot_tracks import fetch_album,clean_track,bridge,PilotError


def track(n):return {'id':f'id{n}','name':f'Track {n}','disc_number':1,'track_number':n,'duration_ms':1000,'artists':[{'id':'artist','name':'Alice'}],'preview_url':'DO_NOT_EXPORT'}


class SpotifyPilotTests(unittest.TestCase):
    def test_pagination_preserves_all_tracks_and_drops_audio(self):
        get=Mock(side_effect=[{'offset':0,'total':3,'items':[track(1),track(2)]},{'offset':2,'total':3,'items':[track(3)]}])
        result=fetch_album({'total_tracks':3},get)
        self.assertEqual(len(result['tracks']),3)
        self.assertEqual(get.call_args_list[1].args,(2,))
        self.assertNotIn('preview_url',result['tracks'][0])

    def test_changed_total_and_repeated_pages_are_rejected(self):
        for page in [{'offset':0,'total':4,'items':[track(1)]},{'offset':0,'total':2,'items':[track(1),track(1)]}]:
            with self.assertRaises(PilotError):fetch_album({'total_tracks':2},Mock(return_value=page))

    def test_auth_rejection_is_not_retried_or_exposed(self):
        run=Mock(returncode=1,stdout='{"status":401,"response":null}',stderr='private details')
        with patch('spotify_pilot_tracks.subprocess.run',return_value=run) as call:
            with self.assertRaises(PilotError) as error:bridge(Path('/python'),'refresh')
            self.assertEqual(call.call_count,1)
            self.assertNotIn('private',str(error.exception))

    def test_portable_restore_refuses_conflict_without_partial_writes(self):
        import gzip,json,tempfile
        from spotify_pilot_tracks import restore_portable
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);path=root/'evidence.gz';output=root/'cache';output.mkdir()
            albums=[{'album_id':'a'*22,'total_tracks':1,'tracks':[clean_track(track(1))]},
                    {'album_id':'b'*22,'total_tracks':1,'tracks':[clean_track(track(2))]}]
            path.write_bytes(gzip.compress(json.dumps({'schema_version':1,'albums':albums}).encode()))
            (output/('b'*22+'.json')).write_text('{}')
            from spotify_pilot_tracks import PilotError
            with self.assertRaises(PilotError):restore_portable(path,output)
            self.assertFalse((output/('a'*22+'.json')).exists())
            (output/('b'*22+'.json')).unlink()
            self.assertEqual(restore_portable(path,output),2)


class BoundedScopeTests(unittest.TestCase):
    def test_scoped_export_checkpoint_and_offline_reuse(self):
        import json,gzip,tempfile
        from unittest.mock import patch,Mock
        from spotify_pilot_tracks import main
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);scope=root/'scope.json';output=root/'worker';archive=root/'portable.gz'
            scope.write_text(json.dumps({'schema_version':1,'entries':[{'discogs_id':'1','album_id':'a'*22,'album_name':'Album','total_tracks':1,'market':'NL'}]}))
            page={'total':1,'offset':0,'items':[track(1)]}
            pace=Mock();pace.requests=0
            args=['worker','--scope',str(scope),'--output',str(output),'--archive',str(archive),'--fetch']
            with patch('sys.argv',args),patch('spotify_pilot_tracks.Pace',return_value=pace),patch('spotify_pilot_tracks.bridge',side_effect=[{'ready':True},page]) as call:
                self.assertEqual(main(),0)
                self.assertEqual(call.call_count,2)
            self.assertEqual(json.loads((output/'progress.json').read_text())['status'],'complete')
            first=archive.read_bytes()
            self.assertEqual(len(json.loads(gzip.decompress(first))['albums']),1)
            with patch('sys.argv',args[:-1]),patch('spotify_pilot_tracks.bridge') as call:
                self.assertEqual(main(),0);call.assert_not_called()
            self.assertEqual(first,archive.read_bytes())

    def test_scoped_first_warning_stops_without_retry(self):
        import json,tempfile
        from unittest.mock import patch,Mock
        from spotify_pilot_tracks import main,PilotError
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);scope=root/'scope.json';output=root/'worker';archive=root/'portable.gz'
            scope.write_text(json.dumps({'schema_version':1,'entries':[{'discogs_id':'1','album_id':'a'*22,'album_name':'Album','total_tracks':1,'market':'NL'}]}))
            args=['worker','--scope',str(scope),'--output',str(output),'--archive',str(archive),'--fetch']
            pace=Mock();pace.requests=0
            with patch('sys.argv',args),patch('spotify_pilot_tracks.Pace',return_value=pace),patch('spotify_pilot_tracks.bridge',side_effect=PilotError('HTTP 429')) as call:
                self.assertEqual(main(),1);self.assertEqual(call.call_count,1)
            self.assertTrue((output/'STOP').exists());self.assertFalse(archive.exists())
            with patch('sys.argv',args),patch('spotify_pilot_tracks.bridge') as call:
                self.assertEqual(main(),1);call.assert_not_called()

    def test_duplicate_track_ids_with_distinct_positions_are_rejected(self):
        duplicate=dict(track(2),id=track(1)['id'])
        with self.assertRaises(PilotError):
            fetch_album({'total_tracks':2},Mock(return_value={'offset':0,'total':2,'items':[track(1),duplicate]}))
