"""Reproduce the four frozen composer/catalogue recording decisions offline."""
import json
from qobuz_lead_review import ROOT
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate


def main():
    rows={str(r['discogs_id']):r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    reviews={r['discogs_id']:r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
    report=json.loads((ROOT/'data/qobuz_focused4_recording_audit.json').read_text())
    if report['frozen_release_ids']!=['5163525','8079435','15438425','15527713']:
        raise ValueError('Focused4scope changed')
    print(json.dumps(validate(report,rows,load_albums(),reviews,4)))


if __name__=='__main__':main()
