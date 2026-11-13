"""Offline comparison of legacy and work-group evidence for 66+10 reviewed releases."""
import hashlib
import json
from collections import Counter
from pathlib import Path
from qobuz_match import evaluate, evaluate_v1
from qobuz_completeness import check_programme
from qobuz_work_groups import contextual_tracks
from qobuz_snapshot import load_snapshot

ROOT = Path(__file__).resolve().parents[1]


def audit(rows, snapshot, baseline, expansion, inventory):
    scope = {r['discogs_id']: r['album_id'] for r in baseline['entries']}
    scope.update({rid: ids[0] for rid, ids in expansion['releases'].items()})
    results = []
    for rid, aid in sorted(scope.items(), key=lambda r: int(r[0])):
        row, album = rows[rid], snapshot['albums'][aid]
        old, new = evaluate_v1(row, album), evaluate(row, album)
        contextual = {**album, 'tracks': {'items': contextual_tracks(row, album['tracks']['items'])}}
        ids = [i for p in new['programme'] for i in p['track_ids']]
        results.append({'discogs_id': rid, 'album_id': aid, 'title': row['title'],
            'legacy_status': old['status'], 'current_status': new['status'],
            'legacy_programme': old['programme'], 'current_programme': new['programme'],
            'legacy_completeness': check_programme(row, album, old, inventory)['status'],
            'current_completeness': check_programme(row, contextual, new, inventory)['status'],
            'shared_track_assignments': len(ids) != len(set(ids))})
    return {'schema_version': 1, 'purpose': 'Metadata evidence comparison; not recording-session validation or score overrides.',
        'releases': results, 'summary': {
            'releases': len(results), 'legacy_statuses': dict(Counter(r['legacy_status'] for r in results)),
            'current_statuses': dict(Counter(r['current_status'] for r in results)),
            'status_changes': sum(r['legacy_status'] != r['current_status'] for r in results),
            'changed_programmes': sum(r['legacy_programme'] != r['current_programme'] for r in results),
            'current_completeness': dict(Counter(r['current_completeness'] for r in results)),
            'shared_track_assignment_releases': sum(r['shared_track_assignments'] for r in results)}}


def main():
    paths = {name: ROOT/'data'/filename for name, filename in {
        'baseline': 'qobuz_baseline_audit_scope.json', 'expansion': 'qobuz_expansion_scope.json',
        'inventory': 'qobuz_work_inventory.json', 'collection': 'collection_matches.json'}.items()}
    data = {k: json.loads(p.read_text()) for k, p in paths.items()}
    rows = {str(r['discogs_id']): r for r in data['collection']}
    snapshot = load_snapshot()
    result = audit(rows, snapshot, data['baseline'], data['expansion'], data['inventory'])
    result['provenance'] = {'matcher_version': 'qobuz-work-groups-v1+reviewed-expansion-v2',
        'inputs_sha256': {k: hashlib.sha256(p.read_bytes()).hexdigest() for k, p in paths.items()},
        'metadata_manifest_fingerprint': snapshot['metadata_manifest']['fingerprint']}
    (ROOT/'data/qobuz_group_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result['summary']))


if __name__ == '__main__':
    main()
