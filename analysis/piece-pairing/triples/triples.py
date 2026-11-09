# runs of 3+ consecutive locks where each lock touches the pieces before it in the run.
import json, sys, csv, glob, collections as C, numpy as np
SW = {'J': 'L', 'L': 'J', 'S': 'Z', 'Z': 'S'}
who = {}
for f in glob.glob('/home/user/ppt2-replay-report/analysis/*/games.csv'):
    for r in csv.DictReader(open(f)): who[(r['id'], r['player'])] = r['who']
def adj(a, b):
    sa = set(map(tuple, a)); return any((r + dr, c + dc) in sa for r, c in b for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)))
def canon(ps):  # ps = [(type, cells)]
    out = []
    for m in (False, True):
        q = [((SW.get(t, t) if m else t), [(r, -c if m else c) for r, c in cs]) for t, cs in ps]
        r0 = min(r for _, cs in q[:1] for r, _ in cs); c0 = min(c for _, cs in q[:1] for _, c in cs)
        out.append(tuple((t, tuple(sorted((r - r0, c - c0) for r, c in cs))) for t, cs in q))
    return min(out)
def draw(k):
    cells = {}
    for j, (t, cs) in enumerate(k):
        for x in cs: cells[x] = t if j % 2 == 0 else t.lower()
    R0 = min(r for r, _ in cells); R = max(r for r, _ in cells); c0 = min(c for _, c in cells); c1 = max(c for _, c in cells)
    return '/'.join(''.join(cells.get((r, c), '.') for c in range(c0, c1 + 1)) for r in range(R, R0 - 1, -1))
obs = C.Counter(); exp = C.Counter(); ex = C.defaultdict(list); wh = C.defaultdict(C.Counter); db = C.defaultdict(list); dh = C.defaultdict(list)
runlen = C.Counter(); exp_step = []; ctx3 = 0; obs3 = 0; steps = 0; touch = 0
for S, off in (('xo', 0), ('fr', 1751)):
    rows = [json.loads(l) for l in open(f'/tmp/claude-0/pp/{S}_table.jsonl')]
    cf = {j['key']: j for j in map(json.loads, open(f'/tmp/claude-0/pp/{S}_cf.jsonl'))}
    by = C.defaultdict(dict)
    for r in rows: by[(r['id'], r['p'])][r['i']] = r
    for (gid, p), seq in by.items():
        run = []  # current run of rows
        def close():
            if len(run) >= 2: runlen[len(run)] += 1
        for i in sorted(seq):
            B = seq[i]; A = seq.get(i - 1)
            ok = A is not None and i - 1 >= 14 and A['trusted'] and B['trusted'] and not A['lines'] and not B['garbage_before'] and B['key'] in cf
            if not ok:
                close(); run = [B] if (i >= 14 and B['trusted']) else []; continue
            if not run or run[-1] is not A: run = [A]
            union = [x for r in run for x in r['cells']]
            pl = cf[B['key']]['placements']
            steps += 1; exp_step.append(np.mean([adj(union, q) for q in pl]))
            # conditional expectation for the third piece of a window (A2, A, B) where A touches A2
            A2 = seq.get(i - 2)
            if len(run) >= 2 and run[-2] is A2:
                ctx3 += 1
                for q in pl:
                    if adj(A2['cells'] + A['cells'], q):
                        exp[canon([(A2['type'], A2['cells']), (A['type'], A['cells']), (B['type'], q)])] += 1 / len(pl)
            if adj(union, B['cells']):
                touch += 1
                run.append(B)
                if len(run) >= 3:
                    obs3 += 1
                    w = run[-3:]
                    k = canon([(r['type'], r['cells']) for r in w])
                    obs[k] += 1; wh[k][who.get((gid, p), p)] += 1
                    db[k].append(B['post']['bump'] - w[0]['pre']['bump']); dh[k].append(B['post']['holes'] - w[0]['pre']['holes'])
                    if len(ex[k]) < 6: ex[k].append(dict(v='XoaWLJowuCQ' if S == 'xo' else 'h3FUsPBZmzE', t=int(w[0]['t'] - 2 + off), who=who.get((gid, p), p), b=w[0]['pre_hex'], ps=[[r['type'], r['cells']] for r in w]))
            else:
                close(); run = [B]
        close()
# expected run-length tail under "each step touches with its uniform probability"
pm = float(np.mean(exp_step))
exp3_total = sum(exp.values())
set_obs = C.Counter(); set_exp = C.Counter()
for k, n in obs.items(): set_obs[''.join(sorted(SW.get(t,t) if False else t for t, _ in k))] += n
for k, v in exp.items(): set_exp[''.join(sorted(t for t, _ in k))] += v
res = dict(steps=steps, touch=touch, p_touch_obs=touch / steps, p_touch_uniform=pm, windows3=ctx3, obs3=obs3, exp3=exp3_total,
           sets=[[k, n, round(set_exp[k],1), round(n/max(set_exp[k],1e-9),2)] for k, n in set_obs.most_common(20)],
           runlen=dict(sorted(runlen.items())), motifs=[])
for k, n in obs.most_common():
    if n < 3: break
    res['motifs'].append(dict(draw=draw(k), key=[[t, list(map(list, cs))] for t, cs in k], n=n, exp=round(exp[k], 2),
        lift=round(n / max(exp[k], 1e-9), 2), dbump=round(float(np.mean(db[k])), 2), dholes=round(float(np.mean(dh[k])), 2),
        who=dict(wh[k]), ex=ex[k]))
json.dump(res, open('/tmp/claude-0/pp/tri/triples.json', 'w'), ensure_ascii=False, indent=1)
print({k: v for k, v in res.items() if k != 'motifs'})
for m in res['motifs'][:30]: print(m['n'], m['exp'], m['lift'], m['dbump'], m['dholes'], m['draw'], m['who'])
