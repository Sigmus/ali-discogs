"""Prepare a fixed 30-release comparison, then explicitly run slow fallback searches."""
import argparse
import fcntl
import gzip
import hashlib
import json
import signal
import time
from pathlib import Path

from qobuz_all_poc import Pace, StopRequested, now, save
from qobuz_catalog import Catalog, CatalogError, ROOT
from qobuz_match import catalogue, evaluate, norm, units, VERSION
from qobuz_snapshot import load_snapshot, album_fields, select, TRACK_FIELDS

SCOPE = ROOT/'data/qobuz_comparison_scope.json'
OUTPUT = ROOT/'.qobuz-poc/comparison'


def spread(items, n):
    if len(items) < n:
        raise ValueError('Insufficient disjoint sample population')
    return [items[i * (len(items) - 1) // (n - 1)] for i in range(n)]


def prepare():
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    reviews = json.loads((ROOT/'data/qobuz_matches.json').read_text())['releases']
    snapshot = load_snapshot()
    if not SCOPE.exists():
        known = ['6381208','6599326','8252155','8121703','5820114','6678433','9739139','13069435','4841406','3198796']
        unresolved = [rid for rid in known if reviews[rid]['status'] == 'unchecked' and reviews[rid]['candidates']]
        if len(unresolved) != 10:
            raise ValueError('Review unresolved sample selection before proceeding')
        empty = spread(sorted([rid for rid in rows if reviews[rid]['status'] == 'unchecked' and not snapshot['searches'][rid]['search']['albums']['items']], key=int), 10)
        used = set(empty + unresolved)
        spotify = []
        for status in ['found', 'probable']:
            spotify.extend(spread(sorted([rid for rid,r in rows.items() if rid not in used and r['spotify']['status'] == status], key=int), 5))
        entries = []
        for category, ids in [('qobuz_empty', empty), ('qobuz_unresolved', unresolved), ('spotify_review', spotify)]:
            for rid in ids:
                row = rows[rid]
                person = (row.get('key_performers') or row.get('performers') or row.get('ensembles') or [''])[0]
                composer = (row.get('composers') or [''])[0]
                queries = []
                if category == 'qobuz_empty':
                    queries.append(' '.join(filter(None, [norm(person), norm(composer).split()[-1] if norm(composer) else ''])))
                    ids_found = sorted(set().union(*(catalogue(t) for t in units(row)))) if units(row) else []
                    if ids_found:
                        kind, number, sub = ids_found[0]
                        queries.append(' '.join(filter(None,[norm(person).split()[-1] if norm(person) else '',norm(composer).split()[-1] if norm(composer) else '',kind,number,sub])))
                    else:
                        queries.append(' '.join(filter(None,[norm(person), ' '.join(norm(row['title']).split()[:3])])))
                    queries = list(dict.fromkeys(queries))
                    queries = [q for q in queries if q and q != snapshot['searches'][rid]['query']]
                entries.append({'discogs_id':rid,'title':row['title'],'category':category,'queries':queries})
        if len({e['discogs_id'] for e in entries}) != 30:
            raise ValueError('Sample is not disjoint')
        scope = {'schema_version':1,'selected_on':'2026-11-13','selection':'10 evenly spaced empty-result IDs; 10 purposive unresolved failure controls; 5 Found and 5 Probable Spotify IDs evenly spaced within status, all disjoint. Not a random or representative catalogue sample.',
                 'entries':entries,'collection_sha256':hashlib.sha256((ROOT/'data/collection_matches.json').read_bytes()).hexdigest()}
        save(SCOPE,scope)
    scope = json.loads(SCOPE.read_text())
    if scope.get('schema_version') != 1 or scope['collection_sha256'] != hashlib.sha256((ROOT/'data/collection_matches.json').read_bytes()).hexdigest():
        raise ValueError('Collection or scope changed; review before replay or API calls')
    OUTPUT.mkdir(parents=True,exist_ok=True)
    tasks = [{'discogs_id':e['discogs_id'],'query':q} for e in scope['entries'] for q in e['queries']]
    manifest = {'fingerprint':hashlib.sha256(json.dumps(tasks,sort_keys=True).encode()).hexdigest(),'entries':tasks}
    path = OUTPUT/'manifest.json'
    if path.exists() and json.loads(path.read_text()) != manifest:
        raise ValueError('Search plan changed; preserve evidence and review before resuming')
    save(path,manifest)
    return scope,rows,snapshot,manifest


def search(manifest, *, metadata=False):
    lock = (OUTPUT/'run.lock').open('w')
    fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    stop = OUTPUT/'STOP'
    if stop.exists():
        lock.close();print('STOP present; await user direction.');return 1
    previous = json.loads((OUTPUT/'progress.json').read_text()) if (OUTPUT/'progress.json').exists() else {}
    pace = Pace(15,stop)
    for sig in [signal.SIGINT,signal.SIGTERM]:
        signal.signal(sig,lambda *_:setattr(pace,'stopping',True))
    state = {'status':'running','phase':'metadata' if metadata else 'search','started_at':now(),'completed':0,'total':len(manifest['entries']),'network_attempts':0,'last_http_epoch':previous.get('last_http_epoch',0)}
    def checkpoint():
        state['updated_at']=now();save(OUTPUT/'progress.json',state)
    def before_request():
        if pace.requests and pace.requests % 50 == 0:
            state['status']='resting';state['rest_until_epoch']=time.time()+120;checkpoint();pace.wait(120)
            state['status']='running';state.pop('rest_until_epoch',None)
        pace.wait(max(0,15-(time.time()-state['last_http_epoch'])))
        pace()
        state['last_http_epoch']=time.time();state['network_attempts']=pace.requests;checkpoint()
    catalog = Catalog(before_request=before_request)
    checkpoint()
    try:
        for i,task in enumerate(manifest['entries']):
            pace.check();state['current_release']=task['discogs_id'];checkpoint()
            path=OUTPUT/f"{'metadata' if metadata else 'search'}-{i:02d}.json"
            if path.exists():
                saved=json.loads(path.read_text())
                if saved['task']!=task:raise CatalogError('Saved query differs from fixed plan.')
                data=saved['album' if metadata else 'search']
            else:
                if metadata:
                    from qobuz_metadata_poc import fetch_complete_album
                    data=fetch_complete_album(catalog,task['album_id'])
                    tracks=data['tracks']['items']
                    if len({t['id'] for t in tracks}) != len(tracks):
                        raise CatalogError('Duplicate track IDs; incomplete metadata evidence.')
                else:
                    data=catalog.fetch('catalog/search',query=task['query'],type='albums',limit=5)
                save(path,{'task':task,'saved_at':now(),'album' if metadata else 'search':data})
            state['completed']=i+1;checkpoint()
            count=len(data['tracks']['items']) if metadata else len(data['albums']['items'])
            print(f"{i+1}/{len(manifest['entries'])} release={task['discogs_id']} {'tracks' if metadata else 'candidates'}={count}",flush=True)
        state['status']='complete';state.pop('current_release',None)
    except StopRequested:
        state['status']='stopped';state['reason']='Stop requested; no automatic resume.'
    except Exception as exc:
        stop.touch();state['status']='failed'
        state['reason']=str(exc) if isinstance(exc,CatalogError) else 'Unexpected local/API failure; review before resuming.'
        print(state['reason'],flush=True)
    finally:
        catalog.close();checkpoint();lock.close()
    return 0 if state['status']=='complete' else 1


def offline_report(scope,rows,snapshot):
    selected = {}
    for e in scope['entries']:
        if e['category']=='spotify_review':
            sp=rows[e['discogs_id']]['spotify'];a=sp.get('album') or sp.get('best_candidate')
            if a:selected[a['id']]=None
    for path in sorted((ROOT/'raw/spotify').glob('*.json')):
        response=json.loads(path.read_text()).get('resp',{})
        for a in response.get('albums',{}).get('items',[]):
            if a['id'] in selected:selected[a['id']]={k:a[k] for k in ['id','name','artists','total_tracks','release_date'] if k in a}
    result=[]
    for e in scope['entries']:
        row=rows[e['discogs_id']];r={**e,'discogs_programme':row['tracklist'], 'expected_performers': list(dict.fromkeys([*(row.get('performers') or []), *(row.get('ensembles') or []), *([row['conductor']] if row.get('conductor') else [])])), 'expected_composers':row.get('composers',[])}
        if e['category']=='spotify_review':
            sp=row['spotify'];a=sp.get('album') or sp.get('best_candidate')
            r.update(spotify_status=sp['status'],spotify_album=a,signals=sp.get('signals',{}),cached_album=selected.get(a['id']) if a else None,
                     limitation='Spotify search cache has album metadata only; movement/recording-credit validation is unavailable. No Spotify API calls made.')
        elif e['category']=='qobuz_unresolved':
            r['candidates']=[{'album_id':str(a['id']),**evaluate(row,snapshot['albums'][str(a['id'])])} for a in snapshot['searches'][e['discogs_id']]['search']['albums']['items']]
        result.append(r)
    save(ROOT/'data/qobuz_comparison_offline.json',{'schema_version':1,'selection':scope['selection'],'collection_sha256':scope['collection_sha256'],'matcher_version':VERSION,'entries':result})


def export_evidence(manifest):
    meta_scope=json.loads((ROOT/'data/qobuz_comparison_metadata_scope.json').read_text())
    searches=[]
    for i,task in enumerate(manifest['entries']):
        raw=json.loads((OUTPUT/f'search-{i:02d}.json').read_text())
        if raw['task'] != task:raise ValueError('Saved search task mismatch')
        searches.append({'task':task,'saved_at':raw['saved_at'],'search':{'albums':{'items':[album_fields(a) for a in raw['search']['albums']['items']]}}})
    metadata=[]
    for i,task in enumerate(meta_scope['entries']):
        raw=json.loads((OUTPUT/f'metadata-{i:02d}.json').read_text())
        if raw['task'] != task:raise ValueError('Saved metadata task mismatch')
        source=raw['album']
        if str(source['id']) != task['album_id']:raise ValueError('Saved metadata album ID mismatch')
        album=album_fields(source);tracks=[]
        for t in source['tracks']['items']:
            track=select(t,TRACK_FIELDS)
            for k in ['composer','performer']:
                if isinstance(t.get(k),dict):track[k]=select(t[k],['id','name'])
            tracks.append(track)
        if len(tracks)!=source['tracks_count'] or len({t['id'] for t in tracks})!=len(tracks):
            raise ValueError('Incomplete metadata cannot be exported')
        album['tracks']={'items':tracks,'total':len(tracks),'offset':0}
        metadata.append({'task':task,'saved_at':raw['saved_at'],'album':album})
    result={'schema_version':1,'searches':searches,'metadata':metadata,
        'scope_sha256':hashlib.sha256(SCOPE.read_bytes()).hexdigest(),
        'metadata_scope_sha256':hashlib.sha256((ROOT/'data/qobuz_comparison_metadata_scope.json').read_bytes()).hexdigest()}
    (ROOT/'data/qobuz_comparison_evidence.json.gz').write_bytes(gzip.compress(json.dumps(result,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode(),mtime=0))
    print(f'Exported {len(searches)} queries / {len(metadata)} complete albums, no credentials.')


def comparison_report(scope,rows,snapshot):
    from qobuz_completeness import check_programme
    inventory=json.loads((ROOT/'data/qobuz_work_inventory.json').read_text())
    with gzip.open(ROOT/'data/qobuz_comparison_evidence.json.gz','rt') as f:evidence=json.load(f)
    if evidence['scope_sha256']!=hashlib.sha256(SCOPE.read_bytes()).hexdigest():
        raise ValueError('Portable evidence scope differs')
    if evidence['metadata_scope_sha256']!=hashlib.sha256((ROOT/'data/qobuz_comparison_metadata_scope.json').read_bytes()).hexdigest():
        raise ValueError('Portable metadata scope differs')
    albums={**snapshot['albums'],**{str(m['album']['id']):m['album'] for m in evidence['metadata']}}
    results=[]
    for entry in scope['entries']:
        rid=entry['discogs_id'];row=rows[rid]
        if entry['category']!='qobuz_empty':continue
        queries=[s for s in evidence['searches'] if s['task']['discogs_id']==rid]
        hits={str(a['id']):a for s in queries for a in s['search']['albums']['items']}
        candidates=[]
        for aid,hit in hits.items():
            candidate={'album_id':aid,'title':hit['title'],'artist':(hit.get('artist') or {}).get('name','')}
            if aid in albums:
                assessed=evaluate(row,albums[aid])
                candidate.update(evidence=assessed,completeness=check_programme(row,albums[aid],assessed,inventory))
            else:candidate['limitation']='No full metadata selected or available; search hit only.'
            candidates.append(candidate)
        results.append({**entry,'unique_search_hits':len(hits),'query_results':[{'query':s['task']['query'],'hits':len(s['search']['albums']['items'])} for s in queries],'candidates':candidates})
    result={'schema_version':1,'selection':scope['selection'],'qobuz_empty_group':results,
        'summary':{'originally_empty_releases':len(results),'fallback_queries':len(evidence['searches']),
            'releases_with_hits':sum(r['unique_search_hits']>0 for r in results),
            'query_hit_count':sum(s['search']['albums']['items']!=[] for s in evidence['searches']),
            'full_metadata_albums_selected':len(evidence['metadata']),
            'selected_metadata_already_in_snapshot':sum(str(m['album']['id']) in snapshot['albums'] for m in evidence['metadata']),
            'releases_with_programme_credit_lead':sum(any(c.get('evidence',{}).get('status') in ['found','probable'] for c in r['candidates']) for r in results),
            'releases_with_complete_programme_credit_lead':sum(any(c.get('evidence',{}).get('status') in ['found','probable'] and c.get('completeness',{}).get('status')=='complete' for c in r['candidates']) for r in results)},
        'limitations':['Search hits are not accepted matches. Publication untouched.','Spotify ten-case cached album review has no track-level verification; see offline report.','Purposive/ID-stratified sample; no catalogue precision/recall estimate.'],
        'provenance':{'matcher_version':VERSION,'evidence_sha256':hashlib.sha256((ROOT/'data/qobuz_comparison_evidence.json.gz').read_bytes()).hexdigest(),'snapshot_metadata_completed_at':snapshot['metadata_completed_at']}}
    save(ROOT/'data/qobuz_comparison_results.json',result)
    print(json.dumps(result['summary']))


def main():
    parser=argparse.ArgumentParser(description=__doc__);modes=parser.add_mutually_exclusive_group();modes.add_argument('--search',action='store_true');modes.add_argument('--metadata',action='store_true');modes.add_argument('--export',action='store_true');modes.add_argument('--report',action='store_true');args=parser.parse_args()
    scope,rows,snapshot,manifest=prepare()
    offline_report(scope,rows,snapshot)
    print(f"Prepared {len(scope['entries'])} releases / {len(manifest['entries'])} fallback queries.",flush=True)
    if args.export:export_evidence(manifest);return 0
    if args.report:comparison_report(scope,rows,snapshot);return 0
    if args.search:return search(manifest)
    if args.metadata:
        scope_path=ROOT/'data/qobuz_comparison_metadata_scope.json'
        metadata_scope=json.loads(scope_path.read_text())
        entries=metadata_scope['entries']
        if not 1 <= len(entries) <= 10 or any(not e['album_id'].isalnum() for e in entries):
            raise ValueError('Metadata scope exceeds bounded pilot or has invalid album IDs')
        if len(list(OUTPUT.glob('search-*.json'))) != len(manifest['entries']):
            raise ValueError('Complete the fixed search stage before fetching metadata')
        return search({'entries':entries},metadata=True)
    return 0


if __name__=='__main__':
    raise SystemExit(main())
