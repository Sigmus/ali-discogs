"""Rebuild cached-review workflow triage; percentages are not match confidence."""
import hashlib
import json
from collections import Counter
from qobuz_lead_review import ROOT

CONSTRAINTS = {
    '8962178': ('Recording-transfer provenance unresolved', 'data/qobuz_gieseking_programme_audit.json'),
    '15221307': ('Known Medtner/Beethoven opus collision; source-composer guard', 'data/qobuz_source_composer_reviews.json'),
    '7609610': ('Credit exception remains an unadopted proposal', 'docs/plans/2026-11-13-bitches-brew-credits.md'),
}


def build(inventory, reviewed):
    entries = []
    for entry in inventory['entries']:
        if entry['category'] != 'work_or_credit_unresolved':
            continue
        rid = entry['discogs_id']
        candidates = [c for c in entry['cached_candidates'] if not c['reviewed_withheld'] and not c['reviewed_rejected']]
        best = max(candidates, key=lambda c: c['coverage'], default=None)
        coverage = best['coverage'] if best else 0
        category = ('reviewed_blocker' if rid in reviewed else 'known_constraint' if rid in CONSTRAINTS
                    else 'priority_review' if coverage >= .5 else 'secondary_partial_lead' if coverage > 0
                    else 'no_current_supported_units')
        result = {'discogs_id': rid, 'title': entry['title'], 'queue': category,
                  'best_cached_album_id': best['album_id'] if best else None,
                  'supported_source_unit_fraction': coverage, 'uncached_hits': entry['uncached_hits']}
        if rid in CONSTRAINTS:
            result['constraint'], result['evidence'] = CONSTRAINTS[rid]
        if rid in reviewed:
            result['evidence'] = reviewed[rid].get('audit_path', 'data/qobuz_priority14_batch_audit.json')
            result['constraint'] = reviewed[rid]['finding']
        entries.append(result)
    entries.sort(key=lambda e: (-e['supported_source_unit_fraction'], int(e['discogs_id'])))
    return {'schema_version': 1, 'reviewed_on': '2026-11-15',
            'population': str(len(entries)) + ' unique releases currently categorized work_or_credit_unresolved',
            'rules': {'priority_review': 'Unheld cached candidate supports >=50% of current source units; known/reviewed blockers excluded.',
                      'secondary_partial_lead': 'Some current support, below50%; known/reviewed blockers excluded.',
                      'known_constraint': 'Previously documented transfer, source-composer or credit-policy constraint.',
                      'reviewed_blocker': 'Completed recording review with a saved decision; no automatic return to the open queue.',
                      'no_current_supported_units': 'No unheld cached candidate supports a source unit under current rules.'},
            'counts': dict(Counter(e['queue'] for e in entries)), 'entries': entries}


def main():
    path = ROOT/'data/qobuz_unmatched_audit.json'
    reviewed = {}
    for name in ['qobuz_priority14_batch_audit.json', 'qobuz_secondary23_recording_audit.json']:
        source = ROOT/'data'/name
        if not source.exists():
            continue
        batch = json.loads(source.read_text())
        if name.startswith('qobuz_secondary23') and batch['status'] != 'complete':
            continue
        for entry in batch['entries']:
            if entry['discogs_id'] in reviewed:
                raise ValueError('Duplicate completed batch case')
            reviewed[entry['discogs_id']] = {**entry, 'audit_path': 'data/'+name}
    result = build(json.loads(path.read_text()), reviewed)
    result['inventory_sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
    (ROOT/'data/qobuz_cached_review_queue.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result['counts']))


if __name__ == '__main__':
    main()
