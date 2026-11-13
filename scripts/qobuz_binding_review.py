"""Hash-bound track bindings. A conflicting catalogue number needs an explicit exception."""
import hashlib
import json
import re
from qobuz_lead_review import ROOT
from qobuz_match import agrees, catalogue, credits, norm


def sonata_no(title):
    found = re.search(r'\bsonata no\s+(\d+)\b', norm(title))
    return found.group(1) if found else None


def allowed(kind, target, title):
    left, right = catalogue(target), catalogue(title)
    if kind is None:
        return not left or not right or left.issubset(right)
    if kind == 'suffix-letter' and len(left) == 1 and len(right) == 1:
        (kind_a, number_a, sub_a), (kind_b, number_b, sub_b) = next(iter(left)), next(iter(right))
        return (kind_a == kind_b and sub_a == sub_b == '' and number_b.startswith(number_a)
                and len(number_b) == len(number_a) + 1 and number_b[-1].isalpha())
    if kind == 'posthumous-token' and not right and 'posth' in norm(title).split():
        text = set(norm(title).split())
        return all(number in text and (not sub or sub in text) for _, number, sub in left)
    if kind == 'bare-subnumber' and len(left) == 1 and len(right) == 1:
        (kind_a, number_a, sub_a), (kind_b, number_b, sub_b) = next(iter(left)), next(iter(right))
        return (kind_a == kind_b and number_a == number_b and sub_a == '' and sub_b
                and sub_b in set(norm(target).split()))
    if kind == 'transcription-bwv':
        text = norm(target)
        if text.count(' transcription ') != 1 or len(left) != 2 or len(right) != 1:
            return False
        if any(kind_name != 'bwv' for kind_name, _, _ in left | right):
            return False
        head, tail = text.split(' transcription ', 1)
        cited = next(iter(right))[1]
        other = next(number for _, number, _ in left if number != cited)
        return cited in head.split() and other in tail.split() and cited not in tail.split()
    if kind == 'stated-sonata-number':
        number = sonata_no(target)
        return bool(number and number == sonata_no(title) and left and right and not left.issubset(right))
    return False


def romans(title):
    return [int(n) for n in ({'I': '1', 'II': '2', 'III': '3', 'IV': '4', 'V': '5', 'VI': '6', 'VII': '7'}[token]
            for token in re.findall(r'(?:^|[\s:])(VII|VI|V|IV|III|II|I)\.', title))]


def assign(row, album, review):
    from qobuz_match import evaluate
    evidence = evaluate(row, album)
    tracks = {t['id']: t for t in album['tracks']['items']}
    order = {t['id']: index for index, t in enumerate(album['tracks']['items'])}
    assigned = {item['target']: list(item['track_ids']) for item in evidence['programme']}
    if review.get('decision') == 'withhold' and (review.get('pulls') or review.get('adds') or review.get('exclusions')):
        raise ValueError('A withhold cannot assign the missing piece')
    for pull in review.get('pulls') or []:
        source, dest, track_id = pull['from_target'], pull['to_target'], pull['track_id']
        if track_id not in assigned.get(source, []) or pull['title_contains'] not in tracks[track_id]['title']:
            raise ValueError('Pull does not match the current track')
        if not allowed(pull.get('catalogue_exception'), dest, tracks[track_id]['title']):
            raise ValueError('Pull catalogue conflict is not an allowed exception')
        assigned[source].remove(track_id)
        assigned[dest].append(track_id)
    for exclusion in review.get('exclusions') or []:
        if exclusion['track_id'] not in assigned.get(exclusion['target'], []):
            raise ValueError('Excluded track is not on that work')
        track = tracks[exclusion['track_id']]
        if exclusion['title_contains'] not in track['title']:
            raise ValueError('Excluded track title changed')
        if 'duration_seconds' in exclusion and abs(track['duration'] - exclusion['duration_seconds']) > 2:
            raise ValueError('Excluded track duration does not match')
        assigned[exclusion['target']].remove(exclusion['track_id'])
    for add in review.get('adds') or []:
        track = tracks.get(add['track_id'])
        if track is None or any(add['track_id'] in ids for ids in assigned.values()):
            raise ValueError('Added track is missing or already used')
        if add['title_contains'] not in track['title']:
            raise ValueError('Added track title changed')
        if not allowed(add.get('catalogue_exception'), add['target'], track['title']):
            raise ValueError('Added catalogue conflict is not an allowed exception')
        if 'duration_seconds' in add and abs(track['duration'] - add['duration_seconds']) > 2:
            raise ValueError('Bound take duration does not match')
        assigned[add['target']].append(add['track_id'])
    assigned = {target: sorted(ids, key=order.get) for target, ids in assigned.items()}
    used = [track_id for ids in assigned.values() for track_id in ids]
    if len(used) != len(set(used)):
        raise ValueError('A track is used by two works')
    extras = [t['id'] for t in album['tracks']['items'] if t['id'] not in set(used)]
    return evidence, assigned, extras


def assess_bindings(row, album, review):
    path = ROOT / f"raw/discogs/releases/{review['discogs_id']}.json"
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != review['source_sha256']:
        raise ValueError('Cached Discogs source changed; review the binding again')
    evidence, assigned, extras = assign(row, album, review)
    if extras != review.get('extra_track_ids', []):
        raise ValueError('Extra tracks changed')
    missing = [target for target, ids in assigned.items() if not ids]
    if review['decision'] == 'withhold':
        if missing != review['missing_targets']:
            raise ValueError('The gap changed; review it again')
        for token in review.get('absent_tokens', []):
            if any(token in norm(track['title']) for track in album['tracks']['items']):
                raise ValueError('A supposedly absent title is present')
        evidence['reasons'] = [review['recording_review']]
        return {'discogs_id': review['discogs_id'], 'album_id': review['album_id'], 'decision': 'withhold',
                'recording_review': review['recording_review'], 'sources': review['sources'],
                'limitations': review['limitations'], 'eligible': False, 'blockers': ['missing:' + t for t in missing],
                'completeness': {'status': 'unknown', 'works': []}}, evidence
    tracks = {t['id']: t for t in album['tracks']['items']}
    if missing or {target: ids for target, ids in assigned.items()} != review['expected']:
        raise ValueError('Bound assignment changed')
    blockers = []
    for ids in assigned.values():
        for track_id in ids:
            if any(not agrees(name, credits(tracks[track_id])) for name in review['required_performers']):
                blockers.append('performer')
    if review.get('movement_runs'):
        for ids in assigned.values():
            labels = []
            for track_id in ids:
                labels.extend(romans(tracks[track_id]['title']))
            if labels != list(range(1, len(labels) + 1)):
                blockers.append('movements')
    for mark in review.get('marks') or []:
        if mark['text'] not in tracks[mark['track_id']]['title']:
            blockers.append('mark')
    blockers = list(dict.fromkeys(blockers))
    works = [{'target': target, 'status': 'complete' if not blockers else 'unknown',
              'scope': 'reviewed-bound-tracks', 'track_ids': ids} for target, ids in assigned.items()]
    if not blockers:
        evidence['programme'] = [{**item, 'track_ids': assigned[item['target']],
                                  'work_tracks': len(assigned[item['target']]),
                                  'credited_tracks': len(assigned[item['target']])}
                                 for item in evidence['programme']]
        evidence.update(covered=len(evidence['programme']), target_count=len(evidence['programme']),
                        coverage=1, reasons=['Reviewed track bindings cover every named piece. Extra tracks stay outside that programme.'])
    result = {'discogs_id': review['discogs_id'], 'album_id': review['album_id'], 'decision': review['decision'],
              'recording_review': review['recording_review'], 'sources': review['sources'], 'limitations': review['limitations'],
              'eligible': review['decision'] == 'probable' and not blockers, 'blockers': blockers,
              'completeness': {'status': 'complete' if not blockers else 'unknown', 'works': works}}
    return result, evidence
