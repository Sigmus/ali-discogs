"""Explicit work-field diagnostic for the frozen 179 title-mapping cases only."""
import hashlib
import json
from collections import Counter
from pathlib import Path
from qobuz_credit_role_audit import load_albums
from qobuz_credit171_diagnostic import explicit_work_copy
from qobuz_lead_review import fingerprint, target_fingerprint
from qobuz_match import evaluate
from qobuz_completeness import check_programme

ROOT = Path(__file__).resolve().parents[1]


def rank(entries):
    result = []
    for entry in entries:
        candidates = [c for c in entry['candidates'] if c['experimental_coverage'] > c['baseline_coverage']]
        if not candidates:
            continue
        best = min(candidates, key=lambda c: (-c['experimental_coverage'],
                   c['experimental_completeness']['status'] != 'complete', c['album_id']))
        bucket = ('full_support_complete_programme' if best['experimental_coverage'] == 1
                  and best['experimental_completeness']['status'] == 'complete' else
                  'full_support_needs_completeness' if best['experimental_coverage'] == 1 else 'partial_support')
        result.append({'discogs_id': entry['discogs_id'], 'title': entry['title'],
                       'bucket': bucket, 'best_album_id': best['album_id'],
                       'experimental_coverage': best['experimental_coverage'],
                       'completeness': best['experimental_completeness']['status']})
    order = {'full_support_complete_programme': 0, 'full_support_needs_completeness': 1, 'partial_support': 2}
    return sorted(result, key=lambda e: (order[e['bucket']], -e['experimental_coverage'], int(e['discogs_id'])))


def review_queue(entries, publication):
    ranked = rank(entries)
    pending, resolved, held = [], [], []
    for entry in ranked:
        saved = publication[entry['discogs_id']]
        if saved['status'] != 'unchecked':
            resolved.append({**entry, 'published_status': saved['status']})
        elif saved.get('review'):
            held.append({**entry, 'saved_review': saved['review']})
        else:
            pending.append(entry)
    return pending, resolved, held


def main():
    scope_path = ROOT/'data/qobuz_title179_scope.json'
    scope = json.loads(scope_path.read_text())
    ids = scope['release_ids']
    if len(ids) != 179 or len(set(ids)) != 179 or set(scope['candidate_ids']) != set(ids):
        raise ValueError('Frozen title179 scope changed')
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    publication_path = ROOT/'data/qobuz_matches.json'
    publication_before = publication_path.read_bytes()
    albums = load_albums()
    inventory = json.loads((ROOT/'data/qobuz_work_inventory.json').read_text())
    entries = []
    for rid in ids:
        row = rows[rid]
        candidates = []
        for aid in scope['candidate_ids'][rid]:
            album = albums[aid]
            baseline = evaluate(row, album)
            experimental, changes = explicit_work_copy(album)
            evidence = evaluate(row, experimental) if changes else baseline
            candidates.append({'album_id': aid, 'title': album['title'], 'album_sha256': fingerprint(album),
                'baseline_coverage': baseline['coverage'], 'experimental_coverage': evidence['coverage'],
                'baseline_status': baseline['status'], 'experimental_status': evidence['status'],
                'programme': evidence['programme'], 'changed_titles': changes,
                'experimental_completeness': check_programme(row, experimental, evidence, inventory)})
        candidates.sort(key=lambda c: (-c['experimental_coverage'], c['album_id']))
        entries.append({'discogs_id': rid, 'title': row['title'], 'target_sha256': target_fingerprint(row),
            'source_sha256': hashlib.sha256((ROOT/f'raw/discogs/releases/{rid}.json').read_bytes()).hexdigest(),
            'candidates': candidates,
            'has_coverage_gain': any(c['experimental_coverage'] > c['baseline_coverage'] for c in candidates),
            'has_coverage_regression': any(c['experimental_coverage'] < c['baseline_coverage'] for c in candidates)})
    gain_ids = [e['discogs_id'] for e in entries if e['has_coverage_gain']]
    report = {'schema_version': 1, 'reviewed_on': '2026-11-16', 'status': 'diagnostic-only',
        'frozen_release_ids': ids, 'entries': entries, 'coverage_gain_ids': gain_ids,
        'coverage_regression_ids': [e['discogs_id'] for e in entries if e['has_coverage_regression']],
        'full_unit_support_ids': [e['discogs_id'] for e in entries if any(c['experimental_coverage'] == 1 for c in e['candidates'])],
        'provider_calls': 0, 'publication_changed': False, 'policy_adopted': False,
        'scope_sha256': hashlib.sha256(scope_path.read_bytes()).hexdigest(),
        'source_hashes': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
                         ['data/collection_matches.json', 'data/qobuz_matches.json', 'data/qobuz_work_inventory.json',
                          'scripts/qobuz_credit171_diagnostic.py', 'scripts/qobuz_title179_diagnostic.py',
                          'scripts/qobuz_match.py', 'scripts/qobuz_work_groups.py']},
        'limitations': ['Read-only hypotheses using each track own explicit work field, on copies of shared metadata.',
                       'Candidate programme support is not recording identity, edition/instrument verification or a publication decision.',
                       'No source title rewrite, role normalization, fuzzy identity, new provider request or automated review completion.']}
    if publication_path.read_bytes() != publication_before:
        raise ValueError('Publication changed during diagnostic')
    report_path = ROOT/'data/qobuz_title179_diagnostic.json'
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    ranked, resolved, held = review_queue(entries, json.loads(publication_before)['releases'])
    ranking = {'schema_version': 1, 'reviewed_on': '2026-11-16', 'frozen_release_count': 179,
               'diagnostic_sha256': hashlib.sha256(report_path.read_bytes()).hexdigest(),
               'counts': dict(Counter(e['bucket'] for e in ranked)), 'entries': ranked,
               'resolved_entries': resolved, 'reviewed_unresolved_entries': held,
               'limitations': ['Experimental candidate evidence, not accepted recordings or completed reviews.',
                               'Use original cached payloads, raw musical credits and recording corroboration before any promotion.']}
    (ROOT/'data/qobuz_title179_ranking.json').write_text(json.dumps(ranking, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ['coverage_gain_ids', 'coverage_regression_ids', 'full_unit_support_ids']}))


if __name__ == '__main__':
    main()
