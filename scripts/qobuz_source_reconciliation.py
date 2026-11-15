"""Hash-bound source diagnostics and nonperformer validation; no source/publication writes."""
import copy
import hashlib
import json
import re
from qobuz_lead_review import ROOT,target_fingerprint
from ali_discogs.model import credit_role_text


def validate_nonperforming_credit(row,raw,credit):
    from qobuz_target_credits import musical
    name=credit['name']
    found=[x for x in raw.get('extraartists',[]) if x['name']==name]
    if not found or credit['role'] not in [x.get('role') for x in found] or any(musical(x.get('role','')) or not re.match(r'^(liner notes|photography|technician|design|illustration)\b',credit_role_text(x.get('role','')).strip()) for x in found):
        raise ValueError('Credit is not exclusively documented as nonperforming')
    def work_credit_names(tracks):
        for track in tracks:
            for artist in track.get('artists',[]):
                yield artist['name']
            for artist in track.get('extraartists',[]):
                if musical(artist.get('role','')):yield artist['name']
            yield from work_credit_names(track.get('sub_tracks',[]))
    if name in set(work_credit_names(raw['tracklist'])):
        raise ValueError('Documented work performer cannot be removed as a liner author')
    if name not in row['performers'] or name in row.get('key_performers',[]) or name==row.get('conductor') or name in [a['name'] for a in raw['artists']]:
        raise ValueError('Cannot remove a principal or absent performer')
    return name


def reconcile(row,review):
    rid=str(row['discogs_id']);path=ROOT/f'raw/discogs/releases/{rid}.json'
    if rid!=review['discogs_id'] or target_fingerprint(row)!=review['target_sha256'] or hashlib.sha256(path.read_bytes()).hexdigest()!=review['source_sha256']:
        raise ValueError('Source reconciliation evidence changed')
    raw=json.loads(path.read_text());proofs=review['source_evidence']
    if not proofs:raise ValueError('Original edition evidence required')
    source_urls={x['uri'] for x in raw.get('images',[])}
    for proof in proofs:
        p=(ROOT/proof['path']).resolve()
        if not p.is_relative_to((ROOT/'data/review_sources').resolve()) or proof['source_image_url'] not in source_urls or hashlib.sha256(p.read_bytes()).hexdigest()!=proof['sha256']:
            raise ValueError('Original label evidence changed')
    result=copy.deepcopy(row)
    for before,after in review['proposed_target_title_correction'].items():
        originals=[t for t in raw['tracklist'] if t['title']==before]
        normalized=[t for t in result['tracklist'] if t['title']==before]
        if len(originals)!=1 or len(normalized)!=1 or not after or before==after:
            raise ValueError('Ambiguous or missing exact source-title correction')
        normalized[0]['title']=after
    name=validate_nonperforming_credit(row,raw,review['nonperforming_source_credit'])
    result['performers']=[p for p in result['performers'] if p!=name]
    return result


def suite_positions(raw):
    """Resolve explicit flat Suite No.N headers and six ordered source bands."""
    groups=[]
    for t in raw['tracklist']:
        start=re.match(r'^Suite No\.(\d+)\.\s*1st Movement:',t['title'])
        if start:groups.append({'suite_number':int(start[1]),'source_tracks':[]})
        if not groups:raise ValueError('Movement before explicit suite header')
        groups[-1]['source_tracks'].append(t)
    sides=set()
    for g in groups:
        ts=g['source_tracks'];s={re.sub(r'\d+$','',t['position']) for t in ts}
        nums=[int(m[1]) if (m:=re.search(r'\b([1-6])(?:st|nd|rd|th) Movement:',t['title'])) else None for t in ts]
        if nums!=list(range(1,7)) or len(s)!=1 or sides&s or [t['position'] for t in ts]!=[next(iter(s))+str(i) for i in range(1,7)]:
            raise ValueError('Incomplete, mixed-side or reordered suite movements')
        sides.update(s)
    if len({g['suite_number'] for g in groups})!=len(groups):raise ValueError('Repeated suite header')
    return groups
