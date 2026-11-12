# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.32,<3", "unidecode>=1.3", "rapidfuzz>=3.6"]
# ///
"""Slow, resumable first-pass catalogue search for every distinct Discogs release."""
import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import sys
import time

from qobuz_catalog import Catalog, CatalogError, DEFAULT_SOURCE, ROOT
from qobuz_sample_poc import SAMPLE

sys.path.insert(0, str(ROOT / "src"))
from ali_discogs.text import norm, short_title, surname


def now():
    return datetime.now(timezone.utc).isoformat()


def save(path, data):
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    temp.replace(path)


def manifest(rows):
    known = {r['discogs_id']: r['query'] for r in SAMPLE}
    entries = {}
    for row in rows:
        release_id = row['discogs_id']
        if release_id in entries:
            entries[release_id]['copies'] += 1
            continue
        people = row.get('key_performers') or row.get('performers') or []
        query = known.get(release_id) or ' '.join(filter(None, [
            norm(people[0]) if people else '',
            surname(row['composers'][0]) if row.get('composers') else '',
            short_title(row['title'], 10),
        ]))
        entries[release_id] = {'discogs_id': release_id, 'title': row['title'],
                               'query': ' '.join(query.split()), 'copies': 1}
    return list(entries.values())


class StopRequested(Exception):
    pass


class Pace:
    def __init__(self, interval, stop):
        self.interval = interval
        self.stop = stop
        self.previous = None
        self.requests = 0
        self.stopping = False

    def check(self):
        if self.stopping or self.stop.exists():
            raise StopRequested

    def wait(self, seconds):
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            self.check()
            time.sleep(min(1, max(0, end - time.monotonic())))
        self.check()

    def __call__(self):
        self.check()
        if self.previous is not None:
            self.wait(max(0, self.interval - (time.monotonic() - self.previous)))
        self.previous = time.monotonic()
        self.requests += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=DEFAULT_SOURCE)
    parser.add_argument('--interval', type=float, default=15)
    parser.add_argument('--batch-size', type=int, default=50)
    parser.add_argument('--rest', type=float, default=120)
    parser.add_argument('--offline', action='store_true')
    args = parser.parse_args()
    if args.interval < 15 or args.batch_size < 1 or args.rest < 120:
        parser.error('Use interval >=15 seconds, batch-size >=1, rest >=120 seconds.')
    output = ROOT / '.qobuz-poc/all'
    output.mkdir(parents=True, exist_ok=True)
    lock = (output / 'run.lock').open('w')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print('Another full-collection search is already running.')
        return 1
    rows = json.loads((ROOT / 'data/collection_matches.json').read_text())
    plan = manifest(rows)
    fingerprint = hashlib.sha256(json.dumps(plan, sort_keys=True).encode()).hexdigest()
    plan_path = output / 'manifest.json'
    if plan_path.exists() and json.loads(plan_path.read_text())['fingerprint'] != fingerprint:
        print('Collection/query plan changed; preserve existing results and review the manifest before resuming.')
        return 1
    save(plan_path, {'fingerprint': fingerprint, 'entries': plan})
    pace = Pace(args.interval, output / 'STOP')
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda *_: setattr(pace, 'stopping', True))
    catalog = Catalog(args.source, offline=args.offline, before_request=pace)
    status = {'status': 'running', 'pid': os.getpid(), 'started_at': now(),
              'copies': len(rows), 'releases': len(plan), 'completed': 0,
              'with_candidates': 0, 'zero_results': 0, 'candidate_count': 0,
              'interval_seconds': args.interval, 'rest_seconds': args.rest,
              'batch_size': args.batch_size, 'network_attempts_this_run': 0}

    def checkpoint():
        status['updated_at'] = now()
        status['network_attempts_this_run'] = pace.requests
        save(output / 'progress.json', status)

    checkpoint()
    searches_since_rest = 0
    try:
        for entry in plan:
            pace.check()
            status['current_release'] = entry['discogs_id']
            checkpoint()
            path = output / f"{entry['discogs_id']}.json"
            if path.exists():
                evidence = json.loads(path.read_text())
                if evidence['query'] != entry['query']:
                    raise CatalogError('Saved release query differs from manifest.')
                data = evidence['search']
            else:
                before = pace.requests
                data = catalog.fetch('catalog/search', query=entry['query'], type='albums', limit=5)
                save(path, {**entry, 'saved_at': now(), 'search': data,
                            'classification': 'unreviewed'})
                if pace.requests > before:
                    searches_since_rest += 1
            count = len(data['albums']['items'])
            status['completed'] += 1
            status['candidate_count'] += count
            status['with_candidates' if count else 'zero_results'] += 1
            checkpoint()
            print(f"{status['completed']}/{len(plan)} release={entry['discogs_id']} candidates={count}", flush=True)
            if searches_since_rest >= args.batch_size and status['completed'] < len(plan):
                print(f'Resting {args.rest:g} seconds.', flush=True)
                pace.wait(args.rest)
                searches_since_rest = 0
        status['status'] = 'complete'
        status.pop('current_release', None)
    except StopRequested:
        status['status'] = 'stopped'
        status['reason'] = 'Stop marker or termination signal; safe to resume.'
    except CatalogError as exc:
        status['status'] = 'failed'
        status['reason'] = str(exc)
        print(str(exc), flush=True)
    except (OSError, ValueError, KeyError, TypeError):
        status['status'] = 'failed'
        status['reason'] = 'Local data/cache/IO error; inspect files before resuming.'
    finally:
        catalog.close()
        checkpoint()
        lock.close()
    print(f"Status: {status['status']}; {status['completed']}/{len(plan)} searched.", flush=True)
    return 0 if status['status'] == 'complete' else 1


if __name__ == '__main__':
    raise SystemExit(main())
