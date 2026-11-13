"""Hash-bound reviews for saved albums whose titles are split across a heading."""
import hashlib
import json
import re
from qobuz_lead_review import ROOT
from qobuz_match import agrees, credits, norm


def assess_labels(row, album, review):
    from qobuz_match import evaluate
    raw = (ROOT / f"raw/discogs/releases/{review['discogs_id']}.json").read_bytes()
    if hashlib.sha256(raw).hexdigest() != review['source_sha256']:
        raise ValueError('Cached Discogs source changed; review the labels again')
    evidence = evaluate(row, album)
    by_target = {item['target']: item for item in evidence['programme']}
    tracks = {t['id']: t for t in album['tracks']['items']}
    for label in review['labels']:
        item, parent = by_target[label['title']], by_target[label['parent']]
        if item['track_ids'] or parent['track_ids'] != label['parent_track_ids']:
            raise ValueError('A movement label is no longer covered by its heading')
        blob = ' '.join(tracks[track_id]['title'] for track_id in parent['track_ids'])
        if any(token not in blob for token in label['title_contains']):
            raise ValueError('The heading tracks no longer contain the movement label')
    kept = [item for item in evidence['programme'] if item['target'] not in {label['title'] for label in review['labels']}]
    if any(not item['track_ids'] for item in kept):
        raise ValueError('A listed work still has no track')
    used = [track_id for item in kept for track_id in item['track_ids']]
    if len(used) != len(set(used)):
        raise ValueError('A track is used by two headings')
    extras = [t['id'] for t in album['tracks']['items'] if t['id'] not in set(used)]
    if extras != review['extra_track_ids']:
        raise ValueError('Extra tracks changed')
    blockers = ['performer'] if any(
        not agrees(name, credits(tracks[track_id]))
        for track_id in used for name in review['required_performers']) else []
    if not blockers:
        evidence['programme'] = kept
        evidence.update(covered=len(kept), target_count=len(kept), coverage=1 if kept else 0,
                        reasons=['The movement labels sit under headings that already have their tracks.'])
    result = {'discogs_id': review['discogs_id'], 'album_id': review['album_id'], 'decision': review['decision'],
              'recording_review': review['recording_review'], 'sources': review['sources'], 'limitations': review['limitations'],
              'eligible': review['decision'] == 'probable' and not blockers, 'blockers': blockers,
              'completeness': {'status': 'complete' if not blockers else 'unknown', 'works': [
                  {'target': item['target'], 'status': 'complete', 'scope': 'reviewed-covered-label', 'track_ids': item['track_ids']}
                  for item in kept]}}
    return result, evidence


def mode_of(title):
    words = norm(title).split()
    if 'minor' in words:
        return 'minor'
    if 'major' in words:
        return 'major'
    return ''


def assess_opus_pieces(row, album, review):
    raw_bytes = (ROOT / f"raw/discogs/releases/{review['discogs_id']}.json").read_bytes()
    if hashlib.sha256(raw_bytes).hexdigest() != review['source_sha256']:
        raise ValueError('Cached Discogs source changed; review the pieces again')
    raw = json.loads(raw_bytes)
    tracks = list(album['tracks']['items'])
    used = {}
    assigned, conflicts = {}, []
    opus = None
    for entry in raw.get('tracklist', []):
        if entry.get('type_') == 'heading':
            opus = entry.get('title') or ''
            continue
        title = entry.get('title') or ''
        number = re.search(r'\b(?:no|nr)\s*(\d+)\b', norm(title))
        opus_number = re.search(r'\b(\d+)\b', norm(opus or ''))
        if number and opus_number:
            hits = [t for t in tracks if t['id'] not in used
                    and re.search(rf'\bno\.?\s*{number.group(1)}\b', norm(t['title']))
                    and re.search(rf'\b{opus_number.group(1)}\b', norm(t['title']))]
        else:
            token = review['nicknames'][title]
            hits = [t for t in tracks if t['id'] not in used and token in norm(t['title'])]
        if len(hits) != 1:
            raise ValueError('A numbered piece does not match one track')
        track = hits[0]
        source_mode, file_mode = mode_of(title), mode_of(track['title'])
        if file_mode == 'minor' and source_mode != 'minor':
            conflicts.append({'opus': opus, 'title': title, 'track_id': track['id'], 'file_mode': file_mode})
        elif source_mode and file_mode and source_mode != file_mode:
            conflicts.append({'opus': opus, 'title': title, 'track_id': track['id'], 'file_mode': file_mode})
        label = f'{opus}: {title}' if opus and opus not in {'-', ''} else title
        if label in assigned:
            raise ValueError('Two pieces resolved to the same title')
        used[track['id']] = label
        assigned[label] = [track['id']]
    extras = [t['id'] for t in tracks if t['id'] not in used]
    if extras != review['extra_track_ids'] or conflicts != review['mode_conflicts']:
        raise ValueError('Piece assignment changed')
    blockers = []
    for track_id in used:
        names = credits(next(t for t in tracks if t['id'] == track_id))
        if any(not agrees(name, names) for name in review['required_performers']):
            blockers.append('performer')
            break
    from qobuz_match import evaluate
    evidence = evaluate(row, album)
    if not blockers:
        evidence['programme'] = [{'target': title, 'track_ids': ids, 'work_tracks': 1, 'credited_tracks': 1}
                                 for title, ids in assigned.items()]
        evidence.update(covered=len(assigned), target_count=len(assigned), coverage=1 if assigned else 0,
                        reasons=['Each opus heading names the pieces that follow it. The heading is not a separate work.'])
    result = {'discogs_id': review['discogs_id'], 'album_id': review['album_id'], 'decision': review['decision'],
              'recording_review': review['recording_review'], 'sources': review['sources'], 'limitations': review['limitations'],
              'eligible': review['decision'] == 'probable' and not blockers, 'blockers': blockers,
              'completeness': {'status': 'complete' if not blockers else 'unknown', 'works': [
                  {'target': title, 'status': 'complete', 'scope': 'reviewed-opus-piece', 'track_ids': ids}
                  for title, ids in assigned.items()]}}
    return result, evidence
