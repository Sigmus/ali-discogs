# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.32,<3", "unidecode>=1.3", "rapidfuzz>=3.6"]
# ///
"""Paced album/get for two later title-aligned hits. No searches or acceptance."""
import argparse
import gzip
import hashlib
import json
from qobuz_match import ROOT
from qobuz_snapshot import album_fields, select, TRACK_FIELDS
import qobuz_comparison_pilot as runner

EXPECTED = [
    ('12329947', '0002894798675'),
    ('15980846', '4053166965917'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true')
    args = parser.parse_args()
    path = ROOT/'data/qobuz_empty_search_follow_scope.json'
    scope = json.loads(path.read_text())
    pairs = [(entry['discogs_id'], entry['album_id']) for entry in scope['entries']]
    if scope['schema_version'] != 1 or pairs != EXPECTED:
        raise ValueError('Follow-up metadata scope changed; review before retrieval')
    entries = [{'discogs_id': discogs_id, 'album_id': album_id} for discogs_id, album_id in pairs]
    manifest = {'entries': entries, 'fingerprint': hashlib.sha256(json.dumps(entries, sort_keys=True).encode()).hexdigest()}
    output = ROOT/'.qobuz-poc/empty-search-follow'
    output.mkdir(parents=True, exist_ok=True)
    saved = output/'manifest.json'
    if saved.exists() and json.loads(saved.read_text()) != manifest:
        raise ValueError('Manifest changed; preserve the prior run')
    runner.save(saved, manifest)
    if not args.fetch:
        print('Prepared two album/get calls. No API calls.')
        return 0
    if (output/'STOP').exists():
        raise ValueError('STOP file is present')
    runner.OUTPUT = output
    if runner.search(manifest, metadata=True):
        return 1
    metadata = []
    for index, task in enumerate(entries):
        raw = json.loads((output/f'metadata-{index:02d}.json').read_text())
        source = raw['album']
        tracks = source['tracks']['items']
        if raw['task'] != task or str(source['id']) != task['album_id'] or len(tracks) != source['tracks_count'] or len({track['id'] for track in tracks}) != len(tracks):
            (output/'STOP').touch()
            raise ValueError('Incomplete or mismatched metadata; paused')
        album = album_fields(source)
        items = []
        for track in tracks:
            item = select(track, TRACK_FIELDS)
            for key in ['composer', 'performer']:
                if isinstance(track.get(key), dict):
                    item[key] = select(track[key], ['id', 'name'])
            items.append(item)
        album['tracks'] = {'items': items, 'total': len(items), 'offset': 0}
        metadata.append({'task': task, 'saved_at': raw['saved_at'], 'album': album})
    payload = {'schema_version': 1, 'scope_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'metadata': metadata}
    (ROOT/'data/qobuz_empty_search_follow_metadata.json.gz').write_bytes(gzip.compress(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode(), mtime=0))
    print('Saved', sum(len(entry['album']['tracks']['items']) for entry in metadata), 'tracks. No match published.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
