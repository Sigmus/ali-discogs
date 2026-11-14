"""Offline audit of the authorized nine-album/eleven-release metadata batch."""
import gzip
import hashlib
import json
from qobuz_match import ROOT,evaluate
from qobuz_completeness import check_programme
from qobuz_lead_review import target_fingerprint,fingerprint


FINDINGS = {'3167056': ('withheld', 'Opera part headings inflate units; track metadata lacks some required conductor/orchestra credits. Needs scoped opera/role review, not global credit inheritance.'), '3290970': ('withheld', 'Work titles have support but required individual cellist credits do not; ensemble name alone is insufficient.'), '6781135': ('withheld', 'Saved four-track file has no current title/credit support for the16-item target; not an accepted whole programme.'), '7194998': ('probable', 'Fourteen waltzes bound one-to-one in LP order; explicit posthumous tokens reviewed, three bonus pieces excluded; July1950 provenance supported.'), '11412875': ('withheld', 'Four candidate movements; duplicate target Allegro labels need source-position mapping before completeness can be established.'), '1458083': ('withheld', 'Target normalized as one umbrella heading;30track BWV programme requires independently validated source hierarchy interpretation.'), '10175959': ('probable', 'Three complete Brahms movements with Kreisler/Barbirolli/London Philharmonic; recording-family lead, exact transfer unverified.'), '5254294': ('withheld', 'Several work titles present, but required credits and KA.226 catalogue correspondence unresolved; no general ensemble alias.'), '6264736': ('withheld', 'Scherzo supported; target Op.5 sonata has no current matching title support in the saved file.'), '6347314': ('withheld', 'Waltz title support alone does not cover listed rhapsodies/ballades; exact scope unresolved.'), '7291398': ('withheld', 'Neither requested sonata currently has title/work support in this saved file; no title-similarity promotion.')}

def audit():
    scope_path=ROOT/'data/qobuz_remaining_metadata_followup_scope.json'
    evidence_path=ROOT/'data/qobuz_remaining_followup_metadata.json.gz'
    scope=json.loads(scope_path.read_text());data=json.loads(gzip.decompress(evidence_path.read_bytes()))
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    if data['scope_sha256']!=digest(scope_path) or data['completed']!=data['total'] or data['total']!=9:
        raise ValueError('Incomplete/frozen metadata evidence changed')
    if len(scope['entries'])!=9 or len(data['metadata'])!=9 or len({str(x['album']['id']) for x in data['metadata']})!=9:
        raise ValueError('Missing/duplicate metadata albums')
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    if digest(ROOT/'data/collection_matches.json')!=scope['collection_sha256']:raise ValueError('Collection changed')
    inventory=json.loads((ROOT/'data/qobuz_work_inventory.json').read_text());entries=[]
    for source,record in zip(scope['entries'],data['metadata']):
        a=record['album'];tracks=a['tracks']['items']
        if record['task']!={'discogs_id':source['discogs_ids'][0],'album_id':source['album_id']} or str(a['id'])!=source['album_id'] or len(tracks)!=a['tracks_count'] or len({t['id'] for t in tracks})!=len(tracks):
            raise ValueError('Incomplete/mismatched metadata task')
        for rid in source['discogs_ids']:
            row=rows[rid];assessment=evaluate(row,a);completeness=check_programme(row,a,assessment,inventory)
            entries.append({'discogs_id':rid,'album_id':str(a['id']),'target_sha256':target_fingerprint(row),'album_sha256':fingerprint(a),'target_title':row['title'],'candidate_title':a['title'],'track_count':len(tracks),'assessment':assessment,'completeness':completeness})
    for entry in entries:
        entry['review_decision'],entry['finding']=FINDINGS[entry['discogs_id']]
    if len(entries)!=11:raise ValueError('Release scope changed')
    result={'schema_version':1,'reviewed_on':'2026-11-14','scope_sha256':digest(scope_path),'metadata_sha256':digest(evidence_path),'inventory_sha256':digest(ROOT/'data/qobuz_work_inventory.json'),'entries':entries,'policy':'Offline structural screen, not match acceptance. Missing support is unresolved, not catalogue absence. Full recording/programme review required.'}
    result['summary']={'metadata_albums':9,'complete_tracks':sum(len(x['album']['tracks']['items']) for x in data['metadata']),'reviewed_release_leads':len(entries),'new_probables':sum(e['review_decision']=='probable' for e in entries),'withheld':sum(e['review_decision']=='withheld' for e in entries)}
    (ROOT/'data/qobuz_remaining_followup_audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    return result

if __name__=='__main__':
    for e in audit()['entries']:print(e['discogs_id'],e['assessment']['covered'],e['assessment']['target_count'],e['completeness']['status'])
