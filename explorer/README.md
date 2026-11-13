# Ali's collection

Static explorer for [ajozi](https://www.discogs.com/user/ajozi/collection) on Discogs: which of the records turn up on Spotify and on Qobuz, and which are on neither.

On sigmus this is served at [/ali-discogs/](https://sigmus.fly.dev/ali-discogs/). Styles, scripts, and JSON use relative paths, so the same files work under that prefix and under a GitHub Pages project site at `/ali-discogs/`. In this repository the match results are [`../data/collection_matches.json`](../data/collection_matches.json); `make build` copies them into the published `data/` folder beside this page. `node test/normalize.test.js` reads that repo file when it is not sitting next to the page.

## Data

`data/collection_matches.json` contains741 collection copies and Spotify results
(254Found,273Probable,210NotFound,4Unchecked as of2026-11-13). The explorer also
loads the independent `data/qobuz_matches.json` overlay:12Found,67Probable,
662Unchecked copies. Details retain `qobuz.search_url`; selected albums and
candidates use canonical Qobuz locale/slug URLs from the shared offline index.
`data/summary.json` contains pipeline totals before the Qobuz overlay.
See [Qobuz enrichment setup](../docs/qobuz.md).

Preferred shape, one object per collection copy:

```json
{
  "items": [
    {
      "discogs": {
        "id": 15221307,
        "master_id": 1015652,
        "title": "Russian Keyboard Masters Vol. 1",
        "artists": ["Emil Gilels"],
        "year": 1974,
        "labels": [{"name": "ABC Westminster Gold", "catno": "WG-8273"}],
        "formats": ["LP"],
        "genres": ["Classical"],
        "styles": [],
        "thumb": "https://i.discogs.com/…",
        "cover_image": "https://i.discogs.com/…",
        "url": "https://www.discogs.com/release/15221307"
      },
      "spotify": {
        "status": "found",
        "confidence": 0.92,
        "album": {
          "id": "…",
          "name": "…",
          "artists": ["…"],
          "release_date": "1974",
          "url": "https://open.spotify.com/album/…",
          "image": "https://…",
          "label": "…"
        },
        "alternates": []
      },
      "qobuz": {"status": "not_found", "confidence": 0.1, "album": null, "alternates": []}
    }
  ]
}
```

The committed file is flatter than that sketch: `discogs_id`, `discogs_url`, `composers`, `performers`, `conductor`, `tracklist`, and a `spotify` object with `best_candidate` on misses. The loader still accepts the nested shape above.

`status` is `found`, `probable`, `not_found`, `pending`, or `unchecked`. `unchecked` is a neutral grey state, not a miss. `confidence` is 0–1, or a 0–100 score. A bare array is accepted, and so are a few aliases (`releases`, `spotify_match`, `score`, `alternatives`, artist objects, Discogs `basic_information`). `data/fixture.json` is a handful of invented rows. Open `?data=fixture` to see them. It is not part of the collection.

`node test/normalize.test.js` checks the loader against the fixture and the committed collection.

## Page

The explorer uses Sonoteque's visual style: compact album table, small covers,
muted metadata, thin rules, violet accents and paired light/dark themes.
Spotify status filtering uses the Spotify match dropdown. Search covers
title, composer, performer, conductor, ensemble, track, label and catalogue number.
Composer, genre/style, label and decade filters combine with Spotify status.
The “Most frequent first” switch before Clear is on by default and orders all
filter options by collection count, with alphabetical ties. Switch it off for
alphabetical ordering (decades oldest first, undated last). Placeholders stay
first and active selections survive reordering. The Sort selector is unchanged.
The default sort is Year, oldest to newest, with undated albums last.
Click Album, Year, Composer, Artists or Spotify headings to sort; click again to
reverse. The active heading shows Sonoteque’s triangle indicator. Spotify sorts
by status then confidence; Artists sorts performance credits. The Sort selector
also offers album artist, label and confidence sorting and stays synchronized.

Open an album title or cover to view full metadata, all tracks, Spotify match
or closest guess and alternate candidates. Discogs and Qobuz search links live
in details. Qobuz is unchecked; no main-page Qobuz totals or filters are shown.
The back link preserves collection filters. Hash links identify release/copy;
rows lacking instance IDs use occurrence order to distinguish duplicates.
On mobile, year and artists columns are hidden; metadata remains in details.
The theme follows the system until switched. Grid view has been removed.
