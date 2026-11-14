"""Hash-bound opera role, ensemble and act review. No catalogue calls."""
import hashlib
import json
import re
from qobuz_lead_review import ROOT, fingerprint
from qobuz_match import norm, person_key, units

ROMAN = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5}
EXEMPT = {'producer', 'engineer', 'balanceengineer', 'digitaleditingengineer', 'composer',
          'lyricist', 'poet', 'writer', 'editor', 'supervisor', 'tonmeister', 'librettist'}
FORBIDDEN = {'ignore', 'omit', 'optional', 'drop', 'skip', 'equate_director', 'uncredited_ok'}
VOICE = ('contralto', 'mezzo', 'baritone', 'soprano', 'tenor', 'bass', 'alto', 'treble')


def kind_of(role):
    text = norm(role)
    if 'chorus master' in text or 'chorusmaster' in text:
        return 'chorus-master'
    if 'conductor' in text:
        return 'conductor'
    if 'orchestra' in text:
        return 'orchestra'
    if re.search(r'\b(chorus|choir|chor)\b', text):
        return 'chorus'
    tokens = text.split()
    if any(tok == 'performer' or tok.startswith(VOICE) or 'vocal' in tok for tok in tokens):
        return 'vocal'
    return None


def voice_categories(text):
    cats = set()
    for tok in norm(text).split():
        if tok.startswith('bassoon'):
            continue
        for name in VOICE:
            if tok == name or tok.startswith(name):
                cats.add(name)
                break
        else:
            if 'vocal' in tok:
                cats.add('vocal')
    return cats - {'vocal'}


def looks_like_ensemble(name):
    return any(tok in {'orchester', 'orchestra', 'chor', 'choir', 'chorus'}
               or tok.endswith(('orchester', 'orchestra', 'spielchor', 'spielorchester'))
               for tok in norm(name).split())


def labelled_act(title):
    match = re.search(r'\bact\s+([ivx]+|\d+)\b', norm(title))
    if not match:
        return None
    value = match.group(1)
    return int(value) if value.isdigit() else ROMAN.get(value)


def source_act(title):
    text = norm(title)
    if re.search(r'\b(probe|rehearsal)\b', text):
        return 'bonus'
    match = re.search(r'\b([ivx]+|\d+)\s+aufzug\b', text)
    if match:
        value = match.group(1)
        return int(value) if value.isdigit() else ROMAN.get(value)
    if re.search(r'\b(ouverture|overture|vorspiel)\b', text) and 'aufzug' not in text:
        return 'prelude'
    return None


def scene_numbers(title, words):
    text = norm(title)
    word = '(?:' + '|'.join(words) + ')'
    before = [int(n) for n in re.findall(r'(\d+)(?=\s*(?:\d+\s*)*' + word + r'\b)', text)]
    after = [int(n) for n in re.findall(r'\b' + word + r'\s+(\d+)\b', text)]
    return list(dict.fromkeys([*before, *after]))


def credit_rows(tracks):
    rows = []
    for track in tracks:
        for part in (track.get('performers') or '').split(' - '):
            name, _, roles = part.partition(',')
            tokens = set(norm(roles).split())
            for segment in [s.strip() for s in name.split('/') if s.strip()]:
                rows.append({'track_id': track['id'], 'name': segment, 'key': person_key(segment), 'tokens': tokens})
    return rows


def assign_acts(tracks, policy):
    labels = [labelled_act(t['title']) for t in tracks]
    assigned, current = [], None
    for index, track in enumerate(tracks):
        label = labels[index]
        if label:
            current = label
            assigned.append(label)
            continue
        title = norm(track['title'])
        overture = bool(re.search(r'\b(ouverture|overture|vorspiel)\b', title))
        if current is None and overture and policy.get('prelude_act'):
            assigned.append(policy['prelude_act'])
        elif current is None and policy.get('attach_leading_unlabelled_to_next_act'):
            nxt = next((item for item in labels[index + 1:] if item), None)
            assigned.append(nxt)
        elif current is not None and policy.get('attach_contiguous_unlabelled'):
            assigned.append(current)
        else:
            assigned.append(None)
    return assigned


def load_source(review):
    path = ROOT / f"raw/discogs/releases/{review['discogs_id']}.json"
    raw_bytes = path.read_bytes()
    if hashlib.sha256(raw_bytes).hexdigest() != review['source_sha256']:
        raise ValueError('Cached Discogs source changed; review the opera again')
    raw = json.loads(raw_bytes)
    if str(raw.get('id')) != str(review['discogs_id']):
        raise ValueError('Cached Discogs release ID mismatch')
    expected = [{'name': a['name'], 'role': a['role'], 'kind': kind_of(a['role'])}
                for a in raw.get('extraartists', []) if kind_of(a['role'])]
    supplied = [{'name': e['name'], 'role': e['role'], 'kind': e['kind']} for e in review['source_roles']]
    if supplied != expected:
        raise ValueError('Source role inventory must list every musical credit; secondary artists cannot be omitted')
    for entry in review['source_roles']:
        if FORBIDDEN & set(entry):
            raise ValueError('Opera review cannot drop or equate a source credit')
    subs = [s for t in raw.get('tracklist', []) for s in t.get('sub_tracks') or []]
    return raw, subs


def assess_opera(row, album, review):
    from qobuz_match import evaluate
    raw, subs = load_source(review)
    titles = units(row)
    if len(titles) != 1 or any(e.get('kind') not in {'chorus-master', 'conductor', 'orchestra', 'chorus', 'vocal'} for e in review['source_roles']):
        raise ValueError('Unsupported opera review')
    policy = review['act_policy']
    classified = [(s, source_act(s.get('title', ''))) for s in subs]
    if any(act is None for _, act in classified):
        raise ValueError('Unclassified source side; do not ignore it')
    bonuses = [s for s, act in classified if act == 'bonus']
    gaps = review.get('edition_gaps', [])
    if [(s.get('position'), s.get('title')) for s in bonuses] != [(g['position'], g['title']) for g in gaps]:
        raise ValueError('Rehearsal or bonus sides must stay explicit')
    for gap in gaps:
        if any(re.search(r'\b' + re.escape(gap['absent_word']) + r'\b', norm(t['title'])) for t in album['tracks']['items']):
            raise ValueError('Listed edition gap is present; review the album again')
        if gap['limitation'] not in review['limitations']:
            raise ValueError('Edition gap must remain visible')
    preludes = [s for s, act in classified if act == 'prelude']
    if preludes and policy.get('prelude_act') not in policy['required_acts']:
        raise ValueError('Source prelude has no reviewed act')
    acts = assign_acts(album['tracks']['items'], policy)
    if 'expected_track_ids' not in review:
        raise ValueError('Opera review must bind every candidate track')
    observed_ids = [t['id'] for t in album['tracks']['items']]
    if len(acts) != len(observed_ids) or any(a not in policy['required_acts'] for a in acts):
        blockers = ['act-assignment']
    else:
        blockers = []
    if review['expected_track_ids'] != observed_ids:
        blockers.append('track-set')
    if any(act not in acts for act in policy['required_acts']):
        blockers.append('missing-act')
    source_scenes = {}
    for sub, act in classified:
        if isinstance(act, int):
            source_scenes.setdefault(act, set()).update(scene_numbers(sub.get('title', ''), ('szene', 'auftritt')))
    observed = {}
    for track, act in zip(album['tracks']['items'], acts):
        if isinstance(act, int):
            observed.setdefault(act, set()).update(scene_numbers(track['title'], ('scene', 'szene', 'auftritt')))
    if policy['scene_evidence'] == 'acts-only':
        if any(observed.values()):
            raise ValueError('Candidate scene labels need a scene review, not acts-only treatment')
    elif policy['scene_evidence'] == 'numbered-scenes':
        for act, numbers in source_scenes.items():
            if numbers - observed.get(act, set()):
                blockers.append(f'missing-scenes-{act}')
    else:
        raise ValueError('Unknown scene evidence policy')
    version = policy.get('version_word')
    if version and (version['source'] not in norm(raw.get('title', '')) or not any(version['candidate'] in norm(t['title']) for t in album['tracks']['items'])):
        blockers.append('version')
    rows = credit_rows([t for t, act in zip(album['tracks']['items'], acts) if act in policy['required_acts']])
    allowed = set()
    for entry in review['source_roles']:
        if entry['kind'] not in {'orchestra', 'chorus'}:
            continue
        candidate = entry.get('candidate_name', entry['name'])
        if person_key(candidate) != person_key(entry['name']) and len(entry.get('alias_reason', '')) < 20:
            raise ValueError('A differing ensemble name needs an explicit recording-specific reason')
        allowed.add(person_key(candidate))
        if not any(r['key'] == person_key(candidate) and (
                ('orchestra' in r['tokens'] or 'orchester' in norm(r['name'])) if entry['kind'] == 'orchestra'
                else bool(r['tokens'] & {'choir', 'chorus', 'chor'}) or 'chor' in norm(r['name']))
                for r in rows):
            blockers.append('missing-' + entry['kind'])
    required = {person_key(e['name']) for e in review['source_roles']}
    tokens_by_key = {}
    for row_credit in rows:
        if looks_like_ensemble(row_credit['name']) or row_credit['tokens'] & {'orchestra', 'choir', 'chorus'}:
            if row_credit['key'] not in allowed:
                blockers.append('conflicting-ensemble:' + row_credit['name'])
            continue
        tokens_by_key.setdefault(row_credit['key'], set()).update(row_credit['tokens'])
        if row_credit['key'] in required:
            continue
        performing = bool(voice_categories(' '.join(row_credit['tokens'])) or 'conductor' in row_credit['tokens'])
        exempt = bool(row_credit['tokens'] & EXEMPT) and not performing
        musical = performing or 'mainartist' in row_credit['tokens'] or {'main', 'artist'} <= row_credit['tokens']
        if musical and not exempt:
            blockers.append('extra-performer:' + row_credit['name'])
    for entry in review['source_roles']:
        key = person_key(entry['name'])
        seen = tokens_by_key.get(key, set())
        if entry['kind'] == 'vocal':
            if not seen:
                blockers.append('absent:' + entry['name'])
                if 'voice_conflict' in entry:
                    raise ValueError('Absent singer cannot carry a voice-type resolution')
                continue
            source_voice, found_voice = voice_categories(entry['role']), voice_categories(' '.join(seen))
            conflict = entry.get('voice_conflict')
            if source_voice != found_voice:
                if conflict != [sorted(source_voice), sorted(found_voice)]:
                    raise ValueError('Voice-type discrepancy must be explicit: ' + entry['name'])
            elif conflict:
                raise ValueError('Voice conflict recorded where categories agree: ' + entry['name'])
            if not found_voice and not seen:
                blockers.append('absent:' + entry['name'])
        elif entry['kind'] == 'chorus-master':
            if 'chorusmaster' not in seen and not ({'chorus', 'master'} <= seen):
                blockers.append('role-mismatch:' + entry['name'])
        elif entry['kind'] == 'conductor':
            conductor_tracks = {r['track_id'] for r in rows if r['key'] == key and 'conductor' in r['tokens']}
            if conductor_tracks != {t['id'] for t, act in zip(album['tracks']['items'], acts) if act in policy['required_acts']}:
                blockers.append('conductor-coverage')
        elif entry['kind'] == 'orchestra':
            candidate = person_key(entry.get('candidate_name', entry['name']))
            covered = {r['track_id'] for r in rows if r['key'] == candidate}
            if covered != {t['id'] for t, act in zip(album['tracks']['items'], acts) if act in policy['required_acts']}:
                blockers.append('orchestra-coverage')
    if policy['scene_evidence'] == 'acts-only' and not any('scene alignment is not claimed' in item for item in review['limitations']):
        raise ValueError('Acts-only coverage must say that scenes are unverified')
    blockers = list(dict.fromkeys(blockers))
    evidence = evaluate(row, album)
    counts = {act: acts.count(act) for act in policy['required_acts']}
    evidence['programme'] = [{'target': titles[0], 'work_tracks': len(acts), 'credited_tracks': 0 if blockers else len(acts),
                              'track_ids': [t['id'] for t, act in zip(album['tracks']['items'], acts) if act in policy['required_acts']],
                              'opera_acts': counts, 'scene_evidence': policy['scene_evidence']}]
    evidence.update(target_count=1, covered=0 if blockers else 1, coverage=0 if blockers else 1,
                    reasons=(['Reviewed act coverage, ensemble names and recording roles support this album.'] if not blockers else
                             ['Opera source-role review unresolved: ' + ', '.join(blockers)]))
    result = {'discogs_id': review['discogs_id'], 'album_id': review['album_id'], 'decision': review['decision'],
              'recording_review': review['recording_review'], 'sources': review['sources'], 'limitations': review['limitations'],
              'eligible': review['decision'] == 'probable' and not blockers,
              'blockers': blockers,
              'completeness': {'status': 'complete' if review['decision'] == 'probable' and not blockers else 'unknown',
                               'works': [{'target': titles[0], 'status': 'complete' if not blockers else 'unknown',
                                          'scope': 'reviewed-opera-acts', 'acts': counts,
                                          'scene_evidence': policy['scene_evidence']}]}}
    return result, evidence


PART_LIMIT = 'The file does not mark the part boundaries inside a scene.'


def side_scenes(title):
    text = norm(title)
    found = []
    for start, end in re.findall(r'\bscenes\s+(\d+)\s+to\s+(\d+)\b', text):
        start, end = int(start), int(end)
        if end < start:
            return None
        found.extend(range(start, end + 1))
    found.extend(int(number) for number in re.findall(r'\bscene\s+(\d+)\b', text))
    return list(dict.fromkeys(found)) or None


def assess_scene_sides(row, album, review):
    from qobuz_match import evaluate
    raw, _subs = load_source(review)
    listed = raw.get('tracklist', [])
    headings = [t for t in listed if t.get('type_') == 'heading']
    sides = [t for t in listed if t.get('type_') != 'heading']
    if len(headings) != 1 or not sides or len(headings) + len(sides) != len(listed):
        raise ValueError('A scene-side release needs one heading and its sides')
    if any(t.get('sub_tracks') for t in listed):
        raise ValueError('Scene sides are the tracks, not headings over subtracks')
    named = []
    for side in sides:
        numbers = side_scenes(side.get('title', ''))
        if not numbers:
            raise ValueError('A side does not name its scenes')
        named.extend(numbers)
    scenes = list(dict.fromkeys(named))
    if scenes != list(range(scenes[0], scenes[-1] + 1)) or scenes[0] != 1:
        raise ValueError('Scene sides must cover 1 through N without a gap')
    split = any(word in norm(side.get('title', '')).split() for side in sides for word in ('part', 'conclusion'))
    if split and PART_LIMIT not in review['limitations']:
        raise ValueError('An unmarked part boundary must stay visible')
    tracks = album['tracks']['items']
    observed = []
    for track in tracks:
        numbers = [int(number) for number in re.findall(r'\bscene\s+(\d+)\b', norm(track['title']))]
        if len(numbers) != 1:
            raise ValueError('A scene side needs one numbered scene on every track')
        observed.append(numbers[0])
    if observed != sorted(observed) or set(observed) != set(scenes):
        raise ValueError('File scenes are not the sides in order')
    if review.get('expected_track_ids') != [t['id'] for t in tracks]:
        raise ValueError('Scene-side review must bind every file track')
    rows = credit_rows(tracks)
    blockers = []
    tokens_by_key = {}
    required = {person_key(e['name']) for e in review['source_roles']}
    allowed = set()
    for entry in review['source_roles']:
        if entry['kind'] == 'orchestra':
            candidate = entry.get('candidate_name', entry['name'])
            if person_key(candidate) != person_key(entry['name']) and len(entry.get('alias_reason', '')) < 20:
                raise ValueError('A differing ensemble name needs an explicit recording-specific reason')
            allowed.add(person_key(candidate))
    for row_credit in rows:
        if looks_like_ensemble(row_credit['name']) or row_credit['tokens'] & {'orchestra', 'choir', 'chorus'}:
            if row_credit['key'] not in allowed and row_credit['key'] not in required:
                blockers.append('conflicting-ensemble:' + row_credit['name'])
            continue
        tokens_by_key.setdefault(row_credit['key'], set()).update(row_credit['tokens'])
        if row_credit['key'] in required:
            continue
        performing = bool(voice_categories(' '.join(row_credit['tokens'])) or 'conductor' in row_credit['tokens'])
        exempt = bool(row_credit['tokens'] & EXEMPT) and not performing
        musical = performing or 'mainartist' in row_credit['tokens'] or {'main', 'artist'} <= row_credit['tokens']
        if musical and not exempt:
            blockers.append('extra-performer:' + row_credit['name'])
    track_ids = {t['id'] for t in tracks}
    for entry in review['source_roles']:
        key = person_key(entry['name'])
        seen = tokens_by_key.get(key, set())
        if entry['kind'] == 'vocal':
            if not seen:
                blockers.append('absent:' + entry['name'])
                if 'voice_conflict' in entry:
                    raise ValueError('Absent singer cannot carry a voice-type resolution')
                continue
            source_voice, found_voice = voice_categories(entry['role']), voice_categories(' '.join(seen))
            conflict = entry.get('voice_conflict')
            if source_voice != found_voice:
                if conflict != [sorted(source_voice), sorted(found_voice)]:
                    raise ValueError('Voice-type discrepancy must be explicit: ' + entry['name'])
            elif conflict:
                raise ValueError('Voice conflict recorded where categories agree: ' + entry['name'])
        elif entry['kind'] == 'conductor':
            covered = {r['track_id'] for r in rows if r['key'] == key and 'conductor' in r['tokens']}
            if covered != track_ids:
                blockers.append('conductor-coverage')
        elif entry['kind'] == 'orchestra':
            candidate = person_key(entry.get('candidate_name', entry['name']))
            covered = {r['track_id'] for r in rows if r['key'] == candidate}
            if covered != track_ids:
                blockers.append('orchestra-coverage')
        else:
            raise ValueError('Scene sides do not review this role')
    blockers = list(dict.fromkeys(blockers))
    evidence = evaluate(row, album)
    evidence['programme'] = [{'target': headings[0]['title'], 'work_tracks': len(tracks),
                              'credited_tracks': 0 if blockers else len(tracks),
                              'track_ids': [t['id'] for t in tracks], 'scene_evidence': 'scene-sides'}]
    evidence.update(target_count=1, covered=0 if blockers else 1, coverage=0 if blockers else 1,
                    reasons=(['Reviewed scene sides, in order, with every named singer.'] if not blockers else
                             ['Scene-side review unresolved: ' + ', '.join(blockers)]))
    result = {'discogs_id': review['discogs_id'], 'album_id': review['album_id'], 'decision': review['decision'],
              'recording_review': review['recording_review'], 'sources': review['sources'], 'limitations': review['limitations'],
              'eligible': review['decision'] == 'probable' and not blockers, 'blockers': blockers,
              'completeness': {'status': 'complete' if review['decision'] == 'probable' and not blockers else 'unknown',
                               'works': [{'target': headings[0]['title'], 'status': 'complete' if not blockers else 'unknown',
                                          'scope': 'reviewed-scene-sides', 'scene_evidence': 'scene-sides'}]}}
    return result, evidence


if __name__ == '__main__':
    reviews = json.loads((ROOT/'data/qobuz_opera_recording_reviews.json').read_text())['releases']
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    import gzip
    albums = {x['task']['discogs_id']: x['album'] for x in json.loads(gzip.decompress((ROOT/'data/qobuz_unmatched_metadata.json.gz').read_bytes()))['metadata']}
    for review in reviews:
        if review['review_kind'] != 'source-role-ensemble':
            continue
        result, _ = assess_opera(rows[review['discogs_id']], albums[review['discogs_id']], review)
        print(review['discogs_id'], result['eligible'], result['blockers'])
        assert fingerprint(albums[review['discogs_id']])
