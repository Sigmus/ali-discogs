"""Bounded programme reviews, independent of album similarity scores.

No missing-title inference: only explicitly reviewed, hash-bound partial or mismatched albums
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
    archive_path = directory/review.get('track_archive', 'spotify_pilot_tracks.json.gz')
    expected_archive_hash = review.get('track_archive_sha256', ledger['track_archive_sha256'])
    if hashlib.sha256(archive_path.read_bytes()).hexdigest() != expected_archive_hash:
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
    if review['decision'] not in {'confirmed_partial_programme', 'confirmed_programme_mismatch'}:
        raise ValueError('Unsupported Spotify programme review decision')
    return {'status': review['decision'], 'reviewed_on': ledger['reviewed_on'],
            'album_id': album['id'], 'reason': review['finding'],
            'missing_programme': review['missing_programme'],
            'review_sha256': hashlib.sha256((directory/'spotify_programme_reviews.json').read_bytes()).hexdigest(),
            'track_archive_sha256': expected_archive_hash,
            'limitation': 'This album does not contain the requested programme. Other candidates still need a full programme and recording review.'}


def reviewed_replacement(item, scored):
    """A separate explicit positive review is needed to select a replacement."""
    from ali_discogs.text import norm
    directory = Path(data_dir())
    ledger_path = directory/'spotify_replacement_reviews.json'
    ledger = json.loads(ledger_path.read_text())
    if ledger['schema_version'] != 1:
        raise ValueError('Unsupported Spotify replacement review schema')
    reviews = [r for r in ledger['entries'] if r['discogs_id'] == str(item['discogs_id'])]
    if not reviews:
        return None
    if len(reviews) != 1:
        raise ValueError('Ambiguous reviewed Spotify replacement')
    review = reviews[0]
    matches = [(signals, a) for signals,a in scored if a['id'] == review['album_id']]
    if not matches:
        return None  # Never synthesize a candidate missing from the current search.
    signals, album = matches[0]
    if (target_fingerprint(item) != review['target_sha256'] or album['name'] != review['album_name']
            or album.get('total_tracks') != review['total_tracks']):
        raise ValueError('Spotify replacement inputs changed; re-review required')
    archive_path = directory/review['track_archive']
    if hashlib.sha256(archive_path.read_bytes()).hexdigest() != review['track_archive_sha256']:
        raise ValueError('Spotify replacement track archive changed')
    archive = json.loads(gzip.decompress(archive_path.read_bytes()))
    sources = [a for a in archive['albums'] if a['album_id'] == review['album_id'] and a['discogs_id'] == review['discogs_id']]
    if archive['schema_version'] != 1 or len(sources) != 1:
        raise ValueError('Missing Spotify replacement evidence')
    source = sources[0]
    if (fingerprint(source) != review['album_evidence_sha256'] or
            len(source['tracks']) != source['total_tracks'] or
            len({t['id'] for t in source['tracks']}) != source['total_tracks']):
        raise ValueError('Incomplete Spotify replacement metadata')
    by_id = {t['id']: t for t in source['tracks']}
    selected = [track_id for w in review['programme'] for track_id in w['track_ids']]
    if len(selected) != len(set(selected)) or not selected:
        raise ValueError('Overlapping or empty Spotify replacement programme')
    required = {norm(a) for a in review['required_artists']}
    if not {norm(a) for a in item['performers']} <= required:
        raise ValueError('Replacement review omits target performer')
    for track_id in selected:
        track = by_id.get(track_id)
        if not track or not required <= {norm(a['name']) for a in track['artists']}:
            raise ValueError('Missing Spotify replacement track or artist')
    return signals, album, {'status': 'reviewed_programme_supported', 'reviewed_on': ledger['reviewed_on'],
        'album_id': album['id'], 'reason': review['finding'], 'limitation': review['limitation'],
        'review_sha256': hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
        'track_archive_sha256': review['track_archive_sha256']}
