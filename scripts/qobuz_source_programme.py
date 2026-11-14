"""Fail-closed publication holds for reviewed incomplete source programmes."""
from copy import deepcopy
from functools import lru_cache
import hashlib
import json
from qobuz_lead_review import ROOT,target_fingerprint

PATH=ROOT/'data/qobuz_source_programme_reviews.json'


def validate_hold(row,raw_bytes,review):
    if (str(row['discogs_id'])!=review['discogs_id'] or
            target_fingerprint(row)!=review['target_sha256'] or
            hashlib.sha256(raw_bytes).hexdigest()!=review['source_sha256'] or
            review['decision']!='withhold-incomplete-source'):
        raise ValueError('Reviewed source programme changed; reconcile before publication')
    raw=json.loads(raw_bytes)
    if str(raw['id'])!=review['discogs_id'] or review['catalogue_number'] not in [x['catno'] for x in raw['labels']]:
        raise ValueError('Reviewed source edition changed')
    if (len(raw['tracklist'])!=review['saved_track_count'] or not review['missing_tracks'] or
            review['physical_track_count']!=review['saved_track_count']+len(review['missing_tracks'])):
        raise ValueError('Source discrepancy inventory changed')
    urls={i['uri'] for i in raw['images']}
    if not review['external_source_files']:
        raise ValueError('An incomplete-source hold needs inspected evidence')
    for item in review['external_source_files']:
        path=(ROOT/item['path']).resolve()
        if (not path.is_relative_to((ROOT/'data/review_sources').resolve()) or
                item['url'] not in urls or hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']):
            raise ValueError('Inspected source programme evidence changed')
    return {k:deepcopy(review[k]) for k in ['reason','saved_track_count','physical_track_count','missing_tracks','sources']}


@lru_cache(maxsize=1)
def load_holds():
    data=json.loads(PATH.read_text())
    if data['schema_version']!=1:raise ValueError('Unsupported source programme schema')
    result={}
    for review in data['releases']:
        rid=review['discogs_id']
        if not rid.isdecimal() or rid in result:raise ValueError('Invalid/duplicate source programme hold')
        result[rid]=(review,(ROOT/f'raw/discogs/releases/{rid}.json').read_bytes())
    return result


def programme_hold(row):
    item=load_holds().get(str(row['discogs_id']))
    return validate_hold(row,item[1],item[0]) if item else None


def withhold_candidates(candidates,hold):
    result=deepcopy(candidates)
    for candidate in result:
        candidate.update(status='unchecked',confidence=None)
        candidate['reasons']=[hold['reason'],*candidate.get('reasons',[])]
        candidate['source_programme_review']='incomplete-source'
    return result
