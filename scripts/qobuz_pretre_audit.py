"""Offline CVL1920 band/credit diagnostic; never changes publication or source data."""
import hashlib
import json
from qobuz_lead_review import ROOT, fingerprint, target_fingerprint, validate_external_sources
from qobuz_match import norm
from qobuz_snapshot import load_snapshot


def seconds(text):
    minutes, value = text.split(':')
    return int(minutes)*60+int(value)


def audit(row, raw, album, review):
    if (str(row['discogs_id']) != review['discogs_id'] or str(album['id']) != review['album_id']
            or target_fingerprint(row) != review['target_sha256'] or fingerprint(album) != review['album_sha256']):
        raise ValueError('Reviewed Prêtre evidence changed')
    validate_external_sources(review)
    source = [t for t in raw['tracklist'] if t['type_'] == 'track']
    bands = review['bands']
    if [(t['position'],t['title'],t['duration']) for t in source] != [(b['position'],b['source_title'],b['source_duration']) for b in bands]:
        raise ValueError('Exact source band order, title or timing changed')
    tracks = {t['id']:t for t in album['tracks']['items']}
    used = [i for b in bands for i in b['candidate_track_ids']]
    if used != [t['id'] for t in album['tracks']['items']] or len(used) != len(set(used)):
        raise ValueError('Every digital section must occur exactly once in source order')
    results = []
    for band in bands:
        items = [tracks[i] for i in band['candidate_track_ids']]
        if ([t['title'] for t in items] != band['candidate_track_titles']
                or [fingerprint(t) for t in items] != band['candidate_track_fingerprints']):
            raise ValueError('Exact bound digital section changed')
        duration = sum(t['duration'] for t in items)
        reference = seconds(band['source_duration'])
        results.append({**band,'source_seconds':reference,'digital_seconds':duration,
                        'difference_seconds':duration-reference,
                        'timing_discrepancy':abs(duration-reference)>max(5,.03*reference)})
    mentions = []
    for credit in review['source_named_credits']:
        surname = norm(credit['name']).split()[-1]
        ids = [t['id'] for t in album['tracks']['items'] if surname in norm(t['performers']).split()]
        mentions.append({**credit,'surname_mentioned_on_track_ids':ids})
    totals = {side:{'source_seconds':sum(b['source_seconds'] for b in results if b['position'].startswith(side)),
                   'digital_seconds':sum(b['digital_seconds'] for b in results if b['position'].startswith(side))}
              for side in ['A','B']}
    return {'schema_version':1,'reviewed_on':'2026-11-15','discogs_id':review['discogs_id'],
            'album_id':review['album_id'],'review_fingerprint':fingerprint(review),
            'programme_mapping_complete':True,'source_bands':len(bands),'digital_sections':len(used),
            'bands':results,'side_totals':totals,'source_image_credit_mentions':mentions,
            'recording_identity_verified':False,'publication_change':False,
            'limitations':review['limitations']+['A surname mention is diagnostic only, not verified performer identity. Aggregate timing agreement does not erase per-band discrepancies.']}


def main():
    review=json.loads((ROOT/'data/qobuz_pretre_band_review.json').read_text())
    path=ROOT/f"raw/discogs/releases/{review['discogs_id']}.json"
    if hashlib.sha256(path.read_bytes()).hexdigest()!=review['source_sha256']:
        raise ValueError('Cached source changed')
    row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])==review['discogs_id'])
    result=audit(row,json.loads(path.read_bytes()),load_snapshot()['albums'][review['album_id']],review)
    (ROOT/'data/qobuz_pretre_band_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'source_bands':result['source_bands'],'digital_sections':result['digital_sections'],
                      'side_totals':result['side_totals'],'recording_identity_verified':False}))

if __name__=='__main__':main()
