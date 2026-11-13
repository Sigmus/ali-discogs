"""Twenty more searches for releases that still have no saved Qobuz hit."""
import argparse
import gzip
import hashlib
import json

from qobuz_match import ROOT
from qobuz_query_plan import propose, relevance
from qobuz_snapshot import load_snapshot, album_fields
import qobuz_comparison_pilot as runner

SCOPE = ROOT/'data/qobuz_empty_search_scope.json'
OUTPUT = ROOT/'.qobuz-poc/empty-search'
EVIDENCE = ROOT/'data/qobuz_empty_searches.json.gz'
PRIOR_SCOPES = ('qobuz_comparison_scope.json', 'qobuz_round2_scope.json', 'qobuz_query_trial_scope.json')

# Query text only. These do not change who the release requires.
REVIEWED_QUERIES = {
    '1216294': ['georg solti wagner walkure', 'kirsten flagstad solti walkure'],
    '6534486': ['adam harasiewicz chopin', 'adam harasiewicz chopin impromptu'],
    '7002243': ['otto klemperer beethoven eroica', 'philharmonia beethoven op 55'],
    '8176289': ['gunther leib bach bwv 201', 'thomanerchor bach bwv 201'],
    '8962178': ['walter gieseking mendelssohn', 'walter gieseking lieder ohne worte'],
    '11584908': ['rafael kubelik dvorak', 'rafael kubelik dvorak tone poems'],
    '13872783': ['john barbirolli mahler symphony 5', 'john barbirolli mahler symphony 9'],
    '15980846': ['hungarian quartet haydn op 76', 'hungarian quartet haydn op 64'],
    '22065910': ['andre cluytens franck', 'andre cluytens franck psyche'],
    '34776194': ['byron janis chopin', 'byron janis schumann'],
}


def queries_for(row, original):
    reviewed = REVIEWED_QUERIES.get(str(row['discogs_id']))
    if reviewed:
        return reviewed
    return list(dict.fromkeys(q for q in propose(row) if q and q != original))[:2]


def fingerprint(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def prepare():
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    original = load_snapshot()
    audit = json.loads((ROOT/'data/qobuz_unmatched_audit.json').read_text())
    excluded = set()
    for name in PRIOR_SCOPES:
        excluded.update(e['discogs_id'] for e in json.loads((ROOT/'data'/name).read_text())['entries'])
    collection_sha = hashlib.sha256((ROOT/'data/collection_matches.json').read_bytes()).hexdigest()
    if not SCOPE.exists():
        pool = []
        for entry in audit['entries']:
            rid = entry['discogs_id']
            if entry['category'] != 'no_saved_hits' or rid in excluded:
                continue
            original_query = original['searches'][rid]['query']
            chosen = queries_for(rows[rid], original_query)
            if len(chosen) == 2 and len(set(chosen)) == 2:
                pool.append((rid, chosen, original_query))
        selected = runner.spread(pool, 20)
        scope = {
            'schema_version': 1,
            'selected_on': '2026-11-13',
            'selection': 'Twenty releases from the 324 with no saved Qobuz hit, excluding earlier comparison, round-two and query-trial scopes. Evenly spaced by release ID. Not a sample of the whole collection.',
            'collection_sha256': collection_sha,
            'entries': [{'discogs_id': rid, 'title': rows[rid]['title'], 'original_query': original_query, 'queries': chosen}
                        for rid, chosen, original_query in selected],
        }
        runner.save(SCOPE, scope)
    scope = json.loads(SCOPE.read_text())
    if scope['schema_version'] != 1 or len(scope['entries']) != 20 or len({e['discogs_id'] for e in scope['entries']}) != 20:
        raise ValueError('Invalid empty-search scope')
    if scope['collection_sha256'] != collection_sha:
        raise ValueError('Collection changed; review the fixed scope before resuming')
    tasks = []
    for entry in scope['entries']:
        rid = entry['discogs_id']
        if rid in excluded or entry['queries'] != queries_for(rows[rid], original['searches'][rid]['query']):
            raise ValueError('Query or eligibility changed; review before resuming')
        tasks.extend({'discogs_id': rid, 'query': query} for query in entry['queries'])
    manifest = {'entries': tasks, 'fingerprint': fingerprint(tasks)}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    path = OUTPUT/'manifest.json'
    if path.exists() and json.loads(path.read_text()) != manifest:
        raise ValueError('Empty-search manifest changed; preserve the prior run')
    runner.save(path, manifest)
    return scope, rows, manifest


def export(scope, rows, manifest):
    saved = []
    for index, task in enumerate(manifest['entries']):
        record = json.loads((OUTPUT/f'search-{index:02d}.json').read_text())
        if record['task'] != task:
            raise ValueError('Saved query differs from the fixed plan')
        saved.append({'task': task, 'saved_at': record['saved_at'],
                      'albums': [album_fields(album) for album in record['search']['albums']['items']]})
    payload = {'schema_version': 1, 'scope_sha256': hashlib.sha256(SCOPE.read_bytes()).hexdigest(),
               'purpose': 'Search evidence only. A hit is not an accepted match. An empty query is not confirmed absence.',
               'results': saved}
    temporary = EVIDENCE.with_suffix('.tmp')
    temporary.write_bytes(gzip.compress(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode(), mtime=0))
    temporary.replace(EVIDENCE)
    snapshot = load_snapshot()
    summary = []
    for entry in scope['entries']:
        rid = entry['discogs_id']
        hits = {str(album['id']): album for result in saved if result['task']['discogs_id'] == rid for album in result['albums']}
        ranked = [{'album_id': aid, 'title': album['title'], 'cached_complete_metadata': aid in snapshot['albums'],
                   **relevance(rows[rid], snapshot['albums'].get(aid, album))} for aid, album in hits.items()]
        ranked.sort(key=lambda album: (-album['score'], album['album_id']))
        summary.append({'discogs_id': rid, 'title': entry['title'], 'unique_hits': len(hits), 'ranked_hits': ranked})
    result = {'schema_version': 1, 'entries': summary,
              'summary': {'releases': 20, 'queries': len(saved), 'nonempty_queries': sum(bool(item['albums']) for item in saved),
                          'releases_with_hits': sum(bool(item['unique_hits']) for item in summary),
                          'release_candidate_pairs': sum(item['unique_hits'] for item in summary)},
              'limitations': ['Search hits are not accepted matches.', 'Empty queries are not confirmed catalogue absence.',
                              'No album metadata was fetched and no match was published.']}
    runner.save(ROOT/'data/qobuz_empty_search_results.json', result)
    print(json.dumps(result['summary']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--search', action='store_true')
    parser.add_argument('--export', action='store_true')
    args = parser.parse_args()
    if args.search and args.export:
        parser.error('Choose only one mode')
    scope, rows, manifest = prepare()
    if args.search:
        runner.OUTPUT = OUTPUT
        if runner.search(manifest):
            return 1
        export(scope, rows, manifest)
    elif args.export:
        export(scope, rows, manifest)
    else:
        print(f'Prepared {len(scope["entries"])} releases / {len(manifest["entries"])} queries. No API calls.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
