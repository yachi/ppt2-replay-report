# Extractor B (method: cell accounting on a debounced occupancy board).
# Reads per-cell mean RGB sampled by sample.py (cells2/<id>.npz); never reads NEXT/HOLD.
import numpy as np, sys, json, itertools, os
FPS = 30
# ---------------- colour classification ----------------
# classes: 0 empty, 1 grey (garbage / flash white), 2 Z, 3 L, 4 O, 5 S, 6 I/J (merged, I-vs-J not load-bearing), 8 T
def hsv(rgb):
    rgb = rgb.astype(np.float32) / 255; mx = rgb.max(-1); mn = rgb.min(-1); d = mx - mn
    s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0); r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    dd = np.maximum(d, 1e-9)
    h = np.where(mx == r, ((g - b) / dd) % 6, np.where(mx == g, (b - r) / dd + 2, (r - g) / dd + 4)) * 60
    return h, s, mx
PROTO = np.array([[204, 48, 54], [240, 114, 12], [240, 192, 24], [102, 180, 42], [12, 156, 204], [12, 90, 180], [138, 48, 138]], np.float32)
def classify(rgb):
    """0 empty, 1 grey (garbage / clear flash), 2 Z, 3 L, 4 O, 5 S, 6 I, 7 J, 8 T, 9 unknown (glow / effect)"""
    h, s, v = hsv(rgb)
    x = rgb.astype(np.float32)
    d = np.sqrt(((x[..., None, :] - PROTO) ** 2).sum(-1))
    k = d.argmin(-1); dm = d.min(-1)
    c = np.full(h.shape, 9, np.int8)
    c[dm < 45] = (k + 2)[dm < 45]
    c[(s < 0.2) & (v >= 0.65)] = 1
    c[v < 0.45] = 0
    return c
def debounce(cls, k):
    # unknown (9 = glow / lock flash) carries no information: forward-fill the previous raw class
    cls = cls.copy()
    cls[0][cls[0] == 9] = 0
    for i in range(1, len(cls)):
        m = cls[i] == 9; cls[i][m] = cls[i - 1][m]
    out = np.zeros_like(cls); cur = cls[0].copy(); prev = cls[0].copy(); run = np.ones(cls.shape[1:], np.int32)
    for i in range(len(cls)):
        x = cls[i]; run = np.where(x == prev, run + 1, 1); prev = x
        cur = np.where(run >= k, x, cur); out[i] = cur
    return out
# ---------------- tetromino geometry ----------------
def norm(cells):
    r0 = min(r for r, c in cells); c0 = min(c for r, c in cells)
    return frozenset((r - r0, c - c0) for r, c in cells)
BASE = {'I': [(0,0),(0,1),(0,2),(0,3)], 'O': [(0,0),(0,1),(1,0),(1,1)], 'T': [(0,0),(0,1),(0,2),(1,1)],
        'S': [(0,0),(0,1),(1,1),(1,2)], 'Z': [(1,0),(1,1),(0,1),(0,2)], 'L': [(0,0),(0,1),(0,2),(1,2)], 'J': [(0,0),(0,1),(0,2),(1,0)]}
SHAPES = {}
for name, cl in BASE.items():
    cur = cl
    for _ in range(4):
        SHAPES[norm(cur)] = name
        cur = [(c, -r) for r, c in cur]
def shape_of(cells):
    if len(cells) != 4: return None
    return SHAPES.get(norm(cells))
# ---------------- board helpers ----------------
def comps(mask):
    seen = np.zeros_like(mask, bool); out = []
    for r, c in zip(*np.nonzero(mask)):
        if seen[r, c]: continue
        st = [(r, c)]; seen[r, c] = True; comp = []
        while st:
            a, b = st.pop(); comp.append((int(a), int(b)))
            for x, y in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)):
                if 0 <= x < 20 and 0 <= y < 10 and mask[x, y] and not seen[x, y]:
                    seen[x, y] = True; st.append((x, y))
        out.append(comp)
    return out
def is_garbage_row(qc_row):
    occ = qc_row > 0
    return occ.sum() == 9 and (qc_row[occ] == 1).sum() >= 8
def supported(cells, board):
    s = set(cells)
    for r, c in cells:
        if r == 0: return True
        if (r-1, c) not in s and board[r-1, c]: return True
    return False
def tspin_kind(cells, pre, lines):
    """pre: occupancy board before the lock (post any garbage shift). Returns None/'full'/'mini'."""
    s = set(cells); ctr = None
    for r, c in cells:
        if sum((r+dr, c+dc) in s for dr, dc in ((1,0),(-1,0),(0,1),(0,-1))) == 3: ctr = (r, c)
    if ctr is None: return None
    r, c = ctr
    miss = [d for d in ((1,0),(-1,0),(0,1),(0,-1)) if (r+d[0], c+d[1]) not in s][0]
    nub = (-miss[0], -miss[1]); perp = (nub[1], nub[0])
    def occ(rr, cc):
        if cc < 0 or cc > 9 or rr < 0: return True
        if rr > 19: return False
        return bool(pre[rr, cc])
    front = [occ(r+nub[0]+perp[0], c+nub[1]+perp[1]), occ(r+nub[0]-perp[0], c+nub[1]-perp[1])]
    back = [occ(r-nub[0]+perp[0], c-nub[1]+perp[1]), occ(r-nub[0]-perp[0], c-nub[1]-perp[1])]
    if sum(front) + sum(back) < 3: return None
    if all(front) or lines >= 3: return 'full'
    return 'mini'
# ---------------- transition solver ----------------
def consistent(E, Qc):
    if (E & (Qc == 0)).any(): return False
    for r in range(20):
        if (Qc[r] > 0).all() and not E[r].all(): return False   # a flashing full row the belief lacks
    extra = (Qc > 1) & (Qc < 9) & ~E
    for cc in comps(extra):
        if len(cc) > 4 or supported(cc, E): return False
    return True
def collapse(E, O, rows):
    keep = [r for r in range(20) if r not in rows]
    E2 = np.zeros_like(E); E2[:len(keep)] = E[keep]
    O2 = np.zeros_like(O); O2[:len(keep)] = O[keep]
    return E2, O2, keep
def ops(st, Qc, gmax):
    """yield successor states. st = (E, O, oplist)"""
    E, O, L = st
    full = [r for r in range(20) if E[r].all()]
    if full:                                          # pending clear: nothing else may happen first
        E2, O2, keep = collapse(E, O, set(full))
        yield (E2, O2, L + [dict(op='clear', rows=full, gc=int(sum((O[r] == 1).sum() >= 6 for r in full)), pc=not E2.any())])
        return
    flash = np.zeros_like(E)
    for r in range(20):
        if (Qc[r] > 0).all() and not E[r].all(): flash[r] = ~E[r]
    extra = ((Qc > 1) | flash) & ~E
    for cc in comps(extra):
        cols = set(int(Qc[r, c]) for r, c in cc if 1 < Qc[r, c] < 9)
        if shape_of(cc) and supported(cc, E):
            E2 = E.copy(); O2 = O.copy()
            for r, c in cc: E2[r, c] = True; O2[r, c] = 2
            yield (E2, O2, L + [dict(op='lock', piece=cc, pre=E.copy(), colour=[int(Qc[r, c]) for r, c in cc])])
        elif len(cc) == 8:   # two pieces landed between snapshots: split into two tetrominoes, lower first
            first = min(cc); rest = [x for x in cc if x != first]
            for sub in itertools.combinations(rest, 3):
                p1 = [first] + list(sub); p2 = [x for x in cc if x not in p1]
                if not (shape_of(p1) and shape_of(p2)): continue
                for a1, a2 in ((p1, p2), (p2, p1)):
                    if not supported(a1, E): continue
                    Ea = E.copy()
                    for r, c in a1: Ea[r, c] = True
                    if not supported(a2, Ea): continue
                    if any(Ea[r].all() for r in range(20)): continue
                    E2 = Ea.copy(); O2 = O.copy()
                    for r, c in a2: E2[r, c] = True
                    for r, c in cc: O2[r, c] = 2
                    yield (E2, O2, L + [dict(op='lock', piece=a1, pre=E.copy(), colour=[]), dict(op='lock', piece=a2, pre=Ea, colour=[])])
                    break
    for g in range(1, gmax + 1):
        if E[20 - g:].any(): break
        E2 = np.zeros_like(E); E2[g:] = E[:20 - g]; E2[:g] = Qc[:g] > 0
        O2 = np.zeros_like(O); O2[g:] = O[:20 - g]; O2[:g] = np.where(Qc[:g] > 0, 1, 0)
        yield (E2, O2, L + [dict(op='garbage', g=g)])
    # lock whose cells are partly removed by the clear it causes (flash state not captured)
    if not (E & (Qc == 0)).any(): return     # nothing vanished: no clear can have happened
    cnt = E.sum(1)
    cand = [r for r in range(20) if 6 <= cnt[r] < 10]
    for n in range(1, 5):
        for R in itertools.combinations(cand, n):
            if R[-1] - R[0] > 3 or sum(10 - cnt[r] for r in R) > 4: continue
            fc = [c for r in R for c in range(10) if not E[r, c]]
            if max(fc) - min(fc) > 3: continue
            Rs = set(R) | set(full)
            E2, O2, keep = collapse(E, O, Rs)
            if (E2 & (Qc == 0)).any(): continue
            add = (Qc > 1) & (Qc < 9) & ~E2
            fl = set()
            for cc in comps(add):
                if not supported(cc, E2) and len(cc) <= 4: fl |= set(cc)
            vis = [(r, c) for r, c in zip(*np.nonzero(add)) if (r, c) not in fl and r < len(keep)]
            piece = [(int(keep[r]), int(c)) for r, c in vis] + [(r, c) for r in R for c in range(10) if not E[r, c]]
            if shape_of(piece) and supported(piece, E):
                Ep = E.copy()
                for r, c in piece: Ep[r, c] = True
                E3, O3, keep = collapse(Ep, O, Rs)
                pre = E.copy()
                yield (E3, O3, L + [dict(op='lock', piece=piece, pre=pre, colour=[], merged=True),
                                    dict(op='clear', rows=sorted(Rs), gc=int(sum((O[r] == 1).sum() >= 6 for r in Rs)), pc=not E3.any())])
def solve(B, Bo, Qc, depth=3):
    gmax = 0
    while gmax < 12 and is_garbage_row(Qc[gmax]): gmax += 1
    if consistent(B, Qc): return []
    frontier = [(B, Bo, [])]
    for d in range(depth):
        nxt = []
        for st in frontier:
            for st2 in ops(st, Qc, gmax):
                if consistent(st2[0], Qc): return st2
                nxt.append(st2)
        frontier = nxt
        if len(frontier) > 80: frontier = frontier[:80]
    return None
def border_end(z, start, end_upper, t0):
    """end of game: first frame (after start+3s) where a board's frame strip leaves its reference for >=10 frames"""
    bd = z['borders'].astype(np.float32)  # n,2,2,25,3
    n = len(bd); i0 = int((start - t0) * FPS); i1 = min(n, int((end_upper - t0) * FPS))
    ref = np.median(bd[i0 + 15:i0 + 90], axis=0)  # first ~0.5-3 s of play
    dist = np.abs(bd - ref[None]).sum(-1)  # n,2,2,25
    match = (dist < 60).mean(axis=(2, 3))  # n,2 fraction of frame points matching
    res = {}
    for p in range(2):
        bad = match[:, p] < 0.5
        run = 0; endf = None
        for i in range(i0 + 90, i1):
            run = run + 1 if bad[i] else 0
            if run >= 10: endf = i - 9; break
        res[p] = endf
    return res, match
def ffill(cls):
    cls = cls.copy(); cls[0][cls[0] == 9] = 0
    for i in range(1, len(cls)):
        m = cls[i] == 9; cls[i][m] = cls[i - 1][m]
    return cls
def flash_events(ff, minrun=2, gap=6, follow=15):
    """rows entirely grey/white = line-clear flash. Returns [(onset_frame_rel, rows)], follow-up flashes of an
    adjacent single row within `follow` frames (the clear animation sliding down) are merged away."""
    full = (ff == 1).all(-1); ev = []; cur = None
    for j in range(len(full)):
        rows = {r for r in np.nonzero(full[j])[0].tolist() if full[j:j + minrun, r].all()}
        new = {r for r in rows if not (j > 0 and full[j - 1, r])}
        if not new: continue
        if cur and j - cur[0] <= gap: cur[1].update(new); continue
        if cur and j - cur[0] <= follow and len(new) == 1 and (min(new) == min(cur[1]) - 1 or max(new) == max(cur[1]) + 1):
            continue
        if cur: ev.append(cur)
        cur = [j, set(new)]
    if cur: ev.append(cur)
    return [(f, sorted(r)) for f, r in ev]
def n_garbage_rows(Qc):
    k = 0
    while k < 20 and (Qc[k] > 0).sum() == 9 and (Qc[k] == 1).sum() >= 8: k += 1
    return k
W_FLASH = 1.0   # calibrated on 40 tracked 1.5-s windows of g000/g051 (calib.py)
W_RATE = 1.0
def gap_estimate(delta, ng_before, ng_after, c_flash, lexp=None):
    """solve 4L - 10C + 9G = delta (method-B identity) for a stretch the tracker could not follow"""
    best = None
    for G in range(max(0, ng_after - ng_before), max(0, ng_after - ng_before) + 13):
        for C in range(0, 13):
            x = delta + 10 * C - 9 * G
            if x < 0 or x % 4: continue
            L = x // 4
            cost = abs(C - c_flash) * W_FLASH + (G - max(0, ng_after - ng_before)) + (0.1 * L if lexp is None else W_RATE * abs(L - lexp))
            if best is None or cost < best[0]: best = (cost, L, C, G)
    return best
def analyze_player(Qall, i_start, i_end, k=4, trace=None):
    off = max(0, i_start - 10)
    db = debounce(Qall[off:i_end], k)
    fev = flash_events(ffill(Qall[off:i_end]))
    gaps = []
    B = np.zeros((20, 10), bool); Bo = np.zeros((20, 10), np.int8)
    locks = []; events = []; resyncs = []; mismatch_since = None; last = None
    pending = None; garbage_rows = 0
    for j in range(len(db)):
        i = j + off
        if i < i_start: continue
        Qc = db[j]; key = Qc.tobytes()
        if key == last: continue
        last = key
        sol = solve(B, Bo, Qc)
        if sol is None and locks and locks[-1].get('undoable'):
            # lock-delay undo: the last lock's cells moved (piece was still active)
            Lk = locks[-1]; B2 = B.copy(); O2 = Bo.copy()
            for r, c in Lk['piece']: B2[r, c] = False; O2[r, c] = 0
            sol2 = solve(B2, O2, Qc)
            if sol2 is not None:
                locks.pop(); events.append(dict(f=i, kind='undo')); B, Bo = B2, O2; sol = sol2
                if pending is not None and pending >= len(locks): pending = None
        if trace: trace(i, B, Qc, sol)
        if sol is None:
            if mismatch_since is None: mismatch_since = i
            if i - mismatch_since >= int(1.5 * FPS):
                nb = (Qc > 0) & (Qc < 9)
                nb |= (Qc == 9) & B   # grey kept only where a block/garbage already was
                for cc in comps(nb):
                    if len(cc) <= 4 and not supported(cc, nb): 
                        for r, c in cc: nb[r, c] = False
                resyncs.append(dict(f=i, since=mismatch_since, delta=int(nb.sum() - B.sum()), B=B.copy(), Q=Qc.copy()))
                j0 = mismatch_since - off - 3
                fl = [r for f, r in fev if j0 <= f <= j]
                bq = np.where(B, np.where(Bo == 1, 1, 2), 0)
                el = (mismatch_since - i_start) / FPS
                rate = 2.0 if el < 5 else min(4.0, max(1.0, (len(locks) + sum(g['pieces'] for g in gaps)) / el))
                est = gap_estimate(int(nb.sum() - B.sum()), n_garbage_rows(bq), n_garbage_rows(Qc), sum(len(r) for r in fl),
                                   lexp=rate * (i - mismatch_since) / FPS)
                if est:
                    _, Lg, Cg, Gg = est
                    gaps.append(dict(f=i, since=mismatch_since, pieces=Lg, lines=Cg, garbage=Gg,
                                     flash=[len(r) for r in fl] if sum(len(r) for r in fl) == Cg else None))
                    garbage_rows += Gg
                Bo = np.where(nb, np.where((Bo == 1) | (Qc == 1), 1, 3), 0).astype(np.int8); B = nb
                mismatch_since = None; pending = None
                for Lk in locks: Lk['undoable'] = False
            continue
        mismatch_since = None
        if not sol: continue
        E, O, oplist = sol
        for Lk in locks: Lk['undoable'] = False
        for op in oplist:
            if op['op'] == 'garbage':
                garbage_rows += op['g']; events.append(dict(f=i, kind='garbage', g=op['g']))
            elif op['op'] == 'lock':
                Lk = dict(f=i, piece=op['piece'], type=shape_of(op['piece']), pre=op['pre'], lines=0, C=[],
                          undoable=not op.get('merged'), colour=op['colour'])
                if any(E[r].all() for r in range(20)) and op is oplist[-1]: Lk['undoable'] = False
                locks.append(Lk); pending = len(locks) - 1
                events.append(dict(f=i, kind='lock', type=Lk['type']))
            elif op['op'] == 'clear':
                ev = dict(f=i, kind='clear', lines=len(op['rows']), garbage_cleared=op['gc'], pc=op['pc'], lock=pending)
                if pending is not None and locks[pending]['lines'] == 0:
                    Lk = locks[pending]; Lk['lines'] = len(op['rows']); Lk['gc'] = op['gc']; Lk['pc'] = op['pc']; Lk['undoable'] = False
                else:
                    ev['orphan'] = True
                events.append(ev); pending = None
        if locks and oplist[-1]['op'] == 'lock' and not E[[r for r in range(20)]].all(1).any():
            pass
        B, Bo = E, O
    return dict(locks=locks, events=events, resyncs=resyncs, gaps=gaps, garbage_rows=garbage_rows, final_cells=int(B.sum()))
def summarize(res):
    clears = dict(single=0, double=0, triple=0, quad=0, tss=0, tsd=0, tst=0, tsmini=0, pc=0)
    NAME = {1: 'single', 2: 'double', 3: 'triple', 4: 'quad'}
    lines = 0; gc = 0; combo = 0; maxcombo = 0; chain = 0; maxchain = 0; orphan_lines = 0; unclassified = 0
    seq = [(L['f'], 0, L) for L in res['locks']] + [(g['f'], 1, g) for g in res['gaps']]
    seq.sort(key=lambda x: (x[0], x[1]))
    for f, kind, x in seq:
        if kind == 1:   # untracked stretch: totals from the identity, chains unknown -> reset
            lines += x['lines']; combo = 0; chain = 0
            if x['flash']:
                for n in x['flash']: clears[NAME[min(n, 4)]] += 1
            else: unclassified += x['lines']
            continue
        L = x; n = L['lines']
        if n == 0:
            combo = 0; continue
        lines += n; gc += L.get('gc', 0)
        combo += 1; maxcombo = max(maxcombo, combo - 1)
        ts = tspin_kind(L['piece'], L['pre'], n) if L['type'] == 'T' else None
        if ts == 'mini' and n == 1: clears['tsmini'] += 1; diff = True
        elif ts: clears[{1: 'tss', 2: 'tsd', 3: 'tst'}.get(n, 'tst')] += 1; diff = True
        else:
            clears[NAME[min(n, 4)]] += 1; diff = n >= 4
        if L.get('pc'): clears['pc'] += 1
        if diff: chain += 1; maxchain = max(maxchain, chain)
        else: chain = 0
    for e in res['events']:
        if e['kind'] == 'clear' and e.get('orphan'):
            orphan_lines += e['lines']; lines += e['lines']; gc += e['garbage_cleared']; unclassified += e['lines']
    gp = sum(g['pieces'] for g in res['gaps'])
    return dict(pieces=len(res['locks']) + gp, lines_cleared=lines, garbage_received_rows=res['garbage_rows'], garbage_cleared=gc,
                clears=clears, max_combo=maxcombo, max_b2b=max(0, maxchain - 1), b2b_chain_max=maxchain,
                tracked_pieces=len(res['locks']), gap_pieces=gp, gap_lines=sum(g['lines'] for g in res['gaps']),
                gap_garbage=sum(g['garbage'] for g in res['gaps']), unclassified_lines=unclassified,
                resyncs=len(res['resyncs']), orphan_clear_lines=orphan_lines)
def run_game(g):
    z = np.load(f'/tmp/claude-0/ak/w/chain/sy/w/B/cells2/{g["id"]}.npz'); t0 = float(z['t0'])
    cells = z['cells']; n = len(cells)
    out = dict(id=g['id'], p1=None, p2=None, duration_s=None, winner=None, confidence=0.0, notes='')
    if n < 60:
        out['notes'] = 'no frames decoded'; return out, None
    ends, match = border_end(z, g['start_s'], g['end_upper_s'], t0)
    cand = [(f, p) for p, f in ends.items() if f is not None]
    notes = []
    if cand:
        f_end, loser = min(cand)
        if len(cand) == 2 and abs(cand[0][0] - cand[1][0]) < 15: notes.append('both board frames left reference within 0.5 s; loser = earlier')
        t_end = t0 + f_end / FPS; dur = t_end - g['start_s']
        out['duration_s'] = round(dur, 2); out['winner'] = 'p2' if loser == 0 else 'p1'
    else:
        f_end = min(n, int((g['end_upper_s'] - t0) * FPS)); loser = None
        notes.append('no board-collapse detected before end_upper_s; duration null, measured to end_upper_s')
    i_start = int((g['start_s'] - t0) * FPS)
    i_end = f_end if f_end is not None else n
    details = {}
    for p, key in ((0, 'p1'), (1, 'p2')):
        cls = classify(cells[:i_end + 1, p])
        res = analyze_player(cls, i_start, min(i_end, len(cls)))
        sm = summarize(res)
        sm['topped_out'] = (loser == p) if loser is not None else None
        sm['accounting_residual'] = res['final_cells'] - (4 * sm['pieces'] - 10 * sm['lines_cleared'] + 9 * sm['garbage_received_rows'])
        frac = sm['tracked_pieces'] / max(1, sm['pieces'])
        sm['confidence'] = round(max(0.05, min(1.0, frac - 0.02 * abs(sm['accounting_residual']))), 2)
        sm['notes'] = (f"tracked {sm['tracked_pieces']}/{sm['pieces']} pieces event-by-event; {sm['resyncs']} untracked stretches "
                       f"filled by the cell identity (+{sm['gap_pieces']} pieces, +{sm['gap_lines']} lines, +{sm['gap_garbage']} garbage rows; "
                       f"{sm['unclassified_lines']} lines without clear type); final-board identity residual {sm['accounting_residual']}")
        out[key] = sm; details[key] = res
    out['confidence'] = round(min(out['p1']['confidence'], out['p2']['confidence']) * (1.0 if loser is not None else 0.5), 2)
    out['notes'] = '; '.join(notes)
    return out, details
try:
    import solve_fast as _sf; solve = _sf.solve   # bitboard drop-in (extractor/perf), byte-identical output
except ImportError:
    pass
if __name__ == '__main__':
    games = {g['id']: g for g in json.load(open('/tmp/claude-0/ak/w/chain/sy/games.json'))}
    for gid in sys.argv[1:]:
        o, d = run_game(games[gid])
        print(json.dumps(o), flush=True)
