"""Fail-closed programme completeness for offline discovery; no publication writes."""
import argparse
import hashlib
from collections import Counter
import json
from pathlib import Path
import re

from qobuz_match import catalogue, evaluate, norm
from qobuz_snapshot import load_snapshot

ROOT = Path(__file__).resolve().parents[1]
ROMAN = {s: i for i, s in enumerate(['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X'], 1)}


def movement_number(title):
    # Only standalone movement labels; IVa-b, II/III and joined movements are
    # deliberately unsupported. Do not confuse work/opus numbers with movements.
    matches = list(re.finditer(r'(?:^|:\s*)([IVX]+|[1-9])\.\s+', title))
    markers = re.findall(r'(?<!\w)([IVX]+|[1-9])\.\s+', title)
    if len(matches) != 1 or len(markers) != 1:
        return None
    value = matches[0].group(1)
    return ROMAN.get(value) if not value.isdigit() else int(value)


def inventory_work(row, title, inventory):
    composers = {norm(c) for c in row.get('composers') or []}
    ids = catalogue(title)
    if len(composers) != 1 or len(ids) != 1:
        return None
    matches = [w for w in inventory['works']
               if norm(w['composer']) in composers and tuple(w['catalogue']) in ids]
    return matches[0] if len(matches) == 1 else None


def target_details(row, title):
    tracks = row.get('tracklist') or []
    entries = [(i, t) for i, t in enumerate(tracks) if t.get('title') == title]
    if len(entries) != 1:
        return None, []
    i, target = entries[0]
    children = []
    if target.get('type') == 'index':
        for t in tracks[i + 1:]:
            if t.get('type') == 'index':
                break
            children.append(t)
    return target, children


def seconds(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d+:\d{2}', value):
        return None
    minutes, sec = map(int, value.split(':'))
    return minutes * 60 + sec if sec < 60 else None


def explicit_track_check(target, item, album):
    # LP timing is supporting evidence for the *listed track*, not proof of an
    # entire composition or session. Require a single credited candidate track.
    duration = seconds(target.get('duration')) if target else None
    if not target or target.get('type') != 'track' or duration is None or duration < 30:
        return None
    tracks = [t for t in album['tracks']['items'] if t['id'] in item['track_ids']]
    if len(tracks) != 1:
        return None
    actual = tracks[0].get('duration')
    if not isinstance(actual, (int, float)) or abs(actual - duration) > max(5, duration * .03):
        return None
    return {'target': item['target'], 'status': 'complete', 'scope': 'listed-target-track',
            'track_ids': [tracks[0]['id']], 'target_duration_seconds': duration,
            'candidate_duration_seconds': actual, 'source': 'collection tracklist',
            'reason': 'Single credited title correspondence with duration within max(5 seconds, 3%); not whole-work or recording-session proof.'}


def check_programme(row, album, evidence, inventory):
    checked = []
    for item in evidence['programme']:
        target = item['target']
        work = inventory_work(row, target, inventory)
        # Target rows can explicitly contain one movement of a known work;
        # those cannot be mistaken for a request for the entire work.
        if work and movement_number(target) is not None:
            work = None
        target_entry, children = target_details(row, target)
        child_numbers = [movement_number(t.get('title', '')) for t in children]
        if work:
            expected, source, scope = work['movements'], work['source'], 'whole-work-inventory'
        elif children and None not in child_numbers and len(set(child_numbers)) == len(child_numbers):
            expected, source, scope = child_numbers, 'collection tracklist', 'listed-target-movements'
        else:
            explicit = explicit_track_check(target_entry, item, album)
            checked.append(explicit or {'target': target, 'status': 'unknown',
                            'reason': 'No unambiguous reviewed inventory, numbered target children or timed target-track correspondence.'})
            continue
        # Completeness requires credited support for every movement, not merely
        # an album-wide artist credit or a work-title hit.
        ids = set(item['track_ids'])
        tracks = [t for t in album['tracks']['items'] if t['id'] in ids]
        numbers = [movement_number(t['title']) for t in tracks]
        observed = sorted({n for n in numbers if n is not None})
        missing = sorted(set(expected) - set(observed))
        status = 'complete'
        if missing:
            status = 'incomplete' if None not in numbers else 'unknown'
        elif numbers != expected:
            status = 'unknown'  # repeats, out of order, splits, or extra numbers
        checked.append({'target': target, 'status': status, 'expected_movements': expected,
                        'observed_movements': numbers, 'missing_movements': missing,
                        'track_ids': [t['id'] for t in tracks], 'source': source, 'scope': scope,
                        'reason': 'Requires each expected movement, in order, with production-required credits; split/joined or ambiguous labels remain unresolved.'})
    # A single candidate track cannot stand in for two different target items.
    complete_ids = [i for w in checked if w['status'] == 'complete' for i in w['track_ids']]
    overlapping = len(complete_ids) != len(set(complete_ids))
    states = {x['status'] for x in checked}
    status = ('incomplete' if 'incomplete' in states else
              'complete' if checked and states == {'complete'} and evidence['status'] != 'unchecked' and not overlapping
              else 'unknown')
    return {'status': status, 'works': checked, 'overlapping_target_tracks': overlapping}


def check_pilot(pilot, rows, albums, inventory):
    # Import here to keep generic checker independent of experimental aliases.
    from qobuz_coverage_pilot import alias_row, alias_album
    report = {'schema_version': 1, 'purpose': 'Research gate only, not accepted matches or session verification.',
              'inventory_reviewed_on': inventory['reviewed_on'], 'releases': []}
    for proposal in pilot['proposals']:
        rid = proposal['discogs_id']
        row = alias_row(rows[rid])
        candidates = []
        for c in proposal['candidates']:
            album = alias_album(albums[c['id']])
            evidence = evaluate(row, album)
            completeness = check_programme(row, album, evidence, inventory)
            ready = completeness['status'] == 'complete' and not c['requires_experimental_alias']
            candidates.append({'album_id': c['id'], 'requires_experimental_alias': c['requires_experimental_alias'],
                               'ready_for_probable_integration': ready, **completeness})
        report['releases'].append({'discogs_id': rid, 'title': proposal['title'], 'candidates': candidates})
    report['summary'] = dict(Counter(c['status'] for r in report['releases'] for c in r['candidates']))
    report['summary']['releases_with_complete_candidate'] = sum(
        any(c['status'] == 'complete' for c in r['candidates']) for r in report['releases'])
    report['summary']['releases_ready_for_probable_integration'] = sum(
        any(c['ready_for_probable_integration'] for c in r['candidates']) for r in report['releases'])
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pilot', type=Path, default=ROOT/'data/qobuz_coverage_pilot.json')
    parser.add_argument('--output', type=Path, default=ROOT/'data/qobuz_completeness_pilot.json')
    args = parser.parse_args()
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    snapshot = load_snapshot()
    inventory_path = ROOT/'data/qobuz_work_inventory.json'
    report = check_pilot(json.loads(args.pilot.read_text()), rows, snapshot['albums'],
                         json.loads(inventory_path.read_text()))
    report['provenance'] = {
        'checker_version': 'qobuz-completeness-pilot-v2',
        'pilot_sha256': hashlib.sha256(args.pilot.read_bytes()).hexdigest(),
        'inventory_sha256': hashlib.sha256(inventory_path.read_bytes()).hexdigest(),
        'collection_sha256': hashlib.sha256((ROOT/'data/collection_matches.json').read_bytes()).hexdigest(),
        'metadata_manifest_fingerprint': snapshot['metadata_manifest']['fingerprint']}
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report['summary']))


if __name__ == '__main__':
    main()
