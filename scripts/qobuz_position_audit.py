"""Offline diagnostic for a frozen Nielsen lead; never changes publication labels.

Position is an additional identity dimension, not permission to pair arbitrary
tracks by row number. Only the exact saved four-movement scope is accepted.
"""
import gzip
import hashlib
import json
from qobuz_lead_review import ROOT, fingerprint, target_fingerprint
from qobuz_match import agrees, credits, evaluate, norm

TARGET = '11412875'
ALBUM = 'v96ulyegxutlc'
POSITIONS = ['Aa', 'Ab', 'Ba', 'Bb']
TEMPOS = ['Allegro', 'Poco Allegretto', 'Poco Adagio Quasi Andante', 'Allegro']
ROMANS = ['I', 'II', 'III', 'IV']


def audit(row, album):
    if str(row['discogs_id']) != TARGET or str(album['id']) != ALBUM:
        raise ValueError('Outside frozen diagnostic scope')
    source = row['tracklist']
    tracks = album['tracks']['items']
    if ([t.get('position') for t in source] != POSITIONS or
            [norm(t['title']) for t in source] != [norm(t) for t in TEMPOS] or
            len(tracks) != 4 or album['tracks_count'] != 4 or
            album['tracks']['total'] != 4 or len({t['id'] for t in tracks}) != 4):
        raise ValueError('Source positions or complete track inventory changed')
    required = ['Sir John Barbirolli', 'Hallé Orchestra']
    mapping = []
    for index, (target, track) in enumerate(zip(source, tracks)):
        expected = f'Symphony No. 4, Op. 29 "The Inextinguishable": {ROMANS[index]}. {TEMPOS[index]}'
        if (norm(track['title']) != norm(expected) or track['track_number'] != index + 1 or
                track['media_number'] != 1 or
                not all(agrees(name, credits(track)) for name in required) or
                norm((track.get('composer') or {}).get('name', '')) != 'carl nielsen'):
            raise ValueError('Movement identity, order, composer or required artist changed')
        mapping.append({'source_position': target['position'], 'source_title': target['title'],
                        'movement': index + 1, 'track_id': track['id'],
                        'track_sha256': fingerprint(track), 'track_title': track['title']})
    return {'discogs_id': TARGET, 'album_id': ALBUM,
            'target_sha256': target_fingerprint(row), 'album_sha256': fingerprint(album),
            'base_evidence': evaluate(row, album), 'positional_mapping': mapping,
            'structurally_supported': True, 'publication_changed': False,
            'decision': 'withheld_pending_position_keyed_publication_review',
            'limitations': ['Ordered programme and artist agreement do not establish exact takes or mastering.',
                'Title-keyed review dictionaries cannot represent Aa and Bb as separate Allegro units.',
                'No generic ordinal pairing rule or new publication review kind is enabled.']}


def main():
    rows = json.loads((ROOT/'data/collection_matches.json').read_text())
    evidence_path = ROOT/'data/qobuz_remaining_followup_metadata.json.gz'
    metadata = json.loads(gzip.decompress(evidence_path.read_bytes()))['metadata']
    row = next(r for r in rows if str(r['discogs_id']) == TARGET)
    album = next(x['album'] for x in metadata if str(x['album']['id']) == ALBUM)
    report = audit(row, album)
    report['metadata_archive_sha256'] = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
    (ROOT/'data/qobuz_position_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print('Nielsen: four distinct position-bound movements supported; publication unchanged.')


if __name__ == '__main__':
    main()
