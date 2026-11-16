"""Validate the complete eighteen-release cached recording review batch."""
import json
from qobuz_lead_review import ROOT
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate


def main():
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    reviews={r['discogs_id']:r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
    report=json.loads((ROOT/'data/qobuz_musician18_recording_audit.json').read_text())
    print(json.dumps(validate(report,rows,load_albums(),reviews,expected_count=18)))


if __name__=='__main__':main()
