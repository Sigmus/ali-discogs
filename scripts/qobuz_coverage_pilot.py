"""Offline candidate-discovery experiment; never writes publication matches or calls APIs."""
import argparse
from collections import defaultdict
import json
from pathlib import Path

from qobuz_match import credits, evaluate, person_key, public_album
from qobuz_snapshot import load_snapshot

ROOT = Path(__file__).resolve().parents[1]
# Explicit experimental spellings observed in saved target/candidate credits.
# Candidate discovery only: these are not enabled in the production matcher.
ALIASES = {
    'david oistrach': 'david oistrakh',
    'kiril kondrashin': 'kirill kondrashin',
    'chicago symphony orchestra cso': 'chicago symphony orchestra',
}


def key(name):
    value = person_key(name)
    return ALIASES.get(value, value)


def alias_row(row):
    result = dict(row)
    for field in ['key_performers', 'performers', 'ensembles']:
        result[field] = [key(p) for p in row.get(field) or []]
    if row.get('conductor'):
        result['conductor'] = key(row['conductor'])
    return result


def alias_album(album):
    result = dict(album)
    tracks = []
    for track in album['tracks']['items']:
        t = dict(track)
        parts = []
        for part in (t.get('performers') or '').split(' - '):
            name, sep, roles = part.partition(',')
            parts.append(key(name) + sep + roles)
        t['performers'] = ' - '.join(parts)
        tracks.append(t)
    result['tracks'] = {'items': tracks}
    return result


def discover(rows, previous, snapshot, limit=12):
    albums = snapshot['albums']
    transformed = {aid: alias_album(a) for aid, a in albums.items()}
    index = defaultdict(set)
    for aid, a in transformed.items():
        for t in a['tracks']['items']:
            for name in credits(t):
                index[person_key(name)].add(aid)
    # Prioritise partial coverage; then deterministic release ID. Bounded pilot.
    unresolved = sorted((rid for rid, r in previous.items() if r['status'] == 'unchecked'),
        key=lambda rid: (-max((c['coverage'] for c in previous[rid]['candidates']), default=0), int(rid)))
    inspected, proposals = [], []
    for rid in unresolved:
        original = rows[rid]
        target = alias_row(original)
        # Ask evaluate for the same production-required credit list; no relaxed role policy.
        required = evaluate(target, {'tracks': {'items': []}})['required_performers']
        if not required:
            continue
        eligible = set.intersection(*(index.get(person_key(p), set()) for p in required))
        own = {c['id'] for c in previous[rid]['candidates']}
        candidates = []
        for aid in sorted(eligible):
            evidence = evaluate(target, transformed[aid])
            if evidence['status'] == 'unchecked':
                continue
            baseline = evaluate(original, albums[aid])
            candidates.append({**public_album(albums[aid]), **evidence,
                'original_search_candidate': aid in own,
                'unmodified_rules_status': baseline['status'],
                'requires_experimental_alias': baseline['status'] == 'unchecked'})
        inspected.append({'discogs_id': rid, 'eligible_albums': len(eligible)})
        if candidates:
            proposals.append({'discogs_id': rid, 'title': original['title'],
                'original_search_empty': not own, 'candidates': candidates})
            if len(proposals) >= limit:
                break
    return {'schema_version': 1, 'purpose': 'Offline discovery only; no accepted matches or recording-session verification.',
        'aliases': ALIASES, 'snapshot_metadata_completed_at': snapshot['metadata_completed_at'],
        'inspected': inspected, 'proposals': proposals,
        'summary': {'releases_inspected': len(inspected), 'proposed_releases': len(proposals),
            'candidate_count': sum(len(p['candidates']) for p in proposals),
            'previously_empty': sum(p['original_search_empty'] for p in proposals),
            'with_unmodified_rule_candidate': sum(any(c['unmodified_rules_status'] != 'unchecked' for c in p['candidates']) for p in proposals)}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit', type=int, default=12)
    parser.add_argument('--output', type=Path, default=ROOT/'data/qobuz_coverage_pilot.json')
    args = parser.parse_args()
    if args.limit < 1:
        parser.error('--limit must be positive')
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    previous = json.loads((ROOT/'data/qobuz_matches.json').read_text())['releases']
    result = discover(rows, previous, load_snapshot(), args.limit)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result['summary']))


if __name__ == '__main__':
    main()
