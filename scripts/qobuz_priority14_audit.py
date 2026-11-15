"""Validate the frozen fourteen-release review batch entirely offline."""
import json
from collections import Counter
from qobuz_credit_role_audit import load_albums
from qobuz_lead_review import ROOT, assess, fingerprint, target_fingerprint


def validate(report, rows, albums, reviews):
    ids = report['frozen_release_ids']
    entries = report['entries']
    if len(ids) != 14 or len(set(ids)) != 14 or [e['discogs_id'] for e in entries] != ids:
        raise ValueError('Incomplete or changed fourteen-release batch')
    decisions = Counter()
    for entry in entries:
        rid = entry['discogs_id']
        row, review = rows[rid], reviews[rid]
        if (target_fingerprint(row) != entry['target_sha256']
                or review['target_sha256'] != entry['target_sha256']
                or review['source_sha256'] != entry['source_sha256']
                or review['album_id'] != entry['review_album_id']
                or review['album_sha256'] != entry['review_album_sha256']
                or review['decision'] != entry['outcome']):
            raise ValueError('Batch review or target changed: ' + rid)
        result, _ = assess(row, albums[review['album_id']], review)
        if result['eligible'] != (entry['outcome'] == 'probable'):
            raise ValueError('Batch eligibility changed: ' + rid)
        for candidate in entry['cached_search_candidates']:
            album = albums[candidate['album_id']]
            if (fingerprint(album) != candidate['album_sha256']
                    or album['tracks_count'] != candidate['metadata_tracks']):
                raise ValueError('Cached alternative changed: ' + rid)
        for group in entry['manual_programme_diagnostics']:
            tracks = {t['id']: t for t in albums[group['album_id']]['tracks']['items']}
            if group['track_ids'] != [t['id'] for t in group['tracks']]:
                raise ValueError('Diagnostic mapping changed: ' + rid)
            for track in group['tracks']:
                if fingerprint(tracks[track['id']]) != track['sha256']:
                    raise ValueError('Diagnostic track changed: ' + rid)
        decisions['withheld' if entry['outcome'] == 'withhold' else entry['outcome']] += 1
    accepted = [e['discogs_id'] for e in entries if e['outcome'] == 'probable']
    if (set(accepted) != set(report['accepted_release_ids'])
            or report['summary'] != {'reviewed': 14, **dict(decisions)}):
        raise ValueError('Batch outcome summary changed')
    return report['summary']


def main():
    report = json.loads((ROOT/'data/qobuz_priority14_batch_audit.json').read_text())
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
    print(json.dumps(validate(report, rows, load_albums(), reviews)))


if __name__ == '__main__':
    main()
