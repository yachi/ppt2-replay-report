"""Extractor A, stage 2: event tracking over the per-frame features of feat.py.

Spawn events  = NEXT-queue shifts (5-slot signature, 3-frame stable, matched as a shift by 1..3).
Lock k        = the end of spawn interval k (one lock per interval, except the interval ended by
                the first hold into an empty hold box, which pulls one extra piece).
Board B_k     = per-cell mode of confident cell codes early in interval k, rows 0..17 only
                (rows 18-19 are where the new piece spawns).
Clear         = rows that flash white (>=8 of 10 cells 'W') for >=2 frames inside the interval,
                cross-checked by the cell count identity  n(B_k+1) = n(B_k) + 4 - 10c  (no garbage on a clear)
Garbage       = growth of the contiguous grey-row block at the bottom on a non-clearing lock.
Piece cells   = (B_k + piece) reconstructed from B_k, B_k+1 and the cleared row set; T-spin from the
                piece colour (T) and the 3-corner rule on B_k.
"""
import numpy as np, json, sys

EMPTY, GREY, WHITE, UNC = 0, 1, 9, 10
TCODE = 8
NAMES = '.GZLOSIJTW?'
FPS = 30.0
TOP = 18  # rows >= TOP excluded from the stack board

def stable_states(nxt, min_run=3):
    """list of (frame, tuple) for NEXT signatures that hold min_run frames with all slots readable"""
    out = []
    n = len(nxt); i = 0
    while i < n:
        j = i
        while j + 1 < n and (nxt[j + 1] == nxt[i]).all():
            j += 1
        if j - i + 1 >= min_run and (nxt[i] > 0).all() and (nxt[i] < 9).all():
            out.append((i, tuple(int(x) for x in nxt[i]), j - i + 1))
        i = j + 1
    return out

def shift_k(a, b):
    for k in (1, 2, 3):
        if a[k:] == b[:5 - k]:
            return k
    return None

def spawns(nxt, lo, hi):
    """spawn frames within [lo,hi): each queue shift is one spawn. returns (frames, revealed seq, anomalies)"""
    st = [s for s in stable_states(nxt[:hi]) if s[0] >= lo - 90]
    # the pre-game signature is the last stable state starting before lo
    pre = [s for s in st if s[0] < lo]
    cur = pre[-1] if pre else None
    rest = [s for s in st if s[0] >= lo]
    if cur is None:
        if not rest:
            return [], [], ['no queue']
        cur = rest[0]; rest = rest[1:]
    frames, seq, anom = [], list(cur[1]), []
    votes = {cur[1][4]: cur[2]}  # stable frames seen per reading of the current queue's newest (5th) slot
    for f, sig, run in rest:
        if sig == cur[1]:
            votes[sig[4]] = votes.get(sig[4], 0) + run
            continue
        if frames and sig[:4] == cur[1][:4]:
            # same first four slots = no spawn (a 7-bag queue cannot shift onto itself); only the newest slot
            # reads differently. The piece just revealed in slot 5 can read I for its first frames when it is
            # J or T (g018 85.10, g042 289.77, i002 353.00), and that 3-frame misread used to become the
            # reference queue, so no later true shift matched it and the read stalled to the game's end.
            # Re-read the slot by votes (stable frames per reading; the fresh misread comes first, so a tie goes
            # to the later reading), add no spawn.
            votes[sig[4]] = votes.get(sig[4], 0) + run
            if votes[sig[4]] >= votes[cur[1][4]]:      # a tie goes to the later reading
                anom.append(f'queue slot-5 re-read at frame {f}: {NAMES[cur[1][4]]}->{NAMES[sig[4]]}')
                seq[-1] = sig[4]; cur = (f, sig, run)
            continue
        k = shift_k(cur[1], sig)
        if not frames and k is not None and k > 1 and cur[2] < 30:
            k = None          # a first shift skipping pieces is a chance match against a noisy pre-game read
        if k is None:
            if not frames:
                # before the first matched shift the queue may still be the previous game's (or settling):
                # adopt the new signature as the pre-game queue rather than waiting for a chance match
                cur = (f, sig, run); seq = list(sig); votes = {sig[4]: run}
                continue
            if run >= 45:
                anom.append(f'queue resync at frame {f}: {cur[1]}->{sig}')
                frames.append(f); seq.append(sig[-1]); cur = (f, sig, run); votes = {sig[4]: run}
            continue
        for q in range(k):
            frames.append(f)
        seq.extend(sig[5 - k:])
        if k > 1:
            anom.append(f'double shift k={k} at frame {f}')
        cur = (f, sig, run); votes = {sig[4]: run}
    return frames, seq, anom

def bag_ok(seq):
    """fraction of 7-windows (best phase) that are permutations"""
    best = 0
    for ph in range(7):
        chunks = [seq[i:i + 7] for i in range(ph, len(seq) - 6, 7)]
        if not chunks:
            continue
        ok = sum(len(set(c)) == 7 for c in chunks) / len(chunks)
        best = max(best, ok)
    return best

def board_at(grid, a, b, prev):
    """per-cell mode of confident codes in frames [a,b); grey/white votes count only inside the
    bottom garbage block of that frame (lock flash and effects are grey/white elsewhere);
    falls back to prev for cells never confident"""
    seg = grid[a:b, :TOP].copy()
    out = prev.copy()
    if len(seg) == 0:
        return out
    gw = (seg == GREY) | (seg == WHITE)
    for f in range(len(seg)):
        h = 0
        while h < TOP and 7 <= gw[f, h].sum() <= 9:
            h += 1
        seg[f][h:][gw[f, h:]] = UNC
        seg[f][:h][gw[f, :h]] = GREY
    for r in range(TOP):
        for c in range(10):
            v = seg[:, r, c]
            v = v[v != UNC]
            if len(v) == 0:
                continue
            cnt = np.bincount(v, minlength=9)
            out[r, c] = cnt.argmax()
    return out

def grey_rows(B):
    n = 0
    for r in range(TOP):
        row = B[r]
        if 7 <= (row == GREY).sum() <= 9:
            n += 1
        else:
            break
    return n

def white_rows(grid, a, b):
    """largest set of rows that are fully white-flashed for 2 consecutive frames in [a,b);
    returns (rows, first frame index of that flash)"""
    best, bf = [], None
    seg = grid[a:b, :20]
    wm = (seg == WHITE).sum(axis=2) >= 10   # [f,20]
    first = None
    for f in range(len(wm) - 1):
        rows = [r for r in range(20) if wm[f, r] and wm[f + 1, r]]
        if rows and first is None:
            first = a + f
        if len(rows) > len(best):
            best = rows
    return best, first

def lock_cells(grid, Bk, f0, colour=None):
    """the locked piece just before the clear flash: scanning back from the flash frame, the first frame
    whose coloured cells that are empty in Bk form exactly one tetromino. returns (cells, colour) or ([], None)"""
    for f in range(f0 - 1, max(0, f0 - 12), -1):
        fr = grid[f, :TOP]
        new = [(r, c) for r in range(TOP) for c in range(10) if Bk[r, c] == EMPTY and 2 <= fr[r, c] <= 8]
        if len(new) == 4 and tetromino(new) is not None:
            cols = [int(fr[r, c]) for r, c in new]
            col = int(np.bincount(cols).argmax())
            if cols.count(col) >= 3 and _is_tetromino(new):
                return new, col
    return [], None

def _is_tetromino(cells):
    s = set(cells)
    seen = {cells[0]}; st = [cells[0]]
    while st:
        r, c = st.pop()
        for q in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if q in s and q not in seen:
                seen.add(q); st.append(q)
    return len(seen) == 4

def tetromino(cells):
    if len(cells) != 4:
        return None
    rs = [r for r, c in cells]; cs = [c for r, c in cells]
    r0, c0 = min(rs), min(cs)
    shape = frozenset((r - r0, c - c0) for r, c in cells)
    return shape

T_SHAPES = {}
def _tshapes():
    # (row up, col right) offsets; centre listed first via key
    base = {'up': [(0, 0), (0, 1), (0, 2), (1, 1)],      # flat, nub up
            'down': [(1, 0), (1, 1), (1, 2), (0, 1)],    # flat, nub down
            'right': [(0, 0), (1, 0), (2, 0), (1, 1)],   # vertical, nub right
            'left': [(0, 1), (1, 1), (2, 1), (1, 0)]}    # vertical, nub left
    centre = {'up': (0, 1), 'down': (1, 1), 'right': (1, 0), 'left': (1, 1)}
    for k, v in base.items():
        T_SHAPES[frozenset(v)] = (k, centre[k])
_tshapes()

def tspin_kind(cells, Bpre, lines):
    """returns None | 'tspin' | 'mini'. 3-corner rule on the pre-lock board; front corners = nub side."""
    shape = tetromino(cells)
    if shape not in T_SHAPES:
        return None
    orient, (cr, cc) = T_SHAPES[shape]
    r0 = min(r for r, c in cells); c0 = min(c for r, c in cells)
    R, C = r0 + cr, c0 + cc
    def occ(r, c):
        if c < 0 or c > 9 or r < 0:
            return True
        if r >= TOP:
            return False
        return Bpre[r, c] != EMPTY
    corners = {'ul': occ(R + 1, C - 1), 'ur': occ(R + 1, C + 1), 'dl': occ(R - 1, C - 1), 'dr': occ(R - 1, C + 1)}
    if sum(corners.values()) < 3:
        return None
    # proxy for 'last move was a rotation': the T could not have been hard-dropped straight in,
    # i.e. some column of the T has an occupied cell above the T's top cell in that column
    covered = False
    for col in set(c for r, c in cells):
        top = max(r for r, c in cells if c == col)
        if any(Bpre[rr, col] != EMPTY for rr in range(top + 1, TOP)):
            covered = True
    if not covered:
        return None
    front = {'up': ('ul', 'ur'), 'down': ('dl', 'dr'), 'right': ('ur', 'dr'), 'left': ('ul', 'dl')}[orient]
    if all(corners[x] for x in front) or lines >= 2:
        return 'tspin'
    return 'mini'

def piece_cells(Bk, Bn, cleared):
    """cells of the locked piece, in pre-clear coordinates. cleared = sorted row indices (pre-clear)."""
    cells = []
    # map post rows back: pre row r (not cleared) -> post row r - (#cleared below r)
    for r in range(TOP):
        if r in cleared:
            for c in range(10):
                if Bk[r, c] == EMPTY:
                    cells.append((r, c))
            continue
        rp = r - sum(1 for x in cleared if x < r)
        if rp >= TOP:
            continue
        for c in range(10):
            if Bk[r, c] == EMPTY and Bn[rp, c] != EMPTY:
                cells.append((r, c))
    return cells

def t_placement(Bk, Bn, cleared, fr):
    """the T placement consistent with the clear: its cells inside the cleared rows are exactly the empty
    cells of Bk there, all its cells are empty in Bk, and its cells outside the cleared rows are filled in
    Bn (row-shifted) or non-empty in frame fr (just before the flash). returns cells or None"""
    holes = {(r, c) for r in cleared if r < TOP for c in range(10) if Bk[r, c] == EMPTY}
    best = None; bscore = -99
    for shape in T_SHAPES:
        for r0 in range(0, TOP):
            for c0 in range(0, 10):
                cells = [(r0 + dr, c0 + dc) for dr, dc in shape]
                if any(c > 9 or r >= TOP for r, c in cells):
                    continue
                if any(Bk[r, c] != EMPTY for r, c in cells):
                    continue
                inrows = {(r, c) for r, c in cells if r in cleared}
                if not inrows or not inrows <= holes:
                    continue
                extra = len(holes - inrows)       # holes the T leaves unfilled: board noise or wrong T
                if extra > 2:
                    continue
                score = -3 * extra
                for r, c in cells:
                    if r in cleared:
                        continue
                    rp = r - sum(1 for x in cleared if x < r)
                    if (rp < TOP and Bn[rp, c] != EMPTY) or (fr is not None and fr[r, c] != EMPTY):
                        score += 1
                    else:
                        score -= 2
                if score > bscore:
                    best, bscore = cells, score
    return best

def piece_colour(grid, a, b, cells):
    codes = []
    for r, c in cells:
        v = grid[a:b, r, c] if r < 20 else []
        codes += [int(x) for x in v if 2 <= x <= 8]
    if not codes:
        return None
    return int(np.bincount(codes, minlength=9).argmax())

def _detect(border, lo, hi, winner_min=0.7):
    """A's original KO test: a frame where a board's border drops below 0.6 and the 30-frame window medians say
    that board lost it (< 0.4) while the other kept it (> winner_min). It can fire early: an attack flash or grey
    top-out blocks over the loser's frame dip the border for a few frames just before the tilt, and the window
    medians still pass because the tilt follows inside the window (g060, h003, ... up to 13 frames early)."""
    n = min(hi, len(border))
    for f in range(lo, n - 30):
        for p in (0, 1):
            if border[f, p] < 0.6:
                w = border[f:f + 30]
                if np.median(w[:, p]) < 0.4 and np.median(w[:, 1 - p]) > winner_min:
                    return f, p
    return None, None

KO_RUN = 30        # frames the loser's border must stay below 0.6 without a break
KO_WALK = 60       # max frames the refinement may move the detected frame

def refine(border, f, p):
    """walk forward from the detected frame to the first frame of the run in which the loser's border stays
    below 0.6 for KO_RUN frames: the border lost for good. Same 0.6 the detector keys on, so a frame that already
    starts such a run (every game whose detection was not early) is returned unchanged. 0.4 would put the
    end 1-2 frames later on ~185 games, because the border fades 0.9 -> 0.3 over 2-3 frames at the tilt."""
    if f is None:
        return f
    g = f
    while g <= f + KO_WALK and g + KO_RUN <= len(border):
        if (border[g:g + KO_RUN, p] < 0.6).all():
            return g
        g += 1
    return f                 # no unbroken run found: keep the detected frame

def find_end(border, lo, hi):
    """first frame where one board's frame border is lost for good (KO tilt) while the other stays"""
    f, p = _detect(border, lo, hi)
    return refine(border, f, p), p

def analyse_player(d, p, lo, end, notes):
    grid = d['grid'][:, p]; nxt = d['nxt'][:, p]; hold = d['hold'][:, p]
    sp, seq, anom = spawns(nxt, lo, end)
    notes += [f'p{p+1}: ' + a for a in anom]
    if len(sp) < 2:
        return None, sp
    # first hold into empty hold: hold box readable non-empty after having been empty
    hold_empty_shift = None
    hz = hold[sp[0]:end]
    nz = np.nonzero((hz > 0) & (hz < 9))[0]
    if len(nz):
        # require 5 stable frames of a non-empty hold
        for i in nz:
            if (hz[i:i + 5] == hz[i]).all():
                hf = sp[0] + i
                # the spawn closest to the hold event
                cand = [q for q, s in enumerate(sp) if s >= hf - 1]
                j = cand[0] if cand else 0
                if cand and sp[j] - hf <= 6 and j > 0:
                    hold_empty_shift = j
                else:
                    notes.append(f'p{p+1}: hold appeared at frame {hf} with no matching queue shift')
                break
    intervals = [(sp[j], sp[j + 1]) for j in range(len(sp) - 1)] + [(sp[-1], end)]
    # stable hold reading (>=4 frames), carried forward
    hs = np.zeros(len(hold), np.uint8); cur = 0; i = 0
    while i < len(hold):
        j2 = i
        while j2 + 1 < len(hold) and hold[j2 + 1] == hold[i]:
            j2 += 1
        if j2 - i + 1 >= 4 and 0 < hold[i] < 9:
            cur = hold[i]
        hs[i:j2 + 1] = cur
        i = j2 + 1
    # active piece at the lock of each interval: spawned piece seq[j], swapped out by hold changes
    active = []
    held = 0
    for j, (a, b) in enumerate(intervals):
        act = seq[j] if j < len(seq) else 0
        hh = hs[a:b]
        for f in range(1, len(hh)):
            if hh[f] != hh[f - 1]:
                old_h = hh[f - 1]
                if old_h:
                    act = int(old_h)
        active.append(int(act))
    prev = np.zeros((TOP, 10), np.uint8)
    boards = []
    for a, b in intervals:
        stop = max(a + 2, b - 3)
        Bk = board_at(grid, a + 1, min(stop, a + 12), prev)
        boards.append(Bk); prev = Bk
    st = dict(pieces=0, lines_cleared=0, garbage_received_rows=0, garbage_cleared=0,
              clears=dict(single=0, double=0, triple=0, quad=0, tss=0, tsd=0, tst=0, tsmini=0, pc=0))
    events = []
    combo = 0; maxcombo = 0; b2b = -1; maxb2b = -1; brun = 0; maxbrun = 0
    resid_ok = 0; resid_n = 0
    lock_ix = 0
    unflashed = 0
    for j in range(len(intervals) - 1):
        a, b = intervals[j]
        if hold_empty_shift is not None and j + 1 == hold_empty_shift:
            events.append(dict(j=j, t=a, kind='hold-empty'))
            continue
        Bk, Bn = boards[j], boards[j + 1]
        nk, nn = int((Bk != EMPTY).sum()), int((Bn != EMPTY).sum())
        wr, wf = white_rows(grid, a, b)
        delta = nn - nk - 4
        c_count = -delta // 10 if delta < 0 and delta % 10 == 0 else None
        g_count = delta // 9 if delta >= 0 and delta % 9 == 0 else None
        lines = len(wr)
        flag = []
        if lines == 0 and c_count:
            flag.append(f'count drop of {c_count} rows without a flash (not counted)')
            unflashed += 1
        if lines and c_count is not None and c_count != lines:
            flag.append(f'flash {lines} vs count {c_count}')
        if lines > 4:
            flag.append(f'flash rows {lines}>4, capped'); lines = 4
        st['pieces'] += 1
        lock_ix += 1
        ev = dict(j=j, t=a, lines=lines, nk=nk, nn=nn, gk=grey_rows(Bk), gn=grey_rows(Bn))
        if lines:
            cleared = wr if len(wr) == lines else None
            if cleared is None:
                # infer: rows of Bk(+piece) that are nearly full
                full = [r for r in range(TOP) if (Bk[r] != EMPTY).sum() >= 6]
                cleared = sorted(full, key=lambda r: -(Bk[r] != EMPTY).sum())[:lines]
                cleared.sort()
            gclr = sum(1 for r in cleared if r < TOP and r < grey_rows(Bk))
            act = active[j]
            fr = grid[wf - 1, :TOP] if wf is not None else None
            if act == TCODE:
                cells = t_placement(Bk, Bn, cleared, fr) or piece_cells(Bk, Bn, cleared)
            else:
                cells = piece_cells(Bk, Bn, cleared)
            col = act
            ts = tspin_kind(cells, Bk, lines) if col == TCODE else None
            # PC: the 'PERFECT CLEAR' overlay is drawn over the board and pollutes Bn, so test the
            # pre-lock board instead: its cells + the 4 piece cells must exactly fill the cleared rows.
            occ_rows = {r for r in range(TOP) if (Bk[r] != EMPTY).any()}
            pc = (nn == 0) or (-2 <= nk + 4 - 10 * lines <= 1 and occ_rows <= set(cleared) | {max(cleared) + 1}
                               and grey_rows(Bk) == gclr)
            st['lines_cleared'] += lines; st['garbage_cleared'] += gclr
            gpost = max(0, grey_rows(Bn) - (grey_rows(Bk) - gclr))
            st['garbage_received_rows'] += gpost
            ev['garbage'] = gpost
            if ts == 'tspin':
                key = {1: 'tss', 2: 'tsd', 3: 'tst'}.get(lines, 'quad')   # [r6] a T read as clearing 4 rows (a misread) crashed here with KeyError None; n041, n045, n059
            elif ts == 'mini':
                key = 'tsmini'
            else:
                key = {1: 'single', 2: 'double', 3: 'triple', 4: 'quad'}[lines]
            st['clears'][key] += 1
            if pc:
                st['clears']['pc'] += 1
            combo += 1; maxcombo = max(maxcombo, combo - 1)
            difficult = lines == 4 or ts is not None
            if difficult:
                b2b += 1; brun += 1
                maxb2b = max(maxb2b, b2b); maxbrun = max(maxbrun, brun)
            else:
                b2b = -1; brun = 0
            ev.update(kind=key, rows=cleared, cells=cells, colour=NAMES[col] if col else None, gclr=gclr, pc=pc)
            if len(cells) != 4:
                flag.append(f'piece cells {len(cells)}')
        else:
            combo = 0
            gk, gn = grey_rows(Bk), grey_rows(Bn)
            g = max(0, gn - gk)
            if g_count is not None and g_count != g:
                flag.append(f'grey rows +{g} vs count +{g_count}')
            st['garbage_received_rows'] += g
            ev.update(kind='lock', garbage=g)
        low = max([r for r in range(TOP) if Bk[r].any() or Bn[r].any()], default=0) < 14
        if low:
            resid_n += 1
            ok = delta == 9 * ev.get('garbage', 0) - 10 * lines
            resid_ok += ok
            if not ok:
                flag.append(f'identity off by {delta - (9 * ev.get("garbage", 0) - 10 * lines)}')
        if flag:
            ev['flag'] = flag
        events.append(ev)
    st['max_combo'] = maxcombo
    st['max_b2b'] = max(maxb2b, 0)
    st['max_b2b_run'] = maxbrun
    st['_resid'] = (resid_ok, resid_n)
    st['_unflashed'] = unflashed
    st['_gres'] = grey_rows(boards[-1]) - (st['garbage_received_rows'] - st['garbage_cleared'])
    st['_bag'] = bag_ok(seq)
    st['_events'] = events
    st['_hold_empty'] = hold_empty_shift is not None
    st['_seq'] = ''.join(NAMES[x] for x in seq)
    return st, sp

def analyse(npz, meta):
    d = np.load(npz)
    t0 = float(d['t0'])
    notes = []
    lo = max(0, int(round((meta['start_s'] - 0.3 - t0) * FPS)))
    hi = len(d['grid'])
    # game start = first queue shift of either player at/after lo
    s0 = []
    for p in (0, 1):
        sp, _, _ = spawns(d['nxt'][:, p], lo, hi)
        if sp:
            s0.append(sp[0])
    if not s0:
        return dict(id=meta['id'], p1=None, p2=None, duration_s=None, winner=None, confidence=0,
                    notes='no queue shift found')
    start = min(s0)
    end, loser = find_end(d['border'], start + 60, hi)
    if end is None:
        notes.append('no KO (frame-border loss) found before end_upper; game end = last frame of window')
        end_f = hi
    else:
        end_f = end
    res = dict(id=meta['id'])
    conf = []
    for p in (0, 1):
        st, sp = analyse_player(d, p, start - 2, end_f, notes)
        key = 'p1' if p == 0 else 'p2'
        if st is None:
            res[key] = None; conf.append(0); continue
        st['duration_s'] = round((end_f - start) / FPS, 2) if end is not None else None
        st['topped_out'] = (loser == p) if end is not None else None
        ro, rn = st.pop('_resid')
        bag = st.pop('_bag')
        unf = st.pop('_unflashed')
        gres = st.pop('_gres')
        st['qa'] = dict(identity_ok=ro, identity_n=rn, bag=round(bag, 3), garbage_balance_residual=int(gres),
                        unflashed_drops=unf)
        c = 0.5 * (ro / rn if rn else 0) + 0.3 * bag + 0.2 * (1 if end is not None else 0)
        st['confidence'] = round(c, 3)
        st['notes'] = f'cell-count identity held on {ro}/{rn} low-stack locks; 7-bag consistency {bag:.2f}; ' + \
                      ('first hold-into-empty excluded from pieces' if st['_hold_empty'] else 'no hold-into-empty seen') + \
                      f'; {unf} cell-count drops without a clear flash (not counted as clears)'
        res[key] = st; conf.append(c)
    res['duration_s'] = round((end_f - start) / FPS, 2) if end is not None else None
    res['winner'] = None if loser is None else ('p2' if loser == 0 else 'p1')
    res['confidence'] = round(min(conf), 3)
    res['start_s'] = round(t0 + start / FPS, 2)
    res['end_s'] = round(t0 + end_f / FPS, 2) if end is not None else None
    res['notes'] = '; '.join(notes[:12])
    return res

if __name__ == '__main__':
    meta = json.loads(sys.argv[2])
    r = analyse(sys.argv[1], meta)
    if '-v' in sys.argv:
        for k in ('p1', 'p2'):
            if r[k]:
                print(k, r[k]['_seq'])
                for e in r[k]['_events']:
                    print('  ', {x: y for x, y in e.items() if x != 'cells'})
    for k in ('p1', 'p2'):
        if r[k]:
            for x in ('_events', '_seq', '_hold_empty'):
                r[k].pop(x, None)
    print(json.dumps(r, ensure_ascii=False))
