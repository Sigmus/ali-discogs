"""Frozen, offline credit-gap triage. Diagnostics never authorize a promotion."""
import gzip
import hashlib
import json
from collections import Counter
from qobuz_lead_review import ROOT, fingerprint, target_fingerprint
from qobuz_credit_role_audit import load_albums
from qobuz_match import agrees, credits, evaluate
from qobuz_work_groups import contextual_tracks, target_work_matches
from qobuz_credit171_diagnostic import declared_gaps

SCOPE = ROOT/'data/qobuz_credit150_scope.json'


def inspect_candidate(row, album):
    evidence = evaluate(row, album)
    tracks = contextual_tracks(row, album['tracks']['items'])
    units = []
    for item in evidence['programme']:
        required = item.get('required_performers', evidence['required_performers'])
        matched = [t for t in tracks if target_work_matches(row, item['target'], t)]
        gaps = declared_gaps(required, matched)
        declarations = []
        for name in required:
            positive = [t['id'] for t in matched if agrees(name, credits(t))]
            elsewhere = [t['id'] for t in tracks if t not in matched and agrees(name, credits(t))]
            raw = []
            for t in matched:
                for part in (t.get('performers') or '').split(' - '):
                    person, sep, roles = part.partition(',')
                    if agrees(name, [person]):
                        raw.append({'track_id': t['id'], 'name': person.strip(), 'roles': roles.strip() if sep else ''})
            declarations.append({'required_name': name, 'positive_work_track_ids': positive,
                                 'positive_other_work_track_ids': elsewhere,
                                 'matching_name_declarations': raw})
        units.append({'target': item['target'], 'work_track_ids': [t['id'] for t in matched],
                      'required_performers': required, 'name_evidence': declarations,
                      'declared_but_unaccepted': gaps})
    flags = set()
    for unit in units:
        if not unit['work_track_ids']:
            flags.add('no_matching_work_tracks')
        for name in unit['name_evidence']:
            if name['positive_work_track_ids']:
                continue
            if name['matching_name_declarations']:
                roles = [d['roles'].lower() for d in name['matching_name_declarations']]
                if any('associated' in r for r in roles):
                    flags.add('associated_role_unresolved')
                elif any(r and 'composer' not in r and 'writer' not in r for r in roles):
                    flags.add('explicit_unaccepted_role')
                else:
                    flags.add('roleless_or_composer_only')
            elif name['positive_other_work_track_ids']:
                flags.add('positive_only_on_other_work')
            else:
                flags.add('required_name_not_declared')
    return {'album_id': str(album['id']), 'title': album['title'], 'album_sha256': fingerprint(album),
            'track_manifest_sha256': fingerprint(album['tracks']['items']),
            'tracks_count': len(album['tracks']['items']), 'coverage': evidence['coverage'],
            'units': units, 'flags': sorted(flags)}


def build(scope, rows, albums):
    entries = []
    for rid in scope['release_ids']:
        raw_path = ROOT/f'raw/discogs/releases/{rid}.json'
        raw = json.loads(raw_path.read_text()); row = rows[rid]
        candidates = [inspect_candidate(row, albums[aid]) for aid in scope['candidate_ids'][rid]]
        def rank(c):
            names = [n for u in c['units'] if u['work_track_ids'] for n in u['name_evidence']]
            fraction = sum(bool(n['positive_work_track_ids']) for n in names)/len(names) if names else 0
            return (fraction, c['coverage'], -len(c['flags']))
        best = max(candidates, key=rank)
        flags = best['flags']
        group = next((f for f in ['required_name_not_declared', 'positive_only_on_other_work',
                                 'associated_role_unresolved', 'roleless_or_composer_only',
                                 'explicit_unaccepted_role', 'no_matching_work_tracks'] if f in flags),
                     'source_programme_mapping_needed')
        entries.append({'discogs_id': rid, 'title': row['title'], 'target_sha256': target_fingerprint(row),
                        'source_sha256': hashlib.sha256(raw_path.read_bytes()).hexdigest(),
                        'source_programme': raw['tracklist'], 'source_credits': raw.get('extraartists', []),
                        'best_diagnostic_album_id': best['album_id'], 'primary_diagnostic_group': group,
                        'best_candidate_flags': flags, 'best_positive_name_fraction': rank(best)[0],
                        'candidates': candidates})
    return {'schema_version': 1, 'reviewed_on': '2026-11-17', 'status': 'diagnostic-only',
            'scope_sha256': hashlib.sha256(SCOPE.read_bytes()).hexdigest(),
            'frozen_release_ids': scope['release_ids'], 'entries': entries,
            'primary_group_counts': dict(Counter(e['primary_diagnostic_group'] for e in entries)),
            'overlapping_best_flags': dict(Counter(f for e in entries for f in e['best_candidate_flags'])),
            'candidate_count': sum(len(e['candidates']) for e in entries),
            'provider_calls': 0, 'publication_changed': False,
            'limitations': ['Best diagnostic candidate uses positive name coverage only, not recording confidence or completeness.',
                'A positive name on one track does not authorize credit inheritance elsewhere.',
                'Absent exact-name evidence may be spelling, source error, different cast or genuinely missing metadata; no identity inferred.',
                'Flags overlap; primary group uses explicit precedence, not a manual recording decision.',
                'No source edits, name/role waivers, match promotions or new provider calls.']}


def main():
    scope = json.loads(SCOPE.read_text())
    if len(scope['release_ids']) != 150 or len(set(scope['release_ids'])) != 150:
        raise ValueError('Frozen credit150 scope changed')
    original = json.loads((ROOT/'data/qobuz_credit171_scope.json').read_text())
    if any(scope['candidate_ids'][rid] != original['candidate_ids'][rid] for rid in scope['release_ids']):
        raise ValueError('Original candidate scope changed')
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    result = build(scope, rows, load_albums())
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
    (ROOT/'data/qobuz_credit150_triage.json.gz').write_bytes(gzip.compress(payload, mtime=0))
    print(json.dumps({k: result[k] for k in ['primary_group_counts', 'overlapping_best_flags', 'candidate_count']}))


if __name__ == '__main__':
    main()
