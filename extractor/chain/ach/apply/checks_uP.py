# [uP run, new file; after amemiya apply/checks_am.py] sanity checks + out/flags.json for out/chain_games.csv,
# plus the KO-tail score-jump check (amemiya check/ocrall/compare.py events() + align.py matching, uP reader).
import csv, json, pickle, collections, os, sys, math
W = '/tmp/claude-0/ak/w/chain/sy/w'; OUT = '/tmp/claude-0/ak/out'; OD = '/tmp/claude-0/ak/w/ocrall'
rows = list(csv.DictReader(open(f'{OUT}/chain_games.csv')))
G = {g['id']: g for g in json.load(open(f'{W}/../games.json'))}
G85 = {g['id']: g for g in json.load(open(f'{W}/../games_all85.json'))}
GAP = json.load(open(f'{W}/R/gaps.json')); BAG = json.load(open(f'{W}/R/bag.json'))
F = pickle.load(open(f'{W}/R/fuse.pkl', 'rb'))
A = {j['id']: j for j in map(json.loads, open(f'{W}/A/games.jsonl'))}
PART = json.load(open(f'{W}/R/part.json')); UNRES = json.load(open(f'{W}/R/unresolved.json'))
CSEQ = json.load(open(f'{W}/tetrio/cseq.json'))
PCDEC = {(g, p): v for g, p, v in json.load(open(f'{W}/../pcdec.json'))}
sys.argv = ['x']; _cwd = os.getcwd(); os.chdir(W)
exec(open('R/pcon.py').read().split('if __name__')[0])   # PC[(g,p)] = PERFECT CLEAR banner onsets
KOF = {}
for g in A:
    d = pickle.load(open(f'R/ev/{g}.pkl', 'rb')); KOF[g] = d.get('kofinal')
os.chdir(_cwd)
flags = []
def flag(i, p, f, d, t): flags.append(dict(id=i, player=p, field_or_issue=f, detail=d, t_s=None if t is None else round(float(t), 2)))
rep = []
# ---- structural
byg = collections.defaultdict(list)
for r in rows: byg[r['id']].append(r)
bad = []
for g, rs in byg.items():
    if sorted(r['player'] for r in rs) != ['p1', 'p2']: bad.append((g, 'players'))
    if sorted(int(r['won']) for r in rs) != [0, 1]: bad.append((g, 'winners'))
    if any(float(r['duration_s']) <= 0 for r in rs): bad.append((g, 'duration'))
    if len({r['opponent'] for r in rs}) != 1 or not rs[0]['opponent']: bad.append((g, 'opponent'))
    if [r['who'] for r in sorted(rs, key=lambda r: r['player'])] != ['syakegohan', rs[0]['opponent']]: bad.append((g, 'who'))
rep.append(f'games {len(byg)}, rows {len(rows)}, structural failures {bad}')
# ---- PPS / APP ranges
out_r = []
for r in rows:
    d = float(r['duration_s']); pc = int(r['pieces']); at = int(r['attack'])
    pps = pc / d; app = at / pc if pc else None
    if not 0.5 <= pps <= 4: out_r.append((r['id'], r['player'], 'PPS', round(pps, 3))); flag(r['id'], r['player'], 'outlier: PPS outside 0.5..4', f'{pps:.3f} ({pc} pieces / {d} s)', float(r['start_s']))
    if app is None or not 0 <= app <= 1.5: out_r.append((r['id'], r['player'], 'APP', app)); flag(r['id'], r['player'], 'outlier: APP outside 0..1.5', f'{app}', float(r['start_s']))
rep.append(f'PPS/APP outliers: {out_r}')
pps = [int(r['pieces']) / float(r['duration_s']) for r in rows]; app = [int(r['attack']) / int(r['pieces']) for r in rows]
rep.append(f'PPS range {min(pps):.3f}..{max(pps):.3f}; APP range {min(app):.3f}..{max(app):.3f}')
# ---- WIN counter cross-check (games.json counter_winner: 1 = left/p1, 2 = right/p2; read by eye at preflight)
mis = []
for g, rs in byg.items():
    w = [r['player'] for r in rs if r['won'] == '1'][0]
    cw = {1: 'p1', 2: 'p2'}.get(G[g]['counter_winner'])
    if cw != w: mis.append((g, w, cw))
rep.append(f'WIN-counter cross-check: {len(byg) - len(mis)}/{len(byg)} agree; disagreements {mis}')
for g, w, c in mis: flag(g, '', 'winner disagrees with WIN counter', f'csv {w}, counter {c}', float(G[g]['start_s']))
wl = [0, 0]
for g, rs in byg.items(): wl[0 if [r for r in rs if r['player'] == 'p1'][0]['won'] == '1' else 1] += 1
rep.append(f'syakegohan W-L in the csv: {wl[0]}-{wl[1]}')
# ---- games not in the csv
for g in G85:
    if g not in byg:
        flag(g, '', 'unresolved: no KO, game not in csv', 'froze at ~5520 s (score stuck 5520-5527.5 s), then the opponent disconnected; no KO, no winner. Dropped from the chain input (A and B have no end).', 5520.0)
flag('l017', '', 'game end at a disconnect', 'KO with syakegohan winning by 1357.2 s, then a 通信中 dialog and disconnect; end_upper_s cut 1367.2 -> 1358.0. Check the KO tail and that no dialog frame was read as play.', 1357.2)
# ---- frame-check flags
for g in GAP:
    for p, x in GAP[g].items():
        for t, L in x['big']:
            if L > 4: flag(g, p, 'gap window > 4 s', f'NEXT queue unread/stalled {L:.2f} s from {t:.2f} s; B events spliced (D2/D3)', t)
        if x['tail'] > 4: flag(g, p, 'gap window > 4 s (tail)', f'{x["tail"]:.2f} s from the last spawn to the KO', A[g]['end_s'])
for g in BAG:
    for p, x in BAG[g].items():
        if x['bad_bags']: flag(g, p, 'bad bag', f'{len(x["bad_bags"])} of {x["nbags"]} bags not a permutation (spawn index {x["bad_bags"]}); anomalies {x.get("anom", [])}', float(A[g]['start_s']))
WL = {'Single': 1, 'Double': 2, 'Triple': 3}
for (g, p), r in F.items():
    for b in r['extra']:
        flag(g, p, 'banner without a clear', f'{"Mini " if b["mini"] else ""}T-SPIN {b["word"][0]} banner at {b["t"]} s, no A clear matched (added by R/build.py)', b['t'])
    for e in r['evs']:
        if e['ban'] and not e['ban']['mini'] and WL[e['ban']['word'][0]] != e['lines']:
            flag(g, p, 'banner/type disagreement', f'A clear {e["lines"]} lines ({e["akind"]}) vs banner T-SPIN {e["ban"]["word"][0]} at {e["t"]} s', e['t'])
        if e['akind'] in ('tss', 'tsd', 'tst', 'tsmini') and not e['ban']:
            flag(g, p, 'T-spin without a banner', f'A {e["akind"]} at {e["t"]} s typed as a plain clear', e['t'])
# ---- PC banner onsets: every R/pcon.py onset, with pcmap's decision
for (g, p), v in sorted(PC.items()):
    if g not in A: continue
    dec = PCDEC.get((g, p), [])
    for e in v:
        acc = e['len'] >= 0.9
        m = [d for d in dec if e['t'] - 2.0 <= d[0] <= e['t'] + 0.2]
        det = (f'PERFECT CLEAR banner onset, {e["len"]} s long; ' + (f'pcmap: PC = clear at {m[0][0]} s, dropped double-logs {m[0][1]}' if acc and m else
               'pcmap: accepted (>= 0.9 s) but no clear matched' if acc else 'pcmap: rejected (< 0.9 s: banner tail or effect?); not counted as a PC'))
        flag(g, p, 'PC banner onset', det, e['t'])
# ---- unresolved lower bounds
for u in UNRES:
    g, p = u[:4], u[4:]
    flag(g, p, 'unresolved lower bound', 'R/build.py: B coverage ends before the window ends; pieces/lines/garbage are lower bounds; game excluded', A[g]['end_s'])
# ---- winner's KO piece not counted (kofinal found no flash and no next spawn)
for g in A:
    if KOF[g] is None and A[g].get('winner'):
        w = A[g]['winner']
        flag(g, w, 'winner KO piece not counted', f'R/kofinal.py: no clear flash and no next spawn by KO+3 frames; a piece locking on the KO frame would be missed (last spawn {GAP[g][w]["tail"]:.2f} s before the KO)', A[g]['end_s'])
# ---- KO-tail score jumps (uP score reader)
sys.path.insert(0, '/tmp/claude-0/ak/w/ocrall')
from jumps import events
tail_n = 0; nocr = []
for g in sorted(A):
    f = f'{OD}/{g}.json'
    if not os.path.exists(f): nocr.append(g); continue
    r = json.load(open(f)); end = A[g]['end_s']
    for p, si in (('p1', 1), ('p2', 3)):
        jumps = [x for x in events([(x[0], x[si]) for x in r]) if x[0] <= end + 0.5]
        seq = CSEQ[f'{g} {p}']
        ch = [(i, z) for i, z in enumerate(seq) if z[1] not in (None, 'BREAK')]
        used = set()
        for i, z in ch:
            hi = (seq[i + 1][0] if i + 1 < len(seq) else end) + 1.0
            k = next((k for k, (t, d) in enumerate(jumps) if k not in used and z[0] - 0.1 <= t <= hi), None)
            if k is not None: used.add(k)
        for k, (t, d) in enumerate(jumps):
            if k not in used and t > end - 1.5:
                tail_n += 1
                flag(g, p, 'KO-tail score jump', f'score +{d} at {t} s (KO {end} s) with no chain clear event (tetrio/cseq.json) matched', t)
rep.append(f'KO-tail score jumps with no chain clear: {tail_n}; games without OCR: {nocr}')
json.dump(flags, open(f'{OUT}/flags.json', 'w'), ensure_ascii=False, indent=1)
c = collections.Counter(f['field_or_issue'] for f in flags)
rep.append(f'flags {len(flags)}: {dict(c)}')
open(f'{OUT}/sanity.txt', 'w').write('\n'.join(rep) + '\n'); print('\n'.join(rep))
