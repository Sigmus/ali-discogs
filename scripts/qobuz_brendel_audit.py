"""Reproduce the source-bound Brendel programme/timing diagnostic without provider calls."""
import hashlib
import json
from qobuz_lead_review import ROOT, assess, fingerprint
from qobuz_snapshot import load_snapshot


def audit(row, raw, album, review):
    if fingerprint(raw)!=review['source_canonical_sha256']:
        raise ValueError('Reviewed Brendel source changed')
    result,evidence=assess(row,album,review)
    if not result['eligible']:raise ValueError('Brendel recording review is unresolved')
    assignments={w['target']:w['track_ids'] for w in result['completeness']['works']}
    tracks={t['id']:t for t in album['tracks']['items']};bands={};works=[];used=[]
    for source in raw['tracklist']:
        parts=source.get('sub_tracks') or [source];ids=assignments[source['title']]
        if len(parts)!=len(ids):raise ValueError('A source movement is unaccounted for')
        work=[]
        for part,track_id in zip(parts,ids):
            if part['position'] in bands:raise ValueError('Duplicate source position')
            track=tracks[track_id];entry={'source_position':part['position'],'source_title':part['title'],
                'source_duration_field':part['duration'],'track_id':track_id,'track_title':track['title'],
                'track_sha256':fingerprint(track),'digital_seconds':track['duration']}
            bands[part['position']]=entry;work.append(entry);used.append(track_id)
        works.append({'source_title':source['title'],'reviewed_work_title':review['target_title_corrections'][source['title']],
                      'source_bands':work})
    groups=[];positions=[]
    for spec in review['source_timing_groups']:
        if spec['target'] not in assignments:raise ValueError('Unknown timing-group work')
        if any(bands[p]['track_id'] not in assignments[spec['target']] for p in spec['positions']):
            raise ValueError('Timing group crosses source works')
        if spec['duration_field_position'] not in spec['positions']:raise ValueError('Timing field outside group')
        field=bands[spec['duration_field_position']]['source_duration_field']
        minutes,seconds=map(int,field.split(':'));reference=minutes*60+seconds
        duration=sum(bands[p]['digital_seconds'] for p in spec['positions'])
        groups.append({**spec,'source_seconds':reference,'digital_seconds':duration,'difference_seconds':duration-reference})
        positions.extend(spec['positions'])
    if len(positions)!=len(set(positions)) or set(positions)!=set(bands):
        raise ValueError('Every source position needs exactly one diagnostic timing scope')
    if len(used)!=len(set(used)):raise ValueError('Digital movement reused')
    return {'schema_version':1,'reviewed_on':'2026-11-15','discogs_id':review['discogs_id'],
            'album_id':review['album_id'],'review_fingerprint':fingerprint(review),
            'source_sha256':review['source_sha256'],'target_sha256':review['target_sha256'],
            'album_sha256':review['album_sha256'],'external_source_files':review['external_source_files'],
            'work_count':len(works),'distinct_tracks':len(used),
            'extra_track_ids':[t['id'] for t in album['tracks']['items'] if t['id'] not in used],
            'works':works,'timing_groups':groups,
            'timing_scope_limitation':'Only marked groups have inspected label images. Other joint-timing interpretations remain diagnostic inference, not source corrections or recording-identity proof.',
            'limitations':review['limitations']}


def main():
    review=next(r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases'] if r['discogs_id']=='5403356')
    path=ROOT/'raw/discogs/releases/5403356.json'
    if hashlib.sha256(path.read_bytes()).hexdigest()!=review['source_sha256']:raise ValueError('Source file changed')
    row=next(r for r in json.loads((ROOT/'data/collection_matches.json').read_text()) if str(r['discogs_id'])==review['discogs_id'])
    result=audit(row,json.loads(path.read_bytes()),load_snapshot()['albums'][review['album_id']],review)
    (ROOT/'data/qobuz_brendel_programme_audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'works':result['work_count'],'tracks':result['distinct_tracks'],'timing_groups':len(result['timing_groups']),
                      'max_group_difference_seconds':max(abs(g['difference_seconds']) for g in result['timing_groups'])}))

if __name__=='__main__':main()
