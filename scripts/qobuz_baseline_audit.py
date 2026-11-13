"""Reproducible offline audit of the frozen original 66 selected Qobuz matches."""
import hashlib
import json
from collections import Counter
from pathlib import Path

from qobuz_completeness import check_programme, movement_number
from qobuz_match import evaluate_v1 as evaluate, work_match, agrees, credits_v1 as credits
from qobuz_snapshot import load_snapshot

ROOT = Path(__file__).resolve().parents[1]


def audit(scope, rows, snapshot, inventory):
    results = []
    for entry in scope['entries']:
        rid, aid = entry['discogs_id'], entry['album_id']
        row, album = rows[rid], snapshot['albums'][aid]
        evidence = evaluate(row, album)
        completeness = check_programme(row, album, evidence, inventory)
        programme = []
        for item in evidence['programme']:
            possible = [t for t in album['tracks']['items'] if work_match(item['target'], t['title'])]
            programme.append({**item, 'title_matched_tracks': [
                {'id': t['id'], 'title': t['title'], 'movement': movement_number(t['title']),
                 'duration': t.get('duration'), 'missing_required_performers': [
                     p for p in evidence['required_performers'] if not agrees(p, credits(t))]}
                for t in possible]})
        title_missing = []
        for work in completeness['works']:
            if work.get('expected_movements'):
                matching = next(p for p in programme if p['target'] == work['target'])
                numbered = {t['movement'] for t in matching['title_matched_tracks']}
                title_missing.extend(n for n in work['expected_movements'] if n not in numbered)
        if completeness['status'] == 'complete':
            audit_status = 'supported'
        elif completeness['status'] == 'incomplete' and not title_missing:
            audit_status = 'insufficient_track_credit_evidence'
        else:
            audit_status = 'unresolved'
        all_ids = [i for p in programme for i in p['track_ids']]
        flags = []
        if any(p['work_tracks'] > p['credited_tracks'] for p in programme):
            flags.append('title_matches_without_full_credits')
        if len(all_ids) != len(set(all_ids)):
            flags.append('shared_track_assignments')
        headings = {t['title'] for t in row.get('tracklist', []) if t.get('type') == 'index'}
        if any(p['target'] in headings and p['credited_tracks'] == 1 for p in programme):
            flags.append('single_credited_track_for_work_heading')
        results.append({**entry, 'title': row['title'], 'album_title': album['title'],
                        'required_performers': evidence['required_performers'],
                        'recomputed_v1_status': evidence['status'],
                        'original_rules_reproduced': evidence['status'] == entry['status'],
                        'one_to_one_catalogue_correspondence': evidence['status'] == 'found',
                        'audit_status': audit_status, 'diagnostic_flags': flags,
                        'programme': programme, 'completeness': completeness})
    return {'schema_version': 1, 'purpose': 'Completeness audit only; unknown is not evidence of absence or a confirmed false match. No recording-session verification.',
            'baseline_commit': scope['baseline_commit'], 'releases': results,
            'summary': {'releases': len(results),
                'original_statuses': dict(Counter(r['status'] for r in results)),
                'completeness': dict(Counter(r['completeness']['status'] for r in results)),
                'one_to_one_catalogue_correspondences': sum(r['one_to_one_catalogue_correspondence'] for r in results),
                'audit_statuses': dict(Counter(r['audit_status'] for r in results)),
                'diagnostic_flags': dict(Counter(f for r in results for f in r['diagnostic_flags'])),
                'v1_status_disagreements': sum(not r['original_rules_reproduced'] for r in results)}}


def main():
    scope_path = ROOT/'data/qobuz_baseline_audit_scope.json'
    inventory_path = ROOT/'data/qobuz_work_inventory.json'
    collection_path = ROOT/'data/collection_matches.json'
    snapshot = load_snapshot()
    scope = json.loads(scope_path.read_text())
    if scope['schema_version'] != 1:
        raise ValueError('Unsupported baseline scope')
    entries = scope['entries']
    if len(entries) != 66 or len({e['discogs_id'] for e in entries}) != 66:
        raise ValueError('Baseline audit requires exactly 66 distinct releases')
    rows = {str(r['discogs_id']): r for r in json.loads(collection_path.read_text())}
    result = audit(scope, rows, snapshot, json.loads(inventory_path.read_text()))
    result['provenance'] = {'checker_version': 'qobuz-completeness-pilot-v2',
        'scope_sha256': hashlib.sha256(scope_path.read_bytes()).hexdigest(),
        'inventory_sha256': hashlib.sha256(inventory_path.read_bytes()).hexdigest(),
        'collection_sha256': hashlib.sha256(collection_path.read_bytes()).hexdigest(),
        'metadata_manifest_fingerprint': snapshot['metadata_manifest']['fingerprint']}
    (ROOT/'data/qobuz_baseline_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result['summary']))


if __name__ == '__main__':
    main()
