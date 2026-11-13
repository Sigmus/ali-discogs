"""Validate two corrected pilot queries, with the existing slow/STOP safeguards."""
import gzip
import hashlib
import json
from pathlib import Path
import qobuz_comparison_pilot as runner
from qobuz_snapshot import album_fields
from qobuz_query_plan import relevance

ROOT=Path(__file__).resolve().parents[1]


def main():
    runner.OUTPUT=ROOT/'.qobuz-poc/query-validation';runner.OUTPUT.mkdir(parents=True,exist_ok=True)
    proposals=json.loads((ROOT/'data/qobuz_query_improvements.json').read_text())['entries']
    queries=[{'discogs_id':'594243','query':'john coltrane a love supreme'},
             {'discogs_id':'8534837','query':'pablo casals mendelssohn'}]
    for task in queries:
        p=next(p for p in proposals if p['discogs_id']==task['discogs_id'])
        if task['query'] not in p['proposed_queries']:raise ValueError('Validation query differs from offline plan')
    manifest={'entries':queries,'fingerprint':hashlib.sha256(json.dumps(queries,sort_keys=True).encode()).hexdigest()}
    path=runner.OUTPUT/'manifest.json'
    if path.exists() and json.loads(path.read_text())!=manifest:raise ValueError('Validation scope changed')
    runner.save(path,manifest)
    result=runner.search(manifest)
    if result:return result
    evidence=[]
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    for i,t in enumerate(queries):
        raw=json.loads((runner.OUTPUT/f'search-{i:02d}.json').read_text())
        evidence.append({'task':t,'saved_at':raw['saved_at'],'albums':[{**album_fields(a),'relevance':relevance(rows[t['discogs_id']],a)} for a in raw['search']['albums']['items']]})
    (ROOT/'data/qobuz_query_validation.json.gz').write_bytes(gzip.compress(json.dumps({'schema_version':1,'purpose':'Search relevance validation only; not recording acceptance.','results':evidence},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode(),mtime=0))
    return 0


if __name__=='__main__':raise SystemExit(main())
