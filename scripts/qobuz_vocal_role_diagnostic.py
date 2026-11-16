"""Experimental exact vocal-role interpretation on copies; never publish or fetch."""
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path
from qobuz_credit_role_audit import load_albums
from qobuz_lead_review import fingerprint
from qobuz_match import evaluate
from qobuz_completeness import check_programme

ROOT = Path(__file__).resolve().parents[1]
# Hypotheses only: these are not imported by the production matching path.
ALIASES = {
    'SopranoVocalist': 'Soprano', 'MezzoSopranoVocalist': 'Mezzo Soprano',
    'Mezzo-SopranoVocalist': 'Mezzo Soprano', 'AltoVocalist': 'Alto',
    'ContraltoVocalist': 'Contralto', 'TenorVocalist': 'Tenor',
    'BaritoneVocalist': 'Baritone', 'BassVocalist': 'Bass',
    'BassBaritoneVocalist': 'Bass Baritone', 'Bass-BaritoneVocalist': 'Bass Baritone'}
_BY_KEY = {k.casefold(): v for k, v in ALIASES.items()}


def experimental_text(value):
    if not isinstance(value, str):
        return value, []
    declarations, parts = [], []
    for part in value.split(' - '):
        fields = part.split(',')
        for i in range(1, len(fields)):
            original = fields[i].strip()
            replacement = _BY_KEY.get(original.casefold())
            if replacement:
                fields[i] = fields[i].replace(original, replacement, 1)
                declarations.append({'name': fields[0].strip(), 'role': original,
                                     'experimental_role': replacement})
        parts.append(','.join(fields))
    return ' - '.join(parts), declarations


def experimental_album(album):
    result = copy.deepcopy(album)
    changes = []
    for track in result['tracks']['items']:
        text, declarations = experimental_text(track.get('performers'))
        if declarations:
            before = fingerprint(track)
            track['performers'] = text
            changes.append({'track_id': track['id'], 'original_track_sha256': before,
                            'experimental_track_sha256': fingerprint(track),
                            'declarations': declarations})
    return result, changes


def evidence_summary(row, album, evidence, inventory):
    return {'status': evidence['status'], 'confidence': evidence['confidence'], 'coverage': evidence['coverage'],
            'covered': evidence['covered'], 'target_count': evidence['target_count'],
            'programme': evidence['programme'],
            'completeness': check_programme(row, album, evidence, inventory)}


def references(publication, unmatched):
    result = {}
    for rid, release in publication['releases'].items():
        result[rid] = {str(c['id']) for c in release['candidates']}
    for entry in unmatched['entries']:
        result.setdefault(entry['discogs_id'], set()).update(c['album_id'] for c in entry['cached_candidates'])
    return result


def main():
    publication_path = ROOT/'data/qobuz_matches.json'
    before_publication = publication_path.read_bytes()
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    publication = json.loads(before_publication)
    unmatched = json.loads((ROOT/'data/qobuz_unmatched_audit.json').read_text())
    inventory = json.loads((ROOT/'data/qobuz_work_inventory.json').read_text())
    refs = references(publication, unmatched)
    albums = load_albums()
    altered, census, role_counts = {}, [], Counter()
    for aid, album in sorted(albums.items()):
        experimental, changes = experimental_album(album)
        if not changes:
            continue
        altered[aid] = experimental
        counts = Counter(d['role'] for c in changes for d in c['declarations'])
        role_counts.update(counts)
        census.append({'album_id': aid, 'title': album['title'], 'album_sha256': fingerprint(album),
                       'affected_tracks': len(changes), 'role_counts': dict(sorted(counts.items())),
                       'track_changes': changes})
    affected_pairs, affected_ids, gains, regressions, full_support = [], set(), set(), set(), set()
    for rid in sorted(rows, key=int):
        for aid in sorted(refs.get(rid, set()) & altered.keys()):
            row, album, experimental = rows[rid], albums[aid], altered[aid]
            baseline, changed = evaluate(row, album), evaluate(row, experimental)
            affected_ids.add(rid)
            if changed['coverage'] > baseline['coverage']:
                gains.add(rid)
            elif changed['coverage'] < baseline['coverage']:
                regressions.add(rid)
            if baseline['coverage'] < 1 and changed['coverage'] == 1:
                full_support.add(rid)
            affected_pairs.append({'discogs_id': rid, 'title': row['title'], 'album_id': aid,
                'album_title': album['title'], 'published_status': publication['releases'][rid]['status'],
                'saved_review': publication['releases'][rid].get('review'),
                'raw_source_sha256': hashlib.sha256((ROOT/f'raw/discogs/releases/{rid}.json').read_bytes()).hexdigest(),
                'baseline': evidence_summary(row, album, baseline, inventory),
                'experimental': evidence_summary(row, experimental, changed, inventory)})
    report = {'schema_version': 1, 'reviewed_on': '2026-11-16', 'status': 'diagnostic-only',
        'aliases': ALIASES, 'cached_albums': len(albums), 'affected_albums': len(census),
        'affected_track_declarations': sum(role_counts.values()), 'roles': dict(sorted(role_counts.items())),
        'target_population': len(rows), 'saved_reference_pairs': sum(len(v) for v in refs.values()),
        'affected_reference_pairs': len(affected_pairs), 'affected_release_ids': sorted(affected_ids, key=int),
        'coverage_gain_ids': sorted(gains, key=int), 'coverage_regression_ids': sorted(regressions, key=int),
        'new_full_unit_support_ids': sorted(full_support, key=int),
        'albums': census, 'candidate_comparisons': affected_pairs,
        'provider_calls': 0, 'publication_changed': False, 'policy_adopted': False,
        'source_hashes': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
            ['data/collection_matches.json', 'data/qobuz_matches.json', 'data/qobuz_unmatched_audit.json',
             'data/qobuz_work_inventory.json', 'scripts/qobuz_match.py', 'scripts/qobuz_work_groups.py',
             'scripts/qobuz_vocal_role_diagnostic.py',
             'data/review_sources/vocal-role-semantics/standards-observation.txt']},
        'limitations': ['Exact role-field hypotheses on temporary metadata copies, not production policy or shared cache rewrites.',
            'Saved-reference universe, not every possible release/catalogue pair; counts are unique releases unless labelled otherwise.',
            'Candidate coverage and completeness diagnostics do not establish recording identity, full source reconciliation or listening verification.',
            'Saved holds, raw source, accepted results, confidence and workflow labels remain unchanged.',
            'Composer, producer, generic Artist, associated roles and near-name identity are not added to the hypotheses.',
            'Current DDEX RDR dictionary defines Vocalist but does not establish the provider contract for these exact compact spellings.']}
    if publication_path.read_bytes() != before_publication:
        raise ValueError('Publication changed during diagnostic')
    (ROOT/'data/qobuz_vocal_role_diagnostic.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in ['cached_albums','affected_albums','affected_track_declarations',
          'affected_reference_pairs','coverage_gain_ids','coverage_regression_ids','new_full_unit_support_ids']}))


if __name__ == '__main__':
    main()
