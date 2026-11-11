"""Spotify Web API album search with an on-disk cache.

Cache hits never touch the network and do not need credentials. A miss uses the
client-credentials flow (`SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`).
"""

import base64
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

from ali_discogs.paths import raw_dir

TOKEN_URL = "https://accounts.spotify.com/api/token"
SEARCH_URL = "https://api.spotify.com/v1/search"


class CacheMiss(FileNotFoundError):
    pass


def cache_path(query, kind="album", limit=10) -> str:
    digest = hashlib.sha1(f"{kind}|{limit}|{query}".encode()).hexdigest()[:16]
    return os.path.join(raw_dir(), "spotify", f"{digest}.json")


class SpotifySearch:
    def __init__(self, offline=False):
        self.offline = offline
        self._token = None
        self._expires = 0.0

    def search(self, query, kind="album", limit=10):
        path = cache_path(query, kind, limit)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)["resp"]
        if self.offline:
            raise CacheMiss(f"Spotify cache miss for {query!r} ({path})")
        response = self._fetch(query, kind, limit)
        if response is None:
            return None
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"q": query, "resp": response}, fh)
        time.sleep(0.25)
        return response

    def _fetch(self, query, kind, limit):
        url = SEARCH_URL + "?" + urllib.parse.urlencode({"q": query, "type": kind, "limit": limit})
        for attempt in range(6):
            token = self._access_token(force=attempt == 0 and self._token is None)
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    return json.loads(resp.read().decode())
            except urllib.error.HTTPError as exc:
                if exc.code == 401 and attempt == 0:
                    self._token = None
                    continue
                if exc.code == 429:
                    retry = exc.headers.get("Retry-After") if exc.headers else None
                    try:
                        wait = float(retry) if retry else 5 * (attempt + 1)
                    except ValueError:
                        wait = 5 * (attempt + 1)
                    time.sleep(wait)
                    continue
                time.sleep(5 * (attempt + 1))
            except Exception:
                time.sleep(5 * (attempt + 1))
        return None

    def _access_token(self, force=False):
        now = time.time()
        if self._token and not force and now < self._expires - 30:
            return self._token
        client_id = os.environ.get("SPOTIFY_CLIENT_ID", "").strip()
        client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET", "").strip()
        if not client_id or not client_secret:
            raise SystemExit(
                "Spotify cache miss. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET "
                "(see .env.example). Cached queries do not need credentials."
            )
        basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
        req = urllib.request.Request(
            TOKEN_URL,
            data=body,
            headers={
                "Authorization": f"Basic {basic}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode())
        self._token = payload["access_token"]
        self._expires = now + int(payload.get("expires_in", 3600))
        return self._token
