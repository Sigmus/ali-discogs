"""Group unresolved evidence for planning; never infer absence or change matches."""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def planning_family(group):
    """Transparent label-based grouping; the original finding remains authoritative."""
    if group.startswith('saved:'):
        kind = group.removeprefix('saved:')
        if any(word in kind for word in ['credit', 'cast', 'members', 'orchestra', 'choir', 'soloist', 'conductor']):
            return 'credit_evidence'
        if any(word in kind for word in ['identity', 'recording', 'session', 'transfer']):
            return 'recording_identity'
        if any(word in kind for word in ['programme', 'source', 'flat', 'band', 'pair', 'box', 'cycle', 'catalogue']):
            return 'source_programme_mapping'
        return 'other_saved_blocker'
    return 'credit_evidence' if group == 'credit_support_unresolved' else group


def build(inventory, publication, findings):
    entries = []
    for entry in inventory['entries']:
        rid = entry['discogs_id']
        release = publication['releases'][rid]
        if release['status'] != 'unchecked':
            raise ValueError('Unmatched inventory is stale')
        review = release.get('review')
        finding = findings.get(rid)
        candidates = entry['cached_candidates']
        programme = [p for c in candidates for p in c.get('programme', [])]
        if review:
            group = 'saved:' + (finding['finding_kind'] if finding else review['decision'])
        elif not candidates:
            group = 'no_cached_candidate'
        elif not any(p.get('work_tracks', 0) for p in programme):
            group = 'work_title_or_catalogue_mapping_unresolved'
        elif not any(p.get('credited_tracks', 0) for p in programme):
            group = 'credit_support_unresolved'
        else:
            group = 'partial_programme_or_completeness'
        entries.append({'discogs_id': rid, 'title': entry['title'],
            'review_state': 'reviewed_unresolved' if review else 'no_saved_decision',
            'group': group, 'planning_family': planning_family(group),
            'cached_candidate_count': len(candidates),
            'uncached_hits': entry['uncached_hits'],
            'finding': finding['finding'] if finding else review['reason'] if review else None,
            'next_action': finding['next_action'] if finding else None})
    return {'schema_version': 1, 'reviewed_on': '2026-11-16',
        'unique_unresolved_releases': len(entries),
        'review_state_counts': dict(Counter(e['review_state'] for e in entries)),
        'planning_families': dict(sorted(Counter(e['planning_family'] for e in entries).items())),
        'groups': dict(sorted(Counter(e['group'] for e in entries).items())),
        'entries': entries, 'provider_calls': 0, 'publication_changed': False,
        'limitations': [
            'Planning groups count unique releases, not collection copies or possible promotions.',
            'Saved finding kinds are preserved verbatim; different labels may describe related blockers.',
            'Planning families use explicit keyword rules on saved finding labels; they are not a new evidence assessment.',
            'Unreviewed groups are current-rule diagnostics, not manual recording reviews.',
            'Zero work support may mean title/catalogue parsing or a different programme; it never proves absence.',
            'Names/credits on another work cannot establish credits on the target recording.',
            'Grouping authorizes no new retrieval, identity alias, role waiver or automatic promotion.']}


def main():
    inventory_path = ROOT/'data/qobuz_unmatched_audit.json'
    publication_path = ROOT/'data/qobuz_matches.json'
    findings, paths = {}, [inventory_path, publication_path]
    for path in sorted((ROOT/'data').glob('qobuz_*recording_audit.json')):
        report = json.loads(path.read_text())
        if report.get('status') != 'complete':
            continue
        paths.append(path)
        for entry in report.get('entries', []):
            if 'finding_kind' in entry:
                findings[entry['discogs_id']] = entry
    result = build(json.loads(inventory_path.read_text()),
                   json.loads(publication_path.read_text()), findings)
    result['source_hashes'] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    (ROOT/'data/qobuz_blocker_groups.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'review_states': result['review_state_counts'], 'families': result['planning_families']}))


if __name__ == '__main__':
    main()
