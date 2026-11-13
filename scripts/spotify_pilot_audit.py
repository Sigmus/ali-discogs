"""Offline Spotify title/artist evidence audit; never changes published matches."""
import gzip
import hashlib
import json
from pathlib import Path
from qobuz_match import units,work_match

ROOT=Path(__file__).resolve().parents[1]


def main():
    path=ROOT/'data/spotify_pilot_tracks.json.gz'
    with gzip.open(path,'rt') as f:data=json.load(f)
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    results=[]
    for album in data['albums']:
        rid=album['discogs_id'];row=rows[rid]
        programme=[{'target':title,'track_ids':[t['id'] for t in album['tracks'] if work_match(title,t['name'])]} for title in units(row)]
        r={'discogs_id':rid,'target_title':row['title'],'published_status':row['spotify']['status'],
           'album_id':album['album_id'],'album_title':album['album_name'],'album_url':'https://open.spotify.com/album/'+album['album_id'],
           'track_count':len(album['tracks']),'programme':programme,'title_supported_items':sum(bool(p['track_ids']) for p in programme),
           'target_items':len(programme),'recording_credit_status':'unverified: Spotify artist lists do not provide instrument/conductor/chorus roles',
           'interpretation':'Unmapped titles may be parser, translation or catalogue gaps; not automatic absence.'}
        if rid=='1012732':
            if len(album['tracks'])!=4 or not all(work_match('Symphony Op.68',t['name']) for t in album['tracks']):
                raise ValueError('Brahms evidence changed; manual finding needs review')
            r['review_status']='confirmed_partial_programme'
            r['finding']='All four tracks are Brahms Symphony No.1 Op.68 movements; requested symphonies 2–4, violin concerto, German Requiem and Haydn Variations absent from this album track list.'
        elif rid=='6119238':
            if any(work_match('Overture Op.62',t['name']) for t in album['tracks']) or not any(work_match('Symphony Op.60',t['name']) for t in album['tracks']):
                raise ValueError('Dvorak evidence changed; manual finding needs review')
            r['review_status']='confirmed_partial_programme'
            r['finding']='Symphony No.6 Op.60 present, but requested My Home Op.62 absent. Extras are In Nature\'s Realm Op.91, Carnival Op.92 and Scherzo capriccioso Op.66.'
        else:r['review_status']='unresolved_recording_validation'
        results.append(r)
    payload={'schema_version':1,'audited_on':'2026-11-13','policy':'Dated review observations, not score overrides. Nonrandom ten-album sample; no accuracy-rate estimate.',
             'track_evidence_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'entries':results,
             'summary':{'albums':len(results),'tracks':sum(r['track_count'] for r in results),'confirmed_partial_programmes':sum(r['review_status']=='confirmed_partial_programme' for r in results),'remaining_recording_validations_unresolved':sum(r['review_status']=='unresolved_recording_validation' for r in results)}}
    (ROOT/'data/spotify_pilot_audit.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(payload['summary']))


if __name__=='__main__':main()
