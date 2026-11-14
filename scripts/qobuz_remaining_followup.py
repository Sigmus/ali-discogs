"""Nine explicitly authorized metadata albums; resumable, no searches/publication."""
import argparse
import gzip
import hashlib
import json
from qobuz_match import ROOT
from qobuz_snapshot import album_fields,select,TRACK_FIELDS
import qobuz_comparison_pilot as runner

SCOPE=ROOT/'data/qobuz_remaining_metadata_followup_scope.json'
OUTPUT=ROOT/'.qobuz-poc/remaining-followup-2026-11-14'
ARCHIVE=ROOT/'data/qobuz_remaining_followup_metadata.json.gz'
EXPECTED=['0002894133212','0825646180943','3610156779780','5099996593059','v96ulyegxutlc','0886444299039','0883629934709','0002894557942','0002894552472']

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def prepare():
    scope=json.loads(SCOPE.read_text())
    if scope['schema_version']!=1 or [e['album_id'] for e in scope['entries']]!=EXPECTED or sum(len(e['discogs_ids']) for e in scope['entries'])!=11:
        raise ValueError('Nine-album/eleven-release scope changed')
    if digest(ROOT/'data/collection_matches.json')!=scope['collection_sha256'] or digest(ROOT/'data/qobuz_remaining_search.json.gz')!=scope['search_evidence_sha256']:
        raise ValueError('Frozen source evidence changed')
    OUTPUT.mkdir(parents=True,exist_ok=True)
    path=OUTPUT/'manifest.json'
    if not path.exists() and digest(ROOT/'data/qobuz_remaining_screen.json')!=scope['screen_sha256']:
        raise ValueError('Screen changed before first retrieval; review scope')
    tasks=[{'discogs_id':e['discogs_ids'][0],'album_id':e['album_id']} for e in scope['entries']]
    manifest={'entries':tasks,'fingerprint':hashlib.sha256(json.dumps(tasks,sort_keys=True).encode()).hexdigest(),'scope_sha256':digest(SCOPE)}
    if path.exists() and json.loads(path.read_text())!=manifest:raise ValueError('Manifest changed; preserve checkpoints')
    runner.save(path,manifest)
    return manifest

def export(manifest):
    metadata=[]
    for i,task in enumerate(manifest['entries']):
        path=OUTPUT/f'metadata-{i:02d}.json'
        if not path.exists():continue
        record=json.loads(path.read_text());a=record['album'];tracks=a['tracks']['items']
        if record['task']!=task or str(a['id'])!=task['album_id'] or len(tracks)!=a['tracks_count'] or len({t['id'] for t in tracks})!=len(tracks):
            (OUTPUT/'STOP').touch();raise ValueError('Incomplete/mismatched metadata; stopped')
        album=album_fields(a);items=[]
        for t in tracks:
            item=select(t,TRACK_FIELDS)
            for key in ['composer','performer']:
                if isinstance(t.get(key),dict):item[key]=select(t[key],['id','name'])
            items.append(item)
        album['tracks']={'items':items,'total':len(items),'offset':0}
        metadata.append({'task':task,'saved_at':record['saved_at'],'album':album})
    payload={'schema_version':1,'scope_sha256':digest(SCOPE),'completed':len(metadata),'total':9,'metadata':metadata}
    ARCHIVE.write_bytes(gzip.compress(json.dumps(payload,ensure_ascii=False,sort_keys=True).encode(),mtime=0))
    print('Exported',len(metadata),'/9 albums;',sum(len(x['album']['tracks']['items']) for x in metadata),'tracks',flush=True)
    return payload

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--fetch',action='store_true');parser.add_argument('--export',action='store_true');args=parser.parse_args();manifest=prepare()
    if args.export:export(manifest);return 0
    if not args.fetch:print('Prepared fixed manifest offline; --fetch retrieves metadata.');return 0
    runner.OUTPUT=OUTPUT
    result=runner.search(manifest,metadata=True)
    export(manifest)
    return result

if __name__=='__main__':raise SystemExit(main())
