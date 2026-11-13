"""Conservative work context and recording-group credit evidence; no API access."""
import re
from qobuz_match import norm, tnorm, catalogue, credits, person_key, agrees, units, evaluate_v1


def role_entries(track):
    entries = []
    for part in (track.get('performers') or '').split(' - '):
        name, _, roles = part.partition(',')
        entries.append((name.strip(), set(norm(roles).split())))
    return entries


def composers(track):
    return {norm(name) for name, roles in role_entries(track) if 'composer' in roles}


def ordinal(title):
    m = re.search(r'(?:^|:\s*)([IVX]+|\d{1,2})\.\s+', title)
    if not m:
        return None
    value = m.group(1)
    roman = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}
    return int(value) if value.isdigit() else roman.get(value)


def anchors(row):
    return list(dict.fromkeys([*(row.get('ensembles') or []),
                              *([row['conductor']] if row.get('conductor') else [])]))


def contextual_tracks(row, tracks):
    result = []
    anchor = anchors(row)
    prefix, last, composer, parent = None, None, None, None
    for original in tracks:
        t = dict(original)
        n = ordinal(t['title'])
        bare = bool(re.match(r'^(?:[IVX]+|\d{1,2})\.\s+', t['title']))
        identities = composers(t)
        supported = anchor and all(agrees(p, credits(t)) for p in anchor)
        previous = result[-1] if result else {}
        same_media = not (t.get('media_number') is not None and previous.get('media_number') is not None and t['media_number'] != previous['media_number'])
        next_track = not (t.get('track_number') is not None and previous.get('track_number') is not None and t['track_number'] != previous['track_number'] + 1)
        a, b = t.get('work'), previous.get('work')
        same_work = True
        if a and b:
            # The catalogue uses formatting variants such as op.14 / Op. 14, H48.
            # Require the same catalogue identity and corroborating name words.
            common = {w for w in set(tnorm(a).split()) & set(tnorm(b).split()) if w.isalpha() and w not in {'op', 'no', 'in', 'h'}}
            same_work = norm(a) == norm(b) or (bool(catalogue(a)) and catalogue(a) == catalogue(b) and len(common) >= 2)
        if prefix and bare and n == last + 1 and identities == composer and supported and same_media and next_track and same_work:
            t['title'] = prefix + ': ' + t['title']
            t['context_parent_track_id'] = parent
            last = n
        else:
            prefix, last, composer, parent = None, None, None, None
            if not bare and n == 1 and supported and len(identities) == 1:
                # Prefix ends immediately before the explicit movement label.
                m = re.search(r':\s*(?:I|1)\.\s+', t['title'])
                if m:
                    prefix, last, composer, parent = t['title'][:m.start()], 1, identities, t['id']
        result.append(t)
    return result


def target_work_matches(row, target, track, collision=None):
    from qobuz_match import work_match
    if not work_match(target, track['title']):
        return False
    declared = {norm(c) for c in row.get('composers') or []}
    # Preserve the baseline composer evidence policy outside ambiguous opus
    # collisions; album-level Discogs composer lists can be incomplete and
    # spellings vary. Stronger grouped credit repair below requires explicit
    # composer-role identity and never inherits composer/performer credits.
    if declared and not any(c.split()[-1] in norm(track.get('performers', '')).split() for c in declared):
        return False
    ids = catalogue(target)
    if collision is None:
        collision = any(ids & catalogue(other) for other in units(row) if other != target)
    if len(declared) > 1 and ids and collision:
        # Shared opus numbers cannot identify a work across composers. Require
        # explicit composer-role evidence and distinctive work-name words.
        if not composers(track) & declared:
            return False
        words = set(tnorm(target).split()) - set('op no nr suite piano violin cello orchestra concerto symphony sonata in major minor a b c d e f g for and et the of'.split())
        words = {w for w in words if not w.isdigit()}
        if len(words) < 2 or not words.issubset(set(tnorm(track['title']).split())):
            return False
    return True


def group_support(row, possible, required):
    anchor = anchors(row)
    if not anchor or not possible or not all(all(agrees(p, credits(t)) for p in anchor) for t in possible):
        return None
    identities = [composers(t) for t in possible]
    if len(identities[0]) != 1 or any(c != identities[0] for c in identities):
        return None
    if len({tnorm(t['title']) for t in possible}) != len(possible):
        return None
    numbers = [ordinal(t['title']) for t in possible]
    if any(n is not None for n in numbers) and numbers != list(range(1, len(numbers) + 1)):
        return None  # repeats, restarts, splits, missing or mixed labels
    if not all(agrees(p, [name for t in possible for name in credits(t)]) for p in required):
        return None
    # Unknown extra main artists/soloists can indicate a different performance.
    # Do not borrow missing credits across such a group, including bad publisher
    # metadata labelled MainArtist. Leave those cases for review.
    for t in possible:
        for name, roles in role_entries(t):
            musical = bool(roles & {'mainartist', 'soloist', 'piano', 'violin', 'cello', 'soprano', 'tenor', 'baritone', 'bass', 'alto'}) or {'main', 'artist'} <= roles
            if musical and not agrees(name, required) and norm(name) not in identities[0]:
                return None
    return {'track_ids': [t['id'] for t in possible], 'anchors': anchor,
            'scope': 'contiguous-work-group', 'credit_policy': 'Anchors on every track; each named performer evidenced within this group; no unknown extra musical main artists.'}


def evaluate_grouped(row, album, legacy=None):
    original = legacy if legacy is not None else evaluate_v1(row, album)
    tracks = contextual_tracks(row, album['tracks']['items'])
    contextual = {**album, 'tracks': {'items': tracks}}
    base = evaluate_v1(row, contextual) if any('context_parent_track_id' in t for t in tracks) else dict(original)
    required = base['required_performers']
    programme = []
    targets = units(row)
    identities = {t: catalogue(t) for t in targets}
    collisions = {t for t in targets if any(identities[t] & identities[o] for o in targets if o != t)}
    for target in targets:
        from qobuz_target_credits import requirements
        work_row, work_required, target_scope = requirements(row, target, required)
        work_tracks = contextual_tracks(work_row, album['tracks']['items']) if target_scope else tracks
        possible = [t for t in work_tracks if target_work_matches(work_row, target, t, target in collisions)]
        direct = [t for t in possible if work_required and all(agrees(p, credits(t)) for p in work_required)]
        # Never merge disjoint runs or repeated performances within an anthology.
        runs = []
        possible_ids = {t['id'] for t in possible}
        for i, t in enumerate(work_tracks):
            if t['id'] not in possible_ids:
                continue
            if not runs or runs[-1][-1][0] != i - 1 or (ordinal(t['title']) == 1 and runs[-1]):
                runs.append([])
            runs[-1].append((i, t))
        groups = [g for run in runs if (g := group_support(work_row, [t for _, t in run], work_required))]
        # If multiple performances qualify, keep direct evidence rather than
        # synthesizing one recording from their combined credits.
        group = groups[0] if len(groups) == 1 else None
        ids = group['track_ids'] if group else [t['id'] for t in direct]
        item = {'target': target, 'work_tracks': len(possible), 'credited_tracks': len(ids), 'track_ids': ids}
        if target_scope:
            item['required_performers'] = work_required
            item['target_credit_scope'] = target_scope
        inherited = [{'track_id': t['id'], 'parent_track_id': t['context_parent_track_id']}
                     for t in possible if 'context_parent_track_id' in t]
        if inherited:
            item['inherited_title_context'] = inherited
        if group and set(ids) != {t['id'] for t in direct}:
            item['recording_group'] = group
        programme.append(item)
    covered = sum(bool(p['track_ids']) for p in programme)
    base.update(programme=programme, target_count=len(programme), covered=covered, coverage=covered / len(programme) if programme else 0)
    if covered != len(programme) or not programme or not required:
        base.update(status='unchecked', confidence=None,
                    reasons=[f'{covered}/{len(programme)} target items supported after composer/work grouping; unresolved.'])
    elif base['status'] == 'unchecked' or len(programme) != original['target_count'] or any('recording_group' in p for p in programme):
        grouped = any('recording_group' in p for p in programme)
        reason = ('Target works have recording-group performer evidence; credits need not list every soloist on every movement. Recording identity requires review.' if grouped else
                  'Each target item has explicit work and performer-role credits; recording identity requires review.')
        base.update(status='probable', confidence=.85, reasons=[reason])
    if programme != original['programme']:
        base['work_group_policy'] = 'qobuz-work-groups-v1'
        base['reasons'] = [*base['reasons'], 'Work-aware evidence uses composer boundaries, bounded movement-title context and conservative contiguous recording groups.']
    return base
