"""Load the cached collection, score it, and write data/collection_matches.json."""

import json
import os
import time
import urllib.parse
from collections import Counter

from ali_discogs.discogs import DEFAULT_USER, ensure_details, load_collection, release_path
from ali_discogs.model import build_item, queries
from ali_discogs.paths import data_dir
from ali_discogs.score import FOUND_MIN, PROB_MIN, classify, score, sp_album
from ali_discogs.spotify import SpotifySearch
from ali_discogs.spotify_programme import programme_review
from ali_discogs.text import norm, short_title

QOBUZ_STATUS = "unchecked"
QOBUZ_REASON = (
    'www.qobuz.com returns HTTP 403 (Akamai "Access Denied") for every page from this machine '
    "(curl, headless and headed Chrome); no other public, key-free Qobuz search route exists."
)


def qobuz_entry(it):
    query = " ".join(filter(None, [norm(it["performers"][0]) if it["performers"] else "", short_title(it["title"], 6)]))
    return {
        "status": QOBUZ_STATUS,
        "confidence": None,
        "album": None,
        "alternates": [],
        "reason": QOBUZ_REASON,
        "search_url": "https://www.qobuz.com/nl-en/search?q=" + urllib.parse.quote(query),
    }


def match_spotify(it, search):
    candidates = {}
    qs = queries(it)
    for query in qs:
        resp = search(query)
        if not resp:
            continue
        for album in resp.get("albums", {}).get("items", []):
            if album and album["id"] not in candidates:
                candidates[album["id"]] = album
    scored = sorted(((score(it, album), album) for album in candidates.values()), key=lambda pair: -pair[0]["confidence"])
    if not scored:
        return {"status": "not_found", "confidence": 0, "album": None, "alternates": [], "queries": qs}
    best_signals, best = scored[0]
    status = classify(best_signals, it)
    alternates = [dict(sp_album(album), confidence=signals["confidence"]) for signals, album in scored[1:3]]
    review = programme_review(it, best)
    if review:
        # Preserve similarity evidence for inspection, but do not present a
        # known partial album or an unaudited runner-up as a complete match.
        return {"status": "unchecked", "confidence": None, "signals": best_signals,
                "album": None, "best_candidate": dict(sp_album(best)),
                "alternates": alternates, "queries": qs, "programme_review": review}
    return {
        "status": status,
        "confidence": best_signals["confidence"],
        "signals": best_signals,
        "album": dict(sp_album(best)) if status != "not_found" else None,
        "best_candidate": dict(sp_album(best)) if status == "not_found" else None,
        "alternates": alternates,
        "queries": qs,
    }


def summary_for(rows):
    return {
        "total": len(rows),
        "spotify": dict(Counter(row["spotify"]["status"] for row in rows)),
        "qobuz": dict(Counter(row["qobuz"]["status"] for row in rows)),
        "qobuz_note": QOBUZ_REASON,
        "thresholds": {"found_min_conf": FOUND_MIN, "probable_min_conf": PROB_MIN},
        "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }


def run_match(user=DEFAULT_USER, offline=False, write=True):
    releases = load_collection(user, offline=offline)
    ensure_details(releases, offline=offline)
    search = SpotifySearch(offline=offline).search
    rows = []
    for n, release in enumerate(releases, 1):
        item = build_item(release)
        item["spotify"] = match_spotify(item, search)
        item["qobuz"] = qobuz_entry(item)
        item.pop("_headings")
        item.pop("_tracks")
        rows.append(item)
        if n % 50 == 0:
            print(n, flush=True)
    summary = summary_for(rows)
    if write:
        os.makedirs(data_dir(), exist_ok=True)
        matches_path = os.path.join(data_dir(), "collection_matches.json")
        summary_path = os.path.join(data_dir(), "summary.json")
        with open(matches_path, "w", encoding="utf-8") as fh:
            json.dump(rows, fh, ensure_ascii=False, indent=1)
        with open(summary_path, "w", encoding="utf-8") as fh:
            json.dump(summary, fh, indent=1)
        print(json.dumps(summary, indent=1))
    return rows, summary


def fetch(user=DEFAULT_USER):
    releases = load_collection(user, offline=False)
    print(f"{len(releases)} collection copies", flush=True)
    missing = 0
    for release in releases:
        if not os.path.exists(release_path(release["basic_information"]["id"])):
            missing += 1
    if missing:
        print(f"fetching {missing} release details", flush=True)
    ensure_details(releases, offline=False)
    print("done", flush=True)
