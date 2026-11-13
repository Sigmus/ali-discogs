# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.32,<3", "unidecode>=1.3", "rapidfuzz>=3.6"]
# ///
"""Slow resumable metadata retrieval for distinct saved Qobuz candidates."""
import fcntl
import hashlib
import json
import os
import signal
import time
from pathlib import Path

from qobuz_all_poc import Pace, StopRequested, now, save
from qobuz_catalog import Catalog, CatalogError, DEFAULT_SOURCE, ROOT


def candidate_plan(source):
    manifest = json.loads((source / 'manifest.json').read_text())
    albums = {}
    for entry in manifest['entries']:
        evidence = json.loads((source / f"{entry['discogs_id']}.json").read_text())
        for album in evidence['search']['albums']['items']:
            album_id = str(album['id'])
            if not album_id.isalnum():
                raise ValueError('Invalid candidate ID')
            albums.setdefault(album_id, set()).add(entry['discogs_id'])
    return [{'album_id': key, 'discogs_ids': sorted(ids)} for key, ids in sorted(albums.items())]


def validate_album(album, album_id):
    tracks = album.get('tracks', {}).get('items')
    if str(album.get('id')) != album_id or not isinstance(tracks, list) or len(tracks) != album.get('tracks_count'):
        raise CatalogError('Incomplete or mismatched album metadata; user review required.')


def fetch_complete_album(catalog, album_id):
    """Assemble cached pages without replacing the original response cache."""
    album = catalog.fetch('album/get', album_id=album_id)
    expected = album.get('tracks_count')
    block = album.get('tracks', {})
    tracks = block.get('items')
    if (str(album.get('id')) != album_id or type(expected) is not int or expected < 0
            or not isinstance(tracks, list) or block.get('offset', 0) != 0
            or block.get('total', expected) != expected or len(tracks) > expected):
        raise CatalogError('Invalid initial album page; user review required.')
    tracks = list(tracks)
    pages = 1
    while len(tracks) < expected:
        if not tracks:
            raise CatalogError('Empty initial album page; user review required.')
        offset = len(tracks)
        page = catalog.fetch('album/get', album_id=album_id, offset=offset, limit=500)
        block = page.get('tracks', {})
        items = block.get('items')
        if (str(page.get('id')) != album_id or page.get('tracks_count') != expected
                or block.get('total') != expected or block.get('offset') != offset
                or not isinstance(items, list) or not items or offset + len(items) > expected):
            raise CatalogError('Invalid/non-advancing album pagination; user review required.')
        tracks.extend(items)
        pages += 1
    if pages > 1:
        ids = [t.get('id') for t in tracks]
        if any(i is None for i in ids) or len(set(ids)) != expected:
            raise CatalogError('Overlapping or missing track IDs in album pages; user review required.')
    result = dict(album)
    result['tracks'] = {**album['tracks'], 'items': tracks, 'offset': 0,
                        'total': expected, 'limit': len(tracks)}
    validate_album(result, album_id)
    return result


def main():
    output = ROOT / '.qobuz-poc/metadata'
    output.mkdir(parents=True, exist_ok=True)
    lock = (output / 'run.lock').open('w')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print('Metadata worker already running.', flush=True)
        return 1
    stop = output / 'STOP'
    if stop.exists():
        print('STOP marker present. Await user direction before resuming.', flush=True)
        return 1
    try:
        plan = candidate_plan(ROOT / '.qobuz-poc/all')
        fingerprint = hashlib.sha256(json.dumps(plan, sort_keys=True).encode()).hexdigest()
        manifest = output / 'manifest.json'
        if manifest.exists() and json.loads(manifest.read_text())['fingerprint'] != fingerprint:
            raise ValueError('Candidate plan changed')
        save(manifest, {'fingerprint': fingerprint, 'entries': plan})
    except (OSError, ValueError, KeyError, TypeError):
        stop.touch()
        print('Candidate manifest invalid/changed; paused for review.', flush=True)
        return 1
    pace = Pace(15, stop)
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda *_: setattr(pace, 'stopping', True))
    def paced_request():
        # Count every HTTP request, including extra album pages and discovery.
        if pace.requests and pace.requests % 50 == 0:
            status['rest_until_epoch'] = time.time() + 120
            checkpoint()
            print('Resting 120 seconds.', flush=True)
            pace.wait(120)
            status.pop('rest_until_epoch', None)
        pace()
    catalog = Catalog(DEFAULT_SOURCE, before_request=paced_request)
    status = {'status': 'running', 'pid': os.getpid(), 'started_at': now(),
              'albums': len(plan), 'completed': 0, 'cached_this_run': 0,
              'fetched_this_run': 0, 'interval_seconds': 15,
              'rest_seconds': 120, 'batch_size': 50}
    def checkpoint():
        status['updated_at'] = now()
        status['network_attempts_this_run'] = pace.requests
        save(output / 'progress.json', status)
    previous_progress = output / 'progress.json'
    if previous_progress.exists():
        save(output / 'previous-run.json', json.loads(previous_progress.read_text()))
    checkpoint()
    try:
        for entry in plan:
            pace.check()
            album_id = entry['album_id']
            status['current_album'] = album_id
            checkpoint()
            path = output / f'{album_id}.json'
            before = pace.requests
            if path.exists():
                album = json.loads(path.read_text())['album']
            else:
                album = fetch_complete_album(catalog, album_id)
            validate_album(album, album_id)
            if not path.exists():
                save(path, {**entry, 'saved_at': now(), 'album': album})
            network = pace.requests > before
            status['fetched_this_run' if network else 'cached_this_run'] += 1
            status['completed'] += 1
            checkpoint()
            print(f"{status['completed']}/{len(plan)} album={album_id} {'fetched' if network else 'cached'}", flush=True)
        status['status'] = 'complete'
        status.pop('current_album', None)
    except StopRequested:
        status.update(status='stopped', reason='STOP marker or termination signal; await direction.')
    except CatalogError as exc:
        stop.touch()
        status.update(status='failed', reason=str(exc))
        print(str(exc), flush=True)
    except Exception:
        stop.touch()
        status.update(status='failed', reason='Unexpected local or metadata error; inspect before resuming.')
    finally:
        catalog.close()
        checkpoint()
        lock.close()
    print(f"Status: {status['status']}; {status['completed']}/{len(plan)} albums.", flush=True)
    return 0 if status['status'] == 'complete' else 1


if __name__ == '__main__':
    raise SystemExit(main())
