"""Rank the remaining-retrieval evidence offline; never fetch or publish matches."""
import gzip
import hashlib
import json
from collections import Counter
from qobuz_match import ROOT, evaluate, norm
from qobuz_completeness import check_programme
from qobuz_query_trial import trial_lead
from rapidfuzz import fuzz


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_album(album):
    tracks = album.get('tracks', {}).get('items', [])
    if not tracks or len(tracks) != album.get('tracks_count') or len({t['id'] for t in tracks}) != len(tracks):
        raise ValueError('Incomplete/duplicate album metadata: ' + str(album.get('id')))
    return album


def screen():
    scope_path = ROOT/'data/qobuz_remaining_scope.json'
    scope = json.loads(scope_path.read_text())
    collection = ROOT/'data/collection_matches.json'
    if scope['collection_sha256'] != fingerprint(collection):
        raise ValueError('Collection changed; review frozen scope')
    rows = {str(r['discogs_id']): r for r in json.loads(collection.read_text())}
    albums, provenance = {}, {}
    for path in sorted((ROOT/'data').glob('qobuz*.json.gz')):
        data = json.loads(gzip.decompress(path.read_bytes()))
        if not isinstance(data, dict):
            continue
        candidates = list(data.get('albums', {}).values()) if isinstance(data.get('albums'), dict) else []
        candidates += [x['album'] for x in data.get('metadata', [])]
        for album in candidates:
            if not isinstance(album, dict) or 'tracks' not in album:
                continue
            validate_album(album)
            aid = str(album['id'])
            if aid in albums and albums[aid] != album:
                raise ValueError('Conflicting album evidence: ' + aid)
            albums[aid] = album
        if candidates:
            provenance[path.name] = fingerprint(path)
    pairs = {}
    def add(rid, album, query):
        rid, aid = str(rid), str(album['id'])
        entry = pairs.setdefault((rid, aid), {'discogs_id': rid, 'album_id': aid,
            'candidate_title': album['title'], 'candidate_artist': (album.get('artist') or {}).get('name', ''), 'queries': []})
        if query and query not in entry['queries']:
            entry['queries'].append(query)
    for phase in ['metadata', 'search']:
        path = ROOT/f'data/qobuz_remaining_{phase}.json.gz'
        data = json.loads(gzip.decompress(path.read_bytes()))
        if data['scope_sha256'] != fingerprint(scope_path) or data['completed'] != data['total'] or data['total'] != len(scope[phase]):
            raise ValueError('Incomplete remaining export')
        records = data['metadata' if phase == 'metadata' else 'results']
        expected = [{k:v for k,v in t.items() if k != 'title'} for t in scope[phase]]
        if [x['task'] for x in records] != expected:
            raise ValueError('Export tasks differ from scope')
        for record in records:
            for album in ([record['album']] if phase == 'metadata' else record['albums']):
                add(record['task']['discogs_id'], album, record['task'].get('query'))
        provenance[path.name] = fingerprint(path)
    # A deduplicated album may have been requested for several metadata-needed releases.
    mids = set(scope['metadata_release_ids'])
    for path in sorted((ROOT/'data').glob('qobuz*.json.gz')):
        data = json.loads(gzip.decompress(path.read_bytes()))
        if not isinstance(data, dict): continue
        records = list(data.get('results', [])) if isinstance(data.get('results', []), list) else []
        searches = data.get('searches', [])
        if isinstance(searches, dict):
            records += [{'task': {'discogs_id': rid, 'query': x.get('query')}, 'albums': x['search']['albums']['items']} for rid,x in searches.items()]
        else:
            records += [{'task': x['task'], 'albums': x['search']['albums']['items']} for x in searches]
        for x in records:
            if not isinstance(x, dict) or 'task' not in x or 'albums' not in x: continue
            if str(x['task']['discogs_id']) in mids:
                provenance[path.name] = fingerprint(path)
                for album in x['albums']: add(x['task']['discogs_id'], album, x['task'].get('query'))
    provenance['qobuz_source_programme_reviews.json'] = fingerprint(ROOT/'data/qobuz_source_programme_reviews.json')
    provenance['qobuz_source_composer_reviews.json'] = fingerprint(ROOT/'data/qobuz_source_composer_reviews.json')
    inventory = json.loads((ROOT/'data/qobuz_work_inventory.json').read_text())
    provenance['qobuz_work_inventory.json'] = fingerprint(ROOT/'data/qobuz_work_inventory.json')
    for name in ['qobuz_match.py','qobuz_completeness.py','qobuz_work_groups.py','qobuz_source_composer.py','qobuz_source_programme.py','qobuz_composer_identity.py']:
        provenance['scripts/' + name] = fingerprint(ROOT/'scripts'/name)
    entries = []
    for (rid, aid), entry in pairs.items():
        row = rows[rid]
        lead = norm(trial_lead(row))
        credit_text = norm(entry['candidate_artist'] + ' ' + entry['candidate_title'])
        entry['title_relevance'] = round(fuzz.token_set_ratio(norm(row['title']), norm(entry['candidate_title'])), 1)
        entry['lead_relevance'] = round(fuzz.token_set_ratio(lead, credit_text), 1) if lead else 0
        entry['discovery_rank'] = round(.55*entry['title_relevance'] + .45*entry['lead_relevance'], 1)
        entry['cached_complete_metadata'] = aid in albums
        if aid in albums:
            evidence = evaluate(row, albums[aid])
            completeness = check_programme(row, albums[aid], evidence, inventory)
            entry['assessment'] = evidence
            entry['completeness'] = completeness
            entry['finding'] = 'needs_recording_review' if evidence['status'] != 'unchecked' and completeness['status'] == 'complete' else 'unresolved_work_credit_or_completeness'
        else:
            entry['finding'] = 'metadata_needed'
        from qobuz_source_programme import programme_hold
        source_hold=programme_hold(row)
        if source_hold:
            entry['source_programme_review']=source_hold
            entry['finding']='source_programme_review_needed'
        entries.append(entry)
    entries.sort(key=lambda x: (x['finding'] != 'needs_recording_review', -x['discovery_rank'], int(x['discogs_id']), x['album_id']))
    report = {'schema_version': 1, 'reviewed_on': '2026-11-15', 'scope_sha256': fingerprint(scope_path),
        'evidence_sha256': provenance, 'summary': dict(Counter(e['finding'] for e in entries)),
        'release_candidate_pairs': len(entries), 'entries': entries,
        'policy': 'Offline triage only, no publication. Discovery rank is title/headline-artist similarity, not match confidence. Missing work/credit support is unresolved, not absence. Full recording review remains required.'}
    (ROOT/'data/qobuz_remaining_screen.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'pairs':len(entries), **report['summary']}))
    for e in entries[:12]: print(e['discogs_id'], e['album_id'], e['finding'], e['discovery_rank'], e['candidate_title'])
    return report

if __name__ == '__main__':
    screen()
