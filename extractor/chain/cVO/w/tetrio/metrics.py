# TETR.IO-style metrics from the reconciled PPT2 counts (syakegohan, 108 games).
# Run from /private/tmp/claude-501/sk/metrics. Inputs: reconciled.jsonl, ../games.json, tetrio/seqs.pkl (tetrio/seqs.py).
import json, pickle, math, collections, csv, sys
from scipy.stats import binomtest

R = {j['id']: j for j in map(json.loads, open('reconciled.jsonl'))}
G = {g['id']: g for g in json.load(open('../games.json'))}
S = pickle.load(open('tetrio/seqs.pkl', 'rb'))
EV = {g: pickle.load(open(f'R/ev/{g}.pkl', 'rb')) for g in R}

# ---------------- attack table (PPT/PPT2 Tetris vs Tetris) ----------------
# tetris.wiki/Puyo_Puyo_Tetris (left value of each slash = Tetris-only matches) and howtotetris.com/combos (PPT2 column)
BASE = dict(single=0, double=1, triple=2, quad=4, tss=2, tsd=4, tst=6, tsmini=0)
DIFF = {'quad', 'tss', 'tsd', 'tst', 'tsmini'}
PC_SEND = 10
COMBO_WIKI = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5]          # REN 0..10, 11+ = 5  (tetris.wiki PPT; also Tetris Online JP)
COMBO_HTT = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 5]     # REN 0..12, 13+ = 5  (howtotetris PPT2)
def combo(ren, tab):
    return tab[min(ren, len(tab) - 1)]

# ---------------- exclusions ----------------
UNRESOLVED = ['h031p2']
NOT_TRUST = []
EXCL = sorted(set([u[:4] for u in UNRESOLVED] + NOT_TRUST))

# ---------------- PC-duplicate correction ----------------
# cVO2eGipjV0: A's pc flag sits on the phantom half of a double-logged PC on this video, so the old
# "drop a same-lines clear <=0.6 s after a pc-flagged clear" rule is replaced by a frame-adjudicated table
# keyed to the PERFECT CLEAR banner (R/pcscan.py + R/pcon.py, every banner checked by eye; see reconcile md).
PCDEC = {
 ('h002','p2'): [(254.43,[254.1])],
 ('h003','p2'): [(400.37,[400.2]),(401.63,[401.4])],
 ('h006','p1'): [(614.77,[614.53])],
 ('h007','p2'): [(646.4,[])],
 ('h010','p2'): [(911.7,[911.33])],
 ('h012','p2'): [(999.7,[999.33])],
 ('h013','p2'): [(1085.87,[1085.67])],
 ('h015','p1'): [(1249.37,[1248.93])],
 ('h015','p2'): [(1249.03,[1248.73])],
 ('h016','p1'): [(1429.6,[1428.43])],
 ('h016','p2'): [(1429.53,[])],
 ('h017','p1'): [(1479.13,[1478.57])],
 ('h017','p2'): [(1479.77,[])],
 ('h018','p1'): [(1515.4,[1514.97])],
 ('h019','p2'): [(1577.93,[1577.7]),(1693.33,[1692.53])],
 ('h020','p1'): [(2033.4,[2033.17])],
 ('h021','p1'): [(2079.9,[2079.0])],
 ('h029','p1'): [(2791.43,[2790.9]),(2798.1,[2797.73,2798.3])],
 ('h029','p2'): [(2791.07,[2790.8])],
 ('h030','p1'): [(2871.6,[]),(2912.3,[2911.57])],
 ('h031','p1'): [(3212.47,[])],
}
CUR = [None]
def correct(seq, window=0.6):
    dec = PCDEC.get(CUR[0], [])
    pcs = {t for t, _ in dec}; drops = {d for _, ds in dec for d in ds}
    hit = set(); out = []; dropped = []
    for z in seq:
        if z[1] in (None, 'BREAK'): out.append(z); continue
        if any(abs(z[0] - d) < 0.02 for d in drops): dropped.append(z); hit.add(('d', z[0])); continue
        ispc = any(abs(z[0] - t) < 0.02 for t in pcs)
        if ispc: hit.add(('p', z[0]))
        out.append((z[0], z[1], z[2], ispc, z[4], z[5]))
    assert len(hit) == len(pcs) + len(drops), (CUR[0], hit, dec)
    return out, dropped

def streaks(kinds):  # referee's rule (R/seqfn.py): REN = clears in a row - 1; B2B = difficult clears in a row - 1
    run = 0; mc = 0; b = -1; mb = 0
    for k in kinds:
        if k == 'BREAK': run = 0; b = -1; continue
        if k is None: run = 0; continue
        run += 1; mc = max(mc, run - 1)
        if k == 'renx': continue   # partial-flash clear: REN yes, B2B transparent
        if k in DIFF: b += 1; mb = max(mb, b)
        else: b = -1
    return mc, max(mb, 0)

import json as _j
RENX = {}
for _g, _p, _t in _j.load(open('/private/tmp/claude-501/sk/endfix/combo/rerun/witnessed.json')): RENX.setdefault((_g, _p), set()).add(_t)
CURX = [None]
KOTAB = {} if '/private/tmp/claude-501/sk/endfix/combo/rerun/kotab.json' == 'none' else _j.load(open('/private/tmp/claude-501/sk/endfix/combo/rerun/kotab.json'))
POSTKO_LOG = []
def postko(g, t):
    if g not in KOTAB: return False
    t0, ko, K = KOTAB[g]
    return round((t - t0) * 30) > K

import json as _oj
OVL = _oj.load(open('/private/tmp/claude-501/sk/endfix/combo3/apply/corrections3.json'))
OVL_APPLIED = []
def _ovl_hits(cs, t):
    return [i for i, z in enumerate(cs) if z[1] not in (None, 'BREAK') and round(z[0], 2) == round(t, 2)]
def overlay(g, p, cs):
    cs = list(cs)
    for ci, c in enumerate(OVL):
        if c['id'] != g or c['side'] != p: continue
        op = c['op']; t = c['t']
        if op == 'add':
            assert not [z for z in cs if round(z[0], 2) == round(t, 2)], ('OVERLAY add: an event already at t', c)
            new = (t, c['kind'], int(c['lines']), bool(c['pc']), int(c.get('gc', 0)), 'O')
            j = next((i for i, z in enumerate(cs) if z[0] > t), len(cs)); cs.insert(j, new)
            OVL_APPLIED.append((ci, g, p, op, None, new)); continue
        if op == 'replace_window':
            idx = [i for i, z in enumerate(cs) if t - 1e-9 <= z[0] <= c['t_end'] + 1e-9]
            assert idx, ('OVERLAY replace_window: empty window', c)
            old = [cs[i] for i in idx]
            if 'was_old' in c:
                assert [[round(z[0], 2), z[1], z[2]] for z in old] == [[round(w[0], 2), w[1], int(w[2])] for w in c['was_old']], ('OVERLAY replace_window was_old mismatch', c, old)
            cs = [z for i, z in enumerate(cs) if i not in set(idx)]
            for e in c['events']:
                new = (e['t'], e['kind'], int(e['lines']), bool(e['pc']), int(e.get('gc', 0)), 'O')
                j = next((i for i, z in enumerate(cs) if z[0] > new[0]), len(cs)); cs.insert(j, new)
            OVL_APPLIED.append((ci, g, p, op, old, c['events'])); continue
        h = _ovl_hits(cs, t)
        assert len(h) == 1, ('OVERLAY: t must match exactly one clear event', c, [cs[i] for i in h])
        i = h[0]; z = cs[i]
        w = c['was']; assert [z[1], z[2], int(bool(z[3]))] == [w[0], int(w[1]), int(w[2])], ('OVERLAY was-mismatch', c, z)
        if op == 'remove': cs.pop(i); new = None
        elif op == 'retype': new = (z[0], c['kind'], int(c['lines']), bool(c['pc']) if 'pc' in c else z[3], int(c['gc']) if 'gc' in c else z[4], z[5]); cs[i] = new
        elif op == 'setpc': new = (z[0], z[1], z[2], bool(c['pc']), z[4], z[5]); cs[i] = new
        else: raise ValueError(('OVERLAY unknown op', c))
        OVL_APPLIED.append((ci, g, p, op, z, new))
    return cs

def tally(seq):
    c = collections.Counter(); lines = 0; gclr = 0; gap_lines = 0
    att = collections.Counter(); run = 0; b2b = False; ren1112 = 0
    for t, k, n, pc, gc, org in seq:
        if k == 'BREAK':
            gap_lines += n; lines += n; run = 0; b2b = False; continue
        if k is None: run = 0; continue
        c[k] += 1; lines += n; gclr += gc
        if pc: c['pc'] += 1
        run += 1; ren = run - 1
        if ren in (11, 12): ren1112 += 1
        att['combo'] += combo(ren, COMBO_WIKI); att['combo_htt'] += combo(ren, COMBO_HTT)
        if pc:
            att['pc'] += PC_SEND
        else:
            att['base'] += BASE[k]
            if k in DIFF and b2b: att['b2b'] += 1
        b2b = (k in DIFF) if k in DIFF else False
    W = RENX.get(CURX[0], set())
    mc, mb = streaks(['renx' if (k is None and org == 'A' and round(t, 2) in W) else k for t, k, n, pc, gc, org in seq])
    return dict(clears=c, lines=lines, gclr=gclr, gap_lines=gap_lines, att=att, max_combo=mc, max_b2b=mb, ren1112=ren1112)

# controls: uncorrected tally reproduces reconciled (except g003 p2 hand override)
ctrl_bad = []
rows = []; dup_log = []; dup_log_any = []
for g in sorted(R):
    r = R[g]
    for p in ('p1', 'p2'):
        seq = S[(g, p)]['seq']
        raw = tally(seq)
        rr = r[p]
        for f, v in [('lines_cleared', raw['lines']), ('garbage_cleared', raw['gclr']), ('max_combo', raw['max_combo']), ('max_b2b', raw['max_b2b'])]:
            if v != rr[f]: ctrl_bad.append((g, p, f, v, rr[f]))
        for k in BASE:
            if raw['clears'][k] != rr['clears'][k]: ctrl_bad.append((g, p, k, raw['clears'][k], rr['clears'][k]))
        CUR[0] = (g, p)
        cseq, dropped = correct(seq)
        dropped_any = dropped
        dup_log += [(g, p, z) for z in dropped]; dup_log_any += [(g, p, z) for z in dropped_any]
        _n0 = len(cseq); cseq = [z for z in cseq if not postko(g, z[0])]; (POSTKO_LOG.append((g, p, _n0 - len(cseq))) if _n0 != len(cseq) else None)
        cseq = overlay(g, p, cseq)
        CURX[0] = (g, p); T = tally(cseq); CURX[0] = None
        rows.append(dict(id=g, player=p, T=T, n_dup=len(dropped), r=rr, dur=r['duration_s'], winner=r['winner']))
print('control mismatches (uncorrected tally vs reconciled):', ctrl_bad)
print('PC duplicates dropped (<=0.6 s):', len(dup_log), 'player-games', len({(g, p) for g, p, _ in dup_log}),
      '| any-gap rule:', len(dup_log_any))
pc_total = sum(x['T']['clears']['pc'] for x in rows)
print('PC events (sequence)', pc_total)
extra_any = sorted(set(dup_log_any) - set(dup_log))
print('extra drops under any-gap rule:', [(g, p, z[0], z[1]) for g, p, z in extra_any])

# loser's last-lock garbage (KO grey-out candidate)
def last_garb(g, p):
    ev = [e for e in EV[g]['a'][p] if e.get('kind') != 'hold-empty']
    return ev[-1].get('garbage', 0) if ev else 0

# ---------------- per player-game metrics ----------------
by = {(x['id'], x['player']): x for x in rows}
out = []
for x in rows:
    g, p = x['id'], x['player']; o = 'p2' if p == 'p1' else 'p1'
    rr = x['r']; T = x['T']; d = x['dur']; pieces = rr['pieces']
    attack = T['att']['base'] + T['att']['b2b'] + T['att']['combo'] + T['att']['pc']
    attack_htt = attack - T['att']['combo'] + T['att']['combo_htt']
    opp_recv = R[g][o]['garbage_received_rows']
    loser = 'p1' if R[g]['p1']['topped_out'] else 'p2'
    opp_recv_noko = opp_recv - (last_garb(g, o) if o == loser else 0)
    gm = G[g]
    rec = dict(id=g, dataset=gm['dataset'], opener=gm['opener'], player=p, who='syakegohan' if p == 'p1' else gm['opponent'],
               won=int(R[g]['winner'] == p), duration_s=d, pieces=pieces, lines_cleared=T['lines'], gap_lines_untyped=T['gap_lines'],
               garbage_received_rows=rr['garbage_received_rows'], garbage_cleared=T['gclr'],
               **{k: T['clears'][k] for k in ['single', 'double', 'triple', 'quad', 'tss', 'tsd', 'tst', 'tsmini', 'pc']},
               max_combo=T['max_combo'], max_b2b=T['max_b2b'], pc_dups_removed=x['n_dup'],
               attack_base=T['att']['base'], attack_b2b=T['att']['b2b'], attack_combo=T['att']['combo'], attack_pc=T['att']['pc'],
               attack=attack, attack_combo_alt=T['att']['combo_htt'], attack_alt=attack_htt, ren11_12_clears=T['ren1112'],
               opp_garbage_received=opp_recv, opp_garbage_received_no_ko=opp_recv_noko,
               confidence=rr['confidence'], excluded=int(g in EXCL),
               reason=('unresolved lower bound' if f'{g}{p}' in UNRESOLVED else '') + (' not-trustworthy verdict game' if g in NOT_TRUST else '') + (' game excluded (other player)' if g in EXCL and f'{g}{p}' not in UNRESOLVED and g not in NOT_TRUST else ''))
    rec.update(PPS=pieces / d, APM=60 * attack / d, VS=100 * (attack + T['gclr']) / d, APP=attack / pieces if pieces else None,
               DS_per_piece=T['gclr'] / pieces if pieces else None, LPM=60 * T['lines'] / d, landed_APM=60 * opp_recv / d,
               landed_APM_no_ko=60 * opp_recv_noko / d)
    out.append(rec)

with open('metrics.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
pickle.dump(dict(out=out, dup=dup_log, dup_any=dup_log_any, ctrl=ctrl_bad, EXCL=EXCL), open('tetrio/out.pkl', 'wb'))
_miss = [c for ci, c in enumerate(OVL) if c['id'] in R and ci not in {a[0] for a in OVL_APPLIED}]
assert not _miss, ('OVERLAY corrections not applied', _miss)
for _a in OVL_APPLIED: print('OVERLAY', _a)
_oj.dump([dict(index=a[0], id=a[1], side=a[2], op=a[3], before=a[4], after=a[5]) for a in OVL_APPLIED], open('/private/tmp/claude-501/sk/endfix/combo3/apply/c3/cVO/w/tetrio/overlay_applied.json', 'w'), indent=1)
print('rows', len(out)); print('postko drops (g,p,n):', POSTKO_LOG, 'kotab games', len(KOTAB))
