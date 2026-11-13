"""Offline screening of query-trial hits; never fetches or publishes matches."""
import gzip
import hashlib
import json
from qobuz_match import ROOT, evaluate
from qobuz_snapshot import load_snapshot
from qobuz_completeness import check_programme

SELECTED = [
    ('1132104', '0002894631652', 'Headline Prague String Quartet and broad quartet collection; verify both No.8 and No.10 plus source players/recording.'),
    ('14934969', '5099992803350', 'Exact advertised Symphony6/Leonore1 programme with Klemperer; compare Philharmonia credits and source recording family.'),
]


def screen():
    evidence_path = ROOT/'data/qobuz_query_trial_searches.json.gz'
    scope_path = ROOT/'data/qobuz_query_trial_scope.json'
    evidence = json.loads(gzip.decompress(evidence_path.read_bytes()))
    if evidence['scope_sha256'] != hashlib.sha256(scope_path.read_bytes()).hexdigest():
        raise ValueError('Query evidence scope changed')
    scope = json.loads(scope_path.read_text())
    if scope['collection_sha256'] != hashlib.sha256((ROOT/'data/collection_matches.json').read_bytes()).hexdigest():
        raise ValueError('Target collection changed')
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    albums = dict(load_snapshot()['albums'])
    for name in ['qobuz_comparison_evidence.json.gz', 'qobuz_round2_metadata.json.gz']:
        for item in json.loads(gzip.decompress((ROOT/'data'/name).read_bytes()))['metadata']:
            album = item['album']; aid = str(album['id']); tracks = album['tracks']['items']
            if aid != item['task']['album_id'] or len(tracks) != album['tracks_count'] or len({t['id'] for t in tracks}) != len(tracks):
                raise ValueError('Incomplete additional evidence')
            if aid in albums and albums[aid] != album:
                raise ValueError('Conflicting cached album; review before screening')
            albums[aid] = album
    inventory = json.loads((ROOT/'data/qobuz_work_inventory.json').read_text())
    entries = []
    for target in scope['entries']:
        rid = target['discogs_id']; hits = {}
        for record in evidence['results']:
            if record['task']['discogs_id'] == rid:
                for album in record['albums']:
                    aid = str(album['id'])
                    hits.setdefault(aid, {'album': album, 'queries': []})['queries'].append(record['task']['query'])
        for aid, hit in hits.items():
            item = {'discogs_id': rid, 'target_title': target['title'], 'album_id': aid, 'candidate_title': hit['album']['title'], 'candidate_artist': (hit['album'].get('artist') or {}).get('name'), 'queries': hit['queries']}
            if aid in albums:
                album = albums[aid]; assessment = evaluate(rows[rid], album)
                completeness = check_programme(rows[rid], album, assessment, inventory)
                item.update(cached_complete_metadata=True, assessment=assessment, completeness=completeness,
                            finding='needs_recording_review' if assessment['status'] != 'unchecked' and completeness['status'] == 'complete' else 'unresolved_work_credit_or_completeness')
            else:
                item.update(cached_complete_metadata=False, finding='metadata_not_available')
            entries.append(item)
    lookup = {(e['discogs_id'], e['album_id']): e for e in entries}
    selected = []
    for rid, aid, reason in SELECTED:
        item = lookup[(rid, aid)]
        if item['cached_complete_metadata']:
            raise ValueError('Selected metadata already available; review scope')
        selected.append({'discogs_id': rid, 'album_id': aid, 'reason': reason})
    report = {'schema_version': 1, 'reviewed_on': '2026-11-13', 'evidence_sha256': hashlib.sha256(evidence_path.read_bytes()).hexdigest(),
              'summary': {'release_candidate_pairs': len(entries), 'cached_metadata_pairs': sum(e['cached_complete_metadata'] for e in entries), 'uncached_pairs': sum(not e['cached_complete_metadata'] for e in entries), 'complete_work_credit_leads': sum(e['finding'] == 'needs_recording_review' for e in entries), 'selected_uncached_leads': len(selected)},
              'entries': entries, 'limitations': ['Offline screen only; no new metadata calls or publication changes.', 'Parser/credit/completeness failures are unresolved, not confirmed wrong recordings or catalogue absence.', 'Relevance scores do not validate recording identity; current trial reporting uses the queried headline artist.', 'Selected leads need full movement/credit and recording-family review before acceptance.']}
    save = lambda path, obj: path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')
    save(ROOT/'data/qobuz_query_trial_screen.json', report)
    save(ROOT/'data/qobuz_query_trial_metadata_scope.json', {'schema_version': 1, 'status': 'proposed_not_fetched', 'search_evidence_sha256': report['evidence_sha256'], 'entries': selected, 'policy': 'Two fixed leads only; no automatic fetching, promotion or scope expansion.'})
    print(json.dumps(report['summary']))
    return report


if __name__ == '__main__':
    screen()
