"""Offline improved query proposals and relevance ranking for the fixed pilot."""
import gzip
import json
from pathlib import Path
from rapidfuzz import fuzz
from qobuz_match import norm, catalogue, units, person_key, work_match
from ali_discogs.text import is_composer

ROOT=Path(__file__).resolve().parents[1]


def lead(row):
    ensembles={person_key(p) for p in row.get('ensembles',[])}
    people=[p for p in row.get('artists',[]) if not is_composer(p) and person_key(p) not in ensembles]
    return (people or row.get('key_performers') or row.get('performers') or [''])[0]


def composer_term(name):
    parts=norm(name).split()
    if 'mendelssohn' in parts:return 'mendelssohn'
    while parts and parts[-1] in {'i','ii','iii','iv','jr','sr'}:parts.pop()
    return parts[-1] if parts else ''


def propose(row):
    person=norm(lead(row));composers=list(dict.fromkeys(composer_term(c) for c in row.get('composers',[])))
    queries=[' '.join(filter(None,[person,c if c not in person.split() else ''])) for c in composers] or [person]
    ids=sorted(set().union(*(catalogue(t) for t in units(row)))) if units(row) else []
    if ids:
        kind,num,sub=ids[0]
        queries.append(' '.join(filter(None,[person,composers[0] if composers else '',kind,num,sub])))
    else:
        # Keep meaningful original text; do not turn a degree sign into "ndeg".
        title=norm(row['title'].replace('°','').replace('º',''))
        queries.append(' '.join(filter(None,[person,' '.join(title.split()[:6])])))
    return list(dict.fromkeys(q for q in queries if q))[:3]


def relevance(row,album):
    names=[(album.get('artist') or {}).get('name',''),*[a.get('name','') for a in album.get('artists',[])]]
    named=any(person_key(lead(row))==person_key(n) for n in names)
    title=fuzz.ratio(norm(row['title']),norm(album['title']))/100
    live_variant='live' in norm(album['title']).split() and 'live' not in norm(row['title']).split()
    targets=units(row);tracks=album.get('tracks',{}).get('items',[])
    coverage=sum(any(work_match(t,x['title']) for x in tracks) for t in targets)/len(targets) if tracks and targets else None
    score=max(0,40*named+20*title+(40*coverage if coverage is not None else 0)-20*live_variant)
    return {'score':round(score,2),'lead_artist_supported':named,'possible_live_variant':live_variant,'programme_title_coverage':coverage,
            'purpose':'Search relevance only; not recording identity, confidence or match acceptance.'}


def main():
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    scope=json.loads((ROOT/'data/qobuz_comparison_scope.json').read_text())
    with gzip.open(ROOT/'data/qobuz_comparison_evidence.json.gz','rt') as f:evidence=json.load(f)
    metadata={str(m['album']['id']):m['album'] for m in evidence['metadata']}
    result=[]
    for e in scope['entries']:
        if e['category']!='qobuz_empty':continue
        rid=e['discogs_id'];row=rows[rid]
        hits={str(a['id']):metadata.get(str(a['id']),a) for s in evidence['searches'] if s['task']['discogs_id']==rid for a in s['search']['albums']['items']}
        ranked=[{'album_id':aid,'title':a['title'],**relevance(row,a)} for aid,a in hits.items()]
        ranked.sort(key=lambda a:(-a['score'],a['album_id']))
        result.append({'discogs_id':rid,'title':row['title'],'lead_artist':lead(row),'proposed_queries':propose(row),'ranked_cached_hits':ranked})
    (ROOT/'data/qobuz_query_improvements.json').write_text(json.dumps({'schema_version':1,'policy':'Offline proposals and cached-hit ranking only; no new API queries or acceptance.','entries':result},ensure_ascii=False,indent=2)+'\n')
    print('Prepared improved proposals and cached rankings for ten pilot releases; no API calls.')


if __name__=='__main__':main()
