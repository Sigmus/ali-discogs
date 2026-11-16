"""Reproduce all16recording decisions from their frozen source and cached evidence."""
import json
from collections import Counter
from qobuz_lead_review import ROOT, assess, target_fingerprint, fingerprint, apply_recording_review
from qobuz_credit_role_audit import load_albums


def validate(report, rows, albums, reviews, expected_count=16):
    ids = report['frozen_release_ids']
    if len(ids) != expected_count or len(set(ids)) != expected_count or ids != [e['discogs_id'] for e in report['entries']]:
        raise ValueError('The complete16release scope changed')
    counts = Counter()
    for entry in report['entries']:
        rid = entry['discogs_id']
        r = reviews[rid]
        if (entry['outcome'] != r['decision'] or entry['target_sha256'] != target_fingerprint(rows[rid])
                or entry['source_sha256'] != r['source_sha256']
                or entry['review_album_id'] != r['album_id']
                or entry['review_album_sha256'] != r['album_sha256']):
            raise ValueError('Frozen source or recording decision changed')
        album = albums[r['album_id']]
        result, _ = assess(rows[rid], album, r)
        if result['eligible'] != (entry['outcome'] == 'probable'):
            raise ValueError('Recording eligibility changed')
        if {str(t['id']): fingerprint(t) for t in album['tracks']['items']} != entry['selected_track_fingerprints']:
            raise ValueError('Selected recording tracks changed')
        for alternative in entry['cached_alternative_checks']:
            a = albums[alternative['album_id']]
            if (fingerprint(a) != alternative['album_sha256']
                    or fingerprint(a['tracks']['items']) != alternative['track_manifest_sha256']
                    or len(a['tracks']['items']) != alternative['tracks_count']):
                raise ValueError('Inspected alternative changed')
        if r['decision'] == 'withhold':
            future = apply_recording_review(rows[rid], album, r, [{'id': r['album_id'], 'status': 'found', 'confidence': .99}])
            if future[0]['status'] != 'unchecked':
                raise ValueError('Future high score bypassed a saved hold')
        counts[r['decision']] += 1
    if report['summary'] != {'reviewed': expected_count, **dict(counts)}:
        raise ValueError('Frozen16summary changed')
    return report['summary']


def main():
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
    report = json.loads((ROOT/'data/qobuz_fullsupport16_recording_audit.json').read_text())
    print(json.dumps(validate(report, rows, load_albums(), reviews)))


if __name__ == '__main__':
    main()
