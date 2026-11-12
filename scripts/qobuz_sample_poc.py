# /// script
# requires-python = ">=3.11"
# dependencies = ["requests>=2.32,<3"]
# ///
"""Collect Qobuz candidate metadata without classifying or publishing matches."""
import argparse
import json
from pathlib import Path
import time

from qobuz_catalog import Catalog, CatalogError, DEFAULT_SOURCE, ROOT

SAMPLE = [
    {"discogs_id": 2175684, "query": "Glenn Gould Bach Well Tempered Clavier"},
    {"discogs_id": 15282801, "query": "Erich Kleiber Beethoven Eroica"},
    {"discogs_id": 15081257, "query": "Karl Munchinger Bach Brandenburg"},
    {"discogs_id": 28220854, "query": "Emil Gilels Beethoven Sonatas 17 18"},
    {"discogs_id": 15221307, "query": "Emil Gilels Russian Keyboard Masters"},
    {"discogs_id": 1445439, "query": "Glenn Gould Byrd Gibbons"},
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--sample-file", type=Path, help="JSON list of {discogs_id, query}; defaults to six-release trial")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    catalog = None
    try:
        sample = json.loads(args.sample_file.read_text()) if args.sample_file else SAMPLE
        rows = {r["discogs_id"]: r for r in json.loads((ROOT / "data/collection_matches.json").read_text())}
        if not isinstance(sample, list) or not sample:
            raise ValueError
        for item in sample:
            if item["discogs_id"] not in rows or not isinstance(item["query"], str) or not item["query"].strip():
                raise ValueError
        catalog = Catalog(args.source, offline=args.offline, refresh=args.refresh)
        output = ROOT / ".qobuz-poc/sample"
        output.mkdir(parents=True, exist_ok=True)
        for item in sample:
            release_id, query = item["discogs_id"], item["query"]
            search = catalog.fetch("catalog/search", query=query, type="albums", limit=5)
            albums = []
            for candidate in search["albums"]["items"]:
                albums.append(catalog.fetch("album/get", album_id=candidate["id"]))
                if not args.offline:
                    time.sleep(0.25)
            result = {"discogs": rows[release_id], "query": query, "search": search, "albums": albums}
            target = output / f"{release_id}.json"
            temp = target.with_suffix(".tmp")
            temp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
            temp.replace(target)
            print(release_id, rows[release_id]["spotify"]["status"], len(albums), "candidates", flush=True)
        return 0
    except CatalogError as exc:
        print(exc)
        return 1
    except (OSError, ValueError, KeyError, TypeError):
        print("Invalid collection/sample file; use a JSON list of valid discogs_id and nonempty query values.")
        return 1
    finally:
        if catalog:
            catalog.close()


if __name__ == "__main__":
    raise SystemExit(main())
