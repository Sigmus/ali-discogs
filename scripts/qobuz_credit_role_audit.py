"""Read-only inventory of associated-only credit roles; no acceptance policy change."""
import gzip
import hashlib
import json
from collections import Counter
from qobuz_lead_review import ROOT, fingerprint
from qobuz_match import agrees, credits, norm
from qobuz_snapshot import load_snapshot


def load_albums():
    albums=dict(load_snapshot()['albums'])
    for path in sorted((ROOT/'data').glob('*.json.gz')):
        for item in json.loads(gzip.decompress(path.read_bytes())).get('metadata',[]):
            album=item['album'];aid=str(album['id']);tracks=album['tracks']['items']
            if len(tracks)!=album['tracks_count'] or len({t['id'] for t in tracks})!=len(tracks):
                raise ValueError('Incomplete metadata in role audit')
            if aid in albums and albums[aid]!=album:raise ValueError('Conflicting cached albums')
            albums[aid]=album
    return albums


def audit(albums, publication):
    references={}
    for rid,release in publication['releases'].items():
        for candidate in release['candidates']:
            references.setdefault(candidate['id'],[]).append((rid,candidate['required_performers']))
    entries=[]
    for aid,album in sorted(albums.items()):
        for track in album['tracks']['items']:
            parts=(track.get('performers') or '').split(' - ')
            for index,part in enumerate(parts):
                fields=[v.strip() for v in part.split(',')];name=fields[0]
                associated=[v for v in fields[1:] if norm(v) in {'associatedperformer','associated performer'}]
                if not associated:continue
                other=[v for v in fields[1:] if v not in associated]
                if agrees(name,credits({'performers':name+', '+', '.join(other)})):continue
                entries.append({'album_id':aid,'track_id':track['id'],'track_sha256':fingerprint(track),
                                'name':name,'roles':fields[1:],'associated_role':associated,
                                'accepted_by_current_parser':agrees(name,credits(track)),
                                'other_accepted_declaration_on_same_track':agrees(name,credits({'performers':' - '.join(parts[:index]+parts[index+1:])})),
                                'required_by_saved_candidate_releases':[rid for rid,names in references.get(aid,[]) if agrees(name,names)]})
    return {'schema_version':1,'reviewed_on':'2026-11-15','policy_changed':False,
            'publication_changed':False,'cached_albums':len(albums),
            'associated_only_declarations':len(entries),
            'by_spelling':dict(Counter(role for e in entries for role in e['associated_role'])),
            'currently_accepted_declarations':sum(e['accepted_by_current_parser'] for e in entries),
            'referenced_declarations':sum(bool(e['required_by_saved_candidate_releases']) for e in entries),
            'accepted_only_through_associated_declaration':sum(e['accepted_by_current_parser'] and not e['other_accepted_declaration_on_same_track'] for e in entries),
            'entries':entries,'sources':['https://service.ddex.net/dd/DD-AVS-CURRENT/dd/avs_ContributorRole_RDR.html'],
            'limitations':['Role declarations are counted per cached album/track, not unique audio recordings or accepted matches.',
                           'A saved candidate reference is triage only, not proof its publication uses that track.',
                           'A name may be accepted through a second declaration on the same track; this is reported separately.',
                           'AssociatedPerformer denotes work-identification association in DDEX. Provider-specific recording semantics remain unresolved.',
                           'Current spaced form can match the generic performer token while compact form does not. No role equivalence or new credit acceptance adopted.']}


def main():
    path=ROOT/'data/qobuz_matches.json';publication=json.loads(path.read_bytes())
    result=audit(load_albums(),publication)
    result['publication_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    (ROOT/'data/qobuz_credit_role_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['cached_albums','associated_only_declarations','by_spelling','currently_accepted_declarations','referenced_declarations']}))

if __name__=='__main__':main()
