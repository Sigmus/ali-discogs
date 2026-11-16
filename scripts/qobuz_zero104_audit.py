"""Reproduce the frozen 104-case review without catalogue requests."""
import json
from qobuz_lead_review import ROOT
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate as validate_batch


def validate(report, rows, albums, reviews):
    result = validate_batch(report, rows, albums, reviews, expected_count=104)
    for entry in report['entries']:
        raw = json.loads((ROOT/f"raw/discogs/releases/{entry['discogs_id']}.json").read_text())
        for field, value in [('source_programme', raw['tracklist']),
                             ('source_credits', raw.get('extraartists', [])),
                             ('source_artists', raw.get('artists', [])),
                             ('source_notes', raw.get('notes', ''))]:
            if entry[field] != value:
                raise ValueError('Frozen source programme or credits changed')
        alternatives = entry['cached_alternative_checks']
        ids = [a['album_id'] for a in alternatives]
        if (ids != report['frozen_candidate_ids'][entry['discogs_id']]
                or len(set(ids)) != len(ids) or entry['review_album_id'] not in ids):
            raise ValueError('Missing or duplicate reviewed candidate')
        for alternative in alternatives:
            album = albums[alternative['album_id']]
            if alternative['track_titles'] != [t['title'] for t in album['tracks']['items']]:
                raise ValueError('Candidate title inventory changed')
        if not entry['finding'] or not entry['next_action']:
            raise ValueError('Every release needs a finding and next action')
    return result


def main():
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
    report = json.loads((ROOT/'data/qobuz_zero104_recording_audit.json').read_text())
    print(json.dumps(validate(report, rows, load_albums(), reviews)))


if __name__ == '__main__':
    main()
