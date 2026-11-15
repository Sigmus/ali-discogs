"""Offline Casals source reconciliation/programme diagnostic; never publish or fetch."""
import gzip
import hashlib
import json
import re
from qobuz_match import ROOT,evaluate,catalogue,agrees,credits,norm
from qobuz_lead_review import fingerprint,target_fingerprint
from qobuz_source_reconciliation import reconcile,suite_positions
from qobuz_completeness import movement_number


def audit():
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    p=ROOT/'data/qobuz_casals_source_audit.json';review=json.loads(p.read_text())
    archive=ROOT/'data/qobuz_metadata_followup_2026_11_15.json.gz'
    album=next(x['album'] for x in json.loads(gzip.decompress(archive.read_bytes()))['metadata'] if x['album']['id']==review['album_id'])
    if fingerprint(album)!=review['album_sha256']:raise ValueError('Casals candidate changed')
    ts=album['tracks']['items']
    if len(ts)!=album['tracks_count'] or len({t['id'] for t in ts})!=len(ts):raise ValueError('Incomplete candidate metadata')
    result=[]
    for rid,work_ids in [('6628473',[1009,1010]),('23950082',[1011,1012])]:
        row=rows[rid];source=ROOT/f'raw/discogs/releases/{rid}.json';raw=json.loads(source.read_text())
        if rid=='6628473':
            effective=reconcile(row,review);assessment=evaluate(effective,album)
            groups=[{'suite_number':n,'source_tracks':g['sub_tracks']} for n,g in zip([3,4],raw['tracklist'])]
            if assessment['coverage']!=1:raise ValueError('Reconciled source programme lost support')
        else:groups=suite_positions(raw)
        if [g['suite_number'] for g in groups] != ([3,4] if rid=='6628473' else [5,6]):
            raise ValueError('Unexpected source suite scope')
        mappings=[]
        for group,bwv in zip(groups,work_ids):
            selected=[t for t in ts if ('bwv',str(bwv),'') in catalogue(t['title'])]
            if len(selected)!=6 or [movement_number(t['title']) for t in selected]!=list(range(1,7)) or any(not agrees('Pablo Casals',credits(t)) or not re.search(r'\bSuite No\. '+str(group['suite_number'])+r'\b',t['title']) for t in selected):
                raise ValueError('Wrong, incomplete or uncredited suite programme')
            from qobuz_work_groups import composers
            names=['prelude','allemande','courante','sarabande','bourree' if group['suite_number'] in [3,4] else 'gavotte','gigue']
            for source_track,candidate,name in zip(group['source_tracks'],selected,names):
                source_title=norm(source_track['title']).replace('praeludium','prelude')
                if name not in source_title or name not in norm(candidate['title']) or composers(candidate)!={'johann sebastian bach'}:
                    raise ValueError('Movement label or positive composer evidence changed')
            mappings.append({'suite_number':group['suite_number'],'bwv':bwv,'source_positions':[t['position'] for t in group['source_tracks']],'source_titles':[t['title'] for t in group['source_tracks']],'track_ids':[t['id'] for t in selected],'candidate_titles':[t['title'] for t in selected]})
        result.append({'discogs_id':rid,'target_sha256':target_fingerprint(row),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'programme':mappings,'decision':'programme_supported_recording_unresolved','reason':'Candidate has no recording-session date or take/version markers; programme/performer correspondence alone cannot identify the LP recording transfer.'})
    payload={'schema_version':1,'reviewed_on':'2026-11-15','reconciliation_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'album_id':album['id'],'album_sha256':fingerprint(album),'releases':result,'limitations':['Diagnostic only: no source data rewrite, publication override, API access or inferred recording date.','Other suites in the six-suite digital album are outside these two LP programmes.']}
    (ROOT/'data/qobuz_casals_reconciliation_audit.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    print('Verified 2 source programmes / 24 distinct candidate movements; recording identity unresolved.')
    return payload

if __name__=='__main__':audit()
