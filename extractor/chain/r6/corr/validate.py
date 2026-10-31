# [r6] dry-run metrics.py's overlay over the pre-overlay sequences (cseq.json "<g> <p> pre") and list EVERY failing correction
# at once, instead of metrics.py's one-assert-at-a-time. Same rules as tetrio/metrics.py overlay().
import json, sys, collections
PRE = json.load(open('/tmp/claude-0/r6/corr/cseq.pre.json'))
OVL = json.load(open(sys.argv[1] if len(sys.argv) > 1 else '/tmp/claude-0/r6/corr/event-corrections.json'))
fails = []
by = collections.defaultdict(list)
for ci, c in enumerate(OVL): by[(c['id'], c['side'])].append((ci, c))
def hits(cs, t): return [i for i, z in enumerate(cs) if z[1] not in (None, 'BREAK') and round(z[0], 2) == round(t, 2)]
for (g, p), lst in sorted(by.items()):
    cs = [tuple(z) for z in PRE[f'{g} {p} pre']]
    for ci, c in lst:
        op, t = c['op'], c['t']
        if op == 'add':
            if [z for z in cs if round(z[0], 2) == round(t, 2)]: fails.append((ci, 'add: event already at t', [z for z in cs if round(z[0], 2) == round(t, 2)])); continue
            new = (t, c['kind'], int(c['lines']), int(bool(c['pc'])), int(c.get('gc', 0)))
            j = next((i for i, z in enumerate(cs) if z[0] > t), len(cs)); cs.insert(j, new); continue
        if op == 'replace_window':
            idx = [i for i, z in enumerate(cs) if t - 1e-9 <= z[0] <= c['t_end'] + 1e-9]
            if not idx: fails.append((ci, 'window empty', None)); continue
            old = [[round(cs[i][0], 2), cs[i][1], cs[i][2]] for i in idx]
            if old != [[round(w[0], 2), w[1], int(w[2])] for w in c['was_old']]: fails.append((ci, 'was_old mismatch', old)); continue
            cs = [z for i, z in enumerate(cs) if i not in set(idx)]
            for e in c['events']:
                new = (e['t'], e['kind'], int(e['lines']), int(bool(e['pc'])), int(e.get('gc', 0)))
                j = next((i for i, z in enumerate(cs) if z[0] > new[0]), len(cs)); cs.insert(j, new)
            continue
        h = hits(cs, t)
        if len(h) != 1:
            near = [z for z in cs if abs(z[0] - t) < 0.4]
            fails.append((ci, f'{op}: {len(h)} clear events at t', near)); continue
        z = cs[h[0]]; w = c['was']
        if [z[1], z[2], int(bool(z[3]))] != [w[0], int(w[1]), int(w[2])]: fails.append((ci, 'was mismatch', z)); continue
        if op == 'remove': cs.pop(h[0])
        else: cs[h[0]] = (z[0], c['kind'], int(c['lines']), int(bool(c.get('pc', z[3]))), int(c.get('gc', z[4])))
print(len(fails), 'failing of', len(OVL))
for ci, why, ctx in fails:
    c = OVL[ci]
    print(ci, c['id'], c['side'], c['op'], c['t'], c.get('was'), '->', c.get('kind'), c.get('lines'), c.get('pc'), '|', why, '|', ctx, '|', c['source'][:60])
