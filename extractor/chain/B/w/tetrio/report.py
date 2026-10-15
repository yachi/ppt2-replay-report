import pickle, math, collections, json
from scipy.stats import binomtest
D = pickle.load(open('tetrio/out.pkl', 'rb')); out = D['out']; EXCL = D['EXCL']
S = pickle.load(open('tetrio/seqs.pkl', 'rb'))

def fl(x, d):
    if x is None: return '—'
    m = 10 ** d; v = math.floor(x * m) / m
    return f'{v:.{d}f}'
def flp(p):
    if p >= 0.001: return fl(p, 3)
    e = math.floor(math.log10(p)); m = p / 10 ** e
    return f'{math.floor(m * 10) / 10:.1f}e{e}'

METRICS = [('PPS', 'pieces', 'dur', 1, 3), ('APM', 'attack', 'dur', 60, 2), ('VS', 'vsnum', 'dur', 100, 2), ('APP', 'attack', 'pieces', 1, 3),
           ('DS/piece', 'garbage_cleared', 'pieces', 1, 3), ('LPM', 'lines_cleared', 'dur', 60, 2), ('landed APM', 'opp_garbage_received', 'dur', 60, 2),
           ('landed APM (no KO-tail)', 'opp_garbage_received_no_ko', 'dur', 60, 2)]
def num(r, f):
    if f == 'dur': return r['duration_s']
    if f == 'vsnum': return r['attack'] + r['garbage_cleared']
    return r[f]
def pool(rs):
    return {m: (k * sum(num(r, a) for r in rs) / sum(num(r, b) for r in rs) if rs else None) for m, a, b, k, _ in METRICS}

def ok(r, excl_dup=False):
    if r['id'] in EXCL: return False
    if excl_dup:
        both = [x for x in out if x['id'] == r['id']]
        if any(x['pc_dups_removed'] for x in both): return False
    return True

L = []; P = L.append
DS = ['upload-2026-07-14', 'upload-2026-08-20', 'upload-2026-09-13', 'stream-2026-10-12']
def pooled_table(excl_dup):
    P('| set | n games | player | ' + ' | '.join(m[0] for m in METRICS) + ' |')
    P('|' + '---|' * (3 + len(METRICS)))
    for ds in DS + ['ALL']:
        for p in ('p1', 'p2'):
            rs = [r for r in out if ok(r, excl_dup) and r['player'] == p and (ds == 'ALL' or r['dataset'] == ds)]
            n = len(rs); pv = pool(rs)
            P(f'| {ds} | {n} | {p} | ' + ' | '.join(fl(pv[m], d) for m, _, _, _, d in METRICS) + ' |')
summ = []

inc = [r for r in out if ok(r)]
ng = len({r['id'] for r in inc})
ndup_g = len({r['id'] for r in out if r['pc_dups_removed']})
ndup_g_inc = len({r['id'] for r in inc if r['pc_dups_removed']})

P('# syakegohan PPT2 — TETR.IO-style metrics (108 games)\n')
P(f'Source: `reconciled.jsonl` (referee of extractors A and B), rebuilt per lock by `tetrio/seqs.py`; metrics by `tetrio/metrics.py`, this report by `tetrio/report.py`. '
  f'Every printed figure is **floored** (p-values too, which makes them read slightly more significant than they are; unrounded values are in `metrics.csv`).\n')
P('## Inclusion\n')
P(f'- **Excluded: {len(EXCL)} of 108 games** — {", ".join(EXCL)}. Eight hold an *unresolved* player-game (A lost the NEXT queue and truncated B does not cover the window, so pieces/lines/garbage are lower bounds: g062p1 g071p2 g074p1 g086p2 g088p1 g092p2 g094p1 g096p1); '
  f'g090 and g101 are named by the *not-trustworthy* verification verdict (g086 is in both). The whole game is dropped so p1 and p2 stay paired.')
P(f'- **Included: {ng} games, {2 * ng} player-games.**')
P(f'- **Corrected, not excluded:** the verdict\'s PC-duplicate defect (a second clear with the same line count logged ≤0.6 s after a Perfect Clear). '
  f'The rule drops {len(D["dup"])} clears in {len({(g, p) for g, p, _ in D["dup"]})} player-games ({ndup_g} games, {ndup_g_inc} of them included) — the verdict\'s scan found 30, the 31st is g003 p2, which the referee had already hand-corrected; '
  f'applied to g003 p2 the rule reproduces that hand override exactly (lines 8, double 1, REN 2, B2B 1). Lines, clear types, garbage_cleared, max REN and max B2B are recomputed from the corrected sequence. '
  f'Five more same-line-count clears follow a PC after 0.6 s (g015p1, g021p1, g040p1, g042p2, g092p1) and are **kept**; they are possible further duplicates.')
P(f'- Control: before correction the rebuilt sequences reproduce reconciled.jsonl on every field for 215 of 216 player-games; the one exception is g003 p2, i.e. the hand override.\n')

P('## Attack table (PPT/PPT2, Tetris vs Tetris)\n')
P('| clear | sent | | REN | sent |\n|---|---|---|---|---|')
ct = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, '5 (howtotetris: 4)', '5 (howtotetris: 4)', 5]
for i, (k, v) in enumerate([('Single', 0), ('Double', 1), ('Triple', 2), ('Tetris', 4), ('T-spin Mini', 0), ('TSS', 2), ('TSD', 4), ('TST', 6), ('Perfect Clear', '10 (flat)'), ('B2B', '+1'), ('', ''), ('', ''), ('', ''), ('', '')]):
    P(f'| {k} | {v} | | {i if i < 13 else "13+"} | +{ct[i]} |')
P('\nSources: [tetris.wiki/Puyo_Puyo_Tetris](https://tetris.wiki/Puyo_Puyo_Tetris) (Garbage mechanics; left value of each slash = Tetris-only matches) and '
  '[howtotetris.com/combos](https://howtotetris.com/combos) (line table + a "Puyo Puyo Tetris 2" combo column). They agree on every line value and on REN 0–10, and disagree only at REN 11–12 (+5 vs +4). '
  '[tetris.wiki/Tetris_Online_(Japan)](https://www.tetris.wiki/Tetris_Online_(Japan)) carries the same REN table as tetris.wiki\'s PPT page (11+ = 5).')
ren = sum(r['ren11_12_clears'] for r in inc); dA = sum(r['attack'] - r['attack_alt'] for r in inc); totA = sum(r['attack'] for r in inc)
P(f'\nPriced: {ren} clears in the included games sit at REN 11–12, so the disagreement moves total attack by {dA} of {totA} lines ({fl(100 * dA / totA, 2)}%). `attack_alt` in the CSV uses the howtotetris column.')
P('\nRules used: REN index = clears-in-a-row − 1 (the referee\'s and PPT2\'s displayed count). B2B +1 on a difficult clear (quad, any T-spin, minis included as in the referee) when the previous clear was difficult. '
  'A Perfect Clear sends a flat 10 in place of its clear value and B2B, plus its REN bonus. Attack is *sent before cancellation*. '
  'Inside a B tracking gap (`BREAK`) REN/B2B reset and the gap\'s untyped lines get **no attack** (unmeasured; listed per row as `gap_lines_untyped`). '
  'The CSV carries `attack_base`, `attack_b2b`, `attack_combo`, `attack_pc` separately so a position-free extractor can be compared on `attack_base + attack_pc`.')
gl = sum(r['gap_lines_untyped'] for r in inc)
comp = collections.Counter()
for r in inc:
    for k in ('attack_base', 'attack_b2b', 'attack_combo', 'attack_pc'): comp[k] += r[k]
P(f'\nIncluded attack total {totA} = base {comp["attack_base"]} + B2B {comp["attack_b2b"]} + REN {comp["attack_combo"]} + PC {comp["attack_pc"]}; untyped gap lines with no attack: {gl}.\n')

P('## Metric definitions\n')
P('PPS = pieces/duration_s · APM = 60·attack/duration_s · VS = 100·(attack+garbage_cleared)/duration_s (TETR.IO) · APP = attack/pieces · DS/piece = garbage_cleared/pieces · LPM = 60·lines_cleared/duration_s · '
  'landed APM = 60·(opponent garbage_received_rows)/duration_s, i.e. post-cancellation garbage that actually entered the opponent\'s board. '
  '"landed APM (no KO-tail)" drops the garbage attached to the loser\'s last recorded lock — the verdict found the KO grey-out counted as garbage in g101 p2, and the loser\'s last lock carries garbage in ' +
  f'{sum(1 for r in out if r["opp_garbage_received"] != r["opp_garbage_received_no_ko"])} of 108 games, which cannot be split into real killing garbage and grey-out; the two columns bracket it.\n')

P('## Pooled — ratio of sums, headline (corrected, 10 games excluded)\n')
pooled_table(False)
P(f'\n### Sensitivity: also excluding the {ndup_g_inc} included games that had a PC duplicate removed\n')
pooled_table(True)

# AUC
P('\n## Paired AUC — did the game\'s winner have the higher value?\n')
P('Ties count half; p = exact two-sided binomial sign test over decided (non-tied) pairs (scipy `binomtest`; it reproduces the repo\'s pooled COMBO 2.4e-04, TST 8.7e-09 and PC 1.6e-04 cells). Included games only. No multiple-comparison correction applied.\n')
AUCM = [('PPS', lambda r: r['PPS']), ('APM', lambda r: r['APM']), ('VS', lambda r: r['VS']), ('APP', lambda r: r['APP']), ('DS/piece', lambda r: r['DS_per_piece']),
        ('LPM', lambda r: r['LPM']), ('landed APM', lambda r: r['landed_APM']), ('landed APM (no KO-tail)', lambda r: r['landed_APM_no_ko']),
        ('attack', lambda r: r['attack']), ('pieces', lambda r: r['pieces']), ('garbage received', lambda r: r['garbage_received_rows']), ('max REN', lambda r: r['max_combo']), ('max B2B', lambda r: r['max_b2b'])]
games = sorted({r['id'] for r in inc})
auc_rows = []
P('| metric | n games | winner higher | ties | decided | AUC % | p (two-sided) |\n|---|---|---|---|---|---|---|')
for m, f in AUCM:
    w = t = 0
    for g in games:
        a = [r for r in inc if r['id'] == g]; W = [r for r in a if r['won']][0]; Lr = [r for r in a if not r['won']][0]
        x, y = f(W), f(Lr)
        if abs(x - y) < 1e-12: t += 1
        elif x > y: w += 1
    n = len(games); dec = n - t; auc = 100 * (w + 0.5 * t) / n; p = binomtest(w, dec).pvalue if dec else 1.0
    auc_rows.append((m, n, w, t, dec, auc, p))
    P(f'| {m} | {n} | {w} | {t} | {dec} | {fl(auc, 1)} | {flp(p)} |')

# by opener
OPN = {'honeycup': 'Honey Cup', 'honey cup': 'Honey Cup', 'gamushiro': 'Gamushiro', 'stray cannon': 'Stray Cannon', 'meisou': 'Stray Cannon'}
def norm(o):
    b = o.replace('*', '').replace('(deviated)', '').strip().lower()
    return OPN.get(b, 'other'), ('*' in o or 'deviated' in o)
P('\n## By opener (p1 = syakegohan), pooled ratio of sums, included games\n')
mp = collections.Counter((r['opener'], norm(r['opener'])[0]) for r in out if r['player'] == 'p1')
P('Label mapping (all 108 games): ' + '; '.join(f'`{a}`→{b} ({n})' for (a, b), n in sorted(mp.items())) + '. '
  f'`*` / "(deviated)" labels folded in: {sum(n for (a, b), n in mp.items() if norm(a)[1])}. Stick Spin is filed as other.\n')
P('| opener | n games | p1 APP | p1 PPS | p1 APM | p1 won |\n|---|---|---|---|---|---|')
for op in ['Honey Cup', 'Gamushiro', 'Stray Cannon', 'other']:
    rs = [r for r in inc if r['player'] == 'p1' and norm(r['opener'])[0] == op]
    pv = pool(rs)
    P(f'| {op} | {len(rs)} | {fl(pv["APP"], 3)} | {fl(pv["PPS"], 3)} | {fl(pv["APM"], 2)} | {sum(r["won"] for r in rs)}/{len(rs)} |')

# records
q = [r for r in inc if r['duration_s'] >= 60]
P(f'\n## Rate records (games ≥ 60 s only: {len({r["id"] for r in q})} included games; counts are over every included game)\n')
P('| record | p1 (syakegohan) | p2 (opponent) |\n|---|---|---|')
for m, d in [('APM', 2), ('VS', 2), ('PPS', 3), ('APP', 3), ('landed_APM', 2)]:
    cells = []
    for p in ('p1', 'p2'):
        b = max((r for r in q if r['player'] == p), key=lambda r: r[m])
        cells.append(f'{fl(b[m], d)} ({b["id"]}, {fl(b["duration_s"], 1)} s{", " + (b["who"] or "opponent unnamed") if p == "p2" else ""})')
    P(f'| {m} | ' + ' | '.join(cells) + ' |')
for m in ['attack', 'max_combo', 'max_b2b', 'lines_cleared']:
    cells = []
    for p in ('p1', 'p2'):
        b = max((r for r in inc if r['player'] == p), key=lambda r: r[m])
        cells.append(f'{b[m]} ({b["id"]})')
    P(f'| {m} (count) | ' + ' | '.join(cells) + ' |')

P('\n## Caveats\n')
CAV = [
 'Pieces are systematically ~1 low per player-game: the A queue trace drops the final NEXT shift in the last 0.2–2.3 s (6 of 6 hand-checked last-15 s windows). PPS and APP are biased by about 0.3% (pieces low → PPS low, APP high).',
 'Stream-game durations (stream-2026-10-12) come from A and end at the board-drop/やった! overlay about 0.7 s after the loser\'s grey-out (g086, g090, g101); the winner\'s pieces locked in that tail are counted. Upload durations come from the frozen in-game timer and are not affected. The per-dataset rows isolate it.',
 'Received garbage is not corrected: the PC-duplicate defect also attached 2 phantom received rows to g101 p1 (that game is excluded), and the same may occur in other PC games. The KO grey-out may be counted as received garbage for losers; see the no-KO-tail landed APM column.',
 'A undercounts T-spins on the stream video; T-spin type is taken from on-screen banners matched by template, and A sometimes labels a TSD a double (verdict: g090, g086 — both excluded). Remaining mislabels lower base attack by 2–3 lines per case.',
 'Attack is computed, not observed: sent-before-cancellation from a published table, with REN bonus from the fused lock order. In spliced B windows REN/B2B are reset at tracking gaps (lower bound) and untyped gap lines carry no attack.',
 'Perfect Clear is treated as a flat 10 replacing the clear\'s own value and B2B; sources list PC as a clear type sending 10 and do not state stacking. B2B continuation through a PC follows the underlying clear kind.',
 'Ratio-of-sums pooling weights long games more; the stream dataset dominates the overall row.',
]
for c in CAV: P('- ' + c)
open('report.md', 'w').write('\n'.join(L) + '\n')
json.dump(dict(auc=auc_rows, cav=CAV), open('tetrio/report_extra.json', 'w'), ensure_ascii=False)
print('\n'.join(L))
