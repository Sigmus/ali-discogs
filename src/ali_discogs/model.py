"""Turn one Discogs collection row plus its cached release detail into a match record."""

import json
import os

from ali_discogs.paths import raw_dir
from ali_discogs.text import ENS_T, is_composer, norm, short_title, surname


def build_item(release):
    b = release['basic_information']
    det = {}
    path = os.path.join(raw_dir(), 'discogs', 'releases', f"{b['id']}.json")
    if os.path.exists(path):
        with open(path, encoding='utf-8') as fh:
            det = json.load(fh)
    artists = [a['name'] for a in b['artists']]
    extra = det.get('extraartists', []) if det else []
    composers, performers = [], []
    for x in extra:
        role = x.get('role', '').lower()
        if 'composed' in role or 'written' in role:
            composers.append(x['name'])
    for tr in (det.get('tracklist', []) if det else []):
        for x in tr.get('extraartists', []):
            if 'composed' in x.get('role', '').lower():
                composers.append(x['name'])
    conductors = [x['name'] for x in extra if 'conductor' in x.get('role', '').lower() and 'chorus' not in x.get('role', '').lower()]
    for a in artists:
        if any(norm(a) == norm(c) for c in conductors):
            performers.append(a)
        elif is_composer(a) or any(norm(a) == norm(c) for c in composers):
            composers.append(a)
        else:
            performers.append(a)
    for x in extra:
        role = x.get('role', '').lower()
        if any(k in role for k in ('conductor', 'orchestra', 'soloist', 'piano', 'violin', 'cello', 'ensemble', 'performer', 'soprano', 'tenor', 'baritone', 'choir', 'chorus')):
            if x['name'] not in performers and (not is_composer(x['name']) or 'conductor' in role):
                performers.append(x['name'])
    if not performers and artists and not composers:
        performers = [artists[0]]
    cn = [norm(c) for c in conductors]
    performers = [p for p in performers if norm(p) in cn] + [p for p in performers if norm(p) not in cn]
    it_conductor = conductors[0] if conductors else None
    soloists = [p for p in performers if norm(p) not in cn and not any(e in norm(p) for e in ENS_T)]
    key_performers = ([it_conductor] if it_conductor else []) + (soloists[:1] if not (it_conductor and len(soloists) >= 2) else [])
    if not key_performers:
        key_performers = performers[:1]

    def dedupe(xs):
        out = []
        for x in xs:
            if all(norm(x) != norm(y) for y in out):
                out.append(x)
        return out

    composers, performers = dedupe(composers), dedupe(performers)
    headings = [t['title'] for t in det.get('tracklist', []) if t.get('type_') in ('heading', 'index')] if det else []
    tracks = [t['title'] for t in det.get('tracklist', []) if t.get('type_') == 'track'] if det else []
    return {
        'discogs_id': b['id'],
        'master_id': b.get('master_id') or None,
        'title': b['title'].strip(),
        'artists': artists,
        'composers': composers,
        'performers': performers,
        'conductor': it_conductor,
        'key_performers': key_performers,
        'ensembles': [p for p in performers if any(e in norm(p) for e in ENS_T) and not any(k in norm(p) for k in ('choir', 'chor', 'singers'))],
        'year': b.get('year') or None,
        'released': det.get('released'),
        'country': det.get('country'),
        'labels': [{'name': l['name'], 'catno': l['catno']} for l in b.get('labels', [])],
        'formats': b.get('formats', []),
        'genres': b.get('genres', []),
        'styles': b.get('styles', []),
        'thumb': b.get('thumb'),
        'cover_image': b.get('cover_image'),
        'discogs_url': f"https://www.discogs.com/release/{b['id']}",
        'date_added': release.get('date_added'),
        'tracklist': [
            {'position': t.get('position'), 'title': t['title'], 'type': t.get('type_'), 'duration': t.get('duration')}
            for t in det.get('tracklist', [])
        ] if det else [],
        '_headings': headings,
        '_tracks': tracks,
    }


def queries(it):
    title = short_title(it['title'])
    perf = it['performers'][:3]
    comp = [surname(c) for c in it['composers'][:2]]
    qs = []
    p0 = norm(perf[0]) if perf else ''
    if p0:
        qs.append(f"{p0} {' '.join(comp[:1])} {title}".strip())
        if len(perf) > 1:
            qs.append(f"{p0} {norm(perf[1])} {short_title(it['title'], 4)}")
        if comp:
            qs.append(f"{p0} {' '.join(comp)}")
        else:
            qs.append(f"{p0} {short_title(it['title'], 4)}")
    if comp:
        qs.append(f"{' '.join(comp)} {title}")
    else:
        qs.append(title)
    if p0 and it['_headings']:
        qs.append(f"{p0} {' '.join(comp[:1])} {short_title(it['_headings'][0], 5)}")
    seen, out = set(), []
    for q in qs:
        q = ' '.join(q.split())
        if q and q not in seen:
            seen.add(q)
            out.append(q)
    return out
