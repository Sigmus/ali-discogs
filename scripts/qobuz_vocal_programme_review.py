"""Frozen single-work vocal programmes; never infer LP-side audio boundaries."""
import json
import re
from qobuz_lead_review import ROOT, fingerprint
from qobuz_match import agrees, credits, norm
from qobuz_composer_identity import composer_key
from qobuz_opera_review import kind_of, labelled_act
from qobuz_work_groups import role_entries


def projection(raw):
    if any(t.get('sub_tracks') for t in raw['tracklist']):
        raise ValueError('Only reviewed flat vocal sources are supported')
    return [{'position': t.get('position', ''), 'title': t['title'],
             'type': t['type_'], 'duration': t.get('duration', '')} for t in raw['tracklist']]


def source_groups(row, raw, tracks, review):
    source = projection(raw)
    if source != row['tracklist'] or source != review['source_projection']:
        raise ValueError('Every source heading and band must be preserved')
    if review['programme_kind'] == 'passion-old-numbered-ranges':
        if (norm(row['title']) != 'st matthew passion' or len(source) != 10
                or source[0]['type'] != 'heading' or norm(source[0]['title']) != 'st matthew passion'
                or composer_key(review['composer']) != composer_key('Johann Sebastian Bach')):
            raise ValueError('Unsupported Passion source')
        parts = [re.search(r'\bPt\. ([12])\b', t['title']) for t in tracks]
        if len(tracks) != 78 or any(p is None for p in parts) or [int(p.group(1)) for p in parts] != [1]*35+[2]*43:
            raise ValueError('The complete reviewed 78-section Passion changed')
        previous, groups = 0, []
        for band in source[1:]:
            match = re.fullmatch(r'part ([12]) nos (\d+) to (\d+) inclusive', norm(band['title']))
            if match is None or band['type'] != 'track' or not band['position']:
                raise ValueError('Unrecognized source numbered side')
            part, start, end = map(int, match.groups())
            if start != previous+1 or end < start or end > 78 or any(int(p.group(1)) != part for p in parts[start-1:end]):
                raise ValueError('Source numbered sides omit, overlap or cross a work part')
            groups.append({'source_position': band['position'], 'source_title': band['title'],
                           'old_source_numbers': [start, end], 'track_ids': [t['id'] for t in tracks[start-1:end]]})
            previous = end
        if previous != 78:
            raise ValueError('Source numbered sides do not cover the complete work')
        # Old source numbers are section order, not the modern 68-plus-subsections labels.
        return groups
    if review['programme_kind'] == 'opera-whole-acts':
        if norm(row['title']) != 'otello' or composer_key(review['composer']) != composer_key('Giuseppe Verdi'):
            raise ValueError('Unsupported single-opera source')
        observed = []
        for band in source:
            match = re.fullmatch(r'act ([1-4])(?: part ([12]))?', norm(band['title']))
            if match is None or band['type'] != 'track' or not band['position']:
                raise ValueError('Unrecognized source opera side')
            observed.append((int(match.group(1)), int(match.group(2)) if match.group(2) else None))
        if observed != [(1, 1), (1, 2), (2, 1), (2, 2), (3, 1), (3, 2), (4, None)]:
            raise ValueError('The complete source act/part programme changed')
        acts = [labelled_act(t['title']) for t in tracks]
        if any(a not in {1, 2, 3, 4} for a in acts) or sorted(acts) != acts or set(acts) != {1, 2, 3, 4}:
            raise ValueError('All four complete ordered digital acts are required')
        return [{'source_act': act,
                 'source_sides': [band for band, pair in zip(source, observed) if pair[0] == act],
                 'track_ids': [t['id'] for t, a in zip(tracks, acts) if a == act]}
                for act in range(1, 5)]
    raise ValueError('Unsupported vocal programme kind')


def assess_vocal_programme(row, album, review):
    from qobuz_match import evaluate
    raw = json.loads((ROOT/f"raw/discogs/releases/{review['discogs_id']}.json").read_text())
    tracks = album['tracks']['items']
    if (len(tracks) != album['tracks_count'] or len({t['id'] for t in tracks}) != len(tracks)
            or [t['id'] for t in tracks] != review['expected_track_ids']
            or {str(t['id']): fingerprint(t) for t in tracks} != review['track_fingerprints']):
        raise ValueError('The reviewed complete vocal recording changed')
    groups = source_groups(row, raw, tracks, review)
    if groups != review['source_groups'] or not review.get('external_source_files'):
        raise ValueError('Vocal programme needs frozen source groups and recording-family proof')
    required = list(dict.fromkeys([*row['performers'],
        *[a['name'] for a in raw.get('extraartists', []) if kind_of(a.get('role', ''))]]))
    if required != review['required_performers']:
        raise ValueError('A named source singer, choir or musical credit was omitted')
    conductor = review['conductor_name']
    if conductor not in required or row.get('conductor') not in (None, conductor):
        raise ValueError('The source conductor identity changed')
    if row.get('conductor') is None and conductor not in [a['name'] for a in raw['artists']]:
        raise ValueError('An untyped conductor must be a named source artist, with external role proof')
    anchors = list(dict.fromkeys([conductor, *row['ensembles']]))
    if anchors != review['on_every_track'] or len(anchors) < 2:
        raise ValueError('Conductor and source orchestra must remain on every track')
    if {composer_key(c) for c in row['composers']} != {composer_key(review['composer'])}:
        raise ValueError('The source composer changed')
    all_credits = [name for t in tracks for name in credits(t)]
    blockers = ['absent:' + n for n in required if not agrees(n, all_credits)]
    for track in tracks:
        entries = role_entries(track)
        if any(not agrees(n, credits(track)) for n in anchors):
            blockers.append('missing-conductor-orchestra')
        if not any(agrees(conductor, [n]) and 'conductor' in roles for n, roles in entries):
            blockers.append('missing-conductor-role')
        composers = {composer_key(n) for n, roles in entries if 'composer' in roles}
        if composers != {composer_key(review['composer'])}:
            blockers.append('composer')
    blockers = list(dict.fromkeys(blockers))
    complete = not blockers
    ids = [t['id'] for t in tracks]
    work = {'target': row['title'], 'scope': 'reviewed-complete-single-vocal-work',
            'status': 'complete' if complete else 'unknown', 'track_ids': ids,
            'source_groups': groups, 'source_side_boundaries_verified': False}
    evidence = evaluate(row, album)
    evidence.update(programme=[{'target': row['title'], 'track_ids': ids, 'work_tracks': len(ids),
                                'credited_tracks': len(ids) if complete else 0}],
                    target_count=1, covered=int(complete), coverage=int(complete), required_performers=required,
                    reasons=['All source sides belong to the same complete named vocal work. Every named source musician remains required; conductor and orchestra are positive on every selected track. LP-side audio boundaries and exact takes are not verified.'])
    result = {'discogs_id': review['discogs_id'], 'album_id': review['album_id'],
              'decision': review['decision'], 'eligible': review['decision'] == 'probable' and complete,
              'recording_review': review['recording_review'], 'sources': review['sources'],
              'limitations': review['limitations'], 'blockers': blockers,
              'completeness': {'status': 'complete' if complete else 'unknown', 'works': [work]}}
    return result, evidence
