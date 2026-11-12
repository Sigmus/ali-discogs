(function (factory) {
  const api = factory();
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (typeof document !== "undefined") api.boot();
})(function () {
  "use strict";

  const STATUS = {
    found: "found",
    matched: "found",
    match: "found",
    yes: "found",
    probable: "probable",
    likely: "probable",
    maybe: "probable",
    possible: "probable",
    not_found: "not_found",
    notfound: "not_found",
    missing: "not_found",
    miss: "not_found",
    none: "not_found",
    no: "not_found",
    absent: "not_found",
    pending: "pending",
    queued: "pending",
    unchecked: "unchecked",
    skipped: "unchecked",
    unknown: "unchecked"
  };
  const STATUS_LABEL = {
    found: "Found",
    probable: "Probable",
    not_found: "Not found",
    pending: "Pending",
    unchecked: "Unchecked"
  };
  const SORTS = ["composer", "artist", "title", "year", "label", "confidence", "performers", "spotify"];
  const THEME_KEY = "ali-discogs-theme";
  const LIST_KEYS = ["items", "releases", "matches", "collection", "results", "data", "records", "entries", "collection_matches", "albums"];

  function asArray(v) {
    if (v == null || v === "") return [];
    return Array.isArray(v) ? v : [v];
  }
  function text(v) {
    if (v == null) return "";
    if (typeof v === "string" || typeof v === "number") return String(v).trim();
    if (typeof v === "object") return text(v.name || v.title || v.anv || v.label || "");
    return "";
  }
  function cleanName(s) {
    return String(s || "").replace(/\s+\(\d+\)\s*$/, "").trim();
  }
  function esc(s) {
    return String(s ?? "").replace(/[&<>"']/g, ch => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    })[ch]);
  }
  function safeUrl(u) {
    const raw = String(u || "").trim();
    if (!raw) return "";
    try {
      const url = new URL(raw);
      if (url.protocol === "http:" || url.protocol === "https:") return url.href;
    } catch (e) { /* ignore */ }
    return "";
  }
  function confidenceOf(v) {
    if (v == null || v === "") return null;
    const n = typeof v === "number" ? v : Number(String(v).trim());
    if (!Number.isFinite(n)) return null;
    const scaled = n > 1 && n <= 100 ? n / 100 : n;
    if (scaled < 0 || scaled > 1) return null;
    return scaled;
  }
  function statusOf(v) {
    const raw = text(v).toLowerCase().replace(/[\s-]+/g, "_");
    if (!raw) return "";
    return STATUS[raw] || "unchecked";
  }
  function yearOf(v) {
    if (v == null || v === "" || v === 0 || v === "0") return null;
    if (typeof v === "number" && Number.isFinite(v)) return v > 0 ? Math.trunc(v) : null;
    const found = String(v).match(/\d{4}/g);
    if (!found) return null;
    const n = Number(found[found.length - 1]);
    return n > 0 ? n : null;
  }
  function yearish(v) {
    const y = yearOf(v);
    return y ? String(y) : "";
  }
  function imageOf(v) {
    if (!v) return "";
    if (typeof v === "string") return safeUrl(v);
    if (Array.isArray(v)) {
      const best = v.slice().sort((a, b) => ((b && b.width) || 0) - ((a && a.width) || 0))[0];
      return imageOf(best);
    }
    if (typeof v === "object") return safeUrl(v.url || v.href || v.link);
    return "";
  }
  function artistList(v) {
    return asArray(v).map(a => {
      if (typeof a === "string" || typeof a === "number") {
        const name = cleanName(a);
        return name ? { name, join: "" } : null;
      }
      if (!a || typeof a !== "object") return null;
      const name = cleanName(a.name || a.artist || a.anv || a.title || "");
      if (!name) return null;
      return { name, join: String(a.join || "") };
    }).filter(Boolean);
  }
  function labelsOf(d) {
    const raw = asArray(d.labels);
    if (raw.length) {
      return raw.map(l => {
        if (typeof l === "string") return { name: cleanName(l), catno: "" };
        if (!l || typeof l !== "object") return null;
        const name = text(l.name || l.label || l.label_name);
        let catno = text(l.catno || l.catalog_number || l.catalogue || l.cat_no || l.catalog);
        if (/^none$/i.test(catno)) catno = "";
        if (!name && !catno) return null;
        return { name, catno };
      }).filter(Boolean);
    }
    const name = text(d.label || d.label_name);
    let catno = text(d.catno || d.catalog_number);
    if (/^none$/i.test(catno)) catno = "";
    return name || catno ? [{ name, catno }] : [];
  }
  function formatList(v) {
    return asArray(v).map(f => {
      if (f == null || f === "") return "";
      if (typeof f === "string" || typeof f === "number") return String(f).trim();
      if (typeof f !== "object") return "";
      const descs = asArray(f.descriptions || f.description).map(text).filter(Boolean);
      const name = text(f.name || f.format);
      if (/^box set$/i.test(name)) return "Box";
      const kind = descs.find(d => /^(lp|ep|cd|7"|10"|12"|45 rpm)$/i.test(d)) || name;
      if (!kind) return descs.join(" · ");
      const qty = text(f.qty || f.quantity);
      let s = qty && qty !== "1" ? qty + "×" + kind : kind;
      const tones = descs.filter(d => /^(mono|stereo|quadraphonic)$/i.test(d));
      if (tones.length) s += " · " + tones.join(" · ");
      return s;
    }).filter(Boolean);
  }
  function strList(v) {
    return asArray(v).flatMap(x => {
      if (x && typeof x === "object") return text(x) ? [text(x)] : [];
      const s = text(x);
      return s ? [s] : [];
    });
  }
  function albumOf(v) {
    if (!v || typeof v !== "object") return null;
    if (Array.isArray(v)) return albumOf(v[0]);
    const name = text(v.name || v.title || v.album);
    const artists = artistList(v.artists || v.artist || v.performers).map(a => a.name);
    const url = safeUrl(v.url || v.link || v.href || v.external_url);
    const id = text(v.id || v.album_id);
    if (!name && !url && !id) return null;
    const album = {
      id,
      name: name || "Untitled album",
      artists,
      release_date: text(v.release_date || v.date || v.year),
      url,
      image: imageOf(v.image || v.cover || v.thumb || v.image_url || v.images),
      label: text(v.label || v.label_name)
    };
    const confidence = confidenceOf(v.confidence ?? v.score);
    if (confidence != null) album.confidence = confidence;
    return album;
  }
  function alternatesOf(v) {
    return asArray(v).map(item => {
      if (!item || typeof item !== "object") return albumOf(item);
      const album = albumOf(item.album || item);
      if (!album) return null;
      const confidence = confidenceOf(item.confidence ?? item.score);
      if (confidence != null) album.confidence = confidence;
      return album;
    }).filter(Boolean);
  }
  function nameList(v) {
    return asArray(v).map(x => cleanName(text(x))).filter(Boolean);
  }
  function serviceOf(v) {
    const empty = { status: "pending", confidence: null, album: null, best_candidate: null, search_url: "", alternates: [] };
    if (v == null || v === "") return empty;
    if (typeof v === "string") return { status: statusOf(v) || "unchecked", confidence: null, album: null, best_candidate: null, search_url: "", alternates: [] };
    if (typeof v !== "object") return empty;
    const rawStatus = v.status ?? v.state ?? v.match ?? v.result;
    const status = text(rawStatus) ? statusOf(rawStatus) : "pending";
    const albumSource = v.album || v.release || v.best || v.hit || ((v.name || v.title) && !v.discogs ? v : null);
    const best = albumOf(v.best_candidate || v.bestCandidate || v.closest);
    return {
      status,
      confidence: confidenceOf(v.confidence ?? v.score ?? v.probability),
      album: albumOf(albumSource),
      best_candidate: best,
      search_url: safeUrl(v.search_url || v.searchUrl || v.search),
      alternates: alternatesOf(v.alternates || v.alternatives || v.candidates || v.others || [])
        .filter(a => !best || !a.id || a.id !== best.id)
    };
  }
  function discogsOf(entry) {
    let d = null;
    if (entry.discogs && typeof entry.discogs === "object") d = entry.discogs;
    else if (entry.release && typeof entry.release === "object" && (entry.release.title || entry.release.id || entry.release.artist)) d = entry.release;
    else if (entry.basic_information) {
      d = Object.assign({}, entry.basic_information, {
        id: entry.id ?? entry.basic_information.id,
        instance_id: entry.instance_id,
        date_added: entry.date_added
      });
    } else d = entry;
    if (d && d.basic_information && typeof d.basic_information === "object") {
      d = Object.assign({}, d.basic_information, d, { id: d.id ?? d.basic_information.id });
    }
    return d || {};
  }
  function pickService(entry, key) {
    if (entry[key] != null) return entry[key];
    if (entry[key + "_match"] != null) return entry[key + "_match"];
    if (entry[key + "Match"] != null) return entry[key + "Match"];
    return null;
  }
  function normalizeEntry(entry) {
    if (!entry || typeof entry !== "object") return null;
    const d = discogsOf(entry);
    const master = Number(d.master_id ?? d.masterId);
    const id = d.id ?? d.discogs_id ?? entry.discogs_id ?? entry.id ?? null;
    const artists = artistList(d.artists != null ? d.artists : d.artist);
    const labels = labelsOf(d);
    const formats = formatList(d.formats != null ? d.formats : d.format);
    const composers = nameList(d.composers != null ? d.composers : d.composer);
    const performers = nameList(d.performers != null ? d.performers : d.performer);
    const ensembles = nameList(d.ensembles != null ? d.ensembles : d.ensemble);
    const conductor = nameList(d.conductor)[0] || "";
    const tracklist = asArray(d.tracklist || d.tracks).map(t => {
      if (t == null || t === "") return "";
      if (typeof t === "string") return t.trim();
      return text(t.title || t.name);
    }).filter(Boolean);
    return {
      discogs: {
        id,
        instance_id: d.instance_id ?? entry.instance_id ?? null,
        master_id: Number.isFinite(master) && master > 0 ? master : null,
        title: text(d.title || entry.title) || "Untitled",
        artists,
        composers,
        performers,
        ensembles,
        conductor,
        tracklist,
        year: yearOf(d.year != null ? d.year : d.released),
        labels,
        formats,
        genres: strList(d.genres != null ? d.genres : d.genre),
        styles: strList(d.styles != null ? d.styles : d.style),
        thumb: safeUrl(d.thumb || d.thumbnail),
        cover_image: safeUrl(d.cover_image || d.cover || d.image),
        url: safeUrl(d.discogs_url || d.url || d.uri || d.web_url) || (id ? "https://www.discogs.com/release/" + id : ""),
        date_added: text(d.date_added || entry.date_added)
      },
      spotify: serviceOf(pickService(entry, "spotify")),
      qobuz: serviceOf(pickService(entry, "qobuz"))
    };
  }
  function listFrom(raw) {
    if (Array.isArray(raw)) return raw;
    if (!raw || typeof raw !== "object") return [];
    for (const key of LIST_KEYS) {
      if (Array.isArray(raw[key])) return raw[key];
    }
    if (raw.title || raw.discogs || raw.basic_information || raw.release) return [raw];
    return [];
  }
  function collectionFrom(raw) {
    return listFrom(raw).map(normalizeEntry).filter(Boolean);
  }
  function metaOf(raw) {
    if (!raw || Array.isArray(raw) || typeof raw !== "object") return {};
    return {
      user: text(raw.user) || "ajozi",
      fetched_at: text(raw.fetched_at || raw.fetchedAt),
      note: text(raw.note)
    };
  }

  function surname(name) {
    const parts = String(name || "").trim().split(/\s+/).filter(Boolean);
    return parts.length ? parts[parts.length - 1] : "";
  }
  function creditFull(artists) {
    if (!artists.length) return "";
    let s = "";
    artists.forEach((a, i) => {
      s += a.name;
      if (i === artists.length - 1) return;
      const j = (a.join || "").trim();
      if (!j || /^[,/·•‧⋅\-–—]$/.test(j)) s += " · ";
      else s += " " + j + " ";
    });
    return s.replace(/\s+/g, " ").trim();
  }
  function cmpStr(a, b) {
    return String(a || "").localeCompare(String(b || ""), undefined, { sensitivity: "base", numeric: true });
  }
  function numNullLast(a, b, dir) {
    const an = typeof a === "number" && Number.isFinite(a);
    const bn = typeof b === "number" && Number.isFinite(b);
    if (!an && !bn) return 0;
    if (!an) return 1;
    if (!bn) return -1;
    return (a - b) * dir;
  }
  function strNullLast(a, b, dir) {
    if (!a && !b) return 0;
    if (!a) return 1;
    if (!b) return -1;
    return cmpStr(a, b) * dir;
  }
  function enrich(it, copies) {
    const d = it.discogs;
    const names = d.artists.map(a => a.name).join(" ");
    const labels = d.labels.map(l => l.name + " " + l.catno).join(" ");
    const matched = ["spotify", "qobuz"].flatMap(key => {
      const svc = it[key];
      return [svc.album, svc.best_candidate, ...svc.alternates].filter(Boolean).flatMap(a => [a.name, ...(a.artists || []), a.label]);
    }).join(" ");
    const raw = [d.title, names, (d.composers || []).join(" "), (d.performers || []).join(" "), d.conductor || "", (d.ensembles || []).join(" "), (d.tracklist || []).join(" "), labels, d.genres.join(" "), d.styles.join(" "), d.formats.join(" "), matched].join(" ").toLowerCase();
    it._blob = raw;
    it._flat = raw.replace(/[^a-z0-9]+/g, "");
    it._artist = surname(d.artists[0] && d.artists[0].name);
    it._artistFull = (d.artists[0] && d.artists[0].name) || "";
    it._composer = surname((d.composers || [])[0]);
    it._label = (d.labels[0] && d.labels[0].name) || "";
    it._catno = (d.labels[0] && d.labels[0].catno) || "";
    const confs = [it.spotify.confidence, it.qobuz.confidence].filter(n => typeof n === "number");
    it._conf = confs.length ? Math.min(...confs) : null;
    it._copies = copies || 1;
    return it;
  }
  function enrichAll(items) {
    const counts = new Map();
    items.forEach(it => {
      if (it.discogs.id != null) counts.set(it.discogs.id, (counts.get(it.discogs.id) || 0) + 1);
    });
    return items.map(it => enrich(it, counts.get(it.discogs.id) || 1));
  }
  function matches(it, state) {
    const q = state.q.trim().toLowerCase();
    if (q) {
      const flat = q.replace(/[^a-z0-9]+/g, "");
      if (!it._blob.includes(q) && !(flat.length >= 3 && it._flat.includes(flat))) return false;
    }
    if (state.sp && it.spotify.status !== state.sp) return false;
    if (state.qb && it.qobuz.status !== state.qb) return false;
    if (state.genre) {
      const g = state.genre.toLowerCase();
      const has = it.discogs.genres.some(x => x.toLowerCase() === g) || it.discogs.styles.some(x => x.toLowerCase() === g);
      if (!has) return false;
    }
    if (state.composer && !(it.discogs.composers || []).some(c => c.toLowerCase() === state.composer.toLowerCase())) return false;
    if (state.label && !it.discogs.labels.some(l => l.name === state.label)) return false;
    if (state.decade === "undated") {
      if (it.discogs.year) return false;
    } else if (state.decade) {
      if (Math.floor((it.discogs.year || 0) / 10) * 10 !== Number(state.decade)) return false;
    }
    return true;
  }
  function compare(a, b, state) {
    const dir = state.dir === "desc" ? -1 : 1;
    let c = 0;
    if (state.sort === "year") c = numNullLast(a.discogs.year, b.discogs.year, dir);
    else if (state.sort === "confidence") c = numNullLast(a._conf, b._conf, dir);
    else if (state.sort === "performers") {
      const credits = it => [it.discogs.conductor, ...it.discogs.performers, ...it.discogs.ensembles]
        .filter(Boolean).join(" ") || it.discogs.artists.map(a => a.name).join(" ");
      c = strNullLast(credits(a), credits(b), dir);
    }
    else if (state.sort === "spotify") {
      const rank = { found: 0, probable: 1, not_found: 2, pending: 3, unchecked: 4 };
      c = (rank[a.spotify.status] - rank[b.spotify.status]) * dir ||
        numNullLast(a.spotify.confidence, b.spotify.confidence, -dir);
    }
    else if (state.sort === "title") c = cmpStr(a.discogs.title, b.discogs.title) * dir;
    else if (state.sort === "label") c = (cmpStr(a._label, b._label) || cmpStr(a._catno, b._catno)) * dir;
    else if (state.sort === "artist") c = strNullLast(a._artist, b._artist, dir) || cmpStr(a._artistFull, b._artistFull) * dir;
    else c = strNullLast(a._composer, b._composer, dir) || strNullLast(a._artist, b._artist, dir);
    if (!c) c = cmpStr(a.discogs.title, b.discogs.title);
    if (!c) c = (Number(a.discogs.id) || 0) - (Number(b.discogs.id) || 0);
    return c;
  }
  function query(items, state) {
    return items.filter(it => matches(it, state)).sort((a, b) => compare(a, b, state));
  }
  function tally(items) {
    const blank = () => ({ found: 0, probable: 0, not_found: 0, pending: 0, unchecked: 0 });
    const out = { spotify: blank(), qobuz: blank(), neither: 0, both: 0, total: items.length };
    items.forEach(it => {
      ["spotify", "qobuz"].forEach(key => {
        const status = it[key].status;
        if (out[key][status] == null) out[key].unchecked += 1;
        else out[key][status] += 1;
      });
      if (it.spotify.status === "not_found" && it.qobuz.status === "not_found") out.neither += 1;
      if (it.spotify.status === "found" && it.qobuz.status === "found") out.both += 1;
    });
    return out;
  }

  function defaultState() {
    return { q: "", sp: "", qb: "", genre: "", composer: "", label: "", decade: "", sort: "composer", dir: "asc" };
  }

  function boot() {
    const $ = id => document.getElementById(id);
    const lede = $("lede");
    const notice = $("notice");
    const tallyEl = $("tally");
    const q = $("q");
    const sp = $("sp");
    const genre = $("genre");
    const composer = $("composer");
    const label = $("label");
    const decade = $("decade");
    const sort = $("sort");
    const reset = $("reset");
    const showing = $("showing");
    const shelf = $("shelf");
    const foot = $("foot");
    const sampleLink = $("sample-link");
    const themeBtn = $("theme");
    const form = $("filters");
    let items = [];
    let counts = null;
    let sample = false;
    let ready = false;
    const state = defaultState();
    readHash();

    function readHash() {
      const params = new URLSearchParams((location.hash || "").replace(/^#/, ""));
      const next = defaultState();
      next.q = params.get("q") || "";
      next.sp = params.get("sp") || "";
      next.genre = params.get("genre") || "";
      next.composer = params.get("composer") || "";
      next.label = params.get("label") || "";
      next.decade = params.get("decade") || "";
      const sortBy = params.get("sort") || "composer";
      next.sort = SORTS.includes(sortBy) ? sortBy : "composer";
      next.dir = params.get("dir") === "desc" ? "desc" : "asc";
      const statuses = ["", "found", "probable", "not_found", "pending", "unchecked"];
      if (!statuses.includes(next.sp)) next.sp = "";
      if (!statuses.includes(next.qb)) next.qb = "";
      Object.assign(state, next);
    }
    function writeHash() {
      const params = new URLSearchParams();
      if (state.q) params.set("q", state.q);
      if (state.sp) params.set("sp", state.sp);
      if (state.qb) params.set("qb", state.qb);
      if (state.genre) params.set("genre", state.genre);
      if (state.composer) params.set("composer", state.composer);
      if (state.label) params.set("label", state.label);
      if (state.decade) params.set("decade", state.decade);
      if (state.sort !== "composer") params.set("sort", state.sort);
      if (state.dir === "desc") params.set("dir", "desc");
      const s = params.toString();
      const same = s ? location.hash === "#" + s : !location.hash;
      if (same) return;
      history.replaceState(null, "", s ? "#" + s : location.pathname + location.search);
    }
    function isDefault() {
      return !state.q && !state.sp && !state.qb && !state.genre && !state.composer && !state.label && !state.decade && state.sort === "composer" && state.dir !== "desc";
    }
    function syncControls() {
      q.value = state.q;
      sp.value = state.sp;
      if ([...genre.options].some(o => o.value === state.genre)) genre.value = state.genre;
      if ([...composer.options].some(o => o.value === state.composer)) composer.value = state.composer;
      if ([...label.options].some(o => o.value === state.label)) label.value = state.label;
      if ([...decade.options].some(o => o.value === state.decade)) decade.value = state.decade;
      sort.value = state.sort;
      reset.disabled = isDefault();
    }
    function readControls() {
      state.q = q.value;
      state.sp = sp.value;
      state.genre = genre.value;
      state.composer = composer.value;
      state.label = label.value;
      state.decade = decade.value;
      state.sort = SORTS.includes(sort.value) ? sort.value : "composer";
    }
    function commit() {
      writeHash();
      renderShelf();
      paintTally();
      reset.disabled = isDefault();
    }
    function fromForm() {
      readControls();
      syncControls();
      commit();
    }

    function applyTheme(theme, persist) {
      const dark = theme === "dark";
      document.documentElement.dataset.theme = dark ? "dark" : "light";
      themeBtn.setAttribute("aria-label", dark ? "Switch to light theme" : "Switch to dark theme");
      if (persist) localStorage.setItem(THEME_KEY, dark ? "dark" : "light");
    }
    function optionList(pairs, placeholder) {
      return [`<option value="">${esc(placeholder)}</option>`].concat(pairs.map(([value, count, textLabel]) => {
        return `<option value="${esc(value)}">${esc(textLabel || value)} (${count})</option>`;
      })).join("");
    }
    function fillFilters() {
      const genres = new Map();
      const composers = new Map();
      const labels = new Map();
      const decades = new Map();
      items.forEach(it => {
        const seen = new Set();
        it.discogs.genres.concat(it.discogs.styles).forEach(name => {
          const key = name.toLowerCase();
          if (seen.has(key)) return;
          seen.add(key);
          genres.set(name, (genres.get(name) || 0) + 1);
        });
        const seenComposer = new Set();
        (it.discogs.composers || []).forEach(name => {
          const key = name.toLowerCase();
          if (seenComposer.has(key)) return;
          seenComposer.add(key);
          let row = composers.get(key);
          if (!row) {
            row = { name, count: 0, best: 0, spells: new Map() };
            composers.set(key, row);
          }
          row.count += 1;
          const n = (row.spells.get(name) || 0) + 1;
          row.spells.set(name, n);
          if (n > row.best) {
            row.best = n;
            row.name = name;
          }
        });
        const seenLabel = new Set();
        it.discogs.labels.forEach(l => {
          if (!l.name || seenLabel.has(l.name)) return;
          seenLabel.add(l.name);
          labels.set(l.name, (labels.get(l.name) || 0) + 1);
        });
        const key = it.discogs.year ? String(Math.floor(it.discogs.year / 10) * 10) : "undated";
        decades.set(key, (decades.get(key) || 0) + 1);
      });
      const byName = (a, b) => cmpStr(a[0], b[0]);
      genre.innerHTML = optionList([...genres.entries()].sort(byName), "Any");
      composer.innerHTML = optionList([...composers.values()].map(row => [row.name, row.count]).sort(byName), "Any");
      label.innerHTML = optionList([...labels.entries()].sort(byName), "Any");
      const decadeKeys = [...decades.keys()].filter(k => k !== "undated").sort();
      if (decades.has("undated")) decadeKeys.push("undated");
      decade.innerHTML = optionList(decadeKeys.map(k => [k, decades.get(k), k === "undated" ? "Undated" : k + "s"]), "Any");
    }

    function buildTally() {
      counts = tally(items);
      tallyEl.innerHTML = `<button type="button" data-set="sp" data-val=""><span class="num">${items.length}</span> All</button>` +
        ["found", "probable", "not_found"].map(status => `<button type="button" data-set="sp" data-val="${status}"><span class="num">${counts.spotify[status]}</span> ${esc(STATUS_LABEL[status])}</button>`).join("");
    }
    function paintTally() {
      tallyEl.querySelectorAll("button").forEach(btn => {
        const kind = btn.dataset.set;
        let on = false;
        if (kind === "sp") on = state.sp === btn.dataset.val;
        else if (kind === "qb") on = state.qb === btn.dataset.val;
        else if (kind === "neither") on = state.sp === "not_found" && state.qb === "not_found";
        else if (kind === "both") on = state.sp === "found" && state.qb === "found";
        btn.classList.toggle("on", on);
        btn.setAttribute("aria-pressed", on ? "true" : "false");
      });
    }

    function addedLabel(iso) {
      const d = new Date(iso);
      if (Number.isNaN(d.getTime())) return "";
      return d.toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" });
    }
    function initials(name) {
      const parts = String(name || "").trim().split(/\s+/).filter(Boolean);
      if (!parts.length) return "?";
      if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }
    function labelHtml(labels) {
      const shown = labels.slice(0, 2).map(l => {
        const cat = l.catno ? ` <span class="cat">${esc(l.catno)}</span>` : "";
        return `<span class="lab">${esc(l.name)}${cat}</span>`;
      });
      if (labels.length > 2) shown.push(`<span class="with">+${labels.length - 2}</span>`);
      return shown.join('<span class="dot">·</span>');
    }
    function matchHtml(album, prefix) {
      const href = safeUrl(album.url);
      const name = album.name || "Untitled album";
      const nameHtml = href
        ? `<a href="${esc(href)}" target="_blank" rel="noopener noreferrer">${esc(name)}</a>`
        : `<span class="aname">${esc(name)}</span>`;
      const who = (album.artists || []).filter(Boolean);
      const extra = [album.label, yearish(album.release_date)].filter(Boolean);
      const conf = typeof album.confidence === "number" ? ` <span class="conf">${Math.round(album.confidence * 100)}%</span>` : "";
      return `<p class="match">${prefix || ""}${nameHtml}${who.length ? ` <span class="by">${esc(who.join(", "))}</span>` : ""}${extra.length ? ` <span class="extra">${esc(extra.join(" · "))}</span>` : ""}${conf}</p>`;
    }
    function supportLine(d, limit = 3) {
      if (!d.composers || !d.composers.length) return [];
      const skip = new Set(d.composers.map(s => s.toLowerCase()));
      const bits = [];
      const add = name => {
        if (!name || skip.has(name.toLowerCase()) || bits.some(b => b.toLowerCase() === name.toLowerCase())) return;
        bits.push(name);
      };
      add(d.conductor);
      (d.performers || []).forEach(add);
      (d.ensembles || []).forEach(add);
      return bits.slice(0, limit);
    }
    function serviceHtml(name, svc) {
      const labelText = STATUS_LABEL[svc.status] || svc.status;
      const conf = typeof svc.confidence === "number" ? `<span class="conf">${Math.round(svc.confidence * 100)}%</span>` : "";
      let body = "";
      if (svc.status === "not_found") {
        const guess = svc.best_candidate || svc.album;
        body = guess
          ? matchHtml(guess, `<span class="closest">Closest guess</span> `)
          : `<p class="match quiet">No album match</p>`;
      } else if (svc.album) body = matchHtml(svc.album, "");
      else if (svc.search_url) body = `<p class="match"><a href="${esc(svc.search_url)}" target="_blank" rel="noopener noreferrer">Search on ${esc(name)}</a></p>`;
      else if (svc.status === "unchecked") body = `<p class="match quiet">Not checked</p>`;
      const alts = svc.alternates.length
        ? `<details class="alts"><summary>${svc.alternates.length} other candidate${svc.alternates.length === 1 ? "" : "s"}</summary><ul>${svc.alternates.map(a => `<li>${matchHtml(a, "")}</li>`).join("")}</ul></details>`
        : "";
      return `<div class="svc"><div class="svc-h"><span class="svc-name">${esc(name)}</span><span class="badge ${esc(svc.status)}">${esc(labelText)}</span>${conf}</div>${body}${alts}</div>`;
    }
    function coverHtml(d, large = false) {
      const url = safeUrl(large ? d.cover_image || d.thumb : d.thumb || d.cover_image);
      return url ? `<img src="${esc(url)}" alt="" loading="lazy" data-initials="${esc(initials(d.title))}">` : `<div class="mono" aria-hidden="true">${esc(initials(d.title))}</div>`;
    }
    function detailHash(it) {
      const params = new URLSearchParams(location.hash.slice(1));
      params.set("album", it._route);
      return "#" + params.toString();
    }
    function rowHtml(it) {
      const d = it.discogs, href = detailHash(it);
      return `<tr><td class="cover-cell"><a href="${esc(href)}" tabindex="-1" aria-hidden="true">${coverHtml(d)}</a></td>
        <td class="title"><a class="album-link" href="${esc(href)}" title="${esc(d.title)}">${esc(d.title)}</a></td>
        <td class="col-year">${d.year || "—"}</td>
        <td><a class="album-link" href="${esc(href)}" title="${esc(d.composers.join(" · "))}">${esc(d.composers.join(" · ") || "—")}</a></td>
        <td class="col-artists"><a class="album-link" href="${esc(href)}" title="${esc(supportLine(d).join(" · "))}">${esc(supportLine(d, Infinity).join(" · ") || d.artists.map(a => a.name).join(" · "))}</a></td>
        <td><a href="${esc(href)}" class="status ${esc(it.spotify.status)}">${typeof it.spotify.confidence === "number" ? Math.round(it.spotify.confidence * 100) + "% (" + esc(STATUS_LABEL[it.spotify.status]) + ")" : esc(STATUS_LABEL[it.spotify.status])}</a></td></tr>`;
    }
    function renderDetail() {
      const params = new URLSearchParams(location.hash.slice(1));
      const id = params.get("album");
      const it = id !== null ? items.find(row => row._route === id) : null;
      $("collection-view").hidden = id !== null;
      const detail = $("detail-view");
      detail.hidden = id === null;
      if (id === null) { document.title = "Ali's collection"; return; }
      params.delete("album");
      const back = params.toString() ? "#" + params.toString() : "#";
      if (!it) { detail.innerHTML = `<a class="back" href="${esc(back)}">← Albums</a><h1>Album not found</h1>`; return; }
      const d = it.discogs;
      document.title = d.title + " · Ali's collection";
      detail.innerHTML = `<a class="back" href="${esc(back)}">← Albums</a><article>
        <div class="detail-head"><div class="detail-cover">${coverHtml(d, true)}</div><div>
        <h1>${esc(d.title)}</h1><p class="composer">${esc(d.composers.join(" · "))}</p>
        <p class="support">${esc(supportLine(d, Infinity).join(" · ") || d.artists.map(a => a.name).join(" · "))}</p>
        <p class="meta">${esc([d.year || "Undated", ...d.formats].join(" · "))}</p>
        <p class="labels">${labelHtml(d.labels)}</p><p class="styles">${esc([...new Set(d.genres.concat(d.styles))].join(" · "))}</p>
        ${it._copies > 1 ? `<p class="copy">Copy added ${esc(addedLabel(d.date_added))}</p>` : ""}
        <div class="external-links">${safeUrl(d.url) ? `<a href="${esc(safeUrl(d.url))}" target="_blank" rel="noopener noreferrer">Discogs ↗</a>` : ""}${safeUrl(it.qobuz.search_url) ? `<a href="${esc(safeUrl(it.qobuz.search_url))}" target="_blank" rel="noopener noreferrer">Search Qobuz ↗</a>` : ""}</div></div></div>
        ${serviceHtml("Spotify", it.spotify)}
        <h2>Tracks <span class="quiet">${d.tracklist.length}</span></h2>
        ${d.tracklist.length ? `<ol class="track-list">${d.tracklist.map((t, i) => `<li><span class="track-number">${i + 1}</span><span>${esc(t)}</span></li>`).join("")}</ol>` : `<p class="quiet">No track list available.</p>`}
        </article>`;
    }
    function emptyMessage() {
      if (state.sp === "not_found" && state.qb === "not_found" && !state.q && !state.genre && !state.composer && !state.label && !state.decade) {
        return "No release is missing on both Spotify and Qobuz.";
      }
      if (state.sp === "not_found" && !state.q && !state.genre && !state.composer && !state.label && !state.decade) {
        return "Every release has a Spotify match.";
      }
      return "No releases match these filters.";
    }
    function headerHtml(name, key, className = "") {
      const active = state.sort === key;
      const direction = active ? (state.dir === "desc" ? "descending" : "ascending") : "none";
      const sortClass = active ? (state.dir === "desc" ? "sort-desc" : "sort-asc") : "";
      return `<th scope="col" class="sortable ${className} ${sortClass}" aria-sort="${direction}"><button type="button" data-sort="${key}">${name} <span class="sort-arrow" aria-hidden="true"></span></button></th>`;
    }
    function renderShelf() {
      if (!ready) return;
      const rows = query(items, state);
      showing.textContent = rows.length === items.length
        ? `${items.length.toLocaleString()} releases`
        : `Showing ${rows.length.toLocaleString()} of ${items.length.toLocaleString()}`;
      shelf.setAttribute("aria-busy", "false");
      if (!rows.length) {
        shelf.innerHTML = `<div class="empty"><p>${esc(emptyMessage())}</p><button type="button" data-clear>Clear filters</button></div>`;
        return;
      }
      shelf.innerHTML = `<div class="table-wrap"><table class="album-table"><colgroup><col style="width:48px"><col class="col-album" style="width:30%"><col class="col-year" style="width:75px"><col class="col-composer" style="width:18%"><col class="col-artists"><col class="col-status" style="width:145px"></colgroup><thead><tr><th aria-label="Cover"></th>${headerHtml("Album", "title")}${headerHtml("Year", "year", "col-year")}${headerHtml("Composer", "composer")}${headerHtml("Artists", "performers", "col-artists")}${headerHtml("Spotify", "spotify")}</tr></thead><tbody>${rows.map(rowHtml).join("")}</tbody></table></div>`;
    }
    function showNotice() {
      const waiting = items.length && items.every(it =>
        (it.spotify.status === "pending" || it.spotify.status === "unchecked") &&
        (it.qobuz.status === "pending" || it.qobuz.status === "unchecked"));
      if (sample) {
        notice.hidden = false;
        notice.className = "notice sample";
        notice.textContent = "Sample matches for trying filters and badges. These are not Ali’s records.";
        return;
      }
      if (waiting) {
        notice.hidden = false;
        notice.className = "notice";
        notice.textContent = "Spotify and Qobuz are still pending. Counts fill in when collection_matches.json includes match results.";
        return;
      }
      notice.hidden = true;
    }

    form.addEventListener("submit", e => e.preventDefault());
    let timer = 0;
    q.addEventListener("input", () => {
      clearTimeout(timer);
      timer = setTimeout(fromForm, 80);
    });
    [sp, genre, composer, label, decade, sort].forEach(el => el.addEventListener("change", fromForm));
    reset.addEventListener("click", clearFilters);
    shelf.addEventListener("click", e => {
      if (e.target.closest("[data-clear]")) clearFilters();
      const button = e.target.closest("button[data-sort]");
      if (!button) return;
      const key = button.dataset.sort;
      state.dir = state.sort === key && state.dir !== "desc" ? "desc" : "asc";
      state.sort = key;
      syncControls();
      commit();
      shelf.querySelector(`button[data-sort="${key}"]`).focus({ preventScroll: true });
    });
    function clearFilters() {
      Object.assign(state, defaultState());
      syncControls();
      commit();
    }
    tallyEl.addEventListener("click", e => {
      const btn = e.target.closest("button");
      if (!btn) return;
      const kind = btn.dataset.set;
      const val = btn.dataset.val;
      if (kind === "sp" || kind === "qb") state[kind] = state[kind] === val ? "" : val;
      else if (kind === "neither") {
        if (state.sp === "not_found" && state.qb === "not_found") { state.sp = ""; state.qb = ""; }
        else { state.sp = "not_found"; state.qb = "not_found"; }
      } else if (kind === "both") {
        if (state.sp === "found" && state.qb === "found") { state.sp = ""; state.qb = ""; }
        else { state.sp = "found"; state.qb = "found"; }
      }
      syncControls();
      commit();
    });
    themeBtn.addEventListener("click", () => {
      applyTheme(document.documentElement.dataset.theme === "dark" ? "light" : "dark", true);
    });
    document.querySelector(".skip").addEventListener("click", e => {
      e.preventDefault();
      const target = $("detail-view").hidden ? shelf : $("detail-view");
      target.focus();
    });
    document.addEventListener("keydown", e => {
      if (e.key === "/" && $("detail-view").hidden && !/^(input|select|textarea)$/i.test(document.activeElement && document.activeElement.tagName)) {
        e.preventDefault();
        q.focus();
      }
    });
    window.addEventListener("hashchange", () => {
      readHash();
      syncControls();
      renderShelf();
      paintTally();
      renderDetail();
      window.scrollTo(0, 0);
      if (!$("detail-view").hidden) $("detail-view").focus({ preventScroll: true });
    });
    $("detail-view").addEventListener("error", e => {
      if (e.target.tagName === "IMG") { const mono = document.createElement("div"); mono.className = "mono"; mono.textContent = e.target.dataset.initials || "?"; e.target.replaceWith(mono); }
    }, true);
    shelf.addEventListener("error", e => {
      const img = e.target;
      if (!img || img.tagName !== "IMG") return;
      const thumb = img.dataset.thumb;
      if (thumb && img.dataset.tried !== "1" && img.src !== thumb) {
        img.dataset.tried = "1";
        img.src = thumb;
        return;
      }
      const mono = document.createElement("div");
      mono.className = "mono";
      mono.setAttribute("aria-hidden", "true");
      mono.textContent = img.dataset.initials || "?";
      img.replaceWith(mono);
    }, true);

    applyTheme(document.documentElement.dataset.theme === "dark" ? "dark" : "light", false);
    const themeQuery = window.matchMedia("(prefers-color-scheme: dark)");
    themeQuery.addEventListener("change", e => {
      if (localStorage.getItem(THEME_KEY)) return;
      applyTheme(e.matches ? "dark" : "light", false);
    });

    const file = new URLSearchParams(location.search).get("data") === "fixture"
      ? "data/fixture.json"
      : "data/collection_matches.json";
    sample = file.endsWith("fixture.json");
    if (sample) {
      sampleLink.href = "./";
      sampleLink.textContent = "Back to the collection";
    }
    fetch(file)
      .then(res => {
        if (!res.ok) throw new Error(res.status + " " + res.statusText);
        return res.json();
      })
      .then(raw => {
        const meta = metaOf(raw);
        items = enrichAll(collectionFrom(raw));
        const occurrences = new Map();
        items.forEach((it, index) => {
          const id = String(it.discogs.id ?? "row-" + index);
          const n = (occurrences.get(id) || 0) + 1;
          occurrences.set(id, n);
          it._route = id + ":" + (it.discogs.instance_id ?? n);
        });
        ready = true;
        fillFilters();
        syncControls();
        buildTally();
        paintTally();
        const who = meta.user && meta.user !== "sample" ? meta.user : "ajozi";
        lede.textContent = sample
          ? `${items.length.toLocaleString()} sample releases with invented matches, for checking badges. Not Ali’s collection.`
          : `${items.length.toLocaleString()} releases · Discogs collection of ${who}`;
        showNotice(meta);
        const when = meta.fetched_at ? addedLabel(meta.fetched_at) : "";
        foot.textContent = when
          ? `Discogs collection fetched ${when}. Cover images load from Discogs.`
          : "Cover images load from Discogs.";
        renderShelf();
        renderDetail();
      })
      .catch(err => {
        shelf.innerHTML = "";
        shelf.setAttribute("aria-busy", "false");
        notice.hidden = false;
        notice.className = "notice error";
        notice.textContent = `Couldn’t load ${file}. ${err.message}`;
        showing.textContent = "";
      });
  }

  return { collectionFrom, enrichAll, query, tally, metaOf, boot };
});
