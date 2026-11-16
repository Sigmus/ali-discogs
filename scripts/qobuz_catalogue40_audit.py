"""Catalogue clues are diagnostics; recording acceptance requires frozen source bands."""
import json
import re
from qobuz_lead_review import ROOT, fingerprint
from qobuz_match import catalogue, credits, agrees
from qobuz_title151_diagnostic import catalogue_text
from qobuz_composer_identity import composer_key
from qobuz_work_groups import role_entries
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate

ROMAN={'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,'X':10,'XI':11,'XII':12,'XIII':13,'XIV':14,'XV':15,'XVI':16,'XVII':17,'XVIII':18,'XIX':19,'XX':20,'XXI':21,'XXII':22}


def notation_copy(text):
    # A comma before a descriptive label is not a numeric range/list. Copy only.
    def hob(m):
        tail=text[m.end():]
        if re.match(r'\s*[-–/]',tail) or re.match(r'\s*,\s*\d',tail):return m[0]
        return f'Hob {ROMAN[m[1].upper()]} No {m[2]}' if m[1].upper() in ROMAN else m[0]
    text=re.sub(r'\bHob\.?\s*([IVX]+)\s*:\s*(\d+)\b',hob,text,flags=re.I)
    text=re.sub(r'\bBWV\s+(\d)\.(\d{3})(?!\d)',r'BWV \1\2',text,flags=re.I)
    return catalogue_text(text)


def related(source, candidate):
    """Bare source opus may point to members, never equate differing members."""
    return bool(source) and all(any(x==y or (x[:2]==y[:2] and x[0]=='op' and x[2]=='') for y in candidate) for x in source)


def clues(row, candidate, observations):
    allowed={composer_key(c) for c in row['composers']}
    result=[]
    for observation in observations:
        ca=catalogue(notation_copy(observation['target']));matches=[]
        for track in candidate['tracks']['items']:
            cb=catalogue(notation_copy((track.get('work') or '')+' '+track['title']))
            if not related(ca,cb):continue
            declared={composer_key(n) for n,roles in role_entries(track) if 'composer' in roles}
            matches.append({'track_id':track['id'],'catalogue':[list(c) for c in sorted(cb)],
                'composer_positive':bool(declared) and declared<=allowed,
                'missing_required_musicians':[n for n in observation['required_performers'] if not agrees(n,credits(track))]})
        if matches:result.append({'target':observation['target'],'source_catalogue':[list(c) for c in sorted(ca)],'tracks':matches})
    return result


def main():
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    reviews={r['discogs_id']:r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
    report=json.loads((ROOT/'data/qobuz_catalogue40_recording_audit.json').read_text());albums=load_albums()
    validate(report,rows,albums,reviews,40)
    diagnostic=json.loads((ROOT/'data/qobuz_title151_diagnostic.json').read_text())
    if fingerprint(diagnostic)!=report['diagnostic_sha256']:raise ValueError('Original diagnostic changed')
    frozen={e['discogs_id']:e for e in diagnostic['entries'] if e['machine_observation_family']=='no_shared_catalogue_in_saved_candidates'}
    if set(frozen)!=set(report['frozen_release_ids']):raise ValueError('Frozen catalogue40scope changed')
    for entry in report['entries']:
        if [c['album_id'] for c in entry['catalogue_clues']] != [c['album_id'] for c in frozen[entry['discogs_id']]['candidates']]:
            raise ValueError('Candidate clue scope changed')
        for saved in entry['catalogue_clues']:
            original=next(c for c in frozen[entry['discogs_id']]['candidates'] if c['album_id']==saved['album_id'])
            if clues(rows[entry['discogs_id']],albums[saved['album_id']],original['observations'])!=saved['clues']:
                raise ValueError('Catalogue diagnostic evidence changed')
    print(json.dumps(report['summary']))


if __name__=='__main__':main()
