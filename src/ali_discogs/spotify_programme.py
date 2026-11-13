"""Bounded negative programme reviews, independent of album similarity scores.

No missing-title inference: only explicitly reviewed, hash-bound partial albums
are blocked. Other albums remain unverified by this guard.
"""
import gzip
import hashlib
import json
from pathlib import Path

from ali_discogs.paths import data_dir

TARGET_FIELDS = ('discogs_id', 'title', 'composers', 'performers', 'conductor',
                 'key_performers', 'ensembles', 'tracklist', 'labels')


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(',', ':')).encode()).hexdigest()


def target_fingerprint(item):
    return fingerprint({k: item.get(k) for k in TARGET_FIELDS})


def programme_review(item, album):
    """Return reviewed partial evidence, or None (not a completeness approval)."""
    directory = Path(data_dir())
    ledger = json.loads((directory/'spotify_programme_reviews.json').read_text())
    if ledger['schema_version'] != 1:
        raise ValueError('Unsupported Spotify programme review schema')
    entries = ledger['entries']
    keys = [(r['discogs_id'], r['album_id']) for r in entries]
    if len(keys) != len(set(keys)):
        raise ValueError('Duplicate Spotify programme review')
    matched = [r for r in entries if r['discogs_id'] == str(item['discogs_id']) and r['album_id'] == album['id']]
    if not matched:
        return None
    review = matched[0]
    if target_fingerprint(item) != review['target_sha256']:
        raise ValueError('Spotify target programme changed; re-review required')
    if album['name'] != review['album_name'] or album.get('total_tracks') != review['total_tracks']:
        raise ValueError('Spotify reviewed album metadata changed; re-review required')
    archive_path = directory/'spotify_pilot_tracks.json.gz'
    if hashlib.sha256(archive_path.read_bytes()).hexdigest() != ledger['track_archive_sha256']:
        raise ValueError('Spotify track archive changed; re-review required')
    archive = json.loads(gzip.decompress(archive_path.read_bytes()))
    if archive['schema_version'] != 1:
        raise ValueError('Unsupported Spotify track evidence schema')
    albums = [a for a in archive['albums'] if a['discogs_id'] == review['discogs_id'] and a['album_id'] == review['album_id']]
    if len(albums) != 1:
        raise ValueError('Missing or ambiguous reviewed Spotify track evidence')
    source = albums[0]
    if (fingerprint(source) != review['album_evidence_sha256'] or
            len(source['tracks']) != source['total_tracks'] or
            len({t['id'] for t in source['tracks']}) != len(source['tracks'])):
        raise ValueError('Incomplete or changed Spotify track evidence')
    if review['decision'] != 'confirmed_partial_programme':
        raise ValueError('Unsupported Spotify programme review decision')
    return {'status': 'confirmed_partial_programme', 'reviewed_on': ledger['reviewed_on'],
            'album_id': album['id'], 'reason': review['finding'],
            'missing_programme': review['missing_programme'],
            'review_sha256': hashlib.sha256((directory/'spotify_programme_reviews.json').read_bytes()).hexdigest(),
            'track_archive_sha256': ledger['track_archive_sha256'],
            'limitation': 'Only this reviewed album is known to be partial. Alternatives and recording identity remain unverified; no catalogue-absence claim.'}
