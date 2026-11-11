"""Discogs collection and release-detail fetch, cached under raw/discogs/.

A personal token in DISCOGS_TOKEN is optional. Without it Discogs allows about
25 requests per minute; with it, about 60. Cached files are returned as-is and
do not need a token. Requests pause according to X-Discogs-Ratelimit-Remaining
and Retry-After.
"""

import json
import os
import time
import urllib.error
import urllib.request

from ali_discogs.paths import raw_dir

USER_AGENT = "ali-discogs/0.1 +https://github.com/Sigmus/ali-discogs"
DEFAULT_USER = "ajozi"


class CacheMiss(FileNotFoundError):
    pass


def headers():
    out = {"User-Agent": USER_AGENT, "Accept": "application/vnd.discogs.v2+json"}
    token = os.environ.get("DISCOGS_TOKEN", "").strip()
    if token:
        out["Authorization"] = f"Discogs token={token}"
    return out


def _pace(response_headers):
    remaining = None
    if response_headers is not None:
        raw = response_headers.get("X-Discogs-Ratelimit-Remaining")
        try:
            remaining = int(raw) if raw is not None else None
        except ValueError:
            remaining = None
    if remaining is not None and remaining < 3:
        time.sleep(3.5)
        return
    time.sleep(1.1 if os.environ.get("DISCOGS_TOKEN", "").strip() else 2.5)


def _retry_after(exc):
    raw = exc.headers.get("Retry-After") if exc.headers else None
    if not raw:
        return 60
    try:
        return max(1.0, float(raw))
    except ValueError:
        return 60


def discogs_get(url, path, offline=False):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    if offline:
        raise CacheMiss(f"Discogs cache miss: {path}")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for _ in range(6):
        try:
            req = urllib.request.Request(url, headers=headers())
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
                response_headers = resp.headers
            with open(path, "wb") as fh:
                fh.write(data)
            _pace(response_headers)
            return json.loads(data)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write("{}")
                return {}
            time.sleep(_retry_after(exc) if exc.code == 429 else 10)
        except Exception:
            time.sleep(10)
    return {}


def collection_page_path(page: int) -> str:
    return os.path.join(raw_dir(), "discogs", f"page_{page}.json")


def release_path(release_id) -> str:
    return os.path.join(raw_dir(), "discogs", "releases", f"{release_id}.json")


def load_collection(user=DEFAULT_USER, offline=False):
    os.makedirs(os.path.join(raw_dir(), "discogs", "releases"), exist_ok=True)
    first = discogs_get(
        f"https://api.discogs.com/users/{user}/collection/folders/0/releases?per_page=100&page=1",
        collection_page_path(1),
        offline=offline,
    )
    pages = first["pagination"]["pages"]
    releases = list(first["releases"])
    for page in range(2, pages + 1):
        payload = discogs_get(
            f"https://api.discogs.com/users/{user}/collection/folders/0/releases?per_page=100&page={page}",
            collection_page_path(page),
            offline=offline,
        )
        releases += payload["releases"]
    return releases


def fetch_release(release_id, offline=False):
    return discogs_get(
        f"https://api.discogs.com/releases/{release_id}",
        release_path(release_id),
        offline=offline,
    )


def ensure_details(releases, offline=False):
    for release in releases:
        release_id = release["basic_information"]["id"]
        if offline and not os.path.exists(release_path(release_id)):
            raise CacheMiss(f"Discogs release cache miss: {release_id}")
        if not os.path.exists(release_path(release_id)):
            print(f"fetch release {release_id}", flush=True)
            fetch_release(release_id, offline=offline)
