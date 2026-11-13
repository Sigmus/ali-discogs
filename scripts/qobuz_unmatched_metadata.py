"""Explicit paced retrieval for the four fixed unmatched metadata leads."""
import argparse
import gzip
import hashlib
import json
from qobuz_match import ROOT
from qobuz_snapshot import album_fields, select, TRACK_FIELDS
import qobuz_comparison_pilot as runner


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch',action='store_true')
    args=parser.parse_args()
    path=ROOT/'data/qobuz_unmatched_metadata_scope.json'
    scope=json.loads(path.read_text())
    if scope['schema_version']!=1 or [(e['discogs_id'],e['album_id']) for e in scope['entries']]!=[('2996680','0002894497722'),('4365080','5099909655058'),('8970069','a5x02z4qm3ana'),('10738828','0002894390212')]:
        raise ValueError('Four-album scope changed; review before retrieval')
    entries=[{'discogs_id':e['discogs_id'],'album_id':e['album_id']} for e in scope['entries']]
    manifest={'entries':entries,'fingerprint':hashlib.sha256(json.dumps(entries,sort_keys=True).encode()).hexdigest()}
    output=ROOT/'.qobuz-poc/unmatched-metadata';output.mkdir(parents=True,exist_ok=True)
    saved_manifest=output/'manifest.json'
    if saved_manifest.exists() and json.loads(saved_manifest.read_text())!=manifest:
        raise ValueError('Manifest changed; preserve prior run')
    runner.save(saved_manifest,manifest)
    if not args.fetch:
        print('Prepared four-album manifest offline; --fetch explicitly retrieves metadata.');return 0
    runner.OUTPUT=output
    result=runner.search(manifest,metadata=True)
    if result:return result
    metadata=[]
    for i,task in enumerate(entries):
        raw=json.loads((output/f'metadata-{i:02d}.json').read_text());source=raw['album']
        tracks=source['tracks']['items']
        if raw['task']!=task or str(source['id'])!=task['album_id'] or len(tracks)!=source['tracks_count'] or len({t['id'] for t in tracks})!=len(tracks):
            (output/'STOP').touch();raise ValueError('Incomplete or mismatched metadata; paused')
        album=album_fields(source);items=[]
        for track in tracks:
            item=select(track,TRACK_FIELDS)
            for key in ['composer','performer']:
                if isinstance(track.get(key),dict):item[key]=select(track[key],['id','name'])
            items.append(item)
        album['tracks']={'items':items,'total':len(items),'offset':0}
        metadata.append({'task':task,'saved_at':raw['saved_at'],'album':album})
    payload={'schema_version':1,'scope_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'metadata':metadata}
    (ROOT/'data/qobuz_unmatched_metadata.json.gz').write_bytes(gzip.compress(json.dumps(payload,ensure_ascii=False,sort_keys=True).encode(),mtime=0))
    print('Saved complete portable metadata:',sum(len(e['album']['tracks']['items']) for e in metadata),'tracks')
    return 0

if __name__=='__main__':raise SystemExit(main())
