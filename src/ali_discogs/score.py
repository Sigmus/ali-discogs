"""Confidence score and the found / probable / not_found decision.

found requires confidence >= 0.80 plus the strict performer, composer, title,
catalogue-number, conductor, and ensemble checks in `classify`.
probable starts at confidence >= 0.62, with the extra branches in `classify`.
"""

import re

from rapidfuzz import fuzz

from ali_discogs.text import ENS_T, ORCH_ALIASES, ids, name_match, norm, surname, tnorm

FOUND_MIN = 0.80
PROB_MIN = 0.62


def sp_album(album):
    return {
        'id': album['id'],
        'name': album['name'],
        'artists': [x['name'] for x in album.get('artists', [])],
        'release_date': album.get('release_date'),
        'total_tracks': album.get('total_tracks'),
        'album_type': album.get('album_type'),
        'url': album.get('external_urls', {}).get('spotify') or f"https://open.spotify.com/album/{album['id']}",
        'image': (album.get('images') or [{}])[0].get('url'),
        'label': None,
    }


def score(it, album):
    sp_artists = [x['name'] for x in album.get('artists', [])]
    name = album['name']
    blob = ' '.join(sp_artists) + ' ' + name

    def hit(person):
        n = norm(person)
        n2 = ORCH_ALIASES.get(n, n)
        best = max([name_match(person, s) for s in sp_artists] + [name_match(n2, s) for s in sp_artists] + [0])
        if best < 88 and len(n.split()) >= 2 and (f' {n} ' in f' {norm(name)} ' or f' {n2} ' in f' {norm(name)} '):
            best = 90
        return best >= 88

    perf = it['performers'][:4]
    perf_hits = [hit(p) for p in perf]
    p_primary = all(hit(p) for p in it.get('key_performers') or []) and bool(it.get('key_performers'))
    p_in_artists = bool(it.get('key_performers')) and all(
        max(
            [name_match(p, x) for x in sp_artists]
            + [name_match(ORCH_ALIASES.get(norm(p), p), x) for x in sp_artists]
            + [0]
        ) >= 88
        for p in it['key_performers']
    )
    p_frac = sum(perf_hits) / len(perf_hits) if perf_hits else 0
    cond_hit = hit(it['conductor']) if it.get('conductor') else None
    sp_ens = [x for x in sp_artists if any(e in norm(x) for e in ENS_T) and not any(k in norm(x) for k in ('choir', 'chor', 'singers'))]
    orch_hit = None
    if it.get('ensembles') and sp_ens:
        orch_hit = any(hit(e) for e in it['ensembles'])
    live_mismatch = ('live' in norm(name).split()) and ('live' not in norm(it['title']).split())
    comps = it['composers'][:3]
    c_hits = [hit(c) or surname(c) in norm(blob).split() for c in comps]
    c_frac = sum(c_hits) / len(c_hits) if c_hits else 1.0
    dt = tnorm(it['title'].split(' = ')[0] if ' = ' in it['title'] else it['title'])
    dt_full = tnorm(it['title'])
    sn = tnorm(name)
    for person in it['composers'] + it['performers']:
        for w in [norm(person), surname(person)]:
            if len(w) > 3:
                sn = re.sub(rf'\b{re.escape(w)}\b', ' ', sn)
    sn = ' '.join(sn.split())
    tsc = max(
        fuzz.token_set_ratio(dt, sn),
        fuzz.token_set_ratio(dt_full, sn),
        fuzz.partial_ratio(dt, sn) * 0.9 if len(dt) > 8 else 0,
    )
    tsort = max(fuzz.token_sort_ratio(dt, sn), fuzz.token_sort_ratio(dt_full, sn))
    hs = ' '.join(it['_headings'][:6])
    if hs:
        tsc = max(tsc, fuzz.token_set_ratio(tnorm(hs), sn) * 0.95)
    di = ids(it['title'] + ' ' + hs)
    si = ids(name)
    if di and si:
        inter = di & si
        dn = {x for x in di if x[0] == 'no'}
        sn_ = {x for x in si if x[0] == 'no'}
        if dn and sn_ and not (dn & sn_):
            num = -1
        elif dn and not (dn <= sn_):
            num = 0
        elif inter and len(inter) >= min(len(di), len(si)) * 0.5:
            num = 1
        elif inter:
            num = 0
        else:
            num = -1
    else:
        num = None
    if num is None:
        words = {'deux': '2', 'zwei': '2', 'two': '2', 'due': '2', 'trois': '3', 'drei': '3', 'three': '3', 'tre': '3', 'quatre': '4', 'vier': '4', 'four': '4', 'quattro': '4'}

        def digits(text):
            return {words.get(w, w) for w in text.split() if words.get(w, w).isdigit() and len(words.get(w, w)) <= 2}

        a_, b_ = digits(dt_full), digits(tnorm(name))
        if a_ and b_ and not (a_ & b_):
            num = -1
    vd = set(re.findall(r'\bvol(?:ume)?\s*([0-9]{1,2})\b', dt_full))
    vs = set(re.findall(r'\bvol(?:ume)?\s*([0-9]{1,2})\b', tnorm(name)))
    if vd and vd != vs:
        num = 0 if not vs else -1
    year_ok = None
    try:
        sy = int((album.get('release_date') or '0')[:4])
        dy = int(it['year'] or 0)
        if sy and dy:
            year_ok = abs(sy - dy) <= 2
    except ValueError:
        pass
    conf = 0.0
    conf += 0.35 * (1 if p_primary else 0) + 0.15 * p_frac
    conf += 0.15 * c_frac
    conf += 0.30 * (tsc / 100)
    if num == 1:
        conf += 0.08
    if num == -1:
        conf -= 0.25
    if year_ok:
        conf += 0.04
    conf = round(max(0, min(1, conf)), 3)
    if cond_hit is False:
        conf -= 0.1
    if orch_hit is False:
        conf -= 0.1
    if live_mismatch:
        conf -= 0.08
    conf = round(max(0, min(1, conf)), 3)
    return {
        'confidence': conf,
        'p_in_artists': p_in_artists,
        'cond_hit': cond_hit,
        'orch_hit': orch_hit,
        'live_mismatch': live_mismatch,
        'p_primary': p_primary,
        'p_frac': round(p_frac, 2),
        'c_frac': round(c_frac, 2),
        'title_score': round(tsc, 1),
        'title_sort': round(tsort, 1),
        'num_agree': num,
        'year_close': year_ok,
    }


def classify(signals, it):
    if not signals:
        return 'not_found'
    title_ok = signals['title_score'] >= 50 or signals['num_agree'] == 1
    if not it['performers']:
        return 'probable' if signals['confidence'] >= 0.75 and signals['title_score'] >= 80 else 'not_found'
    if signals['num_agree'] == -1:
        return 'probable' if signals['p_primary'] and signals['confidence'] >= PROB_MIN and signals['title_score'] >= 60 else 'not_found'
    if it['composers'] and signals['c_frac'] < 0.5:
        return 'not_found'
    if (
        signals['confidence'] >= FOUND_MIN
        and signals['p_primary']
        and signals['c_frac'] >= 0.5
        and signals['title_score'] >= 70
        and (signals['title_sort'] >= 55 or signals['num_agree'] == 1)
        and signals['num_agree'] != 0
        and signals['cond_hit'] is not False
        and signals['orch_hit'] is not False
        and signals['p_in_artists']
        and not signals['live_mismatch']
    ):
        return 'found'
    if signals['confidence'] >= PROB_MIN and signals['p_primary'] and title_ok:
        return 'probable'
    if signals['confidence'] >= 0.72 and signals['title_score'] >= 85 and signals['p_frac'] > 0:
        return 'probable'
    if signals['cond_hit'] and signals['title_score'] >= 85 and signals['num_agree'] != -1:
        return 'probable'
    return 'not_found'
