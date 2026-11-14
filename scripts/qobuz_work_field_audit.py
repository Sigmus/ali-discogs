"""Offline diagnostic: explicit work metadata on bare movements, no publication writes."""
import copy
import gzip
import json
import re
from qobuz_lead_review import ROOT, fingerprint
from qobuz_match import agrees, catalogue, credits, evaluate, norm
from qobuz_completeness import check_programme


def with_work_context(album, performer, composer):
    contextual=copy.deepcopy(album)
    for t in contextual['tracks']['items']:
        work=t.get('work')
        if (isinstance(work,str) and catalogue(work) and
                re.match(r'^(?:[IVX]+|\d{1,2})\.\s+',t['title']) and
                not catalogue(t['title']) and agrees(performer,credits(t)) and
                norm((t.get('composer') or {}).get('name','')) == norm(composer)):
            t['title']=work+': '+t['title']
    return contextual


def main():
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    album=next(x['album'] for x in json.loads(gzip.decompress((ROOT/'data/qobuz_remaining_followup_metadata.json.gz').read_bytes()))['metadata'] if str(x['album']['id'])=='0002894552472')
    contextual=with_work_context(album,'Julius Katchen','Johannes Brahms')
    inventory=json.loads((ROOT/'data/qobuz_work_inventory.json').read_text())
    results=[]
    for rid in ['6264736','6347314','7291398']:
        after=evaluate(rows[rid],contextual)
        results.append({'discogs_id':rid,'base':evaluate(rows[rid],album),'with_explicit_work_context':after,
                        'completeness':check_programme(rows[rid],contextual,after,inventory)})
    report={'album_id':str(album['id']),'album_sha256':fingerprint(album),
            'publication_changed':False,'results':results,
            'limitations':['Diagnostic only. Explicit metadata is not independent recording identity.',
                'Work context never repairs missing performer credits or contradictory title catalogue numbers.',
                'Requires independent work inventory, recording review and broader false-positive audit before publication.']}
    (ROOT/'data/qobuz_work_field_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print([(r['discogs_id'],r['with_explicit_work_context']['coverage'],r['completeness']['status']) for r in results])


if __name__=='__main__':main()
