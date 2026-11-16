"""Read-only source-bound collective identity proposal; not a match adapter."""
import hashlib
import json
from qobuz_lead_review import ROOT, fingerprint, target_fingerprint
from qobuz_credit_role_audit import load_albums
from qobuz_source_leaf_review import source_leaves
from qobuz_match import agrees, credits
from qobuz_work_groups import role_entries
from qobuz_composer_identity import composer_key

RID = '8535848'
AID = 'wtgrq4n06qkbb'
MEMBERS = ['Eugene Istomin', 'Isaac Stern', 'Leonard Rose']
COLLECTIVE = 'The Istomin/Stern/Rose Trio'


def inspect(row, raw, album):
    leaves = source_leaves(raw)
    tracks = album['tracks']['items']
    if len(leaves) != 8 or len(tracks) != 8 or album['tracks_count'] != 8 or len({t['id'] for t in tracks}) != 8:
        raise ValueError('Complete eight-movement source and candidate required')
    result = []
    for leaf, track in zip(leaves, tracks):
        minutes, seconds = map(int, leaf['duration'].split(':'))
        duration = minutes*60+seconds
        names = credits(track)
        missing = [n for n in MEMBERS if not agrees(n, names)]
        composers = {composer_key(n) for n, roles in role_entries(track) if 'composer' in roles}
        result.append({'source_path':leaf['path'], 'source_work':leaf['source_work'],
            'source_title':leaf['title'], 'source_position':leaf['position'],
            'source_seconds':duration, 'track_id':track['id'], 'track_title':track['title'],
            'digital_work':track['work'], 'digital_seconds':track['duration'],
            'delta_seconds':track['duration']-duration,
            'within_existing_tolerance':abs(track['duration']-duration)<=max(5,.03*duration),
            'missing_members':missing, 'collective_positively_declared':agrees(COLLECTIVE,names),
            'composer_positive':composers=={composer_key('Felix Mendelssohn-Bartholdy')},
            'track_sha256':fingerprint(track)})
    return {'schema_version':1,'reviewed_on':'2026-11-16','discogs_id':RID,'album_id':AID,
        'target_sha256':target_fingerprint(row),'source_sha256':fingerprint(raw),
        'album_sha256':fingerprint(album),'source_outline_sha256':fingerprint(raw['tracklist']),
        'required_members':MEMBERS,'collective':COLLECTIVE,'bindings':result,
        'summary':{'source_leaves':8,'candidate_tracks':8,
            'all_members_positively_credited':all(not b['missing_members'] for b in result),
            'all_composer_checks_pass':all(b['composer_positive'] for b in result),
            'all_source_timings_pass':all(b['within_existing_tolerance'] for b in result),
            'collective_declarations':sum(b['collective_positively_declared'] for b in result)},
        'proposal_status':'not_adopted','publication_changed':False,'qobuz_requests':0,
        'limitation':'Ordered source/candidate mapping and positive members support a proposed bounded collective decomposition. No existing review kind encodes that rule. No acceptance or exact pressing/take/transfer claim.'}


def main():
    row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])==RID)
    raw=json.loads((ROOT/f'raw/discogs/releases/{RID}.json').read_text())
    report=inspect(row,raw,load_albums()[AID])
    evidence=ROOT/'data/review_sources/trio-8535848/primary-observation.json'
    report['external_source_file']={'path':str(evidence.relative_to(ROOT)),'sha256':hashlib.sha256(evidence.read_bytes()).hexdigest()}
    (ROOT/'data/qobuz_trio_identity_diagnostic.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report['summary']))


if __name__=='__main__':main()
