"""Bitboard drop-in for extract_b.solve (metrics/B/extract_b.py).

solve(B, Bo, Qc, depth=3) returns exactly what extract_b.solve returns: [] (already consistent), None (no
transition found) or (E, O, oplist) with the same ops, in the same order, the same chosen successor, and
the same numpy dtypes (E like B, O like Bo, every op's `pre` a bool array, `colour` a list of ints).

Representation: a 20x10 board is ONE Python int, cell (r, c) at bit 10*r + c, so row-major scan order is
ascending bit order. O (values 0..3) is two bit planes, O1 = bit 0 and O2 = bit 1. Everything Qc-derived
is a per-call constant mask. Conversion to/from numpy happens only at the solve() boundary and for the
`pre` arrays carried by the returned oplist (those are kept as ints during the search and materialised
only for the one state returned).

Exactness notes (each mirrors a line of the reference):
  * comps(): components are produced in order of their lowest set bit, which is the reference's
    row-major first-unseen-cell order; the DFS cell ORDER (stack, neighbours (r+1,c),(r-1,c),(r,c+1),
    (r,c-1)) is reproduced exactly whenever a cell list is observable (a lock's `piece`, the 8-cell
    split, `colour`); elsewhere only the cell SET matters and a mask flood is used.
  * the merged-clear branch (the reference's hot spot: ~1.1M numpy collapse() calls on g102) visits the
    same R sequence as `for n in 1..4: for R in itertools.combinations(cand, n)` that survive its
    filters, in the same order. Since R[-1] - R[0] <= 3 is required, R = (cand[i],) + a subset of
    cand[i+1:i+4] within 3 rows; enumerating i ascending and itertools.combinations over that window
    is lexicographic order restricted to the window, i.e. the same order. Extra exact filters, all
    tests the reference applies later anyway, cut work before any collapse:
      - vrow: lowest row with a vanished cell (E & Qc==0). Rows below R[0] are unchanged by the
        collapse, so R[0] > vrow fails `(E2 & (Qc == 0)).any()`; cand ascending -> break.
      - X[j] = E & ~(Qc>0 << 10j): row k of E moved down j rows lands on a Qc==0 cell. A collapse
        moves kept row k down by j(k) = #{r in R: r < k}, so the reference's vanished-cell test on
        E2 is: rows above R[-1] in X[n] (i.e. R[-1] < hi, the top row of X[n]), or a middle row k in
        X[j(k)]. collapse() itself is then only run for the R that pass.
      - |vis| + missing != 4 -> shape_of(piece) is None (it needs exactly four cells).
  * memoisation is WITHIN one solve() only: successors of a state are a pure function of
    (E, O1, O2) and the call's Qc, and consistent() of E and Qc. Duplicate states in the frontier
    still appear (and count towards the 80-state truncation) exactly as in the reference; only their
    expansion is reused. A cross-call cache of the merged-clear candidates by E was measured slower
    cold (g102 2.743 s vs 2.487 s) and removed.
  * precondition: Bo values in 0..3 (all extract_b.analyze_player ever writes); anything else raises
    ValueError instead of being searched. Output E/O dtypes follow the input B/Bo dtypes.
"""
import itertools
import numpy as np

FULL = (1 << 200) - 1
ROW = 1023
ROWLSB = 0
for _r in range(20):
    ROWLSB |= 1 << (10 * _r)
COL0 = ROWLSB
COL9 = ROWLSB << 9
NOT_COL0 = FULL & ~COL0
NOT_COL9 = FULL & ~COL9
LOWMASK = [(1 << (10 * k)) - 1 for k in range(21)]          # rows 0..k-1
TOPMASK = [FULL & ~LOWMASK[20 - k] for k in range(21)]      # rows 20-k..19


def _norm(cells):
    r0 = min(r for r, c in cells); c0 = min(c for r, c in cells)
    return frozenset((r - r0, c - c0) for r, c in cells)


_BASE = {'I': [(0, 0), (0, 1), (0, 2), (0, 3)], 'O': [(0, 0), (0, 1), (1, 0), (1, 1)], 'T': [(0, 0), (0, 1), (0, 2), (1, 1)],
         'S': [(0, 0), (0, 1), (1, 1), (1, 2)], 'Z': [(1, 0), (1, 1), (0, 1), (0, 2)], 'L': [(0, 0), (0, 1), (0, 2), (1, 2)],
         'J': [(0, 0), (0, 1), (0, 2), (1, 0)]}
SHAPE_MASKS = set()
for _cl in _BASE.values():
    _cur = _cl
    for _ in range(4):
        SHAPE_MASKS.add(sum(1 << (10 * r + c) for r, c in _norm(_cur)))
        _cur = [(c, -r) for r, c in _cur]


def is_shape(m):
    """shape_of(cells) is truthy, for a cell mask (cells are distinct, so len == popcount)."""
    if m.bit_count() != 4:
        return False
    low = (m & -m).bit_length() - 1
    m >>= 10 * (low // 10)
    if m >> 40:
        return False      # spans > 4 rows: no tetromino does (also keeps `cols` below covering every cell)
    cols = (m | (m >> 10) | (m >> 20) | (m >> 30)) & ROW
    return (m >> ((cols & -cols).bit_length() - 1)) in SHAPE_MASKS


def nbrs(x):
    return ((x << 10) & FULL) | (x >> 10) | ((x & NOT_COL9) << 1) | ((x & NOT_COL0) >> 1)


def comp_masks(m):
    """connected components of mask m, in the reference's order (lowest set bit first)."""
    out = []
    while m:
        c = m & -m
        while True:
            n = c | (nbrs(c) & m)
            if n == c:
                break
            c = n
        out.append(c)
        m &= ~c
    return out


def dfs_order(cmask):
    """the reference comps() cell order for one component."""
    lb = (cmask & -cmask).bit_length() - 1
    seen = {lb}
    st = [divmod(lb, 10)]
    comp = []
    while st:
        a, b = st.pop()
        comp.append((a, b))
        for x, y in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
            if 0 <= x < 20 and 0 <= y < 10:
                k = 10 * x + y
                if (cmask >> k) & 1 and k not in seen:
                    seen.add(k)
                    st.append((x, y))
    return comp


def supported(cm, board):
    return bool((cm & ROW) or ((cm >> 10) & ~cm & board))


def mask_of(cells):
    m = 0
    for r, c in cells:
        m |= 1 << (10 * r + c)
    return m


def full_rows_lsb(e):
    a = e & (e >> 1)
    b = a & (a >> 2)
    c = b & (b >> 4)
    return c & (e >> 8) & (e >> 9) & ROWLSB


def collapse1(x, rows):
    """remove rows (ascending list) and compact downward."""
    for r in reversed(rows):
        s = 10 * r
        x = (x & LOWMASK[r]) | ((x >> (s + 10)) << s)
    return x


def reset_caches():
    pass


def to_int(a):
    return int.from_bytes(np.packbits(np.asarray(a, bool).ravel(), bitorder='little').tobytes(), 'little')


def to_bool(x):
    return np.unpackbits(np.frombuffer(x.to_bytes(25, 'little'), np.uint8), bitorder='little')[:200].reshape(20, 10).astype(bool)


def _row_gc(o1, o2, rows):
    g = 0
    for r in rows:
        if ((o1 & ~o2) >> (10 * r) & ROW).bit_count() >= 6:
            g += 1
    return g


class _Ctx:
    __slots__ = ('nqnz', 'qnz', 'qcol', 'qfull', 'extra_src', 'qflat', 'gmax', 'cons')

    def __init__(self, Qc):
        q = np.asarray(Qc)
        qnz = to_int(q > 0)
        self.qnz = qnz
        self.nqnz = FULL & ~qnz
        self.qcol = to_int((q > 1) & (q < 9))
        qf = full_rows_lsb(qnz) * ROW      # rows where every Qc cell is > 0, as whole-row masks
        self.qfull = qf
        self.extra_src = to_int(q > 1) | qf
        self.qflat = q.ravel().tolist()
        q1 = to_int(q == 1)
        g = 0
        while g < 12:       # is_garbage_row: 9 occupied cells, >= 8 of them grey (a grey cell is occupied)
            if ((qnz >> (10 * g)) & ROW).bit_count() == 9 and ((q1 >> (10 * g)) & ROW).bit_count() >= 8:
                g += 1
            else:
                break
        self.gmax = g
        self.cons = {}

    def consistent(self, e):
        r = self.cons.get(e)
        if r is not None:
            return r
        r = True
        if e & self.nqnz or (e & self.qfull) != self.qfull:
            r = False
        else:
            for c in comp_masks(self.qcol & ~e):
                if c.bit_count() > 4 or supported(c, e):
                    r = False
                    break
        self.cons[e] = r
        return r


def _cells_rowmajor(m):
    out = []
    while m:
        lb = m & -m
        out.append(divmod(lb.bit_length() - 1, 10))
        m ^= lb
    return out


def _ops(ctx, e, o1, o2):
    """successor deltas of state (e, o1, o2): list of (e2, o1', o2', [ops]) with `pre` as ints."""
    res = []
    fl = full_rows_lsb(e)
    if fl:
        full = [r for r in range(20) if (fl >> (10 * r)) & 1]
        e2 = collapse1(e, full)
        res.append((e2, collapse1(o1, full), collapse1(o2, full),
                    [dict(op='clear', rows=full, gc=_row_gc(o1, o2, full), pc=not e2)]))
        return res
    qflat = ctx.qflat
    for cm in comp_masks(ctx.extra_src & ~e):
        pc = cm.bit_count()
        if pc == 4 and is_shape(cm) and supported(cm, e):
            cc = dfs_order(cm)
            res.append((e | cm, o1 & ~cm, o2 | cm,
                        [dict(op='lock', piece=cc, pre=e, colour=[qflat[10 * r + c] for r, c in cc])]))
        elif pc == 8:
            cc = dfs_order(cm)
            first = min(cc); rest = [x for x in cc if x != first]
            for sub in itertools.combinations(rest, 3):
                p1 = [first] + list(sub); p2 = [x for x in cc if x not in p1]
                m1 = mask_of(p1); m2 = cm & ~m1
                if not (is_shape(m1) and is_shape(m2)):
                    continue
                for a1, a2, ma1, ma2 in ((p1, p2, m1, m2), (p2, p1, m2, m1)):
                    if not supported(ma1, e):
                        continue
                    ea = e | ma1
                    if not supported(ma2, ea):
                        continue
                    if full_rows_lsb(ea):
                        continue
                    res.append((ea | ma2, o1 & ~cm, o2 | cm,
                                [dict(op='lock', piece=a1, pre=e, colour=[]), dict(op='lock', piece=a2, pre=ea, colour=[])]))
                    break
    qnz = ctx.qnz
    for g in range(1, ctx.gmax + 1):
        if e & TOPMASK[g]:
            break
        low = qnz & LOWMASK[g]
        s = 10 * g
        res.append((((e << s) & FULL) | low, ((o1 << s) & FULL) | low, (o2 << s) & FULL, [dict(op='garbage', g=g)]))
    van = e & ctx.nqnz
    if not van:
        return res
    vrow = ((van & -van).bit_length() - 1) // 10       # lowest row holding a vanished cell
    rows = [(e >> (10 * r)) & ROW for r in range(20)]
    cnt = [x.bit_count() for x in rows]
    cand = [r for r in range(20) if 6 <= cnt[r] < 10]
    if not cand:
        return res
    missing = {r: 10 - cnt[r] for r in cand}
    empt = {r: ROW & ~rows[r] for r in cand}
    qcol = ctx.qcol; nqnz = ctx.nqnz; qnz = ctx.qnz
    # X[j]: cells of E whose row k, moved down j rows by a collapse, lands on a Qc==0 cell (valid for k >= j).
    # A collapse removing R moves kept row k down by j(k) = #{r in R: r < k}, so the reference's
    # `(collapse(E, R) & (Qc == 0)).any()` is: some kept row k has a bit in X[j(k)] at row k. Rows below R[0]
    # have j = 0 and no vanished cell (R[0] <= vrow); rows above R[-1] have j = n.
    X = [van, e & ~(qnz << 10), e & ~(qnz << 20), e & ~(qnz << 30), e & ~(qnz << 40)]
    nc = len(cand)
    for n in range(1, 5):
        Xn = X[n]
        hi = (Xn.bit_length() - 1) // 10    # R[-1] must reach the highest row of Xn (-1 when Xn == 0)
        for i in range(nc):
            s0 = cand[i]
            if s0 > vrow:
                break             # the vanished cell below R survives the collapse unchanged
            if s0 + 3 < hi:
                continue          # R[-1] <= R[0] + 3 cannot reach row hi
            near = [r for r in cand[i + 1:i + 4] if r - s0 <= 3]
            for sub in itertools.combinations(near, n - 1):
                R = (s0,) + sub
                top = R[-1]
                if top < hi:
                    continue      # a row above R lands on an empty Qc cell
                bad = False; j = 1
                for k in range(s0 + 1, top):
                    if k in sub:
                        j += 1
                    elif (X[j] >> (10 * k)) & ROW:
                        bad = True; break
                if bad:
                    continue
                miss = 0; ec = 0
                for r in R:
                    miss += missing[r]; ec |= empt[r]
                if miss > 4 or (ec.bit_length() - 1) - ((ec & -ec).bit_length() - 1) > 3:
                    continue
                Rl = list(R)
                e2 = collapse1(e, Rl)
                add = qcol & ~e2
                flm = 0
                for c in comp_masks(add):
                    if c.bit_count() <= 4 and not supported(c, e2):
                        flm |= c
                nk = 20 - n
                vis = add & ~flm & LOWMASK[nk]
                if vis.bit_count() + miss != 4:
                    continue          # shape_of() needs exactly four cells
                keep = [r for r in range(20) if r not in R]
                piece = [(keep[r], c) for r, c in _cells_rowmajor(vis)]
                for r in R:
                    er = empt[r]
                    for c in range(10):
                        if (er >> c) & 1:
                            piece.append((r, c))
                pm = mask_of(piece)
                if is_shape(pm) and supported(pm, e):
                    e3 = collapse1(e | pm, Rl)
                    res.append((e3, collapse1(o1, Rl), collapse1(o2, Rl),
                                [dict(op='lock', piece=piece, pre=e, colour=[], merged=True),
                                 dict(op='clear', rows=sorted(Rl), gc=_row_gc(o1, o2, Rl), pc=not e3)]))
    return res


def _materialise(e, o1, o2, L, Edt, Odt):
    E = to_bool(e).astype(Edt, copy=False)
    O = (to_bool(o1).astype(np.int16) + 2 * to_bool(o2).astype(np.int16)).astype(Odt)
    out = []
    for op in L:
        op = dict(op)
        if 'pre' in op:
            op['pre'] = to_bool(op['pre']).astype(Edt, copy=False)
        for k in ('piece', 'colour', 'rows'):
            if k in op:
                op[k] = list(op[k])
        out.append(op)
    return (E, O, out)


def solve(B, Bo, Qc, depth=3):
    B = np.asarray(B); Bo = np.asarray(Bo)
    if B.shape != (20, 10) or Bo.shape != (20, 10) or Bo.min() < 0 or Bo.max() > 3:
        raise ValueError('solve_fast: expects 20x10 boards with Bo in 0..3')
    ctx = _Ctx(Qc)
    e0 = to_int(B)
    if ctx.consistent(e0):
        return []
    bo = Bo.astype(np.int16)
    o1 = to_int(bo & 1); o2 = to_int(bo & 2)
    frontier = [(e0, o1, o2, [])]
    memo = {}
    for d in range(depth):
        nxt = []
        for e, a, b, L in frontier:
            key = (e, a, b)
            succ = memo.get(key)
            if succ is None:
                succ = _ops(ctx, e, a, b)
                memo[key] = succ
            for e2, a2, b2, ops2 in succ:
                L2 = L + ops2
                if ctx.consistent(e2):
                    return _materialise(e2, a2, b2, L2, B.dtype, Bo.dtype)
                nxt.append((e2, a2, b2, L2))
        frontier = nxt
        if len(frontier) > 80:
            frontier = frontier[:80]
    return None
