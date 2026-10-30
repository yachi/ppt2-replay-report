# Score-sum check: sum of score jumps >= 60 (clears; merged jumps keep their sum) vs the clear points the
# chain's corrected event list predicts with guideline scoring at level 3. Drop points (< 60 a piece) are
# left out on both sides, so a residual >= ~400 means a clear the chain lacks (or has extra).
import json, sys
sys.path.insert(0, '/tmp/claude-0/xo/w/ocrall')
from jumps import events
L = 3
BASE = {'single': 100, 'double': 300, 'triple': 500, 'quad': 800, 'tss': 800, 'tsd': 1200, 'tst': 1600, 'tsmini': 200}
HARD = {'quad', 'tss', 'tsd', 'tst', 'tsmini'}
W = '/tmp/claude-0/xo/w'
S = json.load(open(f'{W}/chain/xo/w/tetrio/cseq.json'))
J = {j['id']: j for j in map(json.loads, open(f'{W}/chain/xo/w/A/games.jsonl'))}
def predict(seq):
    pts, ren, b2b, unk = 0, -1, False, 0
    for t, k, n, pc, gc in seq:
        if k is None: ren = -1; continue
        if k == 'BREAK': unk += 1; ren = -1; continue
        ren += 1
        p = BASE[k] * L
        if k in HARD:
            if b2b: p = p * 3 // 2
            b2b = True
        else: b2b = False
        pts += p + 50 * ren * L
    return pts, unk
out = []
for g in sorted(J):
    if f'{g} p1' not in S: continue
    r = json.load(open(f'{W}/ocrall/{g}.json')); end = J[g]['end_s']
    for p, si in (('p1', 1), ('p2', 3)):
        jumps = [x for x in events([(x[0], x[si]) for x in r]) if x[0] <= end + 0.3]
        pred, unk = predict(S[f'{g} {p}'])
        seen = sum(d for _, d in jumps)
        out.append(dict(id=g, player=p, seen=seen, pred=pred, res=seen - pred, breaks=unk,
                        pcs=sum(z[3] for z in S[f'{g} {p}']), n=sum(1 for z in S[f'{g} {p}'] if z[1] not in (None, 'BREAK'))))
json.dump(out, open('/tmp/claude-0/xo/corr/score/scoresum.json', 'w'), indent=0)
import statistics
res = [o['res'] for o in out if not o['breaks'] and not o['pcs']]
print('clean rows', len(res), 'median', statistics.median(res), 'within +-300:', sum(abs(x) <= 300 for x in res))
for o in sorted(out, key=lambda o: -abs(o['res']))[:25]: print(o)
