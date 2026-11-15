"""Source-bound credit corrections within an explicit recording review, never global."""
from qobuz_source_reconciliation import validate_nonperforming_credit
from qobuz_target_credits import musical


def requirements(row,raw,evidence,review,assigned):
    spec=review.get('source_credit_reconciliation')
    if spec is None:return {target:review['required_performers'] for target in assigned}
    excluded={validate_nonperforming_credit(row,raw,c) for c in spec['nonperformers']}
    if len(excluded)!=len(spec['nonperformers']):raise ValueError('Duplicate credit exclusion')
    scopes={}
    for entry in spec['work_scopes']:
        name=entry['name'];role=entry['role'];targets=entry['targets']
        found=[g['title'] for g in raw['tracklist'] if any(a['name']==name and a.get('role')==role for a in g.get('extraartists',[]))]
        if name in scopes or name in excluded or not musical(role) or not found or targets!=found or any(t not in assigned for t in targets):
            raise ValueError('Work-scoped performer lacks exact source assignment')
        if name in row.get('key_performers',[]) or name==row.get('conductor') or name in row.get('ensembles',[]):
            raise ValueError('Cannot rescope a principal performer or ensemble')
        scopes[name]=set(targets)
    baseline=evidence['required_performers']
    if not (excluded|scopes.keys()) <= set(baseline):raise ValueError('Credit correction outside baseline requirements')
    global_names=[name for name in baseline if name not in excluded and name not in scopes]
    if not global_names or review['required_performers']!=global_names:raise ValueError('Unreviewed global credit omission')
    by_target={}
    for item in evidence['programme']:
        # Work-scoped instrumental soloists already required by source derivation
        # remain required. Nothing absent from the digital credits is borrowed.
        names=[n for n in item.get('required_performers',baseline) if n not in excluded and n not in scopes]
        names += [n for n,targets in scopes.items() if item['target'] in targets and n not in names]
        by_target[item['target']]=names
    if by_target!=spec['expected_required_performers']:raise ValueError('Reviewed work credit requirements changed')
    evidence['required_performers']=list(dict.fromkeys(n for names in by_target.values() for n in names))
    for item in evidence['programme']:item['required_performers']=by_target[item['target']]
    return by_target
