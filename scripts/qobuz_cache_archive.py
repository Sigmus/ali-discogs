"""Share/restore successful Qobuz request caches; excludes credentials and run state."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import re
import tarfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'data/qobuz_request_cache.tar.gz'
CACHE = ROOT / '.qobuz-poc/cache'


def validate(name, raw):
    if not re.fullmatch(r'[0-9a-f]{64}\.json', name):
        raise ValueError('Invalid cache member name')
    data = json.loads(raw)
    request = data['request']
    endpoint = request['endpoint']
    allowed = {'catalog/search': {'query', 'type', 'limit', 'offset'},
               'album/get': {'album_id', 'limit', 'offset'}}
    if endpoint not in allowed or set(request['params']) - allowed[endpoint]:
        raise ValueError('Unexpected request endpoint/parameters')
    key = hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest()
    if name != key + '.json' or not isinstance(data['response'], dict):
        raise ValueError('Invalid cache response/key')
    def check(value):
        if isinstance(value, dict):
            for k, v in value.items():
                if re.search(r'token|password|secret|email|session|authorization|user_id|account|file_url', k, re.I):
                    raise ValueError('Potentially sensitive cache field; review before export')
                check(v)
        elif isinstance(value, list):
            for v in value:
                check(v)
    check(data)
    return data


def export(cache=CACHE, archive=ARCHIVE):
    files = sorted(cache.glob('*.json'))
    if not files:
        raise ValueError('No request cache available')
    archive.parent.mkdir(parents=True, exist_ok=True)
    temp = archive.with_suffix('.tmp')
    with temp.open('wb') as output, gzip.GzipFile(fileobj=output, mode='wb', filename='', mtime=0) as zipped, tarfile.open(fileobj=zipped, mode='w|') as tar:
        for path in files:
            raw = path.read_bytes()
            validate(path.name, raw)
            info = tarfile.TarInfo(path.name)
            info.size = len(raw)
            info.mode = 0o600
            tar.addfile(info, io.BytesIO(raw))
    temp.replace(archive)
    print(f'Archived {len(files)} request responses ({archive.stat().st_size:,} bytes)')


def restore(archive=ARCHIVE, cache=CACHE):
    records = {}
    with tarfile.open(archive, 'r:gz') as tar:
        for member in tar:
            if not member.isfile() or member.name in records:
                raise ValueError('Unexpected/duplicate archive member')
            raw = tar.extractfile(member).read()
            validate(member.name, raw)
            path = cache / member.name
            if path.exists() and path.read_bytes() != raw:
                raise ValueError('Existing cache differs; preserve it and choose a new --cache directory')
            records[member.name] = raw
    cache.mkdir(parents=True, exist_ok=True)
    for name, raw in records.items():
        path = cache / name
        if not path.exists():
            temp = path.with_suffix('.tmp')
            temp.write_bytes(raw)
            temp.replace(path)
    print(f'Restored/reused {len(records)} cached responses')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['export', 'restore'])
    parser.add_argument('--archive', type=Path, default=ARCHIVE)
    parser.add_argument('--cache', type=Path, default=CACHE)
    args = parser.parse_args()
    if args.action == 'export':
        export(args.cache, args.archive)
    else:
        restore(args.archive, args.cache)
