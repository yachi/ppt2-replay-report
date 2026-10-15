# YbMeCRhjG1k reconciliation rule (not in reconcile-log.md): when A loses the NEXT-queue read, the A lock event at
# the START of the dropout window aggregates the board change across the whole gap ('piece cells' >> 4) and reports
# a phantom clear (always 3-4 lines here). B's tracked clears inside the window are spliced by build.py too, so
# those lines would be counted twice, and a T-spin banner from inside the window gets attached to the phantom
# (giving a 4-line 'tst'). Rule: zero the lines and banner of an A event at a window start whose piece-cell count
# is > 8. Its banner stays in the banner list, so build.py's window logic still uses it.
import json, pickle, re, shutil, os
if not os.path.exists('R/fuse_raw.pkl'): shutil.copy('R/fuse.pkl', 'R/fuse_raw.pkl')
F = pickle.load(open('R/fuse_raw.pkl', 'rb')); GAP = json.load(open('R/gaps.json'))
log = []
for (g, p), r in F.items():
    d = pickle.load(open(f'R/ev/{g}.pkl', 'rb')); x = GAP[g][p]
    W = [(t, t + L) for t, L in x['big'] if L > 4.0]
    if x['tail'] > 4.0: W.append((d['a_end'] - x['tail'], d['a_end']))
    raw = {e['t']: e for e in d['a'][p] if e.get('kind') != 'hold-empty'}
    for e in r['evs']:
        if not e['lines']: continue
        if not any(abs(e['t'] - a) <= 0.05 for a, b in W): continue
        fl = ' '.join(raw.get(e['t'], {}).get('flag', []) or [])
        m = re.search(r'piece cells (\d+)', fl); n = int(m.group(1)) if m else 4
        log.append((g, p, e['t'], e['lines'], e['akind'], n, e['ban']['word'] if e['ban'] else None, n > 8))
        if n > 8: e['lines'] = 0; e['ban'] = None; e['pc'] = False; e['gclr'] = 0; e['phantom'] = True
pickle.dump(F, open('R/fuse.pkl', 'wb'))
for l in log: print(l)
