"""Frozen, copy-only diagnostics of remaining title/work cases. No publication writes."""
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from qobuz_credit_role_audit import load_albums
from qobuz_credit171_diagnostic import declared_gaps
from qobuz_lead_review import fingerprint, target_fingerprint
from qobuz_match import catalogue, evaluate, tnorm, units, work_match, credits, agrees
from qobuz_work_groups import contextual_tracks, target_work_matches
from qobuz_target_credits import requirements
from qobuz_completeness import check_programme

ROOT = Path(__file__).resolve().parents[1]
ROMAN = dict(zip(['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII',
                  'XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX','XXI','XXII',
                  'XXIII','XXIV','XXV','XXVI','XXVII','XXVIII','XXIX','XXX','XXXI','XXXII'], range(1,33)))


SPOT_CHECKS = {
    '594243': 'Source uses Arabic Part1/2 and a joined Part3/4 band; candidate uses roman Pt.I/II and lacks McCoyTyner performance credit on inspected tracks. A part-number parser alone cannot establish complete cast/programme.',
    '2548602': 'Source Hoboken XVI/slash work numbers and candidate Hob.XVI: work numbers are structurally equivalent in the copy experiment. All six targets gain positive Gould support; completeness and recording review remain open.',
    '7065721': 'Heifetz/BrooksSmith Mozart sonatas have unnumbered movement titles and explicit K378/K454work fields. Prefixing those same-track fields supplies full current-rule unit support, not recording verification.',
    '24278222': 'Dido source splits actIIinto first-part/conclusion LP bands. The context experiment recovers only partial support; track-level vocal/conductor declarations and exact side boundaries remain separate requirements.',
    '5163525': 'Source Wanderer lists both Op15andD760; digital work field lists D760only. Strict catalogue subset remains unresolved. Liszt sonata source lacks its catalogue anchor and has too little distinctive work wording for the current matcher.',
    '8079435': 'Rachmaninoff source surname differs from candidate Rachmaninov spellings. Generic opus title hits can also be another composer. Composer guard rejection is not proof the entire candidate has the wrong programme.',
    '15527713': 'Relevant Serkin Mendelssohn tracks use a full composer name with lifespan annotations; source uses the hyphenated full variant. Orchestra strings also lack performance roles on inspected tracks. Do not equate a composer-name repair with complete cast support.',
    '3788392': 'Brandenburg works exist in the saved candidate, but inspected track strings omit required Abbado/LaScala musicians. Work-field context reveals a credit gap rather than a positive match.'}


def catalogue_text(text):
    """Hypothesis only: exact single Hob section/work and explicit opus subnumbers."""
    def replace(pattern, make, text):
        def apply(match):
            # Never turn a range/list or nested subdivision into its first member.
            if re.match(r'\s*[-–/,]', text[match.end():]):
                return match[0]
            return make(match)
        return re.sub(pattern, apply, text, flags=re.I)
    text = replace(r'\b(?:Hoboken|Hob)\.?\s*([IVX]+)\s*[:/]\s*(\d+)\b',
                   lambda m: f'Hob {ROMAN[m[1].upper()]} No {m[2]}' if m[1].upper() in ROMAN else m[0], text)
    text = replace(r'\bop(?:us)?\.?\s*(\d+)\s*/\s*(\d+)\b',
                   lambda m: f'Op {m[1]} No {m[2]}', text)
    return replace(r'\bop(?:us)?\.?\s*(\d+)\s+(?:N°|Nº|Ndeg)\s*(\d+)\b',
                   lambda m: f'Op {m[1]} No {m[2]}', text)


def work_copy(album, formatting=False):
    result = copy.deepcopy(album)
    changes = []
    for track in result['tracks']['items']:
        old = track['title']
        work = track.get('work')
        # Existing catalogue anchors are never overwritten by a work field.
        if work and not catalogue(old) and tnorm(work) not in tnorm(old):
            track['title'] = work + ': ' + old
        if formatting:
            track['title'] = catalogue_text(track['title'])
        if track['title'] != old:
            changes.append({'track_id': track['id'], 'original_title': old,
                            'work': work, 'experimental_title': track['title']})
    return result, changes


def target_copy(row):
    result = copy.deepcopy(row)
    mapping = {}
    for track in result.get('tracklist') or []:
        original = track['title']
        new = catalogue_text(original)
        if new != original:
            if new in mapping and mapping[new] != original:
                raise ValueError('Catalogue cleanup would merge distinct source titles')
            track['title'] = new
            mapping[new] = original
    originals = {t['title'] for t in row.get('tracklist') or []}
    if any(new in originals and new != old for new, old in mapping.items()):
        raise ValueError('Catalogue cleanup collides with an existing source title')
    result['_reviewed_title_sources'] = mapping
    return result, mapping


def source_flags(row, raw):
    titles = units(row)
    flags = []
    if any(re.search(r'\b(?:act|atto|aufzug|akt|teil|part|fortsetzung|conclusion)\b', t, re.I) for t in titles):
        flags.append('acts_parts_or_side_boundaries')
    if any('=' in t or ' / ' in t for t in titles):
        flags.append('multilingual_or_composite_titles')
    if any(catalogue_text(t) != t for t in titles):
        flags.append('explicit_catalogue_formatting_gap')
    if len(set(titles)) < len(titles):
        flags.append('repeated_source_unit_titles')
    if any(t.get('type_') == 'heading' for t in raw.get('tracklist') or []):
        flags.append('flat_source_headings')
    if not any(catalogue(t) for t in titles):
        flags.append('no_current_catalogue_anchor')
    return flags


def observations(row, album, evidence):
    tracks = contextual_tracks(row, album['tracks']['items'])
    output = []
    for item in evidence['programme']:
        target = item['target']
        work_row, required, scope = requirements(row, target, evidence['required_performers'])
        scoped_tracks = contextual_tracks(work_row, album['tracks']['items']) if scope else tracks
        plain = [t for t in scoped_tracks if work_match(target, t['title'])]
        allowed = [t for t in plain if target_work_matches(work_row, target, t)]
        ca = catalogue(target)
        shared = [t for t in scoped_tracks if ca & catalogue(t['title'])]
        output.append({'target': target, 'catalogue': sorted(ca),
            'title_match_track_ids': [t['id'] for t in plain],
            'composer_guard_pass_track_ids': [t['id'] for t in allowed],
            'shared_catalogue_track_ids': [t['id'] for t in shared],
            'required_performers': required,
            'missing_across_work_tracks': [n for n in required if not any(agrees(n, credits(t)) for t in allowed)],
            'declared_but_unaccepted_roles': declared_gaps(required, allowed)})
    return output


def family(candidates):
    coverage = max((c['formatted_evidence']['coverage'] for c in candidates), default=0)
    if coverage == 1:
        return 'experimental_full_unit_support'
    if coverage > 0:
        return 'experimental_partial_unit_support'
    obs = [o for c in candidates for o in c['observations']]
    if any(o['composer_guard_pass_track_ids'] for o in obs):
        return 'work_title_support_but_musician_gap'
    if any(o['title_match_track_ids'] for o in obs):
        return 'title_similarity_rejected_by_composer_guards'
    if any(o['shared_catalogue_track_ids'] for o in obs):
        return 'shared_catalogue_but_unresolved_title_structure'
    if any(o['catalogue'] for o in obs):
        return 'no_shared_catalogue_in_saved_candidates'
    return 'no_supported_title_or_catalogue_anchor'


def main():
    albums = load_albums()
    scope_path = ROOT/'data/qobuz_title151_scope.json'
    if not scope_path.exists():
        groups = json.loads((ROOT/'data/qobuz_blocker_groups.json').read_text())
        previous = json.loads((ROOT/'data/qobuz_title179_scope.json').read_text())
        ids = [e['discogs_id'] for e in groups['entries'] if e['group'] == 'work_title_or_catalogue_mapping_unresolved']
        if len(ids) != 151 or len(set(ids)) != 151:
            raise ValueError('Expected the agreed151case starting population')
        scope = {'schema_version': 1, 'frozen_on': '2026-11-16', 'release_ids': ids,
                 'candidate_ids': {rid: previous['candidate_ids'][rid] for rid in ids},
                 'baseline_publication_sha256': hashlib.sha256((ROOT/'data/qobuz_matches.json').read_bytes()).hexdigest(),
                 'groups_sha256': hashlib.sha256((ROOT/'data/qobuz_blocker_groups.json').read_bytes()).hexdigest()}
        scope_path.write_text(json.dumps(scope, ensure_ascii=False, indent=2)+'\n')
    scope = json.loads(scope_path.read_text())
    ids = scope['release_ids']
    if len(ids) != 151 or len(set(ids)) != 151 or set(scope['candidate_ids']) != set(ids):
        raise ValueError('Frozen151case scope changed')
    paths = [ROOT/name for name in ['data/qobuz_matches.json','data/collection_matches.json',
             'data/qobuz_remaining_recording_reviews.json','data/qobuz_work_inventory.json',
             'scripts/qobuz_match.py','scripts/qobuz_work_groups.py','scripts/qobuz_source_leaf_review.py',
             'src/ali_discogs/text.py','scripts/qobuz_title151_diagnostic.py']]
    paths += sorted((ROOT/'data').glob('*.json.gz'))
    paths += [ROOT/f'raw/discogs/releases/{rid}.json' for rid in ids]
    before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    inventory = json.loads((ROOT/'data/qobuz_work_inventory.json').read_text())
    entries = []
    for rid in ids:
        row = rows[rid]
        effective, target_changes = target_copy(row)
        raw = json.loads((ROOT/f'raw/discogs/releases/{rid}.json').read_text())
        candidates = []
        for aid in scope['candidate_ids'][rid]:
            album = albums[aid]
            broad, broad_changes = work_copy(album)
            formatted, formatted_changes = work_copy(album, formatting=True)
            baseline = evaluate(row, album)
            extended = evaluate(row, broad) if broad_changes else baseline
            experiment = evaluate(effective, formatted) if formatted_changes or target_changes else baseline
            candidates.append({'album_id': aid, 'title': album['title'], 'album_sha256': fingerprint(album),
                'same_track_required_cast_ids': [t['id'] for t in album['tracks']['items']
                    if baseline['required_performers'] and all(agrees(n, credits(t)) for n in baseline['required_performers'])],
                'baseline_evidence': baseline, 'extended_work_evidence': extended,
                'formatted_evidence': experiment, 'extended_work_title_changes': broad_changes,
                'formatted_title_changes': formatted_changes,
                'experimental_completeness': check_programme(effective, formatted, experiment, inventory),
                'observations': observations(effective, formatted, experiment)})
        entries.append({'discogs_id': rid, 'title': row['title'], 'target_sha256': target_fingerprint(row),
                        'source_sha256': before[f'raw/discogs/releases/{rid}.json'],
                        'source_units': units(row), 'source_flags': source_flags(row, raw),
                        'target_title_hypothesis': target_changes, 'candidates': candidates,
                        'machine_observation_family': family(candidates),
                        'diagnostic_spot_check': SPOT_CHECKS.get(rid)})
    gains, regressions = {}, {}
    for label, key in [('extended_work', 'extended_work_evidence'), ('catalogue_formatting_plus_work', 'formatted_evidence')]:
        gains[label] = [e['discogs_id'] for e in entries if any(c[key]['coverage'] > c['baseline_evidence']['coverage'] for c in e['candidates'])]
        regressions[label] = [e['discogs_id'] for e in entries if any(c[key]['coverage'] < c['baseline_evidence']['coverage'] for c in e['candidates'])]
    if any(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != sha for name,sha in before.items()):
        raise ValueError('A read-only input changed during the diagnostic')
    report = {'schema_version': 1, 'reviewed_on': '2026-11-16', 'status': 'diagnostic-only',
        'frozen_release_ids': ids, 'entries': entries,
        'machine_observation_counts': dict(Counter(e['machine_observation_family'] for e in entries)),
        'overlapping_source_flags': dict(Counter(f for e in entries for f in e['source_flags'])),
        'same_track_cast_release_ids': [e['discogs_id'] for e in entries if any(c['same_track_required_cast_ids'] for c in e['candidates'])],
        'coverage_gain_ids': gains, 'coverage_regression_ids': regressions,
        'diagnostic_spot_check_ids': list(SPOT_CHECKS),
        'scope_sha256': hashlib.sha256(scope_path.read_bytes()).hexdigest(), 'source_hashes': before,
        'provider_calls': 0, 'publication_changed': False, 'policy_adopted': False,
        'limitations': ['Machine observations are not151manual recording decisions or proof of catalogue absence.',
            'The151starting entries have no publication review metadata; older diagnostic/source holds such as Casals23950082still apply.',
            'Missing across work tracks is diagnostic only; names on different works are never borrowed.',
            'Same-track cast is only a discovery hint under current parser roles; it does not prove the requested work, recording, version or complete programme.',
            'Current associated-role token acceptance is measured, not endorsed or broadened.',
            'Full-unit support requires independent source-band completeness, positive composer/musician and recording checks.',
            'Read-only hypotheses preserve original source/cache payloads and excerpt/version words. No alias, role waiver or live rule change.']}
    path = ROOT/'data/qobuz_title151_diagnostic.json'
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    publication = json.loads((ROOT/'data/qobuz_matches.json').read_text())['releases']
    ranked = []
    for entry in entries:
        choices = [c for c in entry['candidates'] if c['formatted_evidence']['coverage'] > c['baseline_evidence']['coverage']]
        if not choices:
            continue
        best = min(choices, key=lambda c: (-c['formatted_evidence']['coverage'], c['experimental_completeness']['status'] != 'complete', c['album_id']))
        saved = publication[entry['discogs_id']]
        ranked.append({'discogs_id': entry['discogs_id'], 'title': entry['title'], 'album_id': best['album_id'],
            'experimental_coverage': best['formatted_evidence']['coverage'],
            'completeness': best['experimental_completeness']['status'],
            'workflow': 'resolved' if saved['status'] != 'unchecked' else 'held' if saved.get('review') else 'candidate_review_needed'})
    ranked.sort(key=lambda e: (-e['experimental_coverage'], int(e['discogs_id'])))
    (ROOT/'data/qobuz_title151_ranking.json').write_text(json.dumps({'schema_version':1,
        'diagnostic_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'entries': ranked,
        'limitations': 'Diagnostic leads only; no match/workflow labels changed. Prior saved constraints remain authoritative.'}, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['machine_observation_counts','overlapping_source_flags','coverage_gain_ids','coverage_regression_ids']}))


if __name__ == '__main__':
    main()
