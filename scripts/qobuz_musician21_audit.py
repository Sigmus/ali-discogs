"""Frozen cached-credit triage. Findings are review leads, never match decisions."""
import hashlib
import json
from collections import Counter
from qobuz_credit_role_audit import load_albums
from qobuz_lead_review import ROOT, fingerprint, target_fingerprint

# Dominant blocker only; overlapping issues remain explicit in each finding.
FINDINGS = {
 '1012732': ('incomplete_or_conflicting_recording', 'Four-symphony candidate omits the violin concerto, Haydn Variations and Requiem. Global singers/choir and roleless orchestra strings add credit gaps; scope cleanup cannot supply missing works.'),
 '3788392': ('missing_positive_credit', 'Brandenburg programme exists, but inspected track declarations omit Abbado and I Solisti del Teatro Alla Scala. Album-level names cannot silently replace positive track credits.'),
 '3798658': ('incomplete_or_conflicting_recording', 'Opera Intermezzi supplies excerpts with Berlin/Karajan, not the complete La Scala operas and source cast.'),
 '4519809': ('missing_positive_credit', 'Compatible Agon/Canticum candidate declares orchestra/chorus as Associated Performer, with a chorus-name difference and source scope issues. Alternative Gielen cast differs; no role waiver.'),
 '5521001': ('missing_positive_credit', 'Compatible Walter Requiem has Westminster Choir versus source Westminster Symphonic Choir and omits chorus master John Finley Williamson. An ensemble-name alias alone is insufficient.'),
 '5806510': ('missing_positive_credit', 'Savaria cantata candidate does not declare all explicitly named source instrumentalists, including Falvay and Balazs. Ensemble membership cannot replace their required credits.'),
 '6052186': ('incomplete_or_conflicting_recording', 'Source names four orchestras; the compatible complete Brahms cycle declares Berlin. Source work allocation must be established; do not delete the other source ensembles.'),
 '6907296': ('incomplete_or_conflicting_recording', 'Saved solo Serkin Bach anthology supports solo couplings, not both three-piano concertos with the source musicians. Work scope cannot fill the missing programme.'),
 '7118750': ('incomplete_or_conflicting_recording', 'Anthology Mozart No.5 tracks have Stern/Szell or Goldberg/Kletzki; Heifetz appears on a different work. Never borrow album-wide cast across works.'),
 '7956843': ('ensemble_identity_unresolved', 'Milstein/Piatigorsky/Reiner candidate b949vmcya5zta declares RCA Victor Symphony Orchestra, not the source Robin Hood Dell Orchestra of Philadelphia. This is not a simple Philadelphia spelling repair; require recording-specific historical proof.'),
 '8199658': ('missing_positive_credit', 'Source Zagreb ensemble has an Italian ANV, but compatible nine-track candidate uses Associated Performer for I Solisti di Zagreb. Identity repair alone does not satisfy positive ensemble roles; other saved albums do not establish the whole source programme.'),
 '8535848': ('collective_identity_unresolved', 'Both Mendelssohn trios have individual Istomin/Stern/Rose instrument credits, but no source collective The Istomin/Stern/Rose Trio declaration. Investigate source-bound collective decomposition without removing any member or adopting a general ensemble waiver.'),
 '8823847': ('incomplete_or_conflicting_recording', 'Relevant Strauss anthology tracks declare Szell or Bohm with Vienna/Dresden, not source Karajan/Berlin. Same work titles do not establish the recording.'),
 '8971581': ('missing_positive_credit', 'Stern-directed source specifies Columbia Chamber/String orchestras and Zakin on Haydn. Compatible track strings omit required declarations; Szell/Cleveland Mozart alternative is a different cast.'),
 '9932683': ('incomplete_or_conflicting_recording', 'Saved complete Tchaikovsky cycle is Abbado/Chicago; source names Tilson Thomas, Atzmon and Mravinsky with other orchestras. No generic cast repair.'),
 '10301402': ('incomplete_or_conflicting_recording', 'Four-symphony Brahms candidate omits concerto, variations and Requiem from the source box. Global cast scope and roleless ensemble strings are additional blockers.'),
 '10344924': ('incomplete_or_conflicting_recording', 'Octet candidate has all eight named players but no source Marlboro ensemble and pairs Mozart Concertone, not the source Mendelssohn Trio. Other candidate pairs Italian Symphony with Octet. Do not combine digital editions.'),
 '11876845': ('bounded_name_review_lead', 'dds4ccexc73aa declares Francescatti violin, Bernstein conductor and New York Philharmonic Orchestra on Brahms Op.77; source says New York Philharmonic. Prioritize independent ensemble/recording corroboration and complete source-band binding. Kremer/Vienna alternatives conflict.'),
 '13792797': ('incomplete_or_conflicting_recording', 'Saved Richter concerto uses Abendroth/USSR Symphony, not Muti/Philharmonia, and does not establish the source Andante Favori coupling.'),
 '20451211': ('incomplete_or_conflicting_recording', 'Modern Borodin quartet candidate has a different named lineup, lacks source pianist Luba Edlina and does not establish the Stravinsky coupling. Ensemble label does not replace historic members.'),
 '21490438': ('bounded_name_review_lead', 'q1ipa0nqgx7qa declares Fischer piano, Furtwangler conductor and The Philharmonia orchestra for Emperor. Source says Philharmonia Orchestra. Prioritize independent name/recording corroboration plus complete source-band/timing review.'),
}


def build(diagnostic, rows, albums):
    scope = [e for e in diagnostic['entries'] if e['machine_observation_family'] == 'work_title_support_but_musician_gap']
    if len(scope) != 21 or {e['discogs_id'] for e in scope} != set(FINDINGS):
        raise ValueError('Frozen musician scope changed')
    entries = []
    for entry in scope:
        rid = entry['discogs_id']
        source = (ROOT/f'raw/discogs/releases/{rid}.json').read_bytes()
        raw = json.loads(source)
        category, finding = FINDINGS[rid]
        candidates = []
        for candidate in entry['candidates']:
            album = albums[candidate['album_id']]
            candidates.append({'album_id': candidate['album_id'], 'title': album['title'],
                'album_sha256': fingerprint(album), 'tracks_count': album['tracks_count'],
                'track_manifest_sha256': fingerprint(album['tracks']['items']),
                'diagnostic_observations': candidate['observations']})
        entries.append({'discogs_id': rid, 'title': rows[rid]['title'],
            'target_sha256': target_fingerprint(rows[rid]),
            'source_sha256': hashlib.sha256(source).hexdigest(),
            'source_artists': raw.get('artists', []), 'source_credits': raw.get('extraartists', []),
            'source_programme': raw['tracklist'], 'category': category, 'finding': finding,
            'workflow': 'corroborate_and_bind' if category == 'bounded_name_review_lead' else 'retain_requirements',
            'candidates': candidates})
    return {'schema_version': 1, 'reviewed_on': '2026-11-16',
        'kind': 'cached_triage_not_recording_decisions', 'qobuz_requests': 0,
        'publication_changed': False, 'policy_changed': False,
        'diagnostic_sha256': fingerprint(diagnostic), 'frozen_release_ids': list(FINDINGS),
        'summary': dict(Counter(e['category'] for e in entries)),
        'next_review_ids': ['11876845', '21490438'], 'entries': entries,
        'limitations': ['Dominant categories overlap; findings do not prove absent recordings.',
            'No acceptance, alias, missing-member waiver or Associated Performer policy adopted.',
            'Name leads still need independent source evidence, full binding, timings and all positive credits.',
            'Original diagnostic, source/cache and saved match decisions remain unchanged.']}


def main():
    diagnostic = json.loads((ROOT/'data/qobuz_title151_diagnostic.json').read_text())
    rows = {str(r['discogs_id']): r for r in json.loads((ROOT/'data/collection_matches.json').read_text())}
    report = build(diagnostic, rows, load_albums())
    (ROOT/'data/qobuz_musician21_audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report['summary']))


if __name__ == '__main__':
    main()
