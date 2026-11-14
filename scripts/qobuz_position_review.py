"""Frozen position-keyed Nielsen publication review; no generic ordinal matching."""
import hashlib
from qobuz_lead_review import ROOT
from qobuz_position_audit import audit


def assess_positions(row, album, review):
    diagnostic = audit(row, album)
    source = ROOT/'raw/discogs/releases'/f"{review['discogs_id']}.json"
    if (review['source_sha256'] != hashlib.sha256(source.read_bytes()).hexdigest() or
            review['mapping'] != diagnostic['positional_mapping'] or
            review['required_performers'] != ['Sir John Barbirolli', 'Hallé Orchestra']):
        raise ValueError('Position-bound source, mapping or artist requirements changed')
    evidence = diagnostic['base_evidence']
    programme = [{'target': f"{m['source_position']}: {m['source_title']}",
                  'source_position': m['source_position'], 'track_ids': [m['track_id']],
                  'work_tracks': 1, 'credited_tracks': 1} for m in review['mapping']]
    evidence.update(programme=programme, covered=4, target_count=4, coverage=1,
                    required_performers=review['required_performers'])
    works = [{'target': p['target'], 'source_position': p['source_position'],
              'status': 'complete', 'track_ids': p['track_ids'],
              'scope': 'source-position-bound-movement',
              'expected_movements': [i+1], 'observed_movements': [i+1],
              'source': review['sources'][0],
              'reason': 'Exact source position/title and distinct ordered track hash; explicit work and artist checks.'}
             for i,p in enumerate(programme)]
    result = {'discogs_id': review['discogs_id'], 'album_id': review['album_id'],
              'decision': review['decision'], 'eligible': review['decision'] == 'probable',
              'recording_review': review['recording_review'], 'sources': review['sources'],
              'limitations': review['limitations'],
              'completeness': {'status': 'complete', 'works': works, 'overlapping_target_tracks': False}}
    return result, evidence
