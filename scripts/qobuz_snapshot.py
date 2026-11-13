"""Export portable catalogue evidence with an explicit field whitelist; no credentials."""
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SNAPSHOT = ROOT / 'data/qobuz_evidence.json.gz'
ALBUM_FIELDS = ['id', 'title', 'version', 'subtitle', 'release_date_original',
                'tracks_count', 'duration', 'media_count', 'upc', 'streamable',
                'release_type', 'recording_information']
TRACK_FIELDS = ['id', 'title', 'version', 'work', 'performers', 'duration',
                'isrc', 'track_number', 'media_number', 'streamable', 'release_date_original']


def select(source, keys):
    return {k: source[k] for k in keys if k in source}


def album_fields(album):
    result = select(album, ALBUM_FIELDS)
    for key in ['artist', 'label', 'composer', 'genre']:
        value = album.get(key)
        if isinstance(value, dict):
            result[key] = select(value, ['id', 'name'])
    result['artists'] = [select(a, ['id', 'name', 'roles']) for a in album.get('artists', [])]
    result['image'] = select(album.get('image') or {}, ['small', 'thumbnail', 'large'])
    return result


def load_snapshot(path=DEFAULT_SNAPSHOT):
    with gzip.open(path, 'rt', encoding='utf-8') as handle:
        data = json.load(handle)
    if data['schema_version'] != 1:
        raise ValueError('Unsupported evidence schema')
    for album_id, album in data['albums'].items():
        tracks = album['tracks']['items']
        if str(album['id']) != album_id or len(tracks) != album['tracks_count'] or len({t['id'] for t in tracks}) != len(tracks):
            raise ValueError('Incomplete snapshot album')
    return data


def export(source=ROOT / '.qobuz-poc', target=DEFAULT_SNAPSHOT):
    read = lambda path: json.loads(path.read_text())
    progress = read(source/'metadata/progress.json')
    if progress['status'] != 'complete':
        raise ValueError('Metadata retrieval must be complete')
    manifest = read(source/'all/manifest.json')
    meta_manifest = read(source/'metadata/manifest.json')
    searches = {}
    for entry in manifest['entries']:
        rid = str(entry['discogs_id'])
        raw = read(source/f'all/{rid}.json')
        searches[rid] = {**select(raw, ['discogs_id', 'title', 'query', 'copies', 'saved_at']),
                         'search': {'albums': {'items': [album_fields(a) for a in raw['search']['albums']['items']]}}}
    albums = {}
    for entry in meta_manifest['entries']:
        album_id = entry['album_id']
        raw = read(source/f'metadata/{album_id}.json')['album']
        album = album_fields(raw)
        tracks = []
        for track in raw['tracks']['items']:
            t = select(track, TRACK_FIELDS)
            for key in ['composer', 'performer']:
                if isinstance(track.get(key), dict):
                    t[key] = select(track[key], ['id', 'name'])
            tracks.append(t)
        album['tracks'] = {'items': tracks, 'total': len(tracks), 'offset': 0}
        albums[album_id] = album
    data = {'schema_version': 1, 'source_revision': '28c3521c3c96e62d7da7166d3edef1aed92a202f',
            'search_manifest': manifest, 'metadata_manifest': meta_manifest,
            'metadata_completed_at': progress['updated_at'], 'searches': searches, 'albums': albums}
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_suffix('.tmp')
    temp.write_bytes(gzip.compress(json.dumps(data, ensure_ascii=False, sort_keys=True,
                                             separators=(',', ':')).encode(), mtime=0))
    load_snapshot(temp)
    temp.replace(target)
    print(f'Exported {len(searches)} searches / {len(albums)} albums to {target.name} ({target.stat().st_size:,} bytes)')


if __name__ == '__main__':
    export()
