"""A source heading may cover works that already have their own tracks."""
import hashlib
import json
import re
from qobuz_lead_review import ROOT
from qobuz_match import agrees, catalogue, credits, norm


def romans(title):
    values = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7}
    return [values[token] for token in re.findall(r'(?:^|[\s:])(VII|VI|V|IV|III|II|I)\.', title)]


def assess_headings(row, album, review):
    from qobuz_match import evaluate
    path = ROOT / f"raw/discogs/releases/{review['discogs_id']}.json"
    raw_bytes = path.read_bytes()
    if hashlib.sha256(raw_bytes).hexdigest() != review['source_sha256']:
        raise ValueError('Cached Discogs source changed; review the heading again')
    raw = json.loads(raw_bytes)
    headings = [t.get('title') for t in raw.get('tracklist', []) if t.get('type_') == 'heading']
    containers = review['container_titles']
    if containers != [title for title in headings if title in containers] or any(title not in headings for title in containers):
        raise ValueError('Container titles must be source headings')
    if any(catalogue(title) or re.search(r'\b(op|bwv|no)\b', norm(title)) for title in containers):
        raise ValueError('A catalogue number cannot be treated as a container')
    evidence = evaluate(row, album)
    unmatched = [item['target'] for item in evidence['programme'] if not item['track_ids']]
    if unmatched != containers:
        raise ValueError('A missing piece cannot be reclassified as a container')
    tracks = {t['id']: t for t in album['tracks']['items']}
    order = {t['id']: index for index, t in enumerate(album['tracks']['items'])}
    assigned = {}
    for item in evidence['programme']:
        if item['target'] in containers:
            continue
        if not item['track_ids']:
            raise ValueError('A listed work has no credited track')
        assigned[item['target']] = sorted(item['track_ids'], key=order.get)
    used = [track_id for ids in assigned.values() for track_id in ids]
    if len(used) != len(set(used)):
        raise ValueError('A track is used by two works')
    extras = [t['id'] for t in album['tracks']['items'] if t['id'] not in set(used)]
    if extras != review.get('extra_track_ids', []) or assigned != review['expected']:
        raise ValueError('Heading assignment changed')
    blockers = []
    for ids in assigned.values():
        labels = []
        for track_id in ids:
            if any(not agrees(name, credits(tracks[track_id])) for name in review['required_performers']):
                blockers.append('performer')
            labels.extend(romans(tracks[track_id]['title']))
        if review.get('movement_runs') and labels != list(range(1, len(labels) + 1)):
            blockers.append('movements')
    blockers = list(dict.fromkeys(blockers))
    works = [{'target': target, 'status': 'complete' if not blockers else 'unknown',
              'scope': 'reviewed-heading-group', 'track_ids': ids} for target, ids in assigned.items()]
    if not blockers:
        evidence['programme'] = [{**item, 'track_ids': assigned.get(item['target'], []),
                                  'work_tracks': len(assigned.get(item['target'], [])),
                                  'credited_tracks': len(assigned.get(item['target'], []))}
                                 for item in evidence['programme'] if item['target'] not in containers]
        evidence.update(covered=len(works), target_count=len(works), coverage=1 if works else 0,
                        reasons=['The source heading names the programme. Each listed work keeps its own credited tracks.'])
    result = {'discogs_id': review['discogs_id'], 'album_id': review['album_id'], 'decision': review['decision'],
              'recording_review': review['recording_review'], 'sources': review['sources'], 'limitations': review['limitations'],
              'eligible': review['decision'] == 'probable' and not blockers, 'blockers': blockers,
              'completeness': {'status': 'complete' if not blockers else 'unknown', 'works': works}}
    return result, evidence
