"""Offline assessment of the fixed four-album unmatched metadata batch."""
import gzip
import hashlib
import json
from qobuz_match import ROOT,evaluate
from qobuz_completeness import check_programme

def audit():
    path=ROOT/'data/qobuz_unmatched_metadata.json.gz';data=json.loads(gzip.decompress(path.read_bytes()))
    scope=ROOT/'data/qobuz_unmatched_metadata_scope.json'
    if data['scope_sha256']!=hashlib.sha256(scope.read_bytes()).hexdigest():raise ValueError('Scope changed')
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    inventory=json.loads((ROOT/'data/qobuz_work_inventory.json').read_text());entries=[]
    for x in data['metadata']:
        a=x['album'];tracks=a['tracks']['items'];rid=x['task']['discogs_id']
        if str(a['id'])!=x['task']['album_id'] or len(tracks)!=a['tracks_count'] or len({t['id'] for t in tracks})!=len(tracks):raise ValueError('Incomplete metadata')
        e=evaluate(rows[rid],a);c=check_programme(rows[rid],a,e,inventory)
        entries.append({'discogs_id':rid,'album_id':str(a['id']),'title':a['title'],'tracks':len(tracks),'assessment':e,'completeness':c})
    findings={'2996680': 'Opera title/track context and multilingual ensemble/individual cast requirements unresolved; not a confirmed missing or wrong recording.', '4365080': 'Dresden-version title and cast support need bounded review; target names include Karl Schmidt while candidate includes Reiner Suss/Rudolf Gonszar. Do not infer cast identity from title.', '8970069': 'Wrong orchestra: target London Symphony Orchestra, candidate Los Angeles Philharmonic. Exclude this candidate from promotion; same conductor/work is insufficient.', '10738828': 'Source hierarchy produces13units from two works; Nutcracker heading carries Op71a/Op71 and movement-group headings. Needs bounded target-unit interpretation, not invented extra works.'}
    for entry in entries: entry['finding']=findings[entry['discogs_id']]
    result={'schema_version':1,'metadata_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'entries':entries,'policy':'Offline evidence only. Full recording/version review required before publication; no automatic promotion.'}
    (ROOT/'data/qobuz_unmatched_metadata_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    for e in entries:print(e['discogs_id'],e['assessment']['status'],e['assessment']['coverage'],e['completeness']['status'])
    return result
if __name__=='__main__':audit()
