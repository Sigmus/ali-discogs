"""Offline workflow ranking of all160newly cached release leads; never publish labels."""
import hashlib
import json
from collections import Counter
from qobuz_lead_review import ROOT
from qobuz_uncached160 import load_completed, SCOPE


def rank(entries, release_ids):
    selected = {e['discogs_id']: e for e in entries if e['discogs_id'] in release_ids}
    if set(selected) != set(release_ids):
        raise ValueError('Ranking must retain every frozen release')
    results = []
    for rid, entry in selected.items():
        candidates = [c for c in entry['cached_candidates']
                      if not c['reviewed_withheld'] and not c['reviewed_rejected']]
        candidates.sort(key=lambda c: (-c['coverage'], c['completeness'] != 'complete', c['album_id']))
        best = candidates[0] if candidates else None
        coverage = best['coverage'] if best else 0
        complete = best is not None and best['completeness'] == 'complete'
        bucket = ('supported_complete_programme' if coverage == 1 and complete
                  else 'supported_programme_needs_completeness' if coverage == 1
                  else 'partial_programme_support' if coverage > 0
                  else 'no_current_rule_support')
        results.append({'discogs_id': rid, 'title': entry['title'], 'bucket': bucket,
                        'best_album_id': best['album_id'] if best else None,
                        'supported_source_unit_fraction': coverage,
                        'completeness': best['completeness'] if best else None,
                        'candidate_count': len(candidates), 'uncached_hits': entry['uncached_hits'],
                        'candidates': candidates})
    order = {b: i for i, b in enumerate(['supported_complete_programme',
        'supported_programme_needs_completeness', 'partial_programme_support', 'no_current_rule_support'])}
    return sorted(results, key=lambda e: (order[e['bucket']], -e['supported_source_unit_fraction'], int(e['discogs_id'])))


def main():
    load_completed()
    scope = json.loads(SCOPE.read_text())
    path = ROOT/'data/qobuz_unmatched_audit.json'
    inventory = json.loads(path.read_text())
    publication = json.loads((ROOT/'data/qobuz_matches.json').read_text())['releases']
    resolved = [{'discogs_id': rid, 'status': publication[rid]['status']}
                for rid in scope['release_ids'] if publication[rid]['status'] != 'unchecked']
    reviewed = []
    for name in ['qobuz_fullsupport16_recording_audit.json', 'qobuz_partial38_recording_audit.json',
                 'qobuz_zero104_recording_audit.json']:
        review_path = ROOT/'data'/name
        batch = json.loads(review_path.read_text()) if review_path.exists() else {}
        if batch.get('status') == 'complete':
            reviewed.extend({'discogs_id': e['discogs_id'], 'decision': e['outcome'], 'finding': e['finding']}
                            for e in batch.get('entries', []) if e['outcome'] != 'probable')
    reviewed_ids = {e['discogs_id'] for e in reviewed}
    pending_ids = [rid for rid in scope['release_ids']
                   if publication[rid]['status'] == 'unchecked' and rid not in reviewed_ids]
    entries = rank(inventory['entries'], pending_ids)
    if any(e['uncached_hits'] for e in entries):
        raise ValueError('A frozen release still has uncached search candidates')
    result = {'schema_version': 1, 'reviewed_on': '2026-11-16',
              'scope_sha256': hashlib.sha256(SCOPE.read_bytes()).hexdigest(),
              'inventory_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'counts': dict(Counter(e['bucket'] for e in entries)), 'entries': entries,
              'resolved_entries': resolved, 'reviewed_unresolved_entries': reviewed, 'frozen_release_count': len(scope['release_ids']),
              'limitations': ['Workflow ranking, not calibrated confidence or recording acceptance.',
                'Coverage requires current programme/composer/performer rules; zero support may reflect parser gaps.',
                'Complete programme still needs recording-family and source-credit review.',
                'Previously withheld/rejected pairs excluded; source and published labels unchanged.']}
    (ROOT/'data/qobuz_uncached160_ranking.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result['counts']))


if __name__ == '__main__':
    main()
