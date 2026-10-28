# TETR.IO-style metrics from the reconciled PPT2 counts (syakegohan, 108 games).  [am port: amemiya set 4xcAmo-s-Tg]
# Run from /private/tmp/claude-501/am/w/chain/am/w. Inputs: reconciled.jsonl, ../games.json, tetrio/seqs.pkl (tetrio/seqs.py).
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
UNRESOLVED = json.load(open('R/unresolved.json'))   # [am port] = R/build.py's printed unres_pg list (cVO hard-coded it)
NOT_TRUST = json.load(open('R/not_trust.json'))     # [am port] games whose A winner disagrees with the on-screen WIN counter
EXCL = sorted(set([u[:4] for u in UNRESOLVED] + NOT_TRUST))

# ---------------- PC-duplicate correction ----------------
# [am port] cVO's PCDEC is a frame-adjudicated table for cVO2eGipjV0 only. This set uses lg's chain instead: pcfix()
# (PERFECT CLEAR banner scan, below) then the generic rule of the B and lg trees: drop a same-lines clear <= 0.6 s
# after a pc-flagged clear. Every PC event is listed in out/flags.json for a frame check.
def correct(seq, window=0.6):
    out = []; dropped = []
    for i, z in enumerate(seq):
        if out and z[1] not in (None, 'BREAK') and out[-1][3] and out[-1][1] not in (None, 'BREAK') \
                and z[2] == out[-1][2] and z[0] - out[-1][0] <= window + 1e-9:
            dropped.append(z); continue
        out.append(z)
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
pass  # [am port] witnessed.json (frame-witnessed partial-flash REN clears) is cVO/lg/B-specific: none for this set
CURX = [None]
KOTAB = {}  # [am port] kotab.json (post-KO drop table) is per-set hand data: none for this set
POSTKO_LOG = []
def postko(g, t):
    if g not in KOTAB: return False
    t0, ko, K = KOTAB[g]
    return round((t - t0) * 30) > K

import json as _oj
import os as _os
_OVLF = '/private/tmp/claude-501/am/corr/event-corrections.json'
OVL = _oj.load(open(_OVLF)) if _os.path.exists(_OVLF) else []  # [am port] this set's frame-check corrections
CSEQ = {}
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

# ---------------- PC fix, copied verbatim from chain/lg/w/tetrio/metrics.py [am port] ----------------
# PC existence/count from the PERFECT CLEAR banner scan (R/pcscan.py -> R/pcban.json, segments >= 0.5 s).
# The PC is the latest A clear in [banner-1.5, banner+0.3]; A clears of the same line count up to 1.0 s before it are
# double-logs of the same clear (frame-verified i000 0.73 s, i008, i012 0.27 s and 0.86 s). A pc flags without a banner are cleared.
PCB = json.load(open('R/pcban.json'))
PCFIX_LOG = []
def pcfix(g, p, seq):
    bans = [t for t, d in PCB[g][p] if d >= 0.5]
    seq = [list(z) for z in seq]; drop = set(); pcidx = set()
    for tb in bans:
        cand = [i for i, z in enumerate(seq) if z[1] not in (None, 'BREAK') and z[5] == 'A' and tb - 1.5 <= z[0] <= tb + 0.3 and i not in drop]
        if not cand:
            PCFIX_LOG.append((g, p, tb, 'NO A CLEAR')); continue
        k = cand[-1]; pcidx.add(k)
        for i in cand[:-1]:
            if seq[i][2] == seq[k][2] and seq[k][0] - seq[i][0] <= 1.0 + 1e-9:
                drop.add(i); PCFIX_LOG.append((g, p, tb, 'drop dup', tuple(seq[i][:3])))
    for i, z in enumerate(seq):
        newpc = i in pcidx
        if bool(z[3]) != newpc: PCFIX_LOG.append((g, p, 'pc flag', tuple(z[:4]), '->', newpc))
        z[3] = newpc
    return [tuple(z) for i, z in enumerate(seq) if i not in drop], len(drop)

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
        fseq, nfix = pcfix(g, p, seq)   # [am port] lg's banner-driven PC fix, then the generic duplicate rule (as lg)
        cseq, dropped = correct(fseq)
        _, dropped_any = correct(seq, window=99)
        dup_log += [(g, p, z) for z in dropped]; dup_log_any += [(g, p, z) for z in dropped_any]
        _n0 = len(cseq); cseq = [z for z in cseq if not postko(g, z[0])]; (POSTKO_LOG.append((g, p, _n0 - len(cseq))) if _n0 != len(cseq) else None)
        CSEQ[f'{g} {p} pre'] = [[round(z[0], 2), z[1], z[2], int(bool(z[3])), z[4]] for z in cseq]
        cseq = overlay(g, p, cseq)
        CSEQ[f'{g} {p}'] = [[round(z[0], 2), z[1], z[2], int(bool(z[3])), z[4]] for z in cseq]
        CURX[0] = (g, p); T = tally(cseq); CURX[0] = None
        rows.append(dict(id=g, player=p, T=T, n_dup=len(dropped) + nfix, r=rr, dur=r['duration_s'], winner=r['winner']))
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
    rec = dict(id=g, dataset=gm['dataset'], opener=gm['opener'], player=p, who='amemiya' if p == 'p1' else gm['opponent'],
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
_oj.dump([dict(index=a[0], id=a[1], side=a[2], op=a[3], before=a[4], after=a[5]) for a in OVL_APPLIED], open('tetrio/overlay_applied.json', 'w'), indent=1)
for x in PCFIX_LOG: print('PCFIX', x)
print('rows', len(out)); print('postko drops (g,p,n):', POSTKO_LOG, 'kotab games', len(KOTAB))
_oj.dump(CSEQ, open('tetrio/cseq.json', 'w'))  # [am port] the exact event list tally() saw, per player-game
