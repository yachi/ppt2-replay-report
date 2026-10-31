# [r6] Score typing: decide each chain clear's kind from its on-screen score jump (OCR, ocrall/), because this capture's
# T-SPIN banner reader fires on clear flashes. Guideline scoring at level 3 (as check/score/scoresum.py): base x3,
# x1.5 for a hard clear after a hard clear (B2B), +150 per REN step, + drop points (< 60). Line count is A's.
import json, sys, collections
sys.path.insert(0, '/tmp/claude-0/r6/w/ocrall')
from jumps import events
W = '/tmp/claude-0/r6/w/chain/r6/w'
BASE = {'single': 100, 'double': 300, 'triple': 500, 'quad': 800, 'tss': 800, 'tsd': 1200, 'tst': 1600, 'tsmini': 200}
HARD = {'quad', 'tss', 'tsd', 'tst', 'tsmini'}
CAND = {1: ['single', 'tss', 'tsmini'], 2: ['double', 'tsd'], 3: ['triple', 'tst'], 4: ['quad']}
TOL = 60
def jumps(g, p):
    r = json.load(open(f'/tmp/claude-0/r6/w/ocrall/{g}.json')); si = 1 if p == 'p1' else 3
    return events([(x[0], x[si]) for x in r])
def fits(d, k, ren, b2b):
    v = BASE[k] * 3
    if k in HARD and b2b: v = v * 3 // 2
    v += 150 * max(ren, 0)
    return 0 <= d - v < TOL
def run(g, p, seq, end):
    J = [j for j in jumps(g, p) if j[0] <= end + 0.5]; used = set(); out = []
    ren, b2b = -1, False
    clears = [(i, z) for i, z in enumerate(seq) if z[1] not in (None, 'BREAK')]
    for ci, (i, z) in enumerate(clears):
        t, k, n, pc, gc = z
        if seq_break(seq, i, clears, ci): ren = -1
        tnext = clears[ci + 1][1][0] if ci + 1 < len(clears) else t + 3
        cand = [(jj, j) for jj, j in enumerate(J) if jj not in used and t - 0.25 <= j[0] <= min(t + 1.8, tnext + 0.5)]
        r1 = ren + 1
        fit = sorted({kk for kk in CAND.get(min(n, 4), []) for b in [b2b] if any(fits(j[1], kk, r1, b) for _, j in cand[:1])})
        if pc: res = ('pc', None)
        elif not cand: res = ('nojump', None)
        elif len(fit) == 1: res = ('ok' if fit[0] == k else 'retype', fit[0]); used.add(cand[0][0])
        elif not fit: res = ('nofit', cand[0][1][1])
        else: res = ('amb', fit)
        out.append(dict(t=t, kind=k, lines=n, res=res[0], val=res[1], jump=cand[0][1] if cand else None))
        kk = res[1] if res[0] in ('ok', 'retype') else k
        ren = r1; b2b = (kk in HARD) if kk in HARD or kk in BASE else b2b
        if kk not in HARD: b2b = False
    return out
def seq_break(seq, i, clears, ci):
    if ci == 0: return True
    j = clears[ci - 1][0]
    return any(z[1] is None or z[1] == 'BREAK' for z in seq[j + 1:i])
if __name__ == '__main__':
    S = json.load(open(f'{W}/tetrio/cseq.json'))
    A = {j['id']: j for j in map(json.loads, open(f'{W}/A/games.jsonl'))}
    R = {}; c = collections.Counter()
    for key, seq in S.items():
        if key.endswith(' pre'): continue
        g, p = key.split(); R[key] = run(g, p, seq, A[g]['end_s'])
        for x in R[key]: c[(x['res'], x['kind'], x['val'] if x['res'] == 'retype' else '')] += 1
    json.dump(R, open('/tmp/claude-0/r6/corr/scoretype.json', 'w'))
    for k, v in sorted(c.items(), key=lambda x: -x[1]): print(k, v)
