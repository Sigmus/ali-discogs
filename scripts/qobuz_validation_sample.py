# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.32,<3"]
# ///
"""Fetch four bounded validation albums, reusing searches and metadata caches."""
import json
import time
from pathlib import Path
from qobuz_catalog import Catalog, CatalogError, DEFAULT_SOURCE, ROOT

PLAN = [(1855288, 'zccb3oe0za3sb'), (7001990, '3610154955247'),
        (8121703, 'ujhzfrl46gycc'), (5820114, 'v97lzb7cicexb')]


def main():
    output = ROOT / '.qobuz-poc/validation-small'
    output.mkdir(parents=True, exist_ok=True)
    stop = output / 'STOP'
    last = 0
    def pace():
        nonlocal last
        while time.monotonic() - last < 15:
            if stop.exists():
                raise CatalogError('Validation stopped; user direction required.')
            time.sleep(min(1, 15 - (time.monotonic() - last)))
        if stop.exists():
            raise CatalogError('Validation stopped; user direction required.')
        last = time.monotonic()
    catalog = Catalog(DEFAULT_SOURCE, before_request=pace)
    try:
        for release, album in PLAN:
            target = output / f'{release}.json'
            if target.exists():
                print(release, 'saved evidence reused', flush=True)
                continue
            metadata = catalog.fetch('album/get', album_id=album)
            tracks = metadata.get('tracks', {}).get('items')
            if not isinstance(tracks, list) or len(tracks) != metadata.get('tracks_count'):
                raise CatalogError('Incomplete album track metadata; validation paused.')
            temp = target.with_suffix('.tmp')
            temp.write_text(json.dumps({'discogs_id': release, 'album': metadata}, ensure_ascii=False, indent=2))
            temp.replace(target)
            print(release, album, len(tracks), 'tracks saved', flush=True)
        print('Complete: four validation albums saved. No matches accepted.', flush=True)
        return 0
    except CatalogError as exc:
        stop.touch()
        print('PAUSED:', exc, flush=True)
        return 1
    finally:
        catalog.close()


if __name__ == '__main__':
    raise SystemExit(main())
