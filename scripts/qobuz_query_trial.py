"""Fixed ten-release query-strategy trial. Default is offline; --search is paced."""
import argparse
import gzip
import hashlib
import json
from qobuz_match import ROOT, catalogue, units, norm
from qobuz_query_plan import lead, composer_term, relevance
from qobuz_snapshot import load_snapshot, album_fields
import qobuz_comparison_pilot as runner
from ali_discogs.text import is_composer

SCOPE = ROOT/'data/qobuz_query_trial_scope.json'
OUTPUT = ROOT/'.qobuz-poc/query-trial'


def trial_lead(row):
    # Keep headline ensembles ahead of individual supporting musicians.
    headline = [a for a in row.get('artists', []) if not is_composer(a)]
    return (headline or [lead(row)])[0]


def strategies(row):
    person = norm(trial_lead(row))
    composers = list(dict.fromkeys(composer_term(c) for c in row.get('composers', []) if composer_term(c)))
    ids = sorted(set().union(*(catalogue(t) for t in units(row)))) if units(row) else []
    # Multi-composer programmes need a per-work composer mapping before this trial.
    if not person or len(composers) != 1 or not ids:
        return []
    base = ' '.join(dict.fromkeys([person, composers[0]]))
    kind, number, sub = ids[0]
    return [{'strategy': 'performer_composer', 'query': base},
            {'strategy': 'performer_composer_catalogue', 'query': ' '.join(filter(None, [base, kind, number, sub]))}]


def prepare():
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    snapshot = load_snapshot()
    excluded = set()
    for name in ['qobuz_comparison_scope.json', 'qobuz_round2_scope.json']:
        excluded.update(e['discogs_id'] for e in json.loads((ROOT/'data'/name).read_text())['entries'])
    publication = json.loads((ROOT/'data/qobuz_matches.json').read_text())['releases']
    source_hash = hashlib.sha256((ROOT/'data/collection_matches.json').read_bytes()).hexdigest()
    if not SCOPE.exists():
        pool = []
        for rid, row in sorted(rows.items(), key=lambda pair: int(pair[0])):
            qs = strategies(row)
            original = snapshot['searches'][rid]
            if rid not in excluded and publication[rid]['status'] == 'unchecked' and not original['search']['albums']['items'] and len(qs) == 2 and all(q['query'] != original['query'] for q in qs):
                pool.append({'discogs_id': rid, 'title': row['title'], 'queries': qs})
        entries = runner.spread(pool, 10)
        runner.save(SCOPE, {'schema_version': 1, 'collection_sha256': source_hash, 'selected_on': '2026-11-13', 'selection': 'Ten evenly spaced IDs with empty original searches, one normalized composer and catalogue identifiers; excludes both prior pilot scopes. Purposive, not representative. Catalogue choice is lexical, not necessarily the main work.', 'entries': entries})
    scope = json.loads(SCOPE.read_text())
    if scope['collection_sha256'] != source_hash or len(scope['entries']) != 10 or len({e['discogs_id'] for e in scope['entries']}) != 10:
        raise ValueError('Trial source/scope changed; review before resuming')
    tasks = []
    for entry in scope['entries']:
        rid = entry['discogs_id']
        if rid in excluded or entry['queries'] != strategies(rows[rid]) or snapshot['searches'][rid]['search']['albums']['items']:
            raise ValueError('Trial eligibility/query strategy changed')
        tasks.extend({'discogs_id': rid, 'query': q['query']} for q in entry['queries'])
    manifest = {'entries': tasks, 'fingerprint': hashlib.sha256(json.dumps(tasks, sort_keys=True).encode()).hexdigest()}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    path = OUTPUT/'manifest.json'
    if path.exists() and json.loads(path.read_text()) != manifest:
        raise ValueError('Manifest changed; do not overwrite a prior run')
    runner.save(path, manifest)
    return scope, rows, snapshot, manifest


def export(scope, rows, snapshot, manifest):
    records = []
    for i, task in enumerate(manifest['entries']):
        raw = json.loads((OUTPUT/f'search-{i:02d}.json').read_text())
        if raw['task'] != task:
            raise ValueError('Saved query mismatch')
        records.append({'task': task, 'saved_at': raw['saved_at'], 'albums': [album_fields(a) for a in raw['search']['albums']['items']]})
    # Include portable full metadata from prior pilots, not only the first snapshot.
    albums = dict(snapshot['albums'])
    for name in ['qobuz_comparison_evidence.json.gz', 'qobuz_round2_metadata.json.gz', 'qobuz_query_trial_metadata.json.gz']:
        archive = ROOT/'data'/name
        if archive.exists():
            for item in json.loads(gzip.decompress(archive.read_bytes()))['metadata']:
                album = item['album']; aid = str(album['id']); tracks = album['tracks']['items']
                if aid != item['task']['album_id'] or len(tracks) != album['tracks_count'] or len({t['id'] for t in tracks}) != len(tracks):
                    raise ValueError('Incomplete portable metadata')
                if aid in albums and albums[aid] != album:
                    raise ValueError('Conflicting portable metadata')
                albums[aid] = album
    scope_hash = hashlib.sha256(SCOPE.read_bytes()).hexdigest()
    payload = {'schema_version': 1, 'scope_sha256': scope_hash, 'results': records}
    (ROOT/'data/qobuz_query_trial_searches.json.gz').write_bytes(gzip.compress(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode(), mtime=0))
    entries = []
    for i, entry in enumerate(scope['entries']):
        queries = []
        for j, strategy in enumerate(entry['queries']):
            hits = records[2*i+j]['albums']
            row = rows[entry['discogs_id']]
            ranking_row = {**row, 'artists': [], 'key_performers': [trial_lead(row)]}
            queries.append({**strategy, 'hits': len(hits), 'candidates': [{'album_id': str(a['id']), 'title': a['title'], 'cached_complete_metadata': str(a['id']) in albums, **relevance(ranking_row, albums.get(str(a['id']), a))} for a in hits]})
        entries.append({'discogs_id': entry['discogs_id'], 'title': entry['title'], 'queries': queries})
    summary = {s: {'nonempty': sum(bool(e['queries'][j]['hits']) for e in entries), 'candidate_entries': sum(e['queries'][j]['hits'] for e in entries)} for j, s in enumerate(['performer_composer', 'performer_composer_catalogue'])}
    report = {'schema_version': 1, 'scope_sha256': scope_hash, 'entries': entries, 'summary': summary, 'limitations': ['Top five hits only; relevance is not match confidence.', 'No new full metadata fetched or matches accepted.', 'Query yield is not recording coverage; no catalogue absence inference.', scope['selection']]}
    runner.save(ROOT/'data/qobuz_query_trial_results.json', report)
    print(json.dumps(summary))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--search', action='store_true')
    modes.add_argument('--export', action='store_true')
    args = parser.parse_args()
    scope, rows, snapshot, manifest = prepare()
    if args.search:
        runner.OUTPUT = OUTPUT
        result = runner.search(manifest)
        if result:
            return result
        export(scope, rows, snapshot, manifest)
    elif args.export:
        export(scope, rows, snapshot, manifest)
    else:
        print('Prepared ten releases / twenty queries, offline; no API calls.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
