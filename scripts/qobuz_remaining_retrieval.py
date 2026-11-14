"""Fixed remaining retrieval: metadata for12release leads, then305fallback searches."""
import argparse,gzip,hashlib,json
from qobuz_match import ROOT,norm
from qobuz_query_plan import propose,composer_term
from qobuz_query_trial import trial_lead
from qobuz_snapshot import album_fields,select,TRACK_FIELDS
import qobuz_comparison_pilot as runner

BASE=ROOT/'.qobuz-poc/remaining-2026-11-14'
SCOPE=ROOT/'data/qobuz_remaining_scope.json'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def prepare():
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    if not SCOPE.exists():
        audit=json.loads((ROOT/'data/qobuz_unmatched_audit.json').read_text())
        mids={e['discogs_id'] for e in audit['entries'] if e['category']=='metadata_needed'}
        empties=[e['discogs_id'] for e in audit['entries'] if e['category']=='no_saved_hits']
        if len(mids)!=12 or len(empties)!=305:raise ValueError('Expected12metadata-needed and305empty releases; review current scope')
        hits={rid:{} for rid in mids};known=set();queries={}
        for path in sorted((ROOT/'data').glob('qobuz*.json.gz')):
            data=json.loads(gzip.decompress(path.read_bytes()))
            if not isinstance(data,dict):continue
            known.update(data.get('albums',{}).keys())
            for x in data.get('metadata',[]):known.add(str(x['album']['id']))
            records=data.get('results',[])
            searches=data.get('searches',[])
            if isinstance(searches,dict):
                records=records+[{'task':{'discogs_id':rid,'query':v.get('query','')},'albums':v['search']['albums']['items']} for rid,v in searches.items()]
            else:records=records+[{'task':x['task'],'albums':x['search']['albums']['items']} for x in searches]
            for x in records:
                if not isinstance(x,dict) or 'task' not in x or 'albums' not in x:continue
                rid=str(x['task']['discogs_id']);queries.setdefault(rid,set()).add(x['task'].get('query',''))
                if rid in hits:
                    for a in x['albums']:hits[rid][str(a['id'])]=a
        metadata=[];seen=set()
        for rid in sorted(mids,key=int):
            for aid,a in sorted(hits[rid].items()):
                if aid in known or aid in seen:continue
                metadata.append({'discogs_id':rid,'album_id':aid,'title':a['title']});seen.add(aid)
        search=[]
        for rid in empties:
            row=rows[rid];person=norm(trial_lead(row));cs=list(dict.fromkeys(composer_term(c) for c in row.get('composers',[])))
            base=' '.join(filter(None,[person,cs[0] if cs else '']))
            options=[base,*propose(row),' '.join(filter(None,[person,' '.join(norm(row['title']).split()[:5])]))]
            chosen=list(dict.fromkeys(q for q in options if q and q not in queries.get(rid,set())))[:2]
            if not chosen:raise ValueError('No new query for '+rid)
            search.extend({'discogs_id':rid,'query':q} for q in chosen)
        scope={'schema_version':1,'created_on':'2026-11-14','collection_sha256':digest(ROOT/'data/collection_matches.json'),'metadata_release_ids':sorted(mids,key=int),'empty_release_ids':empties,'metadata':metadata,'search':search,'policy':'All uncached saved candidate albums for12metadata-needed releases, deduplicated by albumID; up to2new short queries for each305empty release. Metadata/search only, no automatic acceptance or new-hit metadata expansion.'}
        runner.save(SCOPE,scope)
    scope=json.loads(SCOPE.read_text())
    if scope['collection_sha256']!=digest(ROOT/'data/collection_matches.json'):raise ValueError('Collection changed')
    BASE.mkdir(parents=True,exist_ok=True)
    for phase in ['metadata','search']:
        folder=BASE/phase;folder.mkdir(exist_ok=True)
        tasks=[{k:v for k,v in x.items() if k!='title'} for x in scope[phase]]
        manifest={'entries':tasks,'fingerprint':hashlib.sha256(json.dumps(tasks,sort_keys=True).encode()).hexdigest()}
        path=folder/'manifest.json'
        if path.exists() and json.loads(path.read_text())!=manifest:raise ValueError('Fixed manifest changed')
        runner.save(path,manifest)
    return scope

def export(phase):
    folder=BASE/phase;manifest=json.loads((folder/'manifest.json').read_text());records=[]
    for i,task in enumerate(manifest['entries']):
        path=folder/f'{phase}-{i:02d}.json'
        if not path.exists():continue
        x=json.loads(path.read_text())
        if x['task']!=task:raise ValueError('Saved task mismatch')
        if phase=='search':record={'task':task,'saved_at':x['saved_at'],'albums':[album_fields(a) for a in x['search']['albums']['items']]}
        else:
            a=x['album'];tracks=a['tracks']['items']
            if str(a['id'])!=task['album_id'] or len(tracks)!=a['tracks_count'] or len({t['id'] for t in tracks})!=len(tracks):raise ValueError('Incomplete metadata')
            album=album_fields(a);items=[]
            for t in tracks:
                item=select(t,TRACK_FIELDS)
                for key in ['composer','performer']:
                    if isinstance(t.get(key),dict):item[key]=select(t[key],['id','name'])
                items.append(item)
            album['tracks']={'items':items,'total':len(items),'offset':0}
            record={'task':task,'saved_at':x['saved_at'],'album':album}
        records.append(record)
    payload={'schema_version':1,'scope_sha256':digest(SCOPE),'completed':len(records),'total':len(manifest['entries']), 'metadata' if phase=='metadata' else 'results':records}
    (ROOT/f'data/qobuz_remaining_{phase}.json.gz').write_bytes(gzip.compress(json.dumps(payload,ensure_ascii=False,sort_keys=True).encode(),mtime=0))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run',action='store_true');p.add_argument('--export',action='store_true');args=p.parse_args();scope=prepare()
    if args.export:
        for phase in ['metadata','search']:export(phase)
        return 0
    if not args.run:
        print(json.dumps({'metadata_albums':len(scope['metadata']),'search_queries':len(scope['search']),'search_releases':len(scope['empty_release_ids'])}));return 0
    for phase in ['metadata','search']:
        if (BASE/'STOP').exists():return 1
        runner.OUTPUT=BASE/phase
        manifest=json.loads((runner.OUTPUT/'manifest.json').read_text())
        try:
            result=runner.search(manifest,metadata=phase=='metadata')
            export(phase)
            if result:(BASE/'STOP').touch();return result
        except Exception:
            (BASE/'STOP').touch();raise
    runner.save(BASE/'complete.json',{'status':'complete','scope_sha256':digest(SCOPE)})
    return 0
if __name__=='__main__':raise SystemExit(main())
