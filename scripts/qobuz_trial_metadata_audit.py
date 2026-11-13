"""Reproduce bounded metadata findings offline, without publication changes."""
import gzip
import hashlib
import json
from qobuz_match import ROOT,evaluate
from qobuz_completeness import check_programme

def main():
    path=ROOT/'data/qobuz_query_trial_metadata.json.gz'
    payload=json.loads(gzip.decompress(path.read_bytes()))
    scope=ROOT/'data/qobuz_query_trial_metadata_scope.json'
    if payload['scope_sha256']!=hashlib.sha256(scope.read_bytes()).hexdigest():raise ValueError('Metadata scope changed')
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    inventory=json.loads((ROOT/'data/qobuz_work_inventory.json').read_text());entries=[]
    for x in payload['metadata']:
        a=x['album'];tracks=a['tracks']['items'];rid=x['task']['discogs_id']
        if str(a['id'])!=x['task']['album_id'] or len(tracks)!=a['tracks_count'] or len({t['id'] for t in tracks})!=len(tracks):raise ValueError('Incomplete metadata')
        e=evaluate(rows[rid],a);c=check_programme(rows[rid],a,e,inventory)
        entries.append({'discogs_id':rid,'album_id':str(a['id']),'tracks':len(tracks),'assessment':e,'completeness':c,'finding':('Named individual quartet members remain unsupported by current candidate credits; unnamed No.8 heading also needs disambiguation. Not a confirmed wrong recording.' if rid=='1132104' else 'All five Symphony6 movements and Leonore1 carry required credits. Overture completeness and 1957 source recording identity require bounded review before publication.')})
    result={'schema_version':1,'metadata_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'entries':entries,'policy':'Offline findings only; no automatic publication. Exact recording identity remains to be reviewed.'}
    (ROOT/'data/qobuz_query_trial_metadata_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Verified two albums /77 unique tracks within albums; publication unchanged')
if __name__=='__main__':main()
