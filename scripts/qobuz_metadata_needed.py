# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.32,<3", "unidecode>=1.3", "rapidfuzz>=3.6"]
# ///
"""Paced album/get for seven fixed metadata-needed hits. No searches or acceptance."""
import argparse
import gzip
import hashlib
import json
from qobuz_match import ROOT
from qobuz_snapshot import album_fields, select, TRACK_FIELDS
import qobuz_comparison_pilot as runner


EXPECTED = [
    ('594243', '0060253742084'),
    ('4469662', '0002894667272'),
    ('6105272', 'g4nhgjv3d6wbc'),
    ('6465567', '0002894637012'),
    ('6907296', '0886446492919'),
    ('7975379', 'a6g9640whj71a'),
    ('9850479', '3614590915896'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch', action='store_true')
    args = parser.parse_args()
    path = ROOT/'data/qobuz_metadata_needed_scope.json'
    scope = json.loads(path.read_text())
    pairs = [(e['discogs_id'], e['album_id']) for e in scope['entries']]
    if scope['schema_version'] != 1 or pairs != EXPECTED:
        raise ValueError('Metadata-needed scope changed; review before retrieval')
    entries = [{'discogs_id': discogs_id, 'album_id': album_id} for discogs_id, album_id in pairs]
    manifest = {'entries': entries, 'fingerprint': hashlib.sha256(json.dumps(entries, sort_keys=True).encode()).hexdigest()}
    output = ROOT/'.qobuz-poc/metadata-needed'
    output.mkdir(parents=True, exist_ok=True)
    saved_manifest = output/'manifest.json'
    if saved_manifest.exists() and json.loads(saved_manifest.read_text()) != manifest:
        raise ValueError('Manifest changed; preserve prior run')
    runner.save(saved_manifest, manifest)
    if not args.fetch:
        print('Prepared seven-album manifest offline; --fetch explicitly retrieves metadata.')
        return 0
    runner.OUTPUT = output
    result = runner.search(manifest, metadata=True)
    if result:
        return result
    metadata = []
    for index, task in enumerate(entries):
        raw = json.loads((output/f'metadata-{index:02d}.json').read_text())
        source = raw['album']
        tracks = source['tracks']['items']
        if raw['task'] != task or str(source['id']) != task['album_id'] or len(tracks) != source['tracks_count'] or len({t['id'] for t in tracks}) != len(tracks):
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
    (ROOT/'data/qobuz_metadata_needed.json.gz').write_bytes(gzip.compress(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode(), mtime=0))
    print('Saved complete portable metadata:', sum(len(entry['album']['tracks']['items']) for entry in metadata), 'tracks')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
