"""Shared read-only catalogue access and resumable metadata cache for the PoC."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
from datetime import datetime, timezone

import requests

ROOT = Path(__file__).resolve().parents[1]
SOURCE_REVISION = "28c3521c3c96e62d7da7166d3edef1aed92a202f"
DEFAULT_SOURCE = ROOT / ".qobuz-poc/upstream"


class CatalogError(Exception):
    """Credential-safe error suitable for displaying to the user."""


def local_setting(name):
    value = os.environ.get(name, "")
    if not value and (ROOT / ".env").exists():
        for line in (ROOT / ".env").read_text().splitlines():
            key, sep, item = line.partition("=")
            if sep and key.strip() == name:
                value = item.strip().strip("\"'")
    return value


class Catalog:
    def __init__(self, source=DEFAULT_SOURCE, *, offline=False, refresh=False,
                 anonymous=False, cache=ROOT / ".qobuz-poc/cache"):
        if offline and refresh:
            raise CatalogError("--offline and --refresh cannot be combined.")
        self.source = Path(source)
        self.offline = offline
        self.refresh = refresh
        self.anonymous = anonymous
        self.cache = Path(cache)
        self.session = requests.Session()
        self.app_id = None

    def close(self):
        self.session.close()

    def connect(self):
        token = "" if self.anonymous else local_setting("QOBUZ_USER_AUTH_TOKEN")
        if not self.anonymous and not token:
            raise CatalogError("Missing QOBUZ_USER_AUTH_TOKEN in environment or ignored .env.")
        source = self.source / "qobuz_dl/bundle.py"
        try:
            revision = subprocess.check_output(
                ["git", "-C", str(self.source), "rev-parse", "HEAD"],
                stderr=subprocess.DEVNULL, text=True,
            ).strip()
            dirty = subprocess.check_output(
                ["git", "-C", str(self.source), "status", "--porcelain", "--", "qobuz_dl/bundle.py"],
                stderr=subprocess.DEVNULL, text=True,
            ).strip()
        except (OSError, subprocess.CalledProcessError):
            raise CatalogError("Missing upstream checkout; follow docs/qobuz.md setup.") from None
        if revision != SOURCE_REVISION or dirty or not source.is_file():
            raise CatalogError("Upstream revision differs or bundle.py was modified; see docs/qobuz.md.")
        # Import only discovery. The full client initializes audio URL probes.
        spec = importlib.util.spec_from_file_location("qobuz_poc_bundle", source)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        discovery_session = requests.Session()
        original_get = discovery_session.get

        def bounded_get(*args, **kwargs):
            kwargs.setdefault("timeout", 20)
            return original_get(*args, **kwargs)

        discovery_session.get = bounded_get
        module.Session = lambda: discovery_session
        try:
            discovery = module.Bundle()
            self.app_id = discovery.get_app_id()  # Never call get_secrets().
        except requests.HTTPError as exc:
            raise CatalogError(f"App-ID discovery failed: HTTP {exc.response.status_code}.") from None
        except requests.RequestException:
            raise CatalogError("App-ID discovery network failure.") from None
        except (NotImplementedError, ValueError, KeyError, IndexError):
            raise CatalogError("Web-player app-ID discovery is incompatible with the current site.") from None
        finally:
            discovery_session.close()
        if token:
            self.session.headers["X-User-Auth-Token"] = token

    def fetch(self, endpoint, **params):
        if endpoint not in {"catalog/search", "album/get"}:
            raise CatalogError("Only catalogue search and album metadata endpoints are supported.")
        # Cache keys intentionally exclude credentials. Local caches reflect the
        # account/territory at fetch time; refresh after account/territory changes.
        request = {"endpoint": endpoint, "params": params}
        key = hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest()
        path = self.cache / f"{key}.json"
        if path.exists() and not self.refresh:
            try:
                saved = json.loads(path.read_text())
                if saved["request"] != request or not isinstance(saved["response"], dict):
                    raise ValueError
                return saved["response"]
            except (ValueError, KeyError, TypeError):
                raise CatalogError("Invalid cached response; rerun online with --refresh.") from None
        if self.offline:
            raise CatalogError(f"Offline cache miss for {endpoint}; run online first.")
        if self.app_id is None:
            self.connect()
        try:
            response = self.session.get(
                "https://www.qobuz.com/api.json/0.2/" + endpoint,
                params={"app_id": self.app_id, **params}, timeout=20,
            )
            response.raise_for_status()
            data = response.json()
        except requests.HTTPError as exc:
            raise CatalogError(f"{endpoint}: HTTP {exc.response.status_code}; no matches classified.") from None
        except requests.RequestException:
            raise CatalogError(f"{endpoint}: network/JSON failure; no matches classified.") from None
        if not isinstance(data, dict) or data.get("status") == "error":
            raise CatalogError(f"{endpoint}: invalid/error response; no matches classified.")
        if endpoint == "catalog/search" and not isinstance(data.get("albums", {}).get("items"), list):
            raise CatalogError("Search response has no album list; not a confirmed absence.")
        if endpoint == "album/get" and str(data.get("id")) != str(params.get("album_id")):
            raise CatalogError("Album response ID does not match the request.")
        saved = {"request": request, "fetched_at": datetime.now(timezone.utc).isoformat(),
                 "source_revision": SOURCE_REVISION, "response": data}
        self.cache.mkdir(parents=True, exist_ok=True)
        temp = path.with_suffix(".tmp")
        temp.write_text(json.dumps(saved, indent=2, ensure_ascii=False) + "\n")
        temp.replace(path)
        return data
