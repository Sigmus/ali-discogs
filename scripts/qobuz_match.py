"""Offline, conservative programme/credit evidence; scores are heuristic, not probabilities."""
import json
import hashlib
from pathlib import Path
import re
import sys
from collections import Counter
from functools import lru_cache
from qobuz_snapshot import load_snapshot
from rapidfuzz import fuzz
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from ali_discogs.text import tnorm, norm, ORCH_ALIASES, is_composer

ROOT = Path(__file__).resolve().parents[1]
VERSION = 'qobuz-work-groups-v2+explicit-target-credits+reviewed-leads'


def credits_v1(track):
    result = []
    for part in (track.get('performers') or '').split(' - '):
        fields = [x.strip() for x in part.split(',')]
        roles = norm(' '.join(fields[1:])).split()
        if any(r in roles for r in ['conductor', 'orchestra', 'soloist', 'piano', 'violin', 'cello', 'performer', 'mainartist']) or 'main artist' in ' '.join(roles):
            result.append(fields[0])
    return result


def credits(track):
    result = credits_v1(track)
    for part in (track.get('performers') or '').split(' - '):
        name, _, roles = part.partition(',')
        if set(norm(roles).split()) & {'soprano', 'mezzo', 'tenor', 'baritone', 'bass', 'alto', 'contralto', 'choir', 'chorus'}:
            if name.strip() not in result:
                result.append(name.strip())
    return result


def person_key(name):
    name = norm(name)
    name = ORCH_ALIASES.get(name, name)
    return ' '.join(x for x in name.split() if x not in {'the', 'sir', 'royal'})


def agrees(name, available):
    key = person_key(name)
    return bool(key) and any(key == person_key(a) for a in available)


def catalogue(title):
    text = tnorm(title)
    return set((kind, n, sub or '') for kind, n, sub in re.findall(
        r'\b(op|bwv|k|d|hob|rv|hwv|sz|bb|wwv|l|woo)\s*(\d+[a-z]?)(?:\s+(?:no|nr)\s*(\d+))?', text))


@lru_cache(maxsize=65536)
def work_match(target, title):
    a, b = [re.sub(r'\bpart\b', 'pt', tnorm(t)) for t in (target, title)]
    part_a = re.search(r'\b(?:part|pt)\s+([ivx]+|\d+)(?:\s+([a-z]))?\b', a)
    part_b = re.search(r'\b(?:part|pt)\s+([ivx]+|\d+)(?:\s+([a-z]))?\b', b)
    if part_a and (not part_b or part_a.groups() != part_b.groups()):
        return False
    if any(w in b.split() for w in ['excerpt', 'excerpts', 'extract']) and not any(w in a.split() for w in ['excerpt', 'excerpts', 'extract']):
        return False
    ca, cb = catalogue(target), catalogue(title)
    if ca:
        # No cross-catalogue guesses, and preserve opus subdivisions.
        if not ca.issubset(cb):
            return False
        return True
    ordinals = {'first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth'}
    if not (set(a.split()) & ordinals).issubset(set(b.split())):
        return False
    nums = set(re.findall(r'\b\d+\b', a))
    if not nums.issubset(set(re.findall(r'\b\d+\b', b))):
        return False
    words = set(a.split()) - set('in a b c d e f g no major minor first second third movement allegro andante presto adagio moderato vivace assai i ii iii iv v the and for of'.split())
    if words and (a == b or b.endswith(' ' + a)):
        return True
    if len(words) < 2:
        return False
    return fuzz.token_set_ratio(a, b) >= 93


def units_v1(row):
    tracks = row.get('tracklist') or []
    has_headings = any(t.get('type') == 'index' for t in tracks)
    result = []
    for t in tracks:
        title = t.get('title', '')
        if not title:
            continue
        # Skip only clearly generic movement labels under explicit work headings.
        generic = re.fullmatch(r'(?:[ivx]+ |(?:first|second|third|fourth) movement )?(?:allegro|andante|adagio|presto|largo|lento|vivace|scherzo|rondo|menuetto)(?: (?:molto|assai|moderato|con|brio|ma|non|troppo|sostenuto|cantabile|grazioso|espressivo|poco|un|piu|meno|animato|appassionato))*', tnorm(title))
        if has_headings and t.get('type') != 'index' and generic:
            continue
        result.append(title)
    return result


def units(row):
    result=[]
    parent=False
    for t in row.get('tracklist') or []:
        title=t.get('title','')
        if not title:continue
        if t.get('type') in {'index','heading'}:
            parent=True;result.append(title);continue
        numbered=bool(re.match(r'^(?:[IVX]+\s*[:.\-]|\d+\.)',title))
        generic=units_v1({'tracklist':[{'title':'Work heading','type':'index'},t]})==['Work heading']
        if parent and (numbered or generic):continue
        result.append(title)
    return result


def evaluate_v1(row, album):
    targets = units_v1(row)
    tracks = album['tracks']['items']
    required = list(dict.fromkeys([*(row.get('key_performers') or []), *(row.get('performers') or []),
                *(row.get('ensembles') or []), *([row['conductor']] if row.get('conductor') else [])]))
    required = [p for p in required if not is_composer(p)]
    matches = []
    for target in targets:
        possible = [t for t in tracks if work_match(target, t.get('title', ''))]
        compatible = [t for t in possible if required and all(agrees(p, credits_v1(t)) for p in required)
                      and (not row.get('composers') or any(
                          norm(c).split()[-1] in norm(t.get('performers', '')).split()
                          for c in row['composers'] if norm(c)))]
        matches.append({'target': target, 'work_tracks': len(possible),
                        'credited_tracks': len(compatible),
                        'track_ids': [t['id'] for t in compatible]})
    covered = sum(bool(x['credited_tracks']) for x in matches)
    coverage = covered / len(targets) if targets else 0
    exact_named = bool(targets) and len(targets) == len(tracks) and all(
        len(m['track_ids']) == 1 for m in matches) and len({i for m in matches for i in m['track_ids']}) == len(targets)
    # Grouped LP headings cannot prove movement completeness automatically.
    status = 'unchecked'
    confidence = None
    reasons = []
    if not targets or not required:
        reasons.append('Insufficient programme or non-composer performer evidence.')
    elif coverage == 1:
        status = 'found' if exact_named else 'probable'
        confidence = .95 if exact_named else .85
        reasons.append('Each target item has supporting work and performer credits.')
        if not exact_named:
            reasons.append('Grouped movements or extra recordings require review; recording identity is not confirmed.')
    else:
        confidence = None
        reasons.append(f'{covered}/{len(targets)} target items have matching work and performer credits; unresolved.')
    if any(m['work_tracks'] and not m['credited_tracks'] for m in matches):
        reasons.append('Some title/work matches lack the required recording credits.')
    return {'status': status, 'confidence': confidence, 'coverage': coverage,
            'covered': covered, 'target_count': len(targets), 'required_performers': required,
            'programme': matches, 'reasons': reasons}


def evaluate(row, album):
    from qobuz_work_groups import evaluate_grouped
    return evaluate_grouped(row, album)


def publication_evidence(row, album, inventory):
    from qobuz_work_groups import evaluate_grouped
    legacy = evaluate_v1(row, album)
    evidence = evaluate_grouped(row, album, legacy=legacy)
    if legacy['status'] == 'unchecked' and evidence['status'] != 'unchecked':
        from qobuz_completeness import check_programme
        from qobuz_work_groups import contextual_tracks
        contextual = {**album, 'tracks': {'items': contextual_tracks(row, album['tracks']['items'])}}
        completeness = check_programme(row, contextual, evidence, inventory)
        evidence['promotion_review'] = completeness
        if completeness['status'] != 'complete':
            evidence.update(status='unchecked', confidence=None)
            evidence['reasons'] = [*evidence['reasons'],
                'New work-group candidate withheld pending programme-completeness review.']
        else:
            evidence.update(status='probable', confidence=.85)
    return evidence


def public_album(album):
    return {'id': str(album['id']), 'name': album['title'],
            'artists': [(album.get('artist') or {}).get('name', '')],
            'label': (album.get('label') or {}).get('name', ''),
            'release_date': album.get('release_date_original', ''),
            'image': (album.get('image') or {}).get('small', ''),
            'url': 'https://www.qobuz.com/album/' + str(album['id'])}



def expanded_candidate(row, album, inventory):
    """Recompute checks; reviewed candidate scope never overrides missing evidence."""
    from qobuz_completeness import check_programme
    evidence = evaluate(row, album)
    if evidence['status'] == 'unchecked':
        return None
    completeness = check_programme(row, album, evidence, inventory)
    if completeness['status'] != 'complete':
        return None
    # Expansion remains a programme/credit lead, including box-set supersets.
    evidence['status'], evidence['confidence'] = 'probable', .85
    evidence['reasons'] = [*evidence['reasons'],
        'Reviewed cache-wide candidate: all inventoried movements or explicitly listed timed tracks are supported; recording identity still requires review.']
    return {**public_album(album), **evidence, 'discovery': 'reviewed-cache-expansion',
            'completeness': completeness}


def generate():
    rows = {r['discogs_id']: r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    snapshot = load_snapshot()
    manifest = snapshot['search_manifest']
    metadata_manifest = snapshot['metadata_manifest']
    scope_path = ROOT/'data/qobuz_expansion_scope.json'
    inventory_path = ROOT/'data/qobuz_work_inventory.json'
    target_credits_path = ROOT/'data/qobuz_target_credits.json.gz'
    scope = json.loads(scope_path.read_text())
    inventory = json.loads(inventory_path.read_text())
    if scope['schema_version'] != 1 or inventory['schema_version'] != 1:
        raise ValueError('Unsupported expansion evidence schema')
    from qobuz_lead_review import load_reviews, reviewed_candidate, REVIEW, ARCHIVE
    reviews, reviewed_albums = load_reviews()
    lead_reviews = {r['discogs_id']: r for r in reviews}
    results = {}
    for entry in manifest['entries']:
        rid = entry['discogs_id']
        search = snapshot['searches'][str(rid)]
        candidates = []
        for item in search['search']['albums']['items']:
            album = snapshot['albums'][str(item['id'])]
            if str(album['id']) != str(item['id']) or len(album['tracks']['items']) != album['tracks_count']:
                raise ValueError('Incomplete or mismatched metadata')
            evidence = publication_evidence(rows[rid], album, inventory)
            candidates.append({**public_album(album), **evidence})
        own_ids = {c['id'] for c in candidates}
        for aid in scope['releases'].get(str(rid), []):
            if aid not in own_ids:
                extra = expanded_candidate(rows[rid], snapshot['albums'][aid], inventory)
                if extra:
                    candidates.append(extra)
        review = lead_reviews.get(str(rid))
        if review:
            extra = reviewed_candidate(rows[rid], reviewed_albums[review['album_id']], review)
            if extra and extra['id'] not in {c['id'] for c in candidates}:
                candidates.append(extra)
        candidates.sort(key=lambda a: ({'found': 2, 'probable': 1, 'unchecked': 0}[a['status']], a['coverage'], a['confidence'] or 0), reverse=True)
        best = candidates[0] if candidates else None
        results[str(rid)] = {'status': best['status'] if best else 'unchecked',
            'confidence': best['confidence'] if best else None,
            'album': public_album_from_candidate(best) if best and best['status'] != 'unchecked' else None,
            'candidates': candidates, 'query': search['query'], 'searched_at': search['saved_at'],
            'reasons': best['reasons'] if best else ['No first-pass search results; broader search is unresolved.']}
    output = {'schema_version': 1, 'matcher_version': VERSION, 'score_kind': 'heuristic',
              'metadata_completed_at': snapshot['metadata_completed_at'],
              'search_manifest_fingerprint': manifest['fingerprint'],
              'metadata_manifest_fingerprint': metadata_manifest['fingerprint'],
              'collection_fingerprint': hashlib.sha256((ROOT/'data/collection_matches.json').read_bytes()).hexdigest(),
              'expansion_scope_fingerprint': hashlib.sha256(scope_path.read_bytes()).hexdigest(),
              'target_credits_fingerprint': hashlib.sha256(target_credits_path.read_bytes()).hexdigest(),
              'work_inventory_fingerprint': hashlib.sha256(inventory_path.read_bytes()).hexdigest(),
              'lead_review_fingerprint': hashlib.sha256(REVIEW.read_bytes()).hexdigest(),
              'comparison_evidence_fingerprint': hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
              'releases': results}
    path = ROOT/'data/qobuz_matches.json'
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n')
    temp.replace(path)
    print(Counter(r['status'] for r in results.values()))
    return output


def public_album_from_candidate(candidate):
    return {k: candidate[k] for k in ['id', 'name', 'artists', 'label', 'release_date', 'image', 'url']}


if __name__ == '__main__':
    generate()
