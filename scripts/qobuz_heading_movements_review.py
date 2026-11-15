"""Hash-bound flat source headings with individually positioned movement bands."""
from copy import deepcopy
import json
from qobuz_lead_review import ROOT, fingerprint, target_fingerprint
from qobuz_match import catalogue


def grouped_row(row, raw, review):
    """Keep every source band under its exact heading, even repeated tempo labels."""
    groups, projected, positions = [], [], []
    for track in raw['tracklist']:
        kind, title, position = track.get('type_'), track.get('title'), track.get('position', '')
        if track.get('sub_tracks') or not title:
            raise ValueError('Only flat, fully titled source headings/bands are supported')
        projected.append({'position': position, 'title': title, 'type': kind,
                          'duration': track.get('duration', '')})
        if kind == 'heading':
            if position or not catalogue(title):
                raise ValueError('Each source heading must identify a catalogued work')
            groups.append({'source_heading': title, 'source_movements': []})
        elif kind == 'track' and groups and position:
            groups[-1]['source_movements'].append({'position': position, 'title': title})
            positions.append(position)
        else:
            raise ValueError('Unattached or unpositioned source band')
    if projected != row['tracklist'] or groups != review['source_groups']:
        raise ValueError('Source headings, positions or movement titles changed')
    if (not groups or any(not g['source_movements'] for g in groups)
            or len(positions) != len(set(positions))
            or len({g['source_heading'] for g in groups}) != len(groups)):
        raise ValueError('Ambiguous source heading/band structure')
    if [w['target'] for w in review['works']] != [g['source_heading'] for g in groups]:
        raise ValueError('Every source heading must have exactly one reviewed work')
    for group, work in zip(groups, review['works']):
        if (work['movements'] != list(range(1, len(group['source_movements'])+1))
                or work.get('joined_tracks') or work.get('reviewed_sections')):
            raise ValueError('This review requires one distinct digital movement per source band')
    effective = deepcopy(row)
    effective['tracklist'] = [{'title': g['source_heading'], 'type': 'index'} for g in groups]
    return effective


def assess_heading_movements(row, album, review):
    from qobuz_lead_review import assess
    raw = json.loads((ROOT/f"raw/discogs/releases/{review['discogs_id']}.json").read_bytes())
    effective = grouped_row(row, raw, review)
    delegated = {k:v for k,v in review.items() if k != 'review_kind'}
    delegated['target_sha256'] = target_fingerprint(effective)
    result, evidence = assess(effective, album, delegated)
    actual = {w['target']: w['track_ids'] for w in result['completeness']['works']}
    if actual != review['expected_track_ids']:
        raise ValueError('A digital movement was missing, reused or reassigned to another work')
    tracks = {str(t['id']): t for t in album['tracks']['items']}
    used = [str(i) for ids in actual.values() for i in ids]
    if (set(used) != set(review['track_fingerprints'])
            or any(fingerprint(tracks[i]) != review['track_fingerprints'][i] for i in used)):
        raise ValueError('An exact reviewed digital movement changed')
    for work, group in zip(result['completeness']['works'], review['source_groups']):
        work['source_movements'] = group['source_movements']
        work['scope'] = 'reviewed-source-heading-movements'
    evidence['reasons'] = ['Every source movement stays under its explicit work heading and position; repeated tempo labels are not independent works.']
    return result, evidence
