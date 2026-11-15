"""Cache the fixed 160-release saved-hit scope, slowly; no searches or promotions."""
import argparse
import gzip
import hashlib
import json
from qobuz_match import ROOT
from qobuz_snapshot import album_fields, select, TRACK_FIELDS
import qobuz_comparison_pilot as runner

SCOPE = ROOT/'data/qobuz_uncached160_scope.json'
OUTPUT = ROOT/'.qobuz-poc/uncached160-2026-11-15'
ARCHIVE = ROOT/'data/qobuz_uncached160_metadata.json.gz'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    scope = json.loads(SCOPE.read_text())
    entries = scope['entries']
    releases = scope['release_ids']
    if (scope['schema_version'] != 1 or len(releases) != 160 or len(set(releases)) != 160
            or len(entries) != 936 or len({e['album_id'] for e in entries}) != 936
            or {r for e in entries for r in e['discogs_ids']} != set(releases)
            or any(not e['discogs_ids'] for e in entries)):
        raise ValueError('Frozen 160-release/936-album scope changed')
    if digest(ROOT/'data/collection_matches.json') != scope['collection_sha256']:
        raise ValueError('Collection changed; review frozen scope before retrieval')
    for name, expected in scope['search_source_hashes'].items():
        if digest(ROOT/name) != expected:
            raise ValueError('Saved search evidence changed')
    OUTPUT.mkdir(parents=True, exist_ok=True)
    tasks = [{'discogs_id': e['discogs_ids'][0], 'album_id': e['album_id']} for e in entries]
    manifest = {'entries': tasks, 'fingerprint': hashlib.sha256(json.dumps(tasks, sort_keys=True).encode()).hexdigest(),
                'scope_sha256': digest(SCOPE)}
    path = OUTPUT/'manifest.json'
    if path.exists() and json.loads(path.read_text()) != manifest:
        raise ValueError('Manifest changed; preserve checkpoints')
    if not path.exists() and digest(ROOT/'data/qobuz_unmatched_audit.json') != scope['inventory_sha256']:
        raise ValueError('Inventory changed before first preparation')
    runner.save(path, manifest)
    return manifest


def validate_record(record, task):
    album = record['album']
    tracks = album['tracks']['items']
    if (record['task'] != task or str(album['id']) != task['album_id']
            or len(tracks) != album['tracks_count']
            or len({t['id'] for t in tracks}) != len(tracks)):
        raise ValueError('Incomplete, duplicate or mismatched album metadata')
    return album


def export(manifest):
    metadata = []
    for i, task in enumerate(manifest['entries']):
        path = OUTPUT/f'metadata-{i:02d}.json'
        if not path.exists():
            continue
        record = json.loads(path.read_text())
        try:
            raw = validate_record(record, task)
        except Exception:
            (OUTPUT/'STOP').touch()
            raise
        album = album_fields(raw)
        tracks = []
        for track in raw['tracks']['items']:
            item = select(track, TRACK_FIELDS)
            for key in ['composer', 'performer']:
                if isinstance(track.get(key), dict):
                    item[key] = select(track[key], ['id', 'name'])
            tracks.append(item)
        album['tracks'] = {'items': tracks, 'total': len(tracks), 'offset': 0}
        metadata.append({'task': task, 'saved_at': record['saved_at'], 'album': album})
    payload = {'schema_version': 1, 'scope_sha256': digest(SCOPE), 'completed': len(metadata),
               'total': len(manifest['entries']), 'metadata': metadata}
    ARCHIVE.write_bytes(gzip.compress(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode(), mtime=0))
    print(f"Exported {len(metadata)}/{len(manifest['entries'])} validated metadata albums", flush=True)
    return payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true')
    parser.add_argument('--export', action='store_true')
    args = parser.parse_args()
    manifest = prepare()
    if args.export:
        export(manifest)
        return 0
    if not args.fetch:
        print('Prepared 160-release/936-album scope offline; --fetch starts authorized slow retrieval.')
        return 0
    # Validate every existing checkpoint before allowing any further HTTP request.
    for i, task in enumerate(manifest['entries']):
        path = OUTPUT/f'metadata-{i:02d}.json'
        if path.exists():
            try:
                validate_record(json.loads(path.read_text()), task)
            except Exception:
                (OUTPUT/'STOP').touch()
                raise
    runner.OUTPUT = OUTPUT
    result = runner.search(manifest, metadata=True)
    export(manifest)
    return result


if __name__ == '__main__':
    raise SystemExit(main())
