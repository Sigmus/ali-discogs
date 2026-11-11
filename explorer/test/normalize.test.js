const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const { collectionFrom, enrichAll, query, tally } = require("../app.js");

const root = path.join(__dirname, "..");
const fixture = JSON.parse(fs.readFileSync(path.join(root, "data/fixture.json"), "utf8"));
function collectionPath() {
  const beside = path.join(root, "data/collection_matches.json");
  if (fs.existsSync(beside)) return beside;
  return path.join(root, "..", "data", "collection_matches.json");
}
const real = JSON.parse(fs.readFileSync(collectionPath(), "utf8"));

const items = collectionFrom(fixture);
assert.equal(items.length, 8);

const byId = id => items.find(it => it.discogs.id === id);

const both = byId(1001);
assert.equal(both.spotify.status, "found");
assert.equal(both.qobuz.status, "found");
assert.equal(both.spotify.confidence, 0.96);
assert.equal(both.spotify.alternates.length, 1);
assert.equal(both.spotify.alternates[0].confidence, 0.61);
assert.equal(both.discogs.artists[0].name, "Ludwig van Beethoven");

const mismatch = byId(1002);
assert.equal(mismatch.spotify.status, "probable");
assert.equal(mismatch.spotify.album.name, "Piano Concerto No. 2");
assert.equal(mismatch.qobuz.status, "not_found");

const gap = byId(1003);
assert.equal(gap.spotify.status, "not_found");
assert.equal(gap.qobuz.status, "not_found");

const loose = byId(1004);
assert.equal(loose.discogs.title, "The Planets");
assert.equal(loose.discogs.artists[0].name, "Gustav Holst");
assert.equal(loose.discogs.year, 1967);
assert.deepEqual(loose.discogs.labels, [{ name: "Decca", catno: "SXL 2001" }]);
assert.equal(loose.discogs.formats[0], "LP · Stereo");
assert.deepEqual(loose.discogs.genres, ["Classical"]);
assert.deepEqual(loose.discogs.styles, ["Modern"]);
assert.equal(loose.spotify.status, "found");
assert.equal(loose.spotify.confidence, 0.88);
assert.equal(loose.spotify.album.artists[0], "Adrian Boult");
assert.equal(loose.qobuz.status, "not_found");

const jazz = byId(1005);
assert.equal(jazz.discogs.artists[0].name, "Miles Davis");
assert.equal(jazz.qobuz.status, "unchecked");
assert.equal(jazz.spotify.album.artists[0], "Miles Davis");

const blank = byId(1006);
assert.equal(blank.discogs.master_id, null);
assert.equal(blank.discogs.year, null);
assert.equal(blank.discogs.labels[0].catno, "");
assert.equal(blank.spotify.status, "pending");

const likely = byId(1007);
assert.equal(likely.spotify.status, "probable");
assert.equal(likely.spotify.confidence, 0.42);
assert.equal(likely.spotify.alternates.length, 1);
assert.equal(likely.qobuz.confidence, 0.55);

const apiShaped = collectionFrom({
  id: 5,
  instance_id: 9,
  date_added: "2020-01-02T00:00:00Z",
  basic_information: {
    id: 5,
    master_id: 0,
    title: "Api Shape",
    year: 0,
    artists: [{ name: "George Guest (2)", join: "," }, { name: "Choir", join: "" }],
    labels: [{ name: "Decca", catno: "SXL 2001" }],
    formats: [{ name: "Vinyl", qty: "2", descriptions: ["LP", "Mono"] }],
    genres: ["Classical"],
    styles: ["Choral"],
    thumb: "javascript:alert(1)",
    cover_image: ""
  }
});
assert.equal(apiShaped.length, 1);
assert.equal(apiShaped[0].discogs.artists[0].name, "George Guest");
assert.equal(apiShaped[0].discogs.year, null);
assert.equal(apiShaped[0].discogs.master_id, null);
assert.equal(apiShaped[0].discogs.formats[0], "2×LP · Mono");
assert.equal(apiShaped[0].discogs.thumb, "");
assert.equal(apiShaped[0].discogs.url, "https://www.discogs.com/release/5");
assert.equal(apiShaped[0].spotify.status, "pending");
assert.equal(apiShaped[0].discogs.date_added, "2020-01-02T00:00:00Z");

const bare = collectionFrom([
  { title: "Bare", artists: ["Only Name"], year: 1970, label: "Philips", catno: "6500 111" }
]);
assert.equal(bare[0].discogs.labels[0].name, "Philips");
assert.equal(bare[0].spotify.status, "pending");

const enriched = enrichAll(items);
const empty = { q: "", sp: "", qb: "", genre: "", label: "", decade: "", sort: "artist", dir: "asc" };
const counts = tally(enriched);
assert.equal(counts.total, 8);
assert.equal(counts.both, 1);
assert.equal(counts.neither, 1);
assert.equal(counts.spotify.probable, 2);
assert.equal(counts.qobuz.unchecked, 1);

const foundCat = query(enriched, { ...empty, q: "sxl2001" });
assert.ok(foundCat.some(it => it.discogs.id === 1004));

const gaps = query(enriched, { ...empty, sp: "not_found", qb: "not_found" });
assert.deepEqual(gaps.map(it => it.discogs.id), [1003]);

const romantic = query(enriched, { ...empty, genre: "Romantic" });
assert.ok(romantic.every(it => it.discogs.styles.includes("Romantic")));

const seventies = query(enriched, { ...empty, decade: "1970" });
assert.deepEqual(seventies.map(it => it.discogs.id), [1003]);

const undated = query(enriched, { ...empty, decade: "undated" });
assert.ok(undated.some(it => it.discogs.id === 1006));

const byYear = query(enriched, { ...empty, sort: "year", dir: "desc" });
assert.equal(byYear[0].discogs.year, 1984);
assert.equal(byYear.at(-1).discogs.year, null);

const names = query(
  enrichAll(collectionFrom([
    { id: 1, title: "B", artists: ["Ludwig van Beethoven"], year: 1970 },
    { id: 2, title: "A", artists: ["Johann Sebastian Bach"], year: 1960 },
    { id: 3, title: "C", artists: ["Johannes Brahms"], year: null }
  ])),
  empty
).map(it => it._artist);
assert.deepEqual(names, ["Bach", "Beethoven", "Brahms"]);

const flat = collectionFrom([{
  discogs_id: 42,
  discogs_url: "https://www.discogs.com/release/42-flat",
  title: "Flat",
  artists: ["A Person"],
  composers: ["Béla Bartók"],
  performers: ["A Person"],
  conductor: "Fritz Reiner",
  ensembles: ["Chicago Symphony Orchestra"],
  tracklist: [{ position: "A", title: "Music for Strings, Percussion and Celesta", duration: "28:00" }],
  year: 1958,
  labels: [{ name: "RCA", catno: "LM-1" }],
  formats: [{ name: "Vinyl", qty: "1", descriptions: ["LP"] }],
  spotify: {
    status: "not_found",
    confidence: 0.4,
    album: null,
    best_candidate: { id: "abc", name: "Closest Album", artists: ["Someone"], url: "https://open.spotify.com/album/abc" },
    alternates: [
      { id: "abc", name: "Closest Album", artists: ["Someone"] },
      { id: "def", name: "Other", artists: ["X"] }
    ]
  },
  qobuz: { status: "unchecked", search_url: "https://www.qobuz.com/nl-en/search?q=bartok" }
}])[0];
assert.equal(flat.discogs.id, 42);
assert.equal(flat.discogs.url, "https://www.discogs.com/release/42-flat");
assert.deepEqual(flat.discogs.composers, ["Béla Bartók"]);
assert.equal(flat.discogs.conductor, "Fritz Reiner");
assert.equal(flat.discogs.tracklist[0], "Music for Strings, Percussion and Celesta");
assert.equal(flat.spotify.album, null);
assert.equal(flat.spotify.best_candidate.name, "Closest Album");
assert.equal(flat.spotify.alternates.length, 1);
assert.equal(flat.qobuz.status, "unchecked");
assert.equal(flat.qobuz.search_url, "https://www.qobuz.com/nl-en/search?q=bartok");

const flatRows = enrichAll([flat]);
assert.equal(query(flatRows, { ...empty, composer: "Béla Bartók" }).length, 1);
assert.equal(query(flatRows, { ...empty, q: "celesta" }).length, 1);
assert.equal(query(flatRows, { ...empty, q: "reiner" }).length, 1);
assert.equal(query(flatRows, { ...empty, sp: "not_found" }).length, 1);

const collection = enrichAll(collectionFrom(real));
assert.equal(collection.length, 741);
const realCounts = tally(collection);
assert.equal(realCounts.spotify.found, 255);
assert.equal(realCounts.spotify.probable, 276);
assert.equal(realCounts.spotify.not_found, 210);
assert.equal(realCounts.qobuz.unchecked, 741);
assert.equal(realCounts.neither, 0);
assert.ok(collection.every(it => it.discogs.title && it.discogs.url.startsWith("https://www.discogs.com/")));
assert.ok(collection.every(it => it.discogs.master_id !== 0));
assert.ok(!collection.some(it => it.discogs.artists.some(a => /\(\d+\)$/.test(a.name))));
assert.ok(collection.every(it => it.qobuz.status === "unchecked" && it.qobuz.search_url.startsWith("https://www.qobuz.com/")));
const misses = collection.filter(it => it.spotify.status === "not_found");
assert.ok(misses.every(it => it.spotify.album == null && it.spotify.best_candidate && it.spotify.best_candidate.name));
const keyboard = collection.find(it => it.discogs.title === "Russian Keyboard Masters Vol. 1");
assert.equal(keyboard.spotify.status, "not_found");
assert.equal(keyboard.discogs.year, 1974);
assert.ok(keyboard.spotify.best_candidate.name);
assert.ok(keyboard.discogs.tracklist.length > 0);
const dupes = collection.filter(it => it.discogs.id === 11971084);
assert.equal(dupes.length, 2);
assert.ok(dupes.every(it => it._copies === 2));

const gilels = query(collection, { ...empty, q: "gilels" });
assert.ok(gilels.length > 0);
const beethoven = query(collection, { ...empty, composer: "Ludwig van Beethoven" });
assert.equal(beethoven.length, 123);
assert.ok(beethoven.every(it => it.discogs.composers.some(c => c.toLowerCase() === "ludwig van beethoven")));
const beethovenMiss = query(collection, { ...empty, composer: "Ludwig van Beethoven", sp: "not_found" });
assert.equal(beethovenMiss.length, 27);

console.log("normalize tests ok", collection.length, "releases");
