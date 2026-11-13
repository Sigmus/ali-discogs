"""Derive positive work-scoped requirements from cached Discogs credit assignments."""
from functools import lru_cache
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re
from qobuz_match import norm, person_key

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT/'data/qobuz_target_credits.json.gz'
MUSICAL = re.compile(r'\b(?:conductor|orchestra|choir|chorus|vocals|soprano|tenor|baritone|contralto|soloist|piano|violin|cello|violoncello|oboe|flute|clarinet|bassoon|organ|harpsichord|trumpet|trombone|timpani|horn|guitar|double bass)\b',re.I)


def selectors(text, positions=None):
    result=set()
    for item in text.split(','):
        item=item.strip()
        if ' to ' in item and positions is not None:
            first,last=item.split(' to ',1)
            starts=[i for i,p in enumerate(positions) if p==first or (first.isalpha() and re.fullmatch(re.escape(first)+r'\d+',p))]
            ends=[i for i,p in enumerate(positions) if p==last or (last.isalpha() and re.fullmatch(re.escape(last)+r'\d+',p))]
            if not starts or not ends or min(starts)>max(ends):return None
            result.update(positions[min(starts):max(ends)+1])
        else:
            m=re.fullmatch(r'([A-Z]*)(\d+) to ([A-Z]*)(\d+)',item)
            if m and m[1]==m[3] and 0<=int(m[4])-int(m[2])<=100:
                result.update(m[1]+str(i) for i in range(int(m[2]),int(m[4])+1))
            elif re.fullmatch(r'[A-Z]+\d*|\d+',item):result.add(item)
            else:return None  # never accept only the parseable portion of a scope
    return result


def musical(role):
    return any(MUSICAL.search(c) and not re.search(r'engineer|producer|technician|liner|design|photograph|master|recorded|supervis|composed|arrang',c,re.I) for c in role.split(','))


def works(raw):
    groups=[]
    for t in raw.get('tracklist',[]):
        kind=t.get('type_')
        if kind in ['index','heading']:
            groups.append({'title':t['title'],'positions':[],'credits':list(t.get('extraartists',[]))})
            for child in t.get('sub_tracks',[]):
                if child.get('position'):groups[-1]['positions'].append(child['position'])
                groups[-1]['credits'].extend(child.get('extraartists',[]))
        elif groups and re.match(r'^(?:[IVX]+\s*[:.\-]|\d+\.)',t.get('title','')):
            if t.get('position'):groups[-1]['positions'].append(t['position'])
            groups[-1]['credits'].extend(t.get('extraartists',[]))
        else:groups.append({'title':t.get('title',''),'positions':[t['position']] if t.get('position') else [],'credits':list(t.get('extraartists',[]))})
    return groups


def derive(raw):
    groups=works(raw)
    all_positions=[p for g in groups for p in g['positions']]
    duplicate_positions={p for p,n in Counter(all_positions).items() if n>1}
    positions=list(dict.fromkeys(all_positions))
    retained=[]
    for a in raw.get('extraartists',[]):
        if not musical(a.get('role','')):continue
        scope=selectors(a.get('tracks',''),positions)
        matched={p for p in positions if scope and (p in scope or any(re.fullmatch(r'[A-Z]+',s) and re.fullmatch(re.escape(s)+r'\d+',p) for s in scope))}
        if not scope or not matched or duplicate_positions & matched:
            retained.append(a['name']);continue
        for g in groups:
            if any(p in matched for p in g['positions']):
                g['credits'].append(a)
    result=[]
    for g in groups:
        credits=[]
        for a in g['credits']:
            role=a.get('role','')
            if musical(role):
                c={'name':a['name'],'role':role}
                if c not in credits:credits.append(c)
        if credits:result.append({'title':g['title'],'positions':g['positions'],'performers':credits,'retain_global_performers':list(dict.fromkeys(retained))})
    return result


@lru_cache(maxsize=1)
def load():
    with gzip.open(PATH,'rt') as f:data=json.load(f)
    if data.get('schema_version')!=1:raise ValueError('Unsupported target-credit evidence schema')
    return data['releases']


def requirements(row,title,global_required):
    # Only the hash-bound review adapter supplies this mapping. Title cleanup
    # must not discard the original source's per-work performer assignments.
    title = row.get('_reviewed_title_sources', {}).get(title, title)
    entries=load().get(str(row.get('discogs_id')),[])
    active=[e for e in entries if e['title']==title]
    if not entries or len(active)>1:return row,global_required,None
    if not active:active=[{'title':title,'positions':[],'performers':[]}]
    retained={person_key(n) for e in entries for n in e.get('retain_global_performers',[])}
    scoped={person_key(p['name']) for e in entries for p in e['performers']} - retained
    names=[p['name'] for p in active[0]['performers']]
    required=[p for p in global_required if person_key(p) not in scoped]
    required=list(dict.fromkeys([*required,*names]))
    effective=dict(row)
    effective['ensembles']=[p for p in row.get('ensembles',[]) if person_key(p) not in scoped or person_key(p) in {person_key(n) for n in names}]
    if row.get('conductor') and person_key(row['conductor']) in scoped and not any(person_key(n)==person_key(row['conductor']) for n in names):
        effective['conductor']=None
    for p in active[0]['performers']:
        if re.search('conductor',p['role'],re.I):effective['conductor']=p['name']
        if re.search('orchestra|choir|chorus',p['role'],re.I):effective['ensembles']=list(dict.fromkeys([*effective['ensembles'],p['name']]))
    return effective,required,{'source':'cached Discogs explicit work/position credits','positions':active[0]['positions'],'performers':active[0]['performers']}


def export():
    rows={str(r['discogs_id']) for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    releases={};sources={}
    for rid in sorted(rows,key=int):
        path=ROOT/f'raw/discogs/releases/{rid}.json'
        if path.exists():
            raw=json.loads(path.read_text())
            if str(raw.get('id'))!=rid:raise ValueError('Cached target release ID mismatch')
            if value:=derive(raw):
                releases[rid]=value;sources[rid]=hashlib.sha256(path.read_bytes()).hexdigest()
    payload={'schema_version':1,'source':'cached Discogs release responses; only explicit assignments, no candidate-derived requirements','source_release_sha256':sources,'releases':releases}
    PATH.write_bytes(gzip.compress(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode(),mtime=0))
    print(f'Preserved explicit target work credits for {len(releases)} releases.')


if __name__=='__main__':export()
