"""Verify shared follow-up scopes, cached tracks and reviewed findings offline."""
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'src'), str(ROOT/'scripts')]
from ali_discogs.spotify_programme import fingerprint, target_fingerprint
from qobuz_match import units, work_match


def verify():
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    summary={}
    for name in ['dvorak','broader']:
        path=ROOT/f'data/spotify_{name}_tracks.json.gz'
        archive=json.loads(gzip.decompress(path.read_bytes()))
        scope=json.loads((ROOT/f'data/spotify_{name}_scope.json').read_text())
        audit=json.loads((ROOT/f'data/spotify_{name}_audit.json').read_text())
        if archive['schema_version']!=1 or scope['schema_version']!=1 or audit['schema_version']!=1:
            raise ValueError('Unsupported follow-up schema')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=audit['track_archive_sha256']:
            raise ValueError('Follow-up archive changed; review again')
        tasks={(t['discogs_id'],t['album_id']):t for t in scope['entries']}
        if len(tasks)!=len(scope['entries']) or len(archive['albums'])!=len(tasks):
            raise ValueError('Follow-up scope mismatch')
        albums={}
        for album in archive['albums']:
            key=(album['discogs_id'],album['album_id'])
            task=tasks[key]
            if any(album[k]!=v for k,v in task.items()) or key in albums:
                raise ValueError('Changed follow-up album identity')
            tracks=album['tracks']
            if len(tracks)!=album['total_tracks'] or len({t['id'] for t in tracks})!=len(tracks):
                raise ValueError('Incomplete follow-up tracks')
            albums[key]=album
        if name=='broader':
            if hashlib.sha256((ROOT/'data/spotify_broader_scope.json').read_bytes()).hexdigest()!=audit['scope_sha256']:
                raise ValueError('Broader audit scope changed')
            if len(audit['entries'])!=len(albums):raise ValueError('Incomplete broader audit')
            for entry in audit['entries']:
                rid=entry['discogs_id'];album=albums[(rid,entry['album_id'])]
                if target_fingerprint(rows[rid])!=entry['target_sha256'] or fingerprint(album)!=entry['album_evidence_sha256']:
                    raise ValueError('Reviewed broader evidence changed')
                diagnostic=[{'target':title,'track_ids':[t['id'] for t in album['tracks'] if work_match(title,t['name'])]} for title in units(rows[rid])]
                if diagnostic!=entry['automatic_title_mapping_diagnostic_only']:
                    raise ValueError('Diagnostic mapping changed; inspect before updating the review')
        else:
            for candidate in audit['candidates']:
                album=albums[('6119238',candidate['album_id'])]
                for work in candidate['programme']:
                    tracks=[t for t in album['tracks'] if work_match(work['target'],t['name'])]
                    if [t['id'] for t in tracks]!=work['track_ids']:
                        raise ValueError('Dvorak programme mapping changed')
        summary[name]={'albums':len(albums),'tracks':sum(len(a['tracks']) for a in albums.values())}
    return summary


if __name__=='__main__':print(json.dumps(verify()))
