"""Manual source-band mappings: retain every raw leaf, explicit work credit and track hash."""
import json
from qobuz_lead_review import ROOT, fingerprint
from qobuz_match import evaluate, agrees, credits
from qobuz_target_credits import requirements, musical
from qobuz_composer_identity import composer_key
from qobuz_work_groups import role_entries
from qobuz_completeness import seconds


def source_leaves(raw):
    leaves = []
    def visit(track, path, work):
        children = track.get('sub_tracks', [])
        if children:
            for i, child in enumerate(children):
                visit(child, path+[i], work)
        elif track.get('type_') == 'heading':
            return  # Structural headings remain frozen in the entire source outline.
        else:
            if track.get('type_') not in {'track', 'index'} or not track.get('title'):
                raise ValueError('Unsupported source leaf')
            leaves.append({'path': path, 'source_work': work, 'title': track['title'],
                           'position': track.get('position', ''), 'duration': track.get('duration', '')})
    for i, track in enumerate(raw['tracklist']):
        visit(track, [i], track['title'])
    return leaves


def source_headings(raw):
    leaves = source_leaves(raw)
    groups = []
    headings = [i for i, t in enumerate(raw['tracklist']) if t.get('type_') == 'heading' and not t.get('sub_tracks')]
    for n, start in enumerate(headings):
        end = headings[n+1] if n+1 < len(headings) else len(raw['tracklist'])
        paths = [leaf['path'] for leaf in leaves if start < leaf['path'][0] < end]
        if not paths:
            raise ValueError('An unaccounted source heading cannot be ignored')
        groups.append({'source_path': [start], 'title': raw['tracklist'][start]['title'], 'covered_source_paths': paths})
    return groups


def assess_leaves(row, album, review):
    raw = json.loads((ROOT/f"raw/discogs/releases/{review['discogs_id']}.json").read_text())
    leaves = source_leaves(raw)
    if (fingerprint(raw['tracklist']) != review['source_outline_sha256']
            or leaves != review['source_leaves']
            or source_headings(raw) != review['source_heading_groups']
            or not review.get('external_source_files')):
        raise ValueError('Entire source outline and every musical leaf need frozen recording evidence')
    bindings = review['bindings']
    if [b['source_path'] for b in bindings] != [s['path'] for s in leaves]:
        raise ValueError('A source band was omitted, reused or reordered')
    tracks = album['tracks']['items']
    if len(tracks) != album['tracks_count'] or len({t['id'] for t in tracks}) != len(tracks):
        raise ValueError('Incomplete candidate album')
    by_id = {t['id']: t for t in tracks}
    evidence = evaluate(row, album)
    global_names = list(dict.fromkeys([*evidence['required_performers'],
        *[a['name'] for a in raw.get('extraartists', []) if not a.get('tracks') and musical(a.get('role', ''))]]))
    allowed_composers = {composer_key(c) for c in row['composers']}
    for spelling in review.get('source_composer_spellings', []):
        if (spelling['source_name'] not in row['composers']
                or len(spelling['reason']) < 40 or not spelling['file_name']):
            raise ValueError('Composer spelling needs explicit source identity and justification')
        allowed_composers.add(composer_key(spelling['file_name']))
    used, programme, works, blockers = [], [], [], []
    for source, binding in zip(leaves, bindings):
        _, required, _ = requirements(row, source['source_work'], global_names)
        if required != binding['required_performers']:
            raise ValueError('A source musical credit or existing source scope changed')
        selected = [by_id[i] for i in binding['track_ids'] if i in by_id]
        if (not selected or len(selected) != len(binding['track_ids'])
                or any(i in used for i in binding['track_ids'])
                or [fingerprint(t) for t in selected] != binding['track_sha256']):
            raise ValueError('An exact selected source-band track changed or was reused')
        composer = binding['composer']
        if composer_key(composer) not in allowed_composers:
            raise ValueError('A band cannot introduce a composer absent from the source')
        credited = 0
        for track in selected:
            composers = {composer_key(n) for n, roles in role_entries(track) if 'composer' in roles}
            if composers != {composer_key(composer)}:
                blockers.append('composer')
            if all(agrees(n, credits(track)) for n in required):
                credited += 1
            else:
                blockers.append('performer')
        duration = seconds(source['duration'])
        actual_duration = sum(t['duration'] for t in selected)
        duration_notes = [n for n in review.get('source_duration_notes', []) if n['source_path'] == source['path']]
        if duration_notes:
            if (len(duration_notes) != 1 or duration_notes[0]['source_seconds'] != duration
                    or duration_notes[0]['digital_seconds'] != actual_duration
                    or len(duration_notes[0]['reason']) < 40):
                raise ValueError('Reviewed source duration discrepancy changed')
        if duration is not None and abs(actual_duration-duration) > max(5, .03*duration) and not duration_notes:
            blockers.append('source-band-duration')
        used.extend(binding['track_ids'])
        label = (source['position']+': ' if source['position'] else '')+source['title']
        programme.append({'target': label, 'source_path': source['path'],
                          'track_ids': binding['track_ids'], 'work_tracks': len(selected),
                          'credited_tracks': credited, 'required_performers': required})
        works.append({'target': label, 'source_path': source['path'], 'status': 'complete',
                      'track_ids': binding['track_ids'], 'scope': 'reviewed-complete-source-band',
                      'source_duration_seconds': duration, 'digital_duration_seconds': actual_duration,
                      'source_duration_notes': duration_notes})
    if [t['id'] for t in tracks if t['id'] not in set(used)] != review['extra_track_ids']:
        raise ValueError('Candidate extras changed')
    if {str(i): fingerprint(by_id[i]) for i in used} != review['selected_track_fingerprints']:
        raise ValueError('The complete selected programme changed')
    blockers = list(dict.fromkeys(blockers))
    complete = bool(leaves) and not blockers
    for work in works:
        work['status'] = 'complete' if complete else 'unknown'
    evidence.update(programme=programme, covered=len(leaves) if complete else 0,
                    target_count=len(leaves), coverage=1 if complete else 0,
                    reasons=['Every raw source band is retained in a frozen source-position/track mapping. Existing explicit work-scoped musician requirements remain; no credit is borrowed from another piece.'])
    return {'discogs_id': review['discogs_id'], 'album_id': review['album_id'],
            'decision': review['decision'], 'recording_review': review['recording_review'],
            'sources': review['sources'], 'limitations': review['limitations'],
            'eligible': review['decision'] == 'probable' and complete, 'blockers': blockers,
            'completeness': {'status': 'complete' if complete else 'unknown', 'works': works}}, evidence
