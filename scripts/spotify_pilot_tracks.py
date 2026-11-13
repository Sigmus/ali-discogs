"""Slow, resumable metadata-only Spotify track cache using the existing sp login."""
import argparse
import fcntl
import gzip
import json
from pathlib import Path
import re
import signal
import subprocess
import time
from qobuz_all_poc import Pace, StopRequested, now, save

ROOT=Path(__file__).resolve().parents[1]
OUTPUT=ROOT/'.spotify-poc/tracks'
# Token values stay inside this subprocess; only status or catalogue JSON returns.
BRIDGE=r'''
import json,sys
from sp import auth
from sp.clients import spotify
operation=sys.argv[1]
try:
 if operation=='refresh':
  with auth._refresh_lock():
   cached=auth._read_cache()
   if not cached:raise RuntimeError('Login required')
   if not auth._is_valid(cached):
    pkce=auth._pkce(open_browser=False)
    pkce.requests_timeout=20
    from requests.adapters import HTTPAdapter
    pkce._session.mount('https://',HTTPAdapter(max_retries=0))
    pkce.refresh_access_token(cached['refresh_token'])
    auth._secure_cache()
  print(json.dumps({'status':200,'response':{'ready':True}}))
 else:
  cached=auth._read_cache()
  if not cached or not auth._is_valid(cached):raise RuntimeError('Token expiry; review before refresh')
  status,text=spotify.api_request('GET',operation,cached['access_token'])
  print(json.dumps({'status':status,'response':json.loads(text) if status==200 else None}))
except Exception as exc:
 code=getattr(exc,'http_status',None)
 print(json.dumps({'status':code if isinstance(code,int) else 599,'response':None}))
 sys.exit(1)
'''


class PilotError(Exception):pass


def bridge(python,operation):
    try:
        run=subprocess.run([str(python),'-c',BRIDGE,operation],capture_output=True,text=True,timeout=45)
        value=json.loads(run.stdout)
    except (OSError,subprocess.TimeoutExpired,ValueError):
        raise PilotError('sp bridge/authentication/network failure; no retry.') from None
    if run.returncode or value['status']!=200:
        raise PilotError(f"Spotify/sp request failed (status {value['status']}); paused without retry.")
    return value['response']


def clean_track(t):
    fields=['id','name','disc_number','track_number','duration_ms']
    if any(k not in t for k in fields):raise PilotError('Incomplete Spotify track metadata.')
    return {**{k:t[k] for k in fields},'artists':[{'id':a.get('id'),'name':a['name'],'url':(a.get('external_urls') or {}).get('spotify')} for a in t.get('artists',[])],
            'url':(t.get('external_urls') or {}).get('spotify')}


def fetch_album(task,get):
    tracks=[];expected=task['total_tracks'];offset=0
    while offset<expected:
        page=get(offset)
        items=page.get('items')
        if page.get('total')!=expected or page.get('offset')!=offset or not isinstance(items,list) or not items or offset+len(items)>expected:
            raise PilotError('Spotify pagination/track count differs; review before resuming.')
        tracks.extend(clean_track(t) for t in items)
        positions=[(t['disc_number'],t['track_number']) for t in tracks]
        if len(set(positions))!=len(positions):raise PilotError('Repeated Spotify track positions/page.')
        offset=len(tracks)
    return {**task,'tracks':tracks,'saved_at':now(),'limitation':'Artist lists have no explicit composer/conductor/instrument roles; programme audit is not recording-session verification.'}


def restore_portable(path, output):
    with gzip.open(path,'rt') as f:data=json.load(f)
    if data.get('schema_version')!=1:raise PilotError('Unsupported portable Spotify schema.')
    albums=data['albums']
    for album in albums:
        if not re.fullmatch('[A-Za-z0-9]{22}',album['album_id']) or len(album['tracks'])!=album['total_tracks']:
            raise PilotError('Invalid portable Spotify album.')
        target=output/f"{album['album_id']}.json"
        if target.exists() and json.loads(target.read_text())!=album:
            raise PilotError('Existing Spotify cache differs; preserve it and review.')
    output.mkdir(parents=True,exist_ok=True)
    for album in albums:
        target=output/f"{album['album_id']}.json"
        if not target.exists():save(target,album)
    return len(albums)


def main():
    parser=argparse.ArgumentParser(description=__doc__);modes=parser.add_mutually_exclusive_group();modes.add_argument('--fetch',action='store_true');modes.add_argument('--restore',action='store_true')
    parser.add_argument('--sp-python',type=Path,default=ROOT.parent/'SP/.venv/bin/python');args=parser.parse_args()
    review=json.loads((ROOT/'data/qobuz_comparison_offline.json').read_text())['entries']
    plan=[{'discogs_id':e['discogs_id'],'album_id':e['spotify_album']['id'],'album_name':e['spotify_album']['name'],'total_tracks':e['cached_album']['total_tracks'],'market':'NL'} for e in review if e['category']=='spotify_review']
    if len(plan)!=10 or any(not re.fullmatch('[A-Za-z0-9]{22}',e['album_id']) for e in plan):raise PilotError('Invalid fixed Spotify pilot scope.')
    OUTPUT.mkdir(parents=True,exist_ok=True)
    lock=(OUTPUT/'run.lock').open('w');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    manifest=OUTPUT/'manifest.json'
    if manifest.exists() and json.loads(manifest.read_text())!=plan:raise PilotError('Spotify pilot scope changed; review before retrieval.')
    save(manifest,plan)
    stop=OUTPUT/'STOP'
    if stop.exists():print('Spotify pilot STOP exists; await user direction.');lock.close();return 1
    if args.restore:
        print(f'Restored/reused {restore_portable(ROOT/"data/spotify_pilot_tracks.json.gz",OUTPUT)} portable Spotify albums; no API calls.')
    prior=json.loads((OUTPUT/'progress.json').read_text()) if (OUTPUT/'progress.json').exists() else {}
    state={'status':'running' if args.fetch else 'offline','completed':0,'total':10,'started_at':now(),'last_http_epoch':prior.get('last_http_epoch',0),'network_attempts':0}
    pace=Pace(15,stop)
    for sig in [signal.SIGINT,signal.SIGTERM]:signal.signal(sig,lambda *_:setattr(pace,'stopping',True))
    def checkpoint():state['updated_at']=now();save(OUTPUT/'progress.json',state)
    def request(operation):
        pace.check()
        if pace.requests and pace.requests%50==0:
            state['rest_until_epoch']=time.time()+120;checkpoint();pace.wait(120);state.pop('rest_until_epoch',None)
        pace.wait(max(0,15-(time.time()-state['last_http_epoch'])))
        pace();state['last_http_epoch']=time.time();state['network_attempts']=pace.requests;checkpoint()
        return bridge(args.sp_python,operation)
    checkpoint();ready=False;albums=[]
    try:
        for task in plan:
            pace.check();state['current_release']=task['discogs_id'];checkpoint()
            path=OUTPUT/f"{task['album_id']}.json"
            if path.exists():
                album=json.loads(path.read_text())
                if any(album.get(k)!=v for k,v in task.items()) or len(album['tracks'])!=task['total_tracks']:raise PilotError('Saved Spotify album differs from fixed scope.')
            else:
                if not args.fetch:raise PilotError('Offline Spotify cache incomplete; no API requests made.')
                if not ready:request('refresh');ready=True
                def get(offset):
                    page_path=OUTPUT/f"{task['album_id']}-page-{offset}.json"
                    if page_path.exists():return json.loads(page_path.read_text())
                    page=request(f"/albums/{task['album_id']}/tracks?market=NL&limit=50&offset={offset}")
                    safe={'total':page.get('total'),'offset':page.get('offset'),'items':[clean_track(t) for t in page.get('items',[])]}
                    # Preserve API artist shape only in the in-memory replay adapter.
                    save(page_path,safe);return safe
                # Pages are already whitelisted; avoid sanitizing artists twice.
                def adapted(offset):
                    page=get(offset)
                    return {**page,'items':[{**t,'external_urls':{'spotify':t.get('url')},'artists':[{**a,'external_urls':{'spotify':a.get('url')}} for a in t['artists']]} for t in page['items']]}
                album=fetch_album(task,adapted);save(path,album)
            albums.append(album);state['completed']+=1;checkpoint();print(f"{state['completed']}/10 release={task['discogs_id']} tracks={len(album['tracks'])}",flush=True)
        output={'schema_version':1,'source':'Spotify album-tracks API via local sp PKCE login; no credentials/audio','albums':albums}
        (ROOT/'data/spotify_pilot_tracks.json.gz').write_bytes(gzip.compress(json.dumps(output,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode(),mtime=0))
        state['status']='complete';state.pop('current_release',None)
    except StopRequested:state['status']='stopped';state['reason']='User stop; no automatic resume.'
    except Exception as exc:
        state['status']='failed' if args.fetch else 'offline_incomplete'
        state['reason']=str(exc) if isinstance(exc,PilotError) else 'Unexpected Spotify/local metadata error; review required.'
        if args.fetch:stop.touch()
        print(state['reason'],flush=True)
    finally:checkpoint();lock.close()
    return 0 if state['status']=='complete' else 1


if __name__=='__main__':raise SystemExit(main())
