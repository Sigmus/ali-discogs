"""Manually reviewed per-work composer guards from immutable source attributions.

Never infer that every Discogs track artist is a composer. Only explicit reviewed
scopes are used; the normalized collection and legacy matcher stay unchanged.
"""
from functools import lru_cache
import hashlib
import json
from qobuz_lead_review import ROOT, target_fingerprint

PATH = ROOT/'data/qobuz_source_composer_reviews.json'


def validate_scope(row, raw_bytes, review):
    if (str(row['discogs_id']) != review['discogs_id'] or
            target_fingerprint(row) != review['target_sha256'] or
            hashlib.sha256(raw_bytes).hexdigest() != review['source_sha256'] or
            review['review_kind'] != 'reviewed-track-artist-composer'):
        raise ValueError('Reviewed source composer evidence changed')
    raw = json.loads(raw_bytes)
    if str(raw['id']) != review['discogs_id']:
        raise ValueError('Source release ID changed')
    from qobuz_match import units
    if [s['target'] for s in review['targets']] != units(row):
        raise ValueError('Composer scope must cover every source target in order')
    source = raw['tracklist']
    if len(source) != len(review['targets']):
        raise ValueError('Source track scope changed')
    result = {}
    for track,spec in zip(source,review['targets']):
        expected = [{'id':spec['discogs_artist_id'],'name':spec['composer']}]
        attributed = [{'id':a['id'],'name':a['name']} for a in track.get('artists',[])]
        if (track.get('position') != spec['position'] or track['title'] != spec['target'] or
                attributed != expected or spec['target'] in result):
            raise ValueError('Ambiguous or changed reviewed track attribution')
        result[spec['target']] = spec['composer']
    return result


@lru_cache(maxsize=1)
def load_scopes():
    data=json.loads(PATH.read_text())
    if data['schema_version']!=1:
        raise ValueError('Unsupported source composer review schema')
    result={}
    for review in data['releases']:
        rid=review['discogs_id']
        if rid in result:raise ValueError('Duplicate source composer scope')
        raw=(ROOT/f'raw/discogs/releases/{rid}.json').read_bytes()
        result[rid]=(review,raw)
    return result


def required_composer(row,target):
    rid=str(row.get('discogs_id',''))
    if not rid:return None
    scope=load_scopes().get(rid)
    if scope is None:return None
    review,raw=scope
    targets=validate_scope(row,raw,review)
    if target not in targets:
        raise ValueError('Work falls outside reviewed composer scope')
    return targets[target]


def audit():
    """Reproduce the guarded lead and flag other normalized attribution gaps."""
    import gzip
    from qobuz_match import evaluate,evaluate_v1,is_composer
    from qobuz_source_programme import programme_hold
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    def flatten(items):
        for track in items:
            yield track
            yield from flatten(track.get('sub_tracks') or [])
    candidates=[]
    for rid,row in rows.items():
        path=ROOT/f'raw/discogs/releases/{rid}.json'
        if not path.exists() or row.get('composers'):continue
        raw=json.loads(path.read_text())
        attributed=[{'position':t.get('position'),'target':t.get('title'),
                     'artists':[a['name'] for a in t.get('artists',[])]}
                    for t in flatten(raw.get('tracklist',[])) if t.get('artists')]
        if not any(is_composer(n) for t in attributed for n in t['artists']):continue
        candidates.append({'discogs_id':rid,'title':row['title'],
                           'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                           'reviewed_scope':rid in load_scopes(),'source_programme_hold':bool(programme_hold(row)),'source_attributions':attributed})
    album=json.loads(gzip.decompress((ROOT/'data/qobuz_evidence.json.gz').read_bytes()))['albums']['0002894776360']
    row=rows['15221307']
    report={'schema_version':1,'reviewed_on':'2026-11-15',
            'scope_sha256':hashlib.sha256(PATH.read_bytes()).hexdigest(),
            'collection_sha256':hashlib.sha256((ROOT/'data/collection_matches.json').read_bytes()).hexdigest(),
            'candidate_album_sha256':hashlib.sha256(json.dumps(album,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'reviewed_lead':{'discogs_id':'15221307','album_id':str(album['id']),
                'legacy_evidence':evaluate_v1(row,album),'guarded_evidence':evaluate(row,album)},
            'empty_normalized_composer_candidates':candidates,
            'limitations':['Only reviewed source scopes enforce composer requirements. Arbitrary track artists are not automatically composers.',
                'Name-heuristic discovery can miss artists; candidates need manual review. All raw names, including unrecognized names, are retained.',
                'Guarded coverage is programme support, not a recording-identity probability. This audit makes no publication label changes.']}
    (ROOT/'data/qobuz_source_composer_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Source-attribution gap candidates:',len(candidates),'Gilels guarded coverage:',report['reviewed_lead']['guarded_evidence']['coverage'])


if __name__=='__main__':audit()
