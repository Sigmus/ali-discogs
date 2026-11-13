"""Preserve Qobuz canonical public URLs from shared caches, entirely offline."""
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
import tarfile
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT/'data/qobuz_album_urls.json'
ARCHIVE = ROOT/'data/qobuz_request_cache.tar.gz'


def valid_album_url(value, album_id):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9]+', str(album_id)):
        return False
    try:
        parsed = urlsplit(value)
        return (parsed.scheme == 'https' and parsed.netloc == 'www.qobuz.com'
                and not parsed.query and not parsed.fragment
                and re.fullmatch(r'/[a-z]{2}-[a-z]{2}/album/[^/?#]+/' + re.escape(str(album_id)), parsed.path) is not None)
    except ValueError:
        return False


@lru_cache(maxsize=1)
def load_urls():
    data = json.loads(INDEX.read_text())
    if data['schema_version'] != 1 or not all(valid_album_url(url, aid) for aid,url in data['albums'].items()):
        raise ValueError('Invalid canonical Qobuz URL index')
    return data['albums']


def album_url(album, urls=None):
    aid = str(album.get('id', ''))
    # Preserve the provider's exact public route; never synthesize a bare /album/ID.
    if valid_album_url(album.get('url'), aid):
        return album['url']
    url = (load_urls() if urls is None else urls).get(aid)
    if valid_album_url(url, aid):
        return url
    # Missing URL evidence must remain navigable without inventing a slug.
    query = ' '.join(filter(None, [album.get('title', ''), (album.get('artist') or {}).get('name', '')]))
    return 'https://www.qobuz.com/nl-en/search?q=' + quote(query or aid, safe='')


def export(archive=ARCHIVE, target=INDEX):
    from qobuz_cache_archive import validate
    albums = {}
    with tarfile.open(archive, 'r:gz') as tar:
        for member in tar:
            if not member.isfile():
                raise ValueError('Unexpected URL archive member')
            data = validate(member.name, tar.extractfile(member).read())
            request = data['request']
            if request['endpoint'] != 'album/get' or request['params'].get('offset', 0) != 0:
                continue
            album = data['response']
            aid, url = str(album['id']), album.get('url')
            if str(request['params']['album_id']) != aid or not valid_album_url(url, aid):
                raise ValueError('Missing or invalid cached canonical Qobuz album URL')
            if aid in albums and albums[aid] != url:
                raise ValueError('Conflicting cached canonical album URL')
            albums[aid] = url
    if not albums:
        raise ValueError('No cached canonical URLs found')
    payload = {'schema_version': 1, 'source': 'Canonical album URLs from successful cached album/get metadata; no API calls.',
               'request_archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
               'albums': dict(sorted(albums.items()))}
    temp = target.with_suffix('.tmp')
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
    temp.replace(target)
    print(f'Exported {len(albums)} canonical Qobuz album URLs offline')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, default=ARCHIVE)
    parser.add_argument('--output', type=Path, default=INDEX)
    args = parser.parse_args()
    export(args.archive, args.output)
