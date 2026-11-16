"""Read-only tolerance scenarios on existing complete source-band review mappings."""
import hashlib
import json
from collections import Counter
from qobuz_lead_review import ROOT, assess
from qobuz_credit_role_audit import load_albums


def timing_scenario(bands, percentage=.03, floor=5, consensus=False):
    # Existing independently recorded exceptions remain explicit, not generalized.
    timed = [b for b in bands if b['source_duration_seconds'] is not None and not b['source_duration_notes']]
    if not timed:
        return {'applicable': False, 'passes': True, 'timed_bands': 0, 'outliers': []}
    outliers = [b for b in timed if abs(b['source_duration_seconds']-b['digital_duration_seconds']) >
                max(floor, percentage*b['source_duration_seconds'])]
    passes = not outliers
    if consensus and outliers:
        total = sum(b['source_duration_seconds'] for b in timed)
        difference = sum(abs(b['source_duration_seconds']-b['digital_duration_seconds']) for b in timed)
        passes = (len(timed) >= 10 and len(outliers) == 1 and (len(timed)-1)/len(timed) >= .9
                  and abs(outliers[0]['source_duration_seconds']-outliers[0]['digital_duration_seconds']) <= 90
                  and abs(outliers[0]['source_duration_seconds']-outliers[0]['digital_duration_seconds']) <= .35*outliers[0]['source_duration_seconds']
                  and total > 0 and difference/total <= .03)
    return {'applicable': True, 'passes': passes, 'timed_bands': len(timed),
            'outliers': [{'target':b['target'], 'source_seconds':b['source_duration_seconds'],
                          'digital_seconds':b['digital_duration_seconds']} for b in outliers]}


SCENARIOS = {
    'current_3pct_or_5sec': {},
    '5pct_or_5sec': {'percentage': .05},
    '10pct_or_5sec': {'percentage': .10},
    '20pct_or_5sec': {'percentage': .20},
    '35pct_or_5sec': {'percentage': .35},
    '3pct_or_15sec': {'floor': 15},
    # Illustrative hypothesis, not an adopted or calibrated policy.
    'consensus_90pct_close_one_flagged_outlier': {'floor':15, 'consensus':True},
}


def main():
    ledger_path = ROOT/'data/qobuz_remaining_recording_reviews.json'
    publication_path = ROOT/'data/qobuz_matches.json'
    before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in
              [ledger_path, publication_path, ROOT/'data/collection_matches.json']}
    rows = {str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    reviews = json.loads(ledger_path.read_text())['releases']
    albums = load_albums()
    entries = []
    mentions = []
    for review in reviews:
        if review['decision'] == 'withhold' and any(w in review['recording_review'].lower() for w in ['duration','timing']):
            mentions.append({'discogs_id':review['discogs_id'], 'title':rows[review['discogs_id']]['title'],
                             'review_kind':review.get('review_kind'), 'finding':review['recording_review']})
        if review.get('review_kind') != 'source-leaf-bands':
            continue
        result, _ = assess(rows[review['discogs_id']], albums[review['album_id']], review)
        other = [b for b in result['blockers'] if b != 'source-band-duration']
        entries.append({'discogs_id':review['discogs_id'], 'title':rows[review['discogs_id']]['title'],
            'decision':review['decision'], 'album_id':review['album_id'],
            'source_sha256':review['source_sha256'], 'album_sha256':review['album_sha256'],
            'other_mechanical_blockers':other, 'bands':result['completeness']['works'],
            'scenarios':{name:timing_scenario(result['completeness']['works'],**options) for name,options in SCENARIOS.items()}})
    summary = {}
    for name in SCENARIOS:
        unlocked = [e['discogs_id'] for e in entries if e['decision']=='withhold'
                    and not e['other_mechanical_blockers'] and e['scenarios'][name]['applicable'] and e['scenarios'][name]['passes']
                    and not e['scenarios']['current_3pct_or_5sec']['passes']]
        summary[name] = {'would_clear_timing_gate_ids':unlocked,
                         'previously_accepted_regressions':[e['discogs_id'] for e in entries if e['decision']=='probable' and not e['scenarios'][name]['passes']]}
    report = {'schema_version':1,'observed_on':'2026-11-16','status':'proposal-diagnostic-only',
        'mapped_review_count':len(entries),'mapped_review_decisions':dict(Counter(e['decision'] for e in entries)),
        'summary':summary,'entries':entries,'held_reviews_mentioning_timing':mentions,
        'other_timing_mentions_without_complete_leaf_map':[e['discogs_id'] for e in mentions if e['review_kind']!='source-leaf-bands'],
        'source_hashes':before,'provider_calls':0,'publication_changed':False,'policy_adopted':False,
        'limitations':['This measures30existing complete source-band mappings, not every cached candidate or all unmatched albums.',
            'A cleared timing gate is not automatic recording acceptance; saved decisions and other source/recording constraints remain.',
            'Generic holds without frozen full-band maps cannot be assigned honest promotion counts by changing a number.',
            'Consensus is an illustrative proposal: >=10timed bands, >=90%within max15sec/3%, one outlier <=90sec/35%, total absolute error <=3%.',
            'No missing band, reused track, absent musician, composer conflict, wrong instrument or unverified recording is waived.',
            'Source timings are saved metadata, not newly verified printed-label or listening measurements.']}
    for name,sha in before.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:
            raise ValueError('Read-only sensitivity changed an input')
    (ROOT/'data/qobuz_timing_sensitivity.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'mapped':len(entries),'decisions':report['mapped_review_decisions'],'summary':summary,
                      'other_timing_mentions_without_complete_leaf_map':report['other_timing_mentions_without_complete_leaf_map']}))


if __name__ == '__main__':
    main()
