import argparse
import os

from ali_discogs.discogs import DEFAULT_USER
from ali_discogs.envfile import load_dotenv
from ali_discogs.pipeline import fetch, run_match


def main(argv=None):
    load_dotenv()
    parser = argparse.ArgumentParser(prog="ali-discogs", description="Match a Discogs collection against Spotify.")
    parser.add_argument("--user", default=os.environ.get("DISCOGS_USER", DEFAULT_USER), help="Discogs username (default ajozi)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("fetch", help="Download missing Discogs collection pages and release details into raw/")

    match = sub.add_parser("match", help="Score the collection. Uses raw/spotify and raw/discogs; network only on a cache miss.")
    match.add_argument("--offline", action="store_true", help="Fail instead of calling Discogs or Spotify when a cache file is missing")
    match.add_argument("--rescore", action="store_true", help="Alias of --offline")

    args = parser.parse_args(argv)
    if args.cmd == "fetch":
        fetch(args.user)
        return 0
    run_match(args.user, offline=args.offline or args.rescore, write=True)
    return 0
