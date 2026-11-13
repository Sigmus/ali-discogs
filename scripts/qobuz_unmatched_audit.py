"""Offline inventory of remaining unmatched releases using all shared search evidence."""
import gzip
import hashlib
import json
from collections import Counter
from qobuz_match import ROOT,evaluate
from qobuz_snapshot import load_snapshot
from qobuz_completeness import check_programme

def audit():
    snapshot=load_snapshot();albums=dict(snapshot['albums'])
    hits={rid:{str(a['id']) for a in x['search']['albums']['items']} for rid,x in snapshot['searches'].items()}
    sources=['qobuz_evidence.json.gz','qobuz_comparison_evidence.json.gz','qobuz_round2_metadata.json.gz','qobuz_query_trial_metadata.json.gz','qobuz_round2_searches.json.gz','qobuz_query_trial_searches.json.gz','qobuz_query_validation.json.gz','qobuz_unmatched_metadata.json.gz','qobuz_metadata_needed.json.gz']
    for name in sources[1:]:
        data=json.loads(gzip.decompress((ROOT/'data'/name).read_bytes()))
        for x in data.get('metadata',[]):
            a=x['album'];aid=str(a['id']);tracks=a['tracks']['items']
            if aid!=x['task']['album_id'] or len(tracks)!=a['tracks_count'] or len({t['id'] for t in tracks})!=len(tracks):raise ValueError('Incomplete shared metadata')
            if aid in albums and albums[aid]!=a:raise ValueError('Conflicting metadata')
            albums[aid]=a
        for x in data.get('searches',[]):
            hits.setdefault(x['task']['discogs_id'],set()).update(str(a['id']) for a in x['search']['albums']['items'])
        for x in data.get('results',[]):
            hits.setdefault(x['task']['discogs_id'],set()).update(str(a['id']) for a in x['albums'])
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    published=json.loads((ROOT/'data/qobuz_matches.json').read_text())['releases']
    rejected={(r['discogs_id'],r['album_id']) for r in json.loads((ROOT/'data/qobuz_lead_reviews.json').read_text())['releases'] if r['decision'].startswith('reject')}
    withheld=set()
    for name in ('qobuz_binding_reviews.json','qobuz_opera_recording_reviews.json'):
        for review in json.loads((ROOT/'data'/name).read_text())['releases']:
            if review['decision']=='withhold':
                withheld.add((review['discogs_id'],review['album_id']))
    inventory=json.loads((ROOT/'data/qobuz_work_inventory.json').read_text());entries=[]
    for rid in sorted(rows,key=int):
        if published[rid]['status']!='unchecked':continue
        candidates=[]
        for aid in sorted(hits.get(rid,set())):
            if aid not in albums:continue
            e=evaluate(rows[rid],albums[aid]);c=check_programme(rows[rid],albums[aid],e,inventory)
            candidates.append({'album_id':aid,'title':albums[aid]['title'],'coverage':e['coverage'],'status':e['status'],'completeness':c['status'],'reviewed_rejected':(rid,aid) in rejected,'reviewed_withheld':(rid,aid) in withheld,'programme':e['programme']})
        candidates.sort(key=lambda c:(c['status']=='unchecked',-c['coverage'],c['album_id']))
        usable=[c for c in candidates if c['status']!='unchecked' and not c['reviewed_rejected'] and not c['reviewed_withheld']]
        category=('no_saved_hits' if not hits.get(rid) else 'metadata_needed' if not candidates else 'reviewed_withheld' if not usable and any(c['reviewed_withheld'] for c in candidates) else 'work_or_credit_unresolved' if not usable else 'completeness_review_needed' if not any(c['completeness']=='complete' for c in usable) else 'recording_review_needed')
        entries.append({'discogs_id':rid,'title':rows[rid]['title'],'category':category,'saved_hits':len(hits.get(rid,set())),'uncached_hits':len(hits.get(rid,set())-albums.keys()),'cached_candidates':candidates})
    report={'schema_version':1,'reviewed_on':'2026-11-13','source_hashes':{name:hashlib.sha256((ROOT/'data'/name).read_bytes()).hexdigest() for name in [*sources,'collection_matches.json','qobuz_matches.json','qobuz_work_inventory.json','qobuz_binding_reviews.json','qobuz_opera_recording_reviews.json']},'summary':dict(Counter(e['category'] for e in entries)),'unmatched_unique_releases':len(entries),'entries':entries,'limitations':['Offline triage after the published eight-album pass, not independent recording validation or catalogue absence.','No new searches, metadata fetches, publication changes or automatic acceptance.','Recorded withholds stay in the inventory as reviewed_withheld and are not open leads.','Categories prioritize available cached evidence; a release may also have uncached alternatives.']}
    (ROOT/'data/qobuz_unmatched_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report['summary']));return report
if __name__=='__main__':audit()
