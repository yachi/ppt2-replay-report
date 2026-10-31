# [r6] Triage the 717 flags + 161 score spots into frame-check items. Auto-settled, with no correction:
#  - "banner without a clear" where a T-spin-sized score jump (>= 2000) sits in [t-0.6, t+1.0]: the chain already
#    added that T-spin (R/build.py), and the score shows a T-spin there (215 of 226 on this capture)
#  - "banner/type disagreement" and "T-spin without a banner" in a player-game the score check covered
#    (no BREAK, no PC) with no score spot within 2.5 s: the chain's type already adds up on screen
#  - "PC banner onset": handled by the PC pass, as in xo
import json, sys, collections
sys.path.insert(0, '/tmp/claude-0/r6/w/chain/r6/corr')
from scoretype import jumps
F = json.load(open('/tmp/claude-0/r6/out/flags.json'))
SP = json.load(open('/tmp/claude-0/r6/corr/score/spots.json'))
SS = {(r['id'], r['player']): r for r in json.load(open('/tmp/claude-0/r6/corr/score/scoresum.json'))}
cov = {k for k, r in SS.items() if not r['breaks'] and not r['pcs']}
spk = collections.defaultdict(list)
for s in SP: spk[(s['id'], s['player'])].append(s)
def near_spot(k, t): return any((s['t0'] if s['t0'] is not None else s['near'][0][0]) - 2.5 <= t <= s['t1'] + 2.5 for s in spk[k])
items = []; auto = collections.Counter(); J = {}
for f in F:
    k = (f['id'], f['player']); kind = f['field_or_issue']; t = f['t_s']
    if kind == 'PC banner onset': auto['pc pass'] += 1; continue
    if kind == 'banner without a clear':
        if k not in J: J[k] = jumps(*k)
        if any(t - 0.6 <= j[0] <= t + 1.0 and j[1] >= 2000 for j in J[k]): auto[kind + ' (score shows T-spin)'] += 1; continue
    if kind in ('banner/type disagreement', 'T-spin without a banner') and k in cov and not near_spot(k, t):
        auto[kind + ' (score adds up)'] += 1; continue
    items.append(f)
for s in SP: items.append(dict(id=s['id'], player=s['player'], field_or_issue='score_spot', detail=s, t_s=s['t0'] if s['t0'] is not None else s['near'][0][0]))
print('auto', dict(auto), sum(auto.values())); print('items', len(items), collections.Counter(i['field_or_issue'] for i in items))
json.dump(dict(auto=auto, items=items), open('/tmp/claude-0/r6/corr/tri/items.json', 'w'))
