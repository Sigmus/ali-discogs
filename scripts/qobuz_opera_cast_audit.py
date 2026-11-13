"""Offline source-to-candidate opera credit audit; no acceptance overrides."""
import hashlib,json,gzip
from qobuz_match import ROOT,person_key,credits


def audit():
    source=ROOT/'data/qobuz_unmatched_metadata.json.gz'
    metadata=json.loads(gzip.decompress(source.read_bytes()))['metadata'];entries=[]
    for rid in ['2996680','4365080']:
        raw=ROOT/f'raw/discogs/releases/{rid}.json';target=json.loads(raw.read_text())
        album=next(x['album'] for x in metadata if x['task']['discogs_id']==rid)
        tracks=album['tracks']['items'];available={person_key(n):n for t in tracks for n in credits(t)}
        all_names={person_key(p.split(',')[0].strip()) for t in tracks for p in t.get('performers','').split(' - ')}
        cast=[]
        for actor in target.get('extraartists',[]):
            role=actor['role'].lower()
            if not any(k in role for k in ['vocals','performer','chorus','orchestra','conductor']):continue
            key=person_key(actor['name']);cast.append({'name':actor['name'],'target_role':actor['role'],'present_in_candidate_names':key in all_names,'accepted_by_existing_credit_parser':key in available})
        entries.append({'discogs_id':rid,'album_id':str(album['id']),'target_source_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'source_notes':target.get('notes'),'candidate_track_count':len(tracks),'credits':cast,'missing_exact_name_keys':[c['name'] for c in cast if not c['present_in_candidate_names']], 'limitations':['Exact normalized name-key comparison only; missing keys may be translations/aliases or role metadata, not a cast contradiction.','Presence anywhere in album is not scene-level role verification or complete opera proof.','Production normalized requirements omit some raw credited actors; do not promote by satisfying only that subset.']})
    payload={'schema_version':1,'metadata_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'entries':entries,'decision':'Both unresolved; preserve source and candidate evidence without weakening credit requirements.'}
    (ROOT/'data/qobuz_opera_cast_audit.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    for e in entries:print(e['discogs_id'],'unresolved exact-name keys:',e['missing_exact_name_keys'])
    return payload
if __name__=='__main__':audit()
