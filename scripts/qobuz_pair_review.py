"""Hash-bound prelude/fugue pair review. No catalogue calls."""
import hashlib
import json
import re
from qobuz_lead_review import ROOT, fingerprint
from qobuz_match import agrees, credits, norm, units


def bwvs(title):
    text = norm(title)
    found = [int(n) for n in re.findall(r'\bbwv\s*(\d+)\b', text)]
    found.extend(int(n) for n in re.findall(r'\bbwv\s*\d+\s+(\d+)\b', text))
    return found


def pair_work(title):
    return len(bwvs(title)) == 1


def role_of(title):
    text = norm(title)
    if text.startswith('prelude'):
        return 'prelude'
    if text.startswith('fugue'):
        return 'fugue'
    return None


def assess_pairs(row, album, review):
    from qobuz_match import evaluate
    path = ROOT / f"raw/discogs/releases/{review['discogs_id']}.json"
    raw_bytes = path.read_bytes()
    if hashlib.sha256(raw_bytes).hexdigest() != review['source_sha256']:
        raise ValueError('Cached Discogs source changed; review the pairs again')
    raw = json.loads(raw_bytes)
    notes = norm(raw.get('notes') or '')
    if any(marker not in notes for marker in review['source_markers']):
        raise ValueError('Source recording markers are absent')
    if (album.get('label') or {}).get('name') != review['candidate_label']:
        raise ValueError('Candidate label changed')
    titles = units(row)
    containers = [t for t in titles if not pair_work(t)]
    works = [t for t in titles if pair_work(t)]
    if containers != review['container_titles'] or [bwvs(t)[0] for t in works] != list(range(846, 894)):
        raise ValueError('Container headings or BWV sequence changed; do not drop a heading silently')
    tracks = album['tracks']['items']
    if review['expected_track_ids'] != [t['id'] for t in tracks]:
        blockers = ['track-set']
    else:
        blockers = []
    bare_ids = [t['id'] for t in tracks if norm(t['title']) == 'prelude']
    if bare_ids != [b['track_id'] for b in review['bare_preludes']]:
        raise ValueError('Bare prelude set changed')
    bare = {}
    for spec in review['bare_preludes']:
        track = next(t for t in tracks if t['id'] == spec['track_id'])
        if fingerprint(track) != spec['track_sha256'] or norm(track['title']) != 'prelude':
            raise ValueError('Bare prelude changed')
        bare[spec['track_id']] = spec['bwv']
    found, used, order = {}, [], []
    index = 0
    while index < len(tracks):
        track = tracks[index]
        if track['id'] in bare:
            bwv = bare[track['id']]
            nxt = tracks[index + 1] if index + 1 < len(tracks) else None
            if nxt is None or bwvs(nxt['title']) != [bwv] or role_of(nxt['title']) != 'fugue':
                blockers.append(f'bare-prelude-{bwv}')
            else:
                found.setdefault(bwv, {})['prelude'] = track
                found[bwv]['fugue'] = nxt
                used.extend([track['id'], nxt['id']])
                order.append(bwv)
            index += 2
            continue
        nums, role = bwvs(track['title']), role_of(track['title'])
        if len(nums) != 1 or role is None or nums[0] not in range(846, 894):
            blockers.append('unassigned-track')
        else:
            slot = found.setdefault(nums[0], {})
            if role in slot:
                blockers.append(f'duplicate-{nums[0]}')
            else:
                slot[role] = track
                used.append(track['id'])
                if role == 'fugue' and 'prelude' in slot:
                    order.append(nums[0])
        index += 1
    if used != [t['id'] for t in tracks]:
        blockers.append('track-accounting')
    if order != [bwvs(t)[0] for t in works]:
        blockers.append('order')
    programme = []
    for title in works:
        bwv = bwvs(title)[0]
        pair = found.get(bwv, {})
        pair_tracks = [pair.get('prelude'), pair.get('fugue')]
        if any(t is None or not agrees(review['performer'], credits(t)) for t in pair_tracks):
            blockers.append(f'pair-{bwv}')
            programme.append({'target': title, 'work_tracks': 0, 'credited_tracks': 0, 'track_ids': []})
        else:
            programme.append({'target': title, 'work_tracks': 2, 'credited_tracks': 2,
                              'track_ids': [t['id'] for t in pair_tracks]})
    blockers = list(dict.fromkeys(blockers))
    evidence = evaluate(row, album)
    covered = 0 if blockers else len(works)
    evidence.update(programme=programme, target_count=len(works), covered=covered,
                    coverage=covered / len(works) if works else 0,
                    reasons=(['Each BWV has its own prelude and fugue with the required pianist. Volume headings are containers, not extra works.']
                             if not blockers else ['Prelude/fugue review unresolved: ' + ', '.join(blockers)]))
    result = {'discogs_id': review['discogs_id'], 'album_id': review['album_id'], 'decision': review['decision'],
              'recording_review': review['recording_review'], 'sources': review['sources'], 'limitations': review['limitations'],
              'eligible': review['decision'] == 'probable' and not blockers, 'blockers': blockers,
              'completeness': {'status': 'complete' if not blockers else 'unknown',
                               'works': [{'target': item['target'], 'status': 'complete' if item['credited_tracks'] == 2 else 'unknown',
                                          'scope': 'reviewed-prelude-fugue-pair', 'track_ids': item['track_ids']} for item in programme]}}
    return result, evidence
