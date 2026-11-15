"""Offline shadow triage of five cached photographer-credit cases; never publish."""
import copy
import gzip
import hashlib
import json
from qobuz_match import ROOT,evaluate
from qobuz_completeness import check_programme

IDS={'1638548','29719858','14398300','13708175','5987607'}


def run():
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    collection=ROOT/'data/collection_matches.json';role_path=ROOT/'data/discogs_credit_role_audit.json'
    rows={str(r['discogs_id']):r for r in json.loads(collection.read_text())}
    inv={r['discogs_id']:r for r in json.loads((ROOT/'data/qobuz_unmatched_audit.json').read_text())['entries']}
    role=json.loads(role_path.read_text());albums={};sources={}
    for p in sorted((ROOT/'data').glob('qobuz*.json.gz')):
        d=json.loads(gzip.decompress(p.read_bytes()))
        if not isinstance(d,dict):continue
        candidates=list(d.get('albums',{}).values()) if isinstance(d.get('albums'),dict) else []
        candidates += [r['album'] for r in d.get('metadata',[])]
        for a in candidates:
            if not a.get('tracks'):continue
            ts=a['tracks']['items'];aid=str(a['id'])
            if len(ts)!=a['tracks_count'] or len({t['id'] for t in ts})!=len(ts):raise ValueError('Incomplete metadata')
            if aid in albums and albums[aid]!=a:raise ValueError('Conflicting cached evidence')
            albums[aid]=a;sources[p.name]=digest(p)
    inventory=json.loads((ROOT/'data/qobuz_work_inventory.json').read_text());out=[]
    for case in role['affected']:
        rid=case['discogs_id']
        if rid not in IDS:continue
        if digest(ROOT/f'raw/discogs/releases/{rid}.json')!=case['source_sha256']:raise ValueError('Role-audit source changed')
        diff=case['changes']['performers'];removed=set(diff['before'])-set(diff['after']);row=rows[rid];shadow=copy.deepcopy(row)
        for field in ['performers','key_performers','ensembles']:shadow[field]=[p for p in shadow.get(field,[]) if p not in removed]
        candidates=[]
        for lead in inv[rid]['cached_candidates']:
            a=albums[lead['album_id']];e=evaluate(shadow,a);c=check_programme(shadow,a,e,inventory)
            candidates.append({'album_id':lead['album_id'],'before_coverage':lead['coverage'],'shadow_coverage':e['coverage'],'programme':e['programme'],'completeness':c})
        out.append({'discogs_id':rid,'source_sha256':case['source_sha256'],'excluded_for_diagnostic':sorted(removed),'false_key_performer_names':sorted(removed&set(row.get('key_performers',[]))),'source_roles':[a for a in case['source_roles'] if a['name'] in removed],'candidates':candidates})
    if {e['discogs_id'] for e in out}!=IDS:raise ValueError('Fixed triage scope changed')
    payload={'schema_version':1,'reviewed_on':'2026-11-15','collection_sha256':digest(collection),'role_audit_sha256':digest(role_path),'metadata_sources':sources,'entries':out,'limitations':['Shadow triage only, no publication/source changes or credit exclusions activated.','False normalized key-performer cases need explicit source review before extending reconciliation guards.','Full coverage is not completeness or recording identity; all other source musical credits remain required.']}
    (ROOT/'data/qobuz_photographer_credit_triage.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    print('Five cached cases triaged; no publication changes.')
    return payload

if __name__=='__main__':run()
