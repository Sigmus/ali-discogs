"""Source/hash-bound Gould paired BWVs; never flatten away nested source works."""
import hashlib
import json
import re
from qobuz_lead_review import ROOT, fingerprint
from qobuz_match import agrees, credits, evaluate, norm


def assess_nested_pairs(row, album, review):
    if (review['discogs_id'], review['album_id']) != ('1458083','0886444299039'):
        raise ValueError('Outside reviewed nested-pair scope')
    path = ROOT/'raw/discogs/releases/1458083.json'
    if hashlib.sha256(path.read_bytes()).hexdigest() != review['source_sha256']:
        raise ValueError('Nested source changed')
    raw = json.loads(path.read_text())
    parents = raw['tracklist']
    if len(parents) != 1 or parents[0]['title'] != 'Two And Three Part Inventions':
        raise ValueError('Container structure changed')
    children = parents[0]['sub_tracks']; tracks = album['tracks']['items']
    if (len(children) != 15 or len(tracks) != 30 or album['tracks_count'] != 30 or
            album['tracks']['total'] != 30 or len({t['id'] for t in tracks}) != 30 or
            review['track_sha256'] != [fingerprint(t) for t in tracks] or
            review['source_children'] != children):
        raise ValueError('Incomplete or changed nested programme')
    programme=[]; used=[]; bwvs=[]
    for i, child in enumerate(children):
        match = re.fullmatch(r'No\.(\d+) In (.+), BWV (\d+) & (\d+)', child['title'])
        if not match: raise ValueError('Unrecognized paired source title')
        number,key,left,right = match.groups(); left=int(left);right=int(right)
        if left != 771+int(number) or right != left+15:
            raise ValueError('Conflicting invention/sinfonia catalogue identity')
        pair=tracks[2*i:2*i+2]
        for track,role,bwv in zip(pair,['Invention','Sinfonia'],[left,right]):
            expected=f'{role} No. {number} in {key}, BWV {bwv}'
            if (norm(track['title']) != norm(expected) or
                    not agrees('Glenn Gould',credits(track)) or
                    norm((track.get('composer') or {}).get('name','')) != 'johann sebastian bach'):
                raise ValueError('Wrong paired work, composer or pianist')
        used.extend(t['id'] for t in pair); bwvs.extend([left,right])
        programme.append({'target': f"{child['position']}: {child['title']}",
                          'source_position':child['position'], 'work_tracks':2,
                          'credited_tracks':2,'track_ids':[t['id'] for t in pair]})
    if sorted(bwvs) != list(range(772,802)) or used != [t['id'] for t in tracks]:
        raise ValueError('Missing, repeated or reordered BWV programme')
    evidence=evaluate(row,album)
    evidence.update(programme=programme,target_count=15,covered=15,coverage=1,
                    required_performers=['Glenn Gould'], reasons=['Every nested source pair has its explicit Invention and Sinfonia, in LP order, credited to Gould.'])
    result={k:review[k] for k in ['discogs_id','album_id','decision','recording_review','sources','limitations']}
    result.update(eligible=review['decision']=='probable',completeness={'status':'complete','overlapping_target_tracks':False,
        'works':[{'target':p['target'],'source_position':p['source_position'],'track_ids':p['track_ids'],
                  'status':'complete','scope':'source-nested-bwv-pair'} for p in programme]})
    return result,evidence
