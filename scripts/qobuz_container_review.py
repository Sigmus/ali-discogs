"""Hash-bound container headings. A numbered work cannot be reclassified as one."""
import hashlib
import json
import re
from qobuz_lead_review import ROOT
from qobuz_match import agrees, catalogue, credits, norm


def assess_containers(row, album, review):
    from qobuz_match import evaluate
    path = ROOT / f"raw/discogs/releases/{review['discogs_id']}.json"
    raw_bytes = path.read_bytes()
    if hashlib.sha256(raw_bytes).hexdigest() != review['source_sha256']:
        raise ValueError('Cached Discogs source changed; review the headings again')
    raw = json.loads(raw_bytes)
    if str(raw.get('id')) != str(review['discogs_id']):
        raise ValueError('Cached Discogs release ID mismatch')
    headings = [t.get('title') for t in raw.get('tracklist', []) if t.get('type_') == 'heading']
    containers = review['container_titles']
    if containers != [t for t in headings if t in containers] or any(t not in headings for t in containers):
        raise ValueError('Container titles must be source headings')
    if any(catalogue(t) or re.search(r'\b(op|bwv|no)\b', norm(t)) for t in containers):
        raise ValueError('A catalogue number cannot be treated as a container')
    evidence = evaluate(row, album)
    unmatched = [p['target'] for p in evidence['programme'] if not p['track_ids']]
    if unmatched != containers:
        raise ValueError('A missing piece cannot be reclassified as a container')
    tracks = album['tracks']['items']
    ids = []
    programme = []
    blockers = []
    if [t['id'] for t in tracks] != review['expected_track_ids']:
        blockers.append('track-set')
    for item in evidence['programme']:
        if item['target'] in containers:
            continue
        if len(item['track_ids']) != 1:
            blockers.append('not-one-track')
        else:
            track = next(t for t in tracks if t['id'] == item['track_ids'][0])
            if not agrees(review['performer'], credits(track)):
                blockers.append('performer:' + item['target'])
        ids.extend(item['track_ids'])
        programme.append(item)
    if ids != review['expected_track_ids'] or len(set(ids)) != len(ids):
        blockers.append('track-accounting')
    blockers = list(dict.fromkeys(blockers))
    covered = 0 if blockers else len(programme)
    evidence.update(programme=programme, target_count=len(programme), covered=covered,
                    coverage=covered / len(programme) if programme else 0,
                    reasons=(['Each listed piece has its own credited track. The source heading is a container, not an extra work.']
                             if not blockers else ['Container review unresolved: ' + ', '.join(blockers)]))
    result = {'discogs_id': review['discogs_id'], 'album_id': review['album_id'], 'decision': review['decision'],
              'recording_review': review['recording_review'], 'sources': review['sources'], 'limitations': review['limitations'],
              'eligible': review['decision'] == 'probable' and not blockers, 'blockers': blockers,
              'completeness': {'status': 'complete' if not blockers else 'unknown',
                               'works': [{'target': p['target'], 'status': 'complete' if not blockers else 'unknown',
                                          'scope': 'reviewed-single-track', 'track_ids': p['track_ids']} for p in programme]}}
    return result, evidence
