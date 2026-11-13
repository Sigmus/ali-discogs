"""A numbered LP side may cover that many consecutive tracks. Named singers stay required."""
import hashlib
import json
import re
from qobuz_lead_review import ROOT
from qobuz_match import agrees, catalogue, credits, norm


SKIPPED_ROLE = {'producer', 'engineer', 'composed', 'composer', 'editor', 'supervisor', 'tonmeister'}


def source_people(raw):
    names = []
    for artist in raw.get('extraartists') or []:
        if set(norm(artist.get('role') or '').split()) & SKIPPED_ROLE:
            continue
        name = (artist.get('name') or '').strip()
        if not name:
            raise ValueError('Unnamed source credit')
        names.append(name)
    if len(names) != len(set(names)):
        raise ValueError('Duplicate source credit')
    return names


def span(title):
    match = re.fullmatch(r'nr (\d+) (\d+)', norm(title))
    if not match:
        return None
    start, end = (int(match.group(1)), int(match.group(2)))
    if start < 1 or end < start:
        return None
    return start, end


def assess_ranges(row, album, review):
    from qobuz_match import evaluate, units
    path = ROOT / f"raw/discogs/releases/{review['discogs_id']}.json"
    raw_bytes = path.read_bytes()
    if hashlib.sha256(raw_bytes).hexdigest() != review['source_sha256']:
        raise ValueError('Cached Discogs source changed; review the side ranges again')
    raw = json.loads(raw_bytes)
    headings = [track.get('title') for track in raw.get('tracklist', []) if track.get('type_') == 'heading']
    containers = review['container_titles']
    if containers != headings:
        raise ValueError('Container titles must be the source headings')
    if any(catalogue(title) or re.search(r'\b(op|bwv|no)\b', norm(title)) for title in containers):
        raise ValueError('A catalogue number cannot be treated as a container')
    people = source_people(raw)
    listed = [*review['on_every_track'], *review['in_each_range'], *review['somewhere']]
    if sorted(listed) != sorted(people) or len(listed) != len(set(listed)):
        raise ValueError('A named singer, choir, or ensemble is missing from the review')
    evidence = evaluate(row, album)
    ranges = review['ranges']
    if [item['target'] for item in evidence['programme']] != [*containers, *[item['target'] for item in ranges]]:
        raise ValueError('The side ranges do not match the source units')
    if units(row) != [item['target'] for item in evidence['programme']]:
        raise ValueError('The side ranges do not match the source units')
    tracks = {track['id']: track for track in album['tracks']['items']}
    order = {track['id']: index for index, track in enumerate(album['tracks']['items'])}
    assigned, previous = [], 0
    for item in ranges:
        bounds = span(item['target'])
        ids = [track['track_id'] for track in item['tracks']]
        if any(track_id not in tracks for track_id in ids):
            raise ValueError('Bound track is missing')
        if bounds is None or bounds[0] != previous + 1 or len(ids) != bounds[1] - bounds[0] + 1:
            raise ValueError('A side range does not name that many numbers')
        previous = bounds[1]
        if [order[track_id] for track_id in ids] != list(range(order[ids[0]], order[ids[0]] + len(ids))):
            raise ValueError('A side range is not consecutive')
        for track_id, bound in zip(ids, item['tracks']):
            title = tracks[track_id]['title']
            snippet = bound['title_contains']
            if not snippet or snippet not in title or sum(snippet in other['title'] for other in album['tracks']['items']) != 1:
                raise ValueError('Bound title changed')
        assigned.append((item['target'], ids))
    used = [track_id for _, ids in assigned for track_id in ids]
    if len(used) != len(set(used)):
        raise ValueError('A track is used by two sides')
    extras = [track['id'] for track in album['tracks']['items'] if track['id'] not in set(used)]
    if extras != review.get('extra_track_ids', []) or used != [track['id'] for track in album['tracks']['items'] if track['id'] not in set(extras)]:
        raise ValueError('Side ranges do not follow the album')
    blockers = []
    for name in review['on_every_track']:
        if any(not agrees(name, credits(tracks[track_id])) for track_id in used):
            blockers.append('performer')
    for name in review['in_each_range']:
        if any(not any(agrees(name, credits(tracks[track_id])) for track_id in ids) for _, ids in assigned):
            blockers.append('performer')
    for name in review['somewhere']:
        if not any(agrees(name, credits(tracks[track_id])) for track_id in used):
            blockers.append('performer')
    blockers = list(dict.fromkeys(blockers))
    works = [{'target': target, 'status': 'complete' if not blockers else 'unknown',
              'scope': 'reviewed-side-range', 'track_ids': ids} for target, ids in assigned]
    if not blockers:
        kept = [item for item in evidence['programme'] if item['target'] not in containers]
        evidence['programme'] = [{**item, 'track_ids': ids, 'work_tracks': len(ids), 'credited_tracks': len(ids)}
                                 for item, (_, ids) in zip(kept, assigned)]
        evidence.update(covered=len(works), target_count=len(works), coverage=1 if works else 0,
                        reasons=['The heading names the cantata. Each LP side keeps its numbered movements.'])
    result = {'discogs_id': review['discogs_id'], 'album_id': review['album_id'], 'decision': review['decision'],
              'recording_review': review['recording_review'], 'sources': review['sources'], 'limitations': review['limitations'],
              'eligible': review['decision'] == 'probable' and not blockers, 'blockers': blockers,
              'completeness': {'status': 'complete' if not blockers else 'unknown', 'works': works}}
    return result, evidence
