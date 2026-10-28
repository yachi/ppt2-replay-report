# [am port, new file] sanity checks + flags.json for out/chain_games.csv. Run from anywhere.
import csv, json, pickle, collections, numpy as np
W = '/private/tmp/claude-501/am/w/chain/am/w'; OUT = '/private/tmp/claude-501/am/out'
rows = list(csv.DictReader(open(f'{OUT}/chain_games.csv')))
G = {g['id']: g for g in json.load(open(f'{W}/../games.json'))}
CW = json.load(open(f'{W}/R/counter_winner.json'))
GAP = json.load(open(f'{W}/R/gaps.json')); BAG = json.load(open(f'{W}/R/bag.json'))
F = pickle.load(open(f'{W}/R/fuse.pkl', 'rb'))
A = {j['id']: j for j in map(json.loads, open(f'{W}/A/games.jsonl'))}
B = {j['id']: j for j in map(json.loads, open(f'{W}/B/games.jsonl'))}
PART = json.load(open(f'{W}/R/part.json'))
flags = []
def flag(i, p, f, d, t): flags.append(dict(id=i, player=p, field_or_issue=f, detail=d, t_s=t))
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
rep.append(f'games {len(byg)}, rows {len(rows)}, structural failures {bad}')
# ---- PPS / APP ranges
out_r = []
for r in rows:
    d = float(r['duration_s']); pc = int(r['pieces']); at = int(r['attack'])
    pps = pc / d; app = at / pc if pc else None
    if not 0.5 <= pps <= 4: out_r.append((r['id'], r['player'], 'PPS', round(pps, 3))); flag(r['id'], r['player'], 'PPS outside 0.5..4', f'{pps:.3f} ({pc} pieces / {d} s)', float(r['start_s']))
    if app is None or not 0 <= app <= 1.5: out_r.append((r['id'], r['player'], 'APP', app)); flag(r['id'], r['player'], 'APP outside 0..1.5', f'{app}', float(r['start_s']))
rep.append(f'PPS/APP outliers: {out_r}')
# ---- WIN counter cross-check (every game: next game's counter, last game of a set: the 14 that finishes it)
mis = []
for g, rs in byg.items():
    w = [r['player'] for r in rs if r['won'] == '1'][0]
    if CW.get(g) != w: mis.append((g, w, CW.get(g)))
rep.append(f'WIN-counter cross-check: {len(byg) - len(mis)}/{len(byg)} agree; disagreements {mis}')
for g, w, c in mis: flag(g, '', 'winner disagrees with WIN counter', f'csv {w}, counter {c}', float(G[g]['start_s']))
# ---- per-opponent W-L and series score
wl = collections.OrderedDict()
for g, rs in byg.items():
    p1 = [r for r in rs if r['player'] == 'p1'][0]
    o = p1['opponent']; wl.setdefault(o, [0, 0, 0]); wl[o][0 if p1['won'] == '1' else 1] += 1
    if p1['excluded'] == '1': wl[o][2] += 1
rep.append('per-opponent amemiya W-L (excluded games): ' + '; '.join(f'{o} {a}-{b} ({x})' for o, (a, b, x) in wl.items()))
# ---- frame-check flags
for g in GAP:
    for p, x in GAP[g].items():
        for t, L in x['big']:
            if L > 4: flag(g, p, 'gap window > 4 s', f'NEXT queue unread/stalled {L:.2f} s from {t:.2f} s; B events spliced (D2/D3)', t)
        if x['tail'] > 4: flag(g, p, 'gap window > 4 s (tail)', f'{x["tail"]:.2f} s from the last spawn to the KO', A[g]['end_s'])
for g in BAG:
    for p, x in BAG[g].items():
        if x['bad_bags']: flag(g, p, 'bad bag score', f'{len(x["bad_bags"])} of {x["nbags"]} bags not a permutation (spawn index {x["bad_bags"]})', float(G[g]['start_s']))
WL = {'Single': 1, 'Double': 2, 'Triple': 3}
for (g, p), r in F.items():
    for b in r['extra']:
        flag(g, p, 'banner without A clear', f'{"Mini " if b["mini"] else ""}T-SPIN {b["word"][0]} banner at {b["t"]} s, no A clear matched (added by R/build.py)', b['t'])
    for e in r['evs']:
        if e['ban'] and not e['ban']['mini'] and WL[e['ban']['word'][0]] != e['lines']:
            flag(g, p, 'banner/type disagreement', f'A clear {e["lines"]} lines ({e["akind"]}) vs banner T-SPIN {e["ban"]["word"][0]} at {e["t"]} s', e['t'])
        if e['akind'] in ('tss', 'tsd', 'tst', 'tsmini') and not e['ban']:
            flag(g, p, 'A T-spin with no banner', f'A {e["akind"]} at {e["t"]} s typed as a plain clear', e['t'])
# KO-frame last piece: winner whose last spawn is <= 0.25 s before the KO frame (old hand-edits: last piece locks on the KO frame)
for g in A:
    w = A[g]['winner']
    if GAP[g][w]['tail'] <= 0.25:
        flag(g, w, 'KO-frame last piece', f'winner last spawn {GAP[g][w]["tail"]:.2f} s before the KO frame; the last piece may lock on the KO frame (not counted)', A[g]['end_s'])
# PC events (pcfix log in metrics.out)
for l in open(f'{W}/metrics.out'):
    if l.startswith('PCFIX'):
        import ast; x = ast.literal_eval(l.strip()[len('PCFIX '):])
        t = x[2] if isinstance(x[2], float) else x[3][0]
        flag(x[0], x[1], 'PC banner fix', l.strip(), t)
for r in rows:
    if int(r['pc']): flag(r['id'], r['player'], 'PC count', f'{r["pc"]} PC(s) in the row: frame-check (A double-logs PCs on this video)', float(r['start_s']))
for g in PART['trunc']: flag(g, '', 'B truncated', 'B end detector fired > 1.5 s before A; B values not used', float(G[g]['start_s']))
flag('k085', 'p1', 'A crash guard', 'A typed a 4-row flash on a T lock (~6218.8 s, banner T-SPIN Single) as tst after the port guard; lines likely +3 too high', 6218.8)
json.dump(flags, open(f'{OUT}/flags.json', 'w'), ensure_ascii=False, indent=1)
c = collections.Counter(f['field_or_issue'] for f in flags)
rep.append(f'flags {len(flags)}: {dict(c)}')
open(f'{OUT}/sanity.txt', 'w').write('\n'.join(rep) + '\n'); print('\n'.join(rep))
