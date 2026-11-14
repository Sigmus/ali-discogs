"""Frozen Klemperer Ninth/five-section finale review; no global credit repair."""
import hashlib
import json
import re
from qobuz_lead_review import ROOT, fingerprint
from qobuz_match import agrees, credits, evaluate, norm

NINTH = list(range(353969798,353969806))
LEONORE = 353969813
STEPHAN = 353969784
VOICES = ['Aase Nordmo Løvberg','Christa Ludwig','Waldemar Kmentt','Hans Hotter','Philharmonia Chorus']


def assess_finale(row,album,review):
    if review['discogs_id'] not in {'6113868','6119375'} or review['album_id'] != 'vrg5q0y8vzvaa':
        raise ValueError('Outside frozen choral-finale scope')
    path=ROOT/f"raw/discogs/releases/{review['discogs_id']}.json"
    if hashlib.sha256(path.read_bytes()).hexdigest()!=review['source_sha256']:
        raise ValueError('Reviewed source changed')
    raw=json.loads(path.read_text())
    if raw['tracklist']!=review['source_programme'] or len(raw['tracklist'])!=3 or len(raw['tracklist'][0]['sub_tracks'])!=4:
        raise ValueError('Four-movement source programme changed')
    tracks=album['tracks']['items'];by_id={t['id']:t for t in tracks}
    if len(tracks)!=album['tracks_count'] or len(by_id)!=len(tracks):
        raise ValueError('Incomplete/duplicate compilation')
    expected=NINTH+[LEONORE,STEPHAN]
    if review['selected_track_ids']!=expected or any(i not in by_id for i in expected):
        raise ValueError('Missing or substituted programme section')
    selected=[by_id[i] for i in expected]
    if review['track_sha256']!=[fingerprint(t) for t in selected]:
        raise ValueError('Reviewed track data changed')
    if [t['id'] for t in tracks if t['id'] in NINTH]!=NINTH:
        raise ValueError('Finale sections reordered')
    patterns=[r': I\.',r': II\.',r': III\.']+[rf': IV\. \({letter}\)' for letter in 'abcde']
    for t,pattern in zip(selected[:8],patterns):
        if 'Op. 125' not in t['title'] or not re.search(pattern,t['title']):
            raise ValueError('Movement/section identity changed')
    if not ('Leonore Overture No. 3' in by_id[LEONORE]['title'] and 'Op. 72b' in by_id[LEONORE]['title'] and 'Op. 117' in by_id[STEPHAN]['title']):
        raise ValueError('Overture identity changed')
    for t in selected:
        if (not all(agrees(n,credits(t)) for n in ['Otto Klemperer','Philharmonia Orchestra']) or
                norm((t.get('composer') or {}).get('name',''))!='ludwig van beethoven'):
            raise ValueError('Wrong composer/conductor/orchestra')
    # All named source voices remain required within the sung finale. No album
    # credit inheritance, or requirement for singers in instrumental movements.
    sung=[by_id[i] for i in NINTH[4:]]
    available=[name for t in sung for name in credits(t)]
    if not all(agrees(n,available) for n in VOICES):
        raise ValueError('Missing named source voice/chorus')
    if review['voice_metadata_discrepancy']!={'track_id':353969805,'artist':'Hans Hotter','saved_role':'Contralto Vocals','other_section_role':'Bass Vocals'}:
        raise ValueError('Voice metadata discrepancy must remain explicit')
    # Public evidence has four movements, with five distinct tracks for IV.
    target=raw['tracklist'][0]['title'];groups=[NINTH[:1],NINTH[1:2],NINTH[2:3],NINTH[3:]]
    programme=[{'target':target,'track_ids':NINTH,'work_tracks':8,'credited_tracks':8,
                'credit_policy':'Conductor/orchestra on every track; all named singers/chorus evidenced within sung finale.'}]
    for source,tid in zip(raw['tracklist'][1:],[LEONORE,STEPHAN]):
        programme.append({'target':source['title'],'track_ids':[tid],'work_tracks':1,'credited_tracks':1})
    evidence=evaluate(row,album)
    evidence.update(programme=programme,covered=3,target_count=3,coverage=1,
        reasons=['Four complete reviewed movements; IV explicitly contains sections(a)–(e), with scoped positive voice/chorus evidence.'])
    works=[{'target':target,'status':'complete','scope':'source-bound-split-finale',
            'expected_movements':[1,2,3,4],'observed_movements':[1,2,3,4],
            'movement_track_ids':groups,'track_ids':NINTH}]
    works += [{'target':p['target'],'status':'complete','scope':'source-bound-overture','track_ids':p['track_ids']} for p in programme[1:]]
    result={k:review[k] for k in ['discogs_id','album_id','decision','recording_review','sources','limitations']}
    result.update(eligible=review['decision']=='probable',completeness={'status':'complete','works':works,'overlapping_target_tracks':False})
    return result,evidence
