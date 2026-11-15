"""Validate all twenty-three saved recording decisions from complete shared caches."""
import json
from collections import Counter
from qobuz_credit_role_audit import load_albums
from qobuz_lead_review import ROOT, assess, fingerprint, target_fingerprint, apply_recording_review


def validate(report, rows, albums, reviews):
    ids = report['frozen_release_ids']
    if len(ids) != 23 or len(set(ids)) != 23 or ids != [e['discogs_id'] for e in report['entries']]:
        raise ValueError('The complete frozen23review scope changed')
    counts = Counter()
    accepted = []
    for entry in report['entries']:
        rid = entry['discogs_id']
        review, row = reviews[rid], rows[rid]
        if (entry['target_sha256'] != target_fingerprint(row)
                or entry['source_sha256'] != review['source_sha256']
                or entry['review_album_id'] != review['album_id']
                or entry['review_album_sha256'] != review['album_sha256']
                or entry['outcome'] != review['decision']):
            raise ValueError('Frozen23target or recording decision changed: ' + rid)
        result, _ = assess(row, albums[review['album_id']], review)
        if result['eligible'] != (entry['outcome'] == 'probable'):
            raise ValueError('Frozen23recording eligibility changed: ' + rid)
        if result['eligible']:
            accepted.append(rid)
        else:
            held = apply_recording_review(row, albums[review['album_id']], review,
                [{'id': review['album_id'], 'status': 'found', 'confidence': .99}])
            if held[0]['status'] != 'unchecked':
                raise ValueError('A future score bypassed a recording decision')
        for candidate in entry['cached_alternative_checks']:
            album = albums[candidate['album_id']]
            if (fingerprint(album) != candidate['album_sha256']
                    or len(album['tracks']['items']) != candidate['tracks_count']
                    or fingerprint(album['tracks']['items']) != candidate['track_manifest_sha256']):
                raise ValueError('A reviewed cached alternative changed: ' + rid)
        counts[{'withhold': 'withheld', 'reject-recording': 'rejected_recording'}.get(entry['outcome'], entry['outcome'])] += 1
    if report['summary'] != {'reviewed': 23, **dict(counts)} or set(accepted) != set(report['accepted_release_ids']):
        raise ValueError('Frozen23summary changed')
    return report['summary']


def main():
    report = json.loads((ROOT/'data/qobuz_secondary23_recording_audit.json').read_text())
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
    print(json.dumps(validate(report, rows, load_albums(), reviews)))


if __name__ == '__main__':
    main()
