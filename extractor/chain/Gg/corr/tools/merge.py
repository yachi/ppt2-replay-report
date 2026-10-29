# Merge checker proposals with skeptic verdicts -> corr/event-corrections.json + corr/cells.json
import json
O = '/private/tmp/claude-501/Gg/corr/out'; C = '/private/tmp/claude-501/Gg/corr'
L = lambda f: json.load(open(f'{O}/{f}.json'))
ev, cells, frz = [], [], []
def tag(x, s): x = dict(x); x['source'] = f"{s}: {x.get('source','')}"; return x
# group 0: v0 reviews {kind,index,keep,amended}
b, v = L('b0'), L('v0')
R = {(r['kind'], r['index']): r for r in v['reviews']}
for i, e in enumerate(b['event_corrections']):
    r = R[('event', i)]
    if r['keep']: ev.append(tag(e, 'b0 frame check, verified'))
    elif r.get('amended'): ev.append(tag(r['amended'], 'b0 frame check, amended by skeptic'))
for i, c in enumerate(b['cell_edits']):
    r = R[('cell', i)]
    if r['keep']: cells.append(tag(c, 'b0 frame check, verified'))
    elif r.get('amended'): cells.append(tag(r['amended'], 'b0 frame check, amended by skeptic'))
for m in v['missed']:
    (ev if 'op' in m else cells).append(tag(m, 'b0 skeptic (found by the reviewer)'))
frz += b.get('freeze_windows', [])
# groups 1, 2: refs e/c/f, verdict keep|amend|reject, amended = partial override
for g in ('1', '2'):
    b, v = L('b' + g), {x['ref']: x for x in L('v' + g)}
    for pre, lst, out in (('e', 'event_corrections', ev), ('c', 'cell_edits', cells), ('f', 'freezes' if 'freezes' in b else 'freeze_windows', frz)):
        for i, e in enumerate(b.get(lst, [])):
            r = v[f'{pre}{i}']
            if r['verdict'] == 'reject': continue
            x = {**e, **(r.get('amended') or {})}
            out.append(x if pre == 'f' else tag(x, f"b{g} frame check, {'verified' if r['verdict']=='keep' else 'amended by skeptic'}"))
# PC group: vpc verdicts on bpc; amended = full record
b, v = L('bpc'), L('vpc')
V = {x['ref']: x for x in v['verdict']}
for i, e in enumerate(b['event_corrections']):
    r = V[f'e{i}']
    if r['verdict'] == 'reject': continue
    x = {**e, **(r.get('amended') or {})}
    x.pop('n', None)
    ev.append(tag(x, f"PC frame check, {'verified' if r['verdict']=='keep' else 'amended by skeptic'}"))
for e in v['dup']['event_corrections']: ev.append(tag(e, 'double-log frame check (second reader)'))
cells += v['dup'].get('cell_edits', [])
for e in ev:
    e.pop('n', None); e['t'] = round(e['t'], 2)
    # metrics.py retype matches clear events only; a retype of a plain lock (None) goes as a one-event replace_window
    if e['op'] == 'retype' and e['was'][0] is None:
        e['op'] = 'replace_window'; e['t_end'] = e['t']
        e['events'] = [dict(t=e['t'], kind=e.pop('kind'), lines=e.pop('lines'), pc=e.pop('pc', 0), gc=e.pop('gc', 0))]
        e['was_old'] = [[e['t'], None, 0]]; e.pop('was')
    if e['op'] == 'remove' and e['was'][0] in (None, 'BREAK'):
        e['op'] = 'replace_window'; e['t_end'] = e['t']; e['events'] = []
        e['was_old'] = [[e['t'], e['was'][0], e['was'][1]]]; e.pop('was')
_x = []
for e in ev:   # an empty-window replace_window is a list of adds (metrics.py refuses an empty window)
    if e['op'] == 'replace_window' and not e['was_old']:
        _x += [dict(id=e['id'], side=e['side'], op='add', t=round(w['t'], 2), kind=w['kind'], lines=w['lines'], pc=w['pc'], gc=w['gc'], source=e['source']) for w in e['events']]
    else: _x.append(e)
ev = _x
json.dump(ev, open(f'{C}/event-corrections.json', 'w'), ensure_ascii=False, indent=1)
json.dump(dict(cells=cells, freezes=frz), open(f'{C}/cells.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print(len(ev), Counter(e['op'] for e in ev), len(cells), len(frz))
for c in cells: print(c['id'], c['player'], c['field'], c['was'], '->', c['value'])
