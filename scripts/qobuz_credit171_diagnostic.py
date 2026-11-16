"""Read-only credit/parser diagnostics; never publish matches or fetch metadata."""
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from qobuz_credit_role_audit import load_albums
from qobuz_match import agrees, credits, evaluate
from qobuz_work_groups import contextual_tracks, target_work_matches

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ['669978', '1724303', '1132104', '2170750', '1035152', '1723557',
          '1896362', '2060839', '1470008', '1524282', '1180104', '2345819']
FINDINGS = {
 '669978': ('explicit-instrument-role-and-identity', 'Required guitarists occur on the matching work but their Guitar role is not accepted; Robert Irving name variants add an identity gap. No associated-role waiver.', 'Audit a narrowly defined explicit-instrument role list and exact identities; retain recording checks.'),
 '1724303': ('source-scope-and-instrument-role', 'Various is required as a performer; global featuring musicians are imposed across tracks. Some exact guitar/brass names also have unaccepted instrument roles.', 'Reconcile raw per-track source roles on a diagnostic copy before any role or publication change.'),
 '1132104': ('ensemble-role-and-members', 'Prague String Quartet is declared with an unaccepted role; source individual players remain missing. Accepting the ensemble role alone cannot resolve this LP.', 'Retain individual player requirements and audit the full raw lineup.'),
 '2170750': ('source-opus-subdivision', 'The actual Arrau nocturne cycle has positive piano/artist evidence but source Op.9/1-style titles do not map under current rules. Generic compilations give misleading work-only hits.', 'Design catalogue-subdivision handling with negative tests and source-band/timing checks.'),
 '1035152': ('work-context-source-scope-and-orchestra-identity', 'The Richter box contains relevant work fields and Warsaw orchestra spelling; two source conductors lack track scopes. Global casts cannot be borrowed between solo pieces and concertos.', 'Resolve source work-specific conductors and exact orchestra identity, then bind the complete source programme.'),
 '1723557': ('work-context-and-associated-role', 'Explicit work-field prefixing recovers current-rule support for the Stern/Barenboim concerto, but New York Philharmonic is only Associated Performer. The current spaced-role parser accepts performer as a token.', 'Keep withheld from promotion until provider-specific associated-role semantics and recording evidence are resolved.'),
 '1896362': ('explicit-work-context', 'Reiner Conducts Tchaikovsky has bare numbered movement titles with the complete symphony in work fields and positive conductor/orchestra credits. Diagnostic prefixing recovers support.', 'Verify source recording/timings and adopt only a bounded, tested work-field rule or existing hash-bound mapping.'),
 '2060839': ('raw-chorusmaster-and-programme', 'The strongest matching Jochum family has most source musicians but source chorus master Gerhard Hellwig remains unproven; more generic candidates lack the target cast.', 'Retain chorus-master evidence and map the complete source vocal programme.'),
 '1470008': ('source-heading-and-programme', 'A generic piano Baroque hit matches the umbrella Art of Fugue title; the full Gould box has the source organ lead but source Contrapunctus1-9 needs an instrument-specific leaf mapping.', 'Verify the organ session and all nine source bands, not a piano compilation title.'),
 '1524282': ('exact-ensemble-identity', 'Source Choir of Mount Angel Abbey and cached Choir Of The Abbey Of Mount Angel are near full-name variants. Similar wording alone is not authority evidence.', 'Corroborate exact ensemble identity, both choirs and the complete Requiem family.'),
 '1180104': ('dangerous-near-name', 'The full Solti lead declares Paul Kuentz while source tenor Mime is Paul Kuen. These names must not be merged by fuzzy matching; an excerpt alternative names Kuen but is not the complete opera.', 'Investigate provider misattribution with primary cast evidence; preserve full-opera completeness.'),
 '2345819': ('arrangement-and-recording-identity', 'Generic Op.61 work hits can be the violin original; the source is the piano arrangement and matching musicians somewhere in the box are insufficient.', 'Verify piano instrumentation, source movement/timing boundaries and exact recording family.')}


def explicit_work_copy(album):
    """Diagnostic only: prefix bare numbered titles with their own explicit work."""
    result = copy.deepcopy(album)
    changed = []
    for track in result['tracks']['items']:
        if track.get('work') and re.match(r'^(?:[IVX]+|\d+)[.)]\s', track['title']):
            changed.append({'track_id': track['id'], 'original_title': track['title'], 'work': track['work']})
            track['title'] = track['work'] + ': ' + track['title']
    return result, changed


def declared_gaps(required, tracks):
    """Exact identity only, on work-matching tracks; no fuzzy or borrowed credit."""
    result = []
    for name in required:
        declarations = []
        for track in tracks:
            if agrees(name, credits(track)):
                continue
            for part in (track.get('performers') or '').split(' - '):
                person, sep, roles = part.partition(',')
                if sep and agrees(name, [person]):
                    declarations.append({'track_id': track['id'], 'name': person.strip(), 'roles': roles.strip()})
        if declarations:
            result.append({'required_name': name, 'declarations': declarations})
    return result


def main():
    scope_path = ROOT/'data/qobuz_credit171_scope.json'
    scope = json.loads(scope_path.read_text())
    ids = scope['release_ids']
    if (len(ids) != 171 or len(set(ids)) != 171
            or set(scope['candidate_ids']) != set(ids) or not set(SAMPLE) <= set(ids)):
        raise ValueError('Frozen 171-case diagnostic scope changed')
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    albums = load_albums()
    entries, role_counts, context_ids = [], Counter(), []
    for rid in ids:
        row = rows[rid]
        candidates, roles_for_release, has_context_gain = [], set(), False
        for aid in scope['candidate_ids'][rid]:
            album = albums[aid]
            baseline = evaluate(row, album)
            tracks = contextual_tracks(row, album['tracks']['items'])
            gaps = []
            for item in baseline['programme']:
                matched = [t for t in tracks if target_work_matches(row, item['target'], t)]
                for gap in declared_gaps(item.get('required_performers', baseline['required_performers']), matched):
                    gaps.append({'source_unit': item['target'], **gap})
                    roles_for_release.update(d['roles'] for d in gap['declarations'])
            contextual, changes = explicit_work_copy(album)
            experimental = evaluate(row, contextual) if changes else baseline
            gain = experimental['coverage'] > baseline['coverage']
            has_context_gain |= gain
            candidates.append({'album_id': aid, 'title': album['title'],
                'album_sha256': hashlib.sha256(json.dumps(album, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
                'baseline_coverage': baseline['coverage'], 'diagnostic_work_context_coverage': experimental['coverage'],
                'explicit_work_title_changes': changes if rid in SAMPLE or gain else [],
                'declared_but_unaccepted': gaps})
        role_counts.update(sorted(roles_for_release))
        if has_context_gain:
            context_ids.append(rid)
        raw_path = ROOT/f'raw/discogs/releases/{rid}.json'
        entry = {'discogs_id': rid, 'title': row['title'],
                 'raw_source_sha256': hashlib.sha256(raw_path.read_bytes()).hexdigest(),
                 'candidates': candidates, 'manual_sample': rid in SAMPLE}
        if rid in SAMPLE:
            raw = json.loads(raw_path.read_text())
            kind, finding, next_action = FINDINGS[rid]
            entry.update(finding_kind=kind, finding=finding, next_action=next_action,
                         source_programme=raw['tracklist'], source_credits=raw.get('extraartists', []))
        entries.append(entry)
    result = {'schema_version': 1, 'reviewed_on': '2026-11-16', 'frozen_release_ids': ids,
        'manual_sample_ids': SAMPLE, 'diagnostic_count': len(entries),
        'explicit_work_context_gain_ids': context_ids,
        'unaccepted_role_strings_release_counts': dict(role_counts.most_common()),
        'entries': entries, 'provider_calls': 0, 'publication_changed': False,
        'scope_sha256': hashlib.sha256(scope_path.read_bytes()).hexdigest(),
        'baseline_publication_sha256': scope['baseline_publication_sha256'],
        'source_hashes': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
                         ['data/collection_matches.json', 'scripts/qobuz_match.py', 'scripts/qobuz_work_groups.py', 'scripts/qobuz_credit171_diagnostic.py']},
        'limitations': ['12 purposeful diverse cases, not a random population sample; no accuracy or promotion estimate.',
          '171 is the frozen starting cohort, not a claim all remain unreviewed. Machine diagnostics never complete recording reviews or change workflow labels.',
          'Existing spaced Associated Performer token acceptance is reported, not endorsed or broadened.',
          'Work-field experiments preserve credits but do not prove recording identity, completeness, instrument or version.',
          'Role counts overlap across releases and count exact role strings; an explicit name is not proof of the right recording.',
          'Unaccepted Composer or writer declarations can expose false source performer requirements; never accept these as musical performance roles.',
          'No source normalization, global alias, role-policy change, new match or provider request.']}
    (ROOT/'data/qobuz_credit171_diagnostic.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'sample': len(SAMPLE), 'diagnostics': len(entries), 'context_gain_ids': context_ids,
                      'unaccepted_roles': dict(role_counts.most_common())}))


if __name__ == '__main__':
    main()
