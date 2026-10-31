import json, random, sys
sys.path.insert(0, '/tmp/claude-0/pp')
P = '/tmp/claude-0/pp/'
rows = json.load(open(P + 'ccrun/rows.json'))
T = {}
for s in ['xo', 'fr']:
    for l in open(P + s + '_table.jsonl'):
        j = json.loads(l); T[j['key']] = j
cf = {}
for s in ['xo', 'fr']:
    for l in open(P + s + '_cf.jsonl'):
        j = json.loads(l); cf[j['key']] = j['placements']
def nxt(key):
    g, p, i = key.split('|'); return T.get(f'{g}|{p}|{int(i)+1}')
random.seed(7)
cands = []
for x in rows:
    if x['cc'] is None: continue
    n = nxt(x['key'])
    if not n or not n['trusted'] or n['garbage_before']: continue
    r = T[x['key']]
    if r['lines']: continue  # keep pair overlay simple: first piece clears nothing
    sa = {tuple(c) for c in r['cells']}
    if not any((rr + dr, cc + dc) in sa for rr, cc in n['cells'] for dr, dc in ((1,0),(-1,0),(0,1),(0,-1))): continue  # pro's two pieces touch
    if n['post']['holes'] > r['pre']['holes']: continue
    K = x['ks']; lk, pro, cc = K[x['lk']] == K[x['ch']], 1, K[x['cc']] == K[x['ch']]
    cands.append((('agree' if lk and cc else 'lk' if lk else 'cc' if cc else 'none'), x, r, n))
pick = []
for cat, k in [('lk', 14), ('cc', 12), ('agree', 8), ('none', 6)]:
    pool = [c for c in cands if c[0] == cat]; pick += random.sample(pool, k)
random.shuffle(pick)
S = []
for cat, x, r, n in pick:
    pl = cf[x['key']]
    S.append(dict(b=r['pre_hex'], a=r['type'], n=n['type'], pro=r['cells'], pro2=n['cells'], cc=pl[x['cc']],
                  src=[0 if x['s'] == 'xo' else 1, int(x['t'] - 2 + (1751 if x['s'] == 'fr' else 0))]))
acc = json.load(open(P + 'page/acc.json'))
html = open(P + 'page/template.html').read()
for k, v in [('/*SRS*/', open(P + 'page/srs.js').read()), ('/*CORE*/', open(P + 'page/core.js').read()),
             ('/*RATES*/', open(P + 'page/rates_page.json').read()), ('/*SAMPLES*/', json.dumps(S, separators=(',', ':'))),
             ('/*ACC*/', json.dumps(acc, ensure_ascii=False)), ('/*MOTIFS*/', open(P + 'page/motifs_page.json').read()), ('/*APP*/', open(P + 'page/app.js').read())]:
    html = html.replace(k, v)
open(sys.argv[1], 'w').write(html); print(len(S), len(html))
