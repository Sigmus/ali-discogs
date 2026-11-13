"""Offline, hash-bound review of four pilot leads; never performs catalogue calls."""
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT/'data/qobuz_lead_reviews.json'
ARCHIVE = ROOT/'data/qobuz_comparison_evidence.json.gz'
TARGET_FIELDS = ('discogs_id', 'title', 'composers', 'performers', 'conductor',
                 'key_performers', 'ensembles', 'tracklist', 'labels', 'year', 'released')


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def target_fingerprint(row):
    return fingerprint({k: row.get(k) for k in TARGET_FIELDS})


def load_reviews():
    review = json.loads(REVIEW.read_text())
    archive = json.loads(gzip.decompress(ARCHIVE.read_bytes()))
    if review['schema_version'] != 1 or archive['schema_version'] != 1:
        raise ValueError('Unsupported lead review schema')
    entries = review['releases']
    if len({r['discogs_id'] for r in entries}) != len(entries):
        raise ValueError('Duplicate reviewed target')
    albums = {}
    for item in archive['metadata']:
        album = item['album']
        aid = str(album['id'])
        tracks = album['tracks']['items']
        if (aid != str(item['task']['album_id']) or len(tracks) != album['tracks_count']
                or len({t['id'] for t in tracks}) != len(tracks) or aid in albums):
            raise ValueError('Incomplete or duplicate comparison metadata')
        albums[aid] = album
    return entries, albums


def assess(row, album, review):
    from qobuz_match import evaluate
    from qobuz_completeness import movement_number
    if (str(row['discogs_id']) != review['discogs_id'] or
            str(album['id']) != review['album_id'] or
            target_fingerprint(row) != review['target_sha256'] or
            fingerprint(album) != review['album_sha256']):
        raise ValueError('Reviewed evidence changed; review again before publication')
    if review.get('review_kind') == 'source-role-ensemble':
        from qobuz_opera_review import assess_opera
        return assess_opera(row, album, review)
    if review.get('review_kind') == 'prelude-fugue-pairs':
        from qobuz_pair_review import assess_pairs
        return assess_pairs(row, album, review)
    if review.get('review_kind') == 'container-headings':
        from qobuz_container_review import assess_containers
        return assess_containers(row, album, review)
    if review.get('review_kind') == 'bound-tracks':
        from qobuz_binding_review import assess_bindings
        return assess_bindings(row, album, review)
    if review.get('review_kind') == 'heading-over-groups':
        from qobuz_heading_review import assess_headings
        return assess_headings(row, album, review)
    if review.get('review_kind') == 'covered-labels':
        from qobuz_cached_review import assess_labels
        return assess_labels(row, album, review)
    if review.get('review_kind') == 'opus-pieces':
        from qobuz_cached_review import assess_opus_pieces
        return assess_opus_pieces(row, album, review)
    if review.get('review_kind') == 'side-ranges':
        from qobuz_side_range_review import assess_ranges
        return assess_ranges(row, album, review)
    corrections = review.get('target_title_corrections', {})
    groups = review.get('target_unit_groups', [])
    if groups:
        from copy import deepcopy
        from qobuz_match import units
        titles = units(row)
        flattened = [title for group in groups for title in group['source_titles']]
        if corrections or flattened != titles or len(set(flattened)) != len(flattened) or any(not group['source_titles'] or not group['canonical_title'] for group in groups) or len({g['canonical_title'] for g in groups}) != len(groups):
            raise ValueError('Ambiguous or incomplete reviewed target grouping')
        effective = deepcopy(row)
        effective['tracklist'] = [{'title': g['canonical_title'], 'type': 'index'} for g in groups]
        effective['_reviewed_title_sources'] = {g['canonical_title']: g['source_titles'][0] for g in groups}
        evidence = evaluate(effective, album)
        for item in evidence['programme']:
            item['target'] = effective['_reviewed_title_sources'].get(item['target'], item['target'])
    elif corrections:
        from copy import deepcopy
        from qobuz_match import units
        titles = units(row)
        if (any(titles.count(t) != 1 for t in corrections) or
                any(not isinstance(t, str) or not t for t in corrections.values()) or
                len(set(corrections.values())) != len(corrections)):
            raise ValueError('Ambiguous reviewed target title correction')
        effective = deepcopy(row)
        for track in effective['tracklist']:
            track['title'] = corrections.get(track.get('title'), track.get('title'))
        effective['_reviewed_title_sources'] = {v:k for k,v in corrections.items()}
        evidence = evaluate(effective, album)
        for item in evidence['programme']:
            item['target'] = effective['_reviewed_title_sources'].get(item['target'], item['target'])
    else:
        evidence = evaluate(row, album)
    result = {'discogs_id': review['discogs_id'], 'album_id': review['album_id'],
              'decision': review['decision'], 'recording_review': review['recording_review'],
              'sources': review['sources'], 'limitations': review['limitations'],
              'eligible': False, 'completeness': {'status': 'unknown', 'works': []}}
    if review['decision'] != 'probable':
        return result, evidence
    expected = review['works']
    if [w['target'] for w in expected] != [w['target'] for w in evidence['programme']]:
        raise ValueError('Reviewed programme changed')
    seen = set()
    works = []
    for spec, item in zip(expected, evidence['programme']):
        ids = set(item['track_ids'])
        tracks = [t for t in album['tracks']['items'] if t['id'] in ids]
        numbers = []
        for track in tracks:
            joined = (spec.get('reviewed_sections', {}).get(str(track['id'])) or
                      spec.get('joined_tracks', {}).get(str(track['id'])))
            if joined:
                # Only an exact reviewed track may supply a named section or join.
                if fingerprint(track) != joined['track_sha256']:
                    raise ValueError('Reviewed joined track changed')
                numbers.extend(joined['movements'])
            else:
                numbers.append(movement_number(track['title']))
        complete = (numbers == spec['movements'] and bool(ids) and
                    len(tracks) == len(ids) and not seen.intersection(ids) and
                    item['credited_tracks'] == item['work_tracks'])
        if spec['scope'] == 'listed-target-excerpt':
            # The target is the Adagio alone, never a complete Tenth Symphony.
            complete = complete and len(tracks) == 1 and 'adagio' in tracks[0]['title'].lower()
        seen.update(ids)
        works.append({'target': spec['target'], 'status': 'complete' if complete else 'unknown',
                      'expected_movements': spec['movements'], 'observed_movements': numbers,
                      'track_ids': [t['id'] for t in tracks], 'scope': spec['scope'],
                      'source': spec['source'], 'reason': spec['reason']})
    complete = bool(works) and all(w['status'] == 'complete' for w in works)
    result['completeness'] = {'status': 'complete' if complete else 'unknown',
                              'works': works, 'overlapping_target_tracks': len(seen) != sum(len(w['track_ids']) for w in works)}
    result['eligible'] = complete and evidence['status'] != 'unchecked'
    return result, evidence


def reviewed_candidate(row, album, review):
    from qobuz_match import public_album
    result, evidence = assess(row, album, review)
    if not result['eligible']:
        return None
    evidence.update(status='probable', confidence=.85)
    evidence['reasons'] = [*evidence['reasons'], review['recording_review'],
        'Bounded reviewed programme is complete; 85% is a heuristic Probable level, not exact-edition verification.',
        *review['limitations']]
    return {**public_album(album), **evidence, 'discovery': 'reviewed-pilot-lead',
            'completeness': result['completeness'], 'recording_review': result['recording_review'],
            'review_sources': result['sources']}


def report():
    reviews, albums = load_reviews()
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    results = [assess(rows[r['discogs_id']], albums[r['album_id']], r)[0] for r in reviews]
    output = {'schema_version': 1, 'reviewed_on': '2026-11-13',
              'review_sha256': hashlib.sha256(REVIEW.read_bytes()).hexdigest(),
              'archive_sha256': hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
              'releases': results,
              'summary': {'reviewed': len(results), 'eligible_probable': sum(r['eligible'] for r in results),
                          'rejected_recording': sum(r['decision'] == 'reject-recording' for r in results)}}
    (ROOT/'data/qobuz_lead_audit.json').write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(output['summary']))


if __name__ == '__main__':
    report()
