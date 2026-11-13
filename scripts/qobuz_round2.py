"""Fixed 20-release fallback search; slow/resumable live mode is explicit."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path

from qobuz_match import ROOT
from qobuz_query_plan import propose, relevance
from qobuz_snapshot import load_snapshot, album_fields
import qobuz_comparison_pilot as runner

SCOPE = ROOT/'data/qobuz_round2_scope.json'
OUTPUT = ROOT/'.qobuz-poc/coverage-round2'
EVIDENCE = ROOT/'data/qobuz_round2_searches.json.gz'


# Reviewed query-only corrections from cached target titles/credits. These do not
# alter production composer/performer requirements or claim recording identity.
REVIEWED_QUERIES = {
    '1035152': ['sviatoslav richter schumann', 'sviatoslav richter schumann piano concerto op 54'],
    '2345819': ['daniel barenboim beethoven', 'daniel barenboim beethoven piano concerto op 61'],
    '3667210': ['sviatoslav richter bartok piano concerto 2', 'sviatoslav richter prokofiev piano concerto 5'],
    '4365080': ['franz konwitschny wagner tannhauser', 'elisabeth grummer hans hopf tannhauser'],
    '7358646': ['werner haas mendelssohn songs without words', 'werner haas mendelssohn lieder ohne worte'],
    '8151148': ['gioconda de vito brahms violin sonatas', 'gioconda de vito brahms op 108'],
    '13927062': ['rubinstein chopin piano concerto 1', 'rubinstein chopin polonaises waltzes'],
    '36122362': ['leonard bernstein haydn masses', 'bernstein haydn harmonie theresien pauken nelson'],
}


def queries_for(row):
    return REVIEWED_QUERIES.get(str(row['discogs_id']), propose(row))


def fingerprint(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def prepare():
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    original=load_snapshot()
    publication=json.loads((ROOT/'data/qobuz_matches.json').read_text())['releases']
    if not SCOPE.exists():
        prior={e['discogs_id'] for e in json.loads((ROOT/'data/qobuz_comparison_scope.json').read_text())['entries']}
        pool=[]
        for rid,row in sorted(rows.items(),key=lambda x:int(x[0])):
            if rid in prior or publication[rid]['status']!='unchecked' or original['searches'][rid]['search']['albums']['items']:
                continue
            qs=[q for q in queries_for(row) if q != original['searches'][rid]['query']][:2]
            if len(qs)==2:pool.append((rid,qs))
        selected=[pool[i*(len(pool)-1)//19] for i in range(20)]
        entries=[{'discogs_id':rid,'title':rows[rid]['title'],'original_query':original['searches'][rid]['query'],'queries':qs} for rid,qs in selected]
        scope={'schema_version':1,'selected_on':'2026-11-13','selection':'Twenty unique unchecked releases with empty original Qobuz searches, excluding all prior30 comparison releases; evenly spaced by numeric release ID among cases with two distinct improved queries. Not random or representative.',
               'collection_sha256':hashlib.sha256((ROOT/'data/collection_matches.json').read_bytes()).hexdigest(),'entries':entries}
        runner.save(SCOPE,scope)
    scope=json.loads(SCOPE.read_text())
    if scope['schema_version']!=1 or len(scope['entries'])!=20 or len({e['discogs_id'] for e in scope['entries']})!=20:
        raise ValueError('Invalid fixed round-two scope')
    if scope['collection_sha256']!=hashlib.sha256((ROOT/'data/collection_matches.json').read_bytes()).hexdigest():
        raise ValueError('Collection changed; review the fixed scope before resuming')
    tasks=[]
    for entry in scope['entries']:
        rid=entry['discogs_id']
        if len(entry['queries'])!=2 or len(set(entry['queries']))!=2:
            raise ValueError('Expected two distinct reviewed queries per release')
        if original['searches'][rid]['search']['albums']['items'] or any(q not in queries_for(rows[rid]) for q in entry['queries']):
            raise ValueError('Source or query planner changed; review before resuming')
        tasks.extend({'discogs_id':rid,'query':q} for q in entry['queries'])
    manifest={'entries':tasks,'fingerprint':fingerprint(tasks)}
    OUTPUT.mkdir(parents=True,exist_ok=True)
    path=OUTPUT/'manifest.json'
    if path.exists() and json.loads(path.read_text())!=manifest:
        raise ValueError('Round-two manifest changed; preserve prior run')
    runner.save(path,manifest)
    return scope,rows,manifest


def export(scope,rows,manifest):
    saved=[]
    for i,task in enumerate(manifest['entries']):
        record=json.loads((OUTPUT/f'search-{i:02d}.json').read_text())
        if record['task']!=task:raise ValueError('Saved round-two query differs')
        saved.append({'task':task,'saved_at':record['saved_at'],
                      'albums':[album_fields(a) for a in record['search']['albums']['items']]})
    payload={'schema_version':1,'scope_sha256':hashlib.sha256(SCOPE.read_bytes()).hexdigest(),
             'purpose':'Fallback search evidence and relevance only; not accepted programme/recording matches.','results':saved}
    temp=EVIDENCE.with_suffix('.tmp')
    temp.write_bytes(gzip.compress(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode(),mtime=0))
    temp.replace(EVIDENCE)
    snapshot=load_snapshot();summary=[]
    for e in scope['entries']:
        rid=e['discogs_id'];hits={str(a['id']):a for s in saved if s['task']['discogs_id']==rid for a in s['albums']}
        ranked=[{'album_id':aid,'title':a['title'],'cached_complete_metadata':aid in snapshot['albums'],**relevance(rows[rid],snapshot['albums'].get(aid,a))} for aid,a in hits.items()]
        ranked.sort(key=lambda a:(-a['score'],a['album_id']))
        summary.append({'discogs_id':rid,'title':e['title'],'unique_hits':len(hits),'ranked_hits':ranked})
    result={'schema_version':1,'entries':summary,'summary':{'releases':20,'queries':len(saved),'nonempty_queries':sum(bool(s['albums']) for s in saved),'releases_with_hits':sum(bool(s['unique_hits']) for s in summary),'release_candidate_pairs':sum(s['unique_hits'] for s in summary)},'limitations':['Search hits and relevance are not accepted matches.','Empty queries are not confirmed catalogue absence.','No publication changes derive automatically from search results.']}
    runner.save(ROOT/'data/qobuz_round2_results.json',result)
    print(json.dumps(result['summary']))


def metadata():
    from qobuz_snapshot import select, TRACK_FIELDS
    scope_path=ROOT/'data/qobuz_round2_metadata_scope.json'
    scope=json.loads(scope_path.read_text())
    if scope['schema_version']!=1 or len(scope['entries'])!=2:
        raise ValueError('Metadata exceeds fixed two-album scope')
    evidence=json.loads(gzip.decompress(EVIDENCE.read_bytes()))
    if evidence['scope_sha256']!=hashlib.sha256(SCOPE.read_bytes()).hexdigest():
        raise ValueError('Search scope changed before metadata selection')
    for task in scope['entries']:
        ids={str(a['id']) for s in evidence['results'] if s['task']['discogs_id']==task['discogs_id'] for a in s['albums']}
        if task['album_id'] not in ids:raise ValueError('Metadata selection not in saved results')
    manifest={'entries':scope['entries'],'fingerprint':fingerprint(scope['entries'])}
    path=OUTPUT/'metadata-manifest.json'
    if path.exists() and json.loads(path.read_text())!=manifest:
        raise ValueError('Metadata scope changed; preserve prior run')
    runner.save(path,manifest)
    runner.OUTPUT=OUTPUT
    result=runner.search(manifest,metadata=True)
    if result:return result
    entries=[]
    for i,task in enumerate(scope['entries']):
        saved=json.loads((OUTPUT/f'metadata-{i:02d}.json').read_text())
        if saved['task']!=task:raise ValueError('Saved metadata selection changed')
        source=saved['album'];album=album_fields(source);tracks=[]
        for t in source['tracks']['items']:
            item=select(t,TRACK_FIELDS)
            for key in ['composer','performer']:
                if isinstance(t.get(key),dict):item[key]=select(t[key],['id','name'])
            tracks.append(item)
        if str(source['id'])!=task['album_id'] or len(tracks)!=source['tracks_count'] or len({t['id'] for t in tracks})!=len(tracks):
            raise ValueError('Incomplete or mismatched metadata')
        album['tracks']={'items':tracks,'total':len(tracks),'offset':0}
        entries.append({'task':task,'saved_at':saved['saved_at'],'album':album})
    payload={'schema_version':1,'scope_sha256':hashlib.sha256(scope_path.read_bytes()).hexdigest(),'metadata':entries}
    (ROOT/'data/qobuz_round2_metadata.json.gz').write_bytes(gzip.compress(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode(),mtime=0))
    print(f'Exported{len(entries)} complete selected albums; no automatic match acceptance.')
    return 0


def audit():
    from qobuz_lead_review import assess
    from qobuz_match import evaluate
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    albums=load_snapshot()['albums']
    extra=json.loads(gzip.decompress((ROOT/'data/qobuz_round2_metadata.json.gz').read_bytes()))['metadata']
    albums={**albums,**{str(e['album']['id']):e['album'] for e in extra}}
    reviews=json.loads((ROOT/'data/qobuz_round2_reviews.json').read_text())['releases']
    entries=[assess(rows[r['discogs_id']],albums[r['album_id']],r)[0] for r in reviews]
    runner.save(ROOT/'data/qobuz_round2_cached_audit.json',{'schema_version':1,'reviewed_on':'2026-11-13','entries':entries,
        'summary':{'reviewed':len(entries),'eligible_probable':sum(e['eligible'] for e in entries),'from_original_cache':2,'from_recovered_search':1},
        'limitations':'Hash-bound programme/recording-family reviews, not exact session/mastering verification. Other aliases remain unresolved.'})
    selected=[]
    for record in extra:
        rid=record['task']['discogs_id'];album=record['album'];e=evaluate(rows[rid],album)
        selected.append({'discogs_id':rid,'album_id':str(album['id']),'title':album['title'],'track_count':len(album['tracks']['items']),
            'unmodified_matcher_evidence':e,'reviewed_for_probable':any(r['discogs_id']==rid and r['decision']=='probable' for r in reviews),
            'finding':('Target says Sz83# versus candidate Sz95 and G minor versus G major. Both concertos have correct named performers/orchestras, but catalogue correction is not automatically accepted; remains Unchecked.' if rid=='3667210' else 'Malformed duplicated Op78N1/Op78 heading cleaned only within this exact reviewed target/candidate pair. Three plus four movements with both named players pass; Probable85, remaster/take unverified.')})
    runner.save(ROOT/'data/qobuz_round2_metadata_audit.json',{'schema_version':1,'entries':selected,'summary':{'selected_albums':len(selected),'tracks':sum(e['track_count'] for e in selected),'promoted':sum(e['reviewed_for_probable'] for e in selected)}})
    print(json.dumps({'reviews':len(entries),'eligible_probable':sum(e['eligible'] for e in entries),'selected_metadata_albums':len(selected)}))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--search',action='store_true')
    parser.add_argument('--export',action='store_true')
    parser.add_argument('--metadata',action='store_true')
    parser.add_argument('--audit',action='store_true')
    args=parser.parse_args()
    if sum([args.search,args.export,args.metadata,args.audit])>1:parser.error('Choose only one mode')
    scope,rows,manifest=prepare()
    if args.search:
        runner.OUTPUT=OUTPUT
        result=runner.search(manifest)
        if result:return result
        export(scope,rows,manifest)
    elif args.export:export(scope,rows,manifest)
    elif args.metadata:return metadata()
    elif args.audit:audit()
    else:print(f'Prepared20 releases /{len(manifest["entries"])} fixed queries; offline, no API calls.')
    return 0


if __name__=='__main__':raise SystemExit(main())
