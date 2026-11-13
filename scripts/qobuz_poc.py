# /// script
# requires-python = ">=3.11"
# dependencies = ["qobuz==0.0.2"]
# ///
"""Read-only Qobuz catalogue probe. Run: uv run scripts/qobuz_poc.py."""
import argparse
import json
import os
from pathlib import Path

import qobuz
import requests

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="Bach Glenn Gould Goldberg Variations")
    parser.add_argument("--output", type=Path, default=ROOT / ".qobuz-poc/result.json")
    args = parser.parse_args()
    # Read only the required setting; never log environment values or HTTP URLs.
    app_id = os.environ.get("QOBUZ_APP_ID", "")
    if not app_id and (ROOT / ".env").exists():
        for line in (ROOT / ".env").read_text().splitlines():
            key, sep, value = line.partition("=")
            if sep and key.strip() == "QOBUZ_APP_ID":
                app_id = value.strip().strip("\"'")
    if not app_id:
        print("Missing QOBUZ_APP_ID. Set it in .env or the environment.")
        return 2
    qobuz.register_app(app_id)
    # Upstream requests have no timeout; bound every request for this probe.
    original_get = qobuz.api.requests.get
    def bounded_get(*a, **kw):
        kw.setdefault("timeout", 20)
        return original_get(*a, **kw)
    qobuz.api.requests.get = bounded_get
    try:
        albums = qobuz.Album.search(args.query, limit=5)
        raw = qobuz.api.request("album/search", query=args.query, limit=5, offset=0)
        result = {"query": args.query, "library_count": len(albums), "response": raw}
        if albums:
            result["first_album"] = qobuz.api.request("album/get", album_id=albums[0].id)
    except requests.HTTPError as exc:
        print(f"Qobuz API returned HTTP {exc.response.status_code}; no matches classified.")
        return 1
    except requests.RequestException:
        print("Qobuz API network request failed; no matches classified.")
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(f"Library returned {len(albums)} albums. Metadata saved to {args.output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
