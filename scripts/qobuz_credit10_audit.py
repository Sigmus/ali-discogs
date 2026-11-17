"""Reproduce the first ten recording decisions from the frozen credit150 cohort."""
import hashlib
import json
from qobuz_lead_review import ROOT
from qobuz_credit_role_audit import load_albums
from qobuz_fullsupport16_audit import validate

IDS = ['3100828', '7228304', '11077579', '12218789', '5085113',
       '10675304', '4079723', '8949471', '12872526', '13406445']


def main():
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    reviews = {r['discogs_id']: r for r in json.loads((ROOT/'data/qobuz_remaining_recording_reviews.json').read_text())['releases']}
    report = json.loads((ROOT/'data/qobuz_credit10_recording_audit.json').read_text())
    if (report['frozen_release_ids'] != IDS or report['accepted_release_ids'] != ['4079723']
            or report['parent_scope_sha256'] != hashlib.sha256((ROOT/'data/qobuz_credit150_scope.json').read_bytes()).hexdigest()):
        raise ValueError('Frozen credit10 scope changed')
    print(json.dumps(validate(report, rows, load_albums(), reviews, 10)))


if __name__ == '__main__':
    main()
