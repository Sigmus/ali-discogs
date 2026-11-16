"""Validate all38frozen partial-support recording decisions offline."""
import json
from qobuz_lead_review import ROOT
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate as validate_batch


def validate(report, rows, albums, reviews):
    return validate_batch(report, rows, albums, reviews, expected_count=38)


def main():
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
    report = json.loads((ROOT/'data/qobuz_partial38_recording_audit.json').read_text())
    print(json.dumps(validate(report, rows, load_albums(), reviews)))


if __name__ == '__main__':
    main()
