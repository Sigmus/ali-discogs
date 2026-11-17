"""Reproduce the complete title83 source/recording decisions without provider calls."""
import json
from qobuz_lead_review import ROOT, fingerprint
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate

ACCEPTED = ['3103644', '3729749', '6790241', '6900724', '12561696']


def validate_title83(report, diagnostic, rows, albums, reviews):
    frozen = [e for e in diagnostic['entries']
              if e['machine_observation_family'] == 'no_supported_title_or_catalogue_anchor']
    if (fingerprint(diagnostic) != report['diagnostic_sha256']
            or [e['discogs_id'] for e in frozen] != report['frozen_release_ids']
            or report['accepted_release_ids'] != ACCEPTED
            or [e['discogs_id'] for e in report['entries'] if e['outcome'] == 'probable'] != ACCEPTED
            or report['qobuz_requests'] != 0):
        raise ValueError('Frozen title83 diagnostic, scope or acceptance set changed')
    for original, entry in zip(frozen, report['entries']):
        if any(original[k] != entry[k] for k in ('target_sha256', 'source_sha256')):
            raise ValueError('Original title83 source identity changed')
        original_candidates = original['candidates']
        checks = entry['cached_alternative_checks']
        if [(c['album_id'], c['album_sha256']) for c in original_candidates] != [
                (c['album_id'], c['album_sha256']) for c in checks]:
            raise ValueError('Original title83 candidate scope changed')
    return validate(report, rows, albums, reviews, 83)


def main():
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
    report = json.loads((ROOT/'data/qobuz_title83_recording_audit.json').read_text())
    diagnostic = json.loads((ROOT/'data/qobuz_title151_diagnostic.json').read_text())
    print(json.dumps(validate_title83(report, diagnostic, rows, load_albums(), reviews)))


if __name__ == '__main__':
    main()
