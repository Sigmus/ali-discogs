# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.32,<3"]
# ///
"""Search five Qobuz candidates and save the first album's metadata."""
import argparse
import json
from pathlib import Path

from qobuz_catalog import Catalog, CatalogError, DEFAULT_SOURCE, ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--query", default="Bach Glenn Gould Goldberg Variations")
    parser.add_argument("--anonymous", action="store_true")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    catalog = None
    try:
        catalog = Catalog(args.source, offline=args.offline, refresh=args.refresh, anonymous=args.anonymous)
        search = catalog.fetch("catalog/search", query=args.query, type="albums", limit=5)
        items = search["albums"]["items"]
        result = {"query": args.query, "search": search}
        if items:
            result["album"] = catalog.fetch("album/get", album_id=items[0]["id"])
        output = ROOT / ".qobuz-poc/catalog-result.json"
        output.parent.mkdir(exist_ok=True)
        output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        print(f"Returned {len(items)} candidates; metadata saved to {output}.")
        return 0
    except CatalogError as exc:
        print(exc)
        return 1
    finally:
        if catalog:
            catalog.close()


if __name__ == "__main__":
    raise SystemExit(main())
