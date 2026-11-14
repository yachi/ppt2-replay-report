"""Faster drop-ins for a chain's corr/tools/nextcount.py hot functions, same answers.

locate():    scipy.signal.fftconvolve(m, t[::-1,::-1], 'valid') done by hand with scipy.fft, the template's
             transform cached per player. The same rfftn/irfftn calls on the same shapes, so the same floats.
             Also skips importing scipy.signal (about 7 s the first time).
classify2(): the seven colour masks in one array operation; argmax over the counts picks the first maximum,
             as the original's strict '>' scan does.
white():     on uint8 without the int16 copy (max >= min, so the difference cannot wrap), channel by channel
             (numpy reduces a length-3 last axis slowly).
shape_of():  np.percentile's linear method written out for a sorted array (pct); np.nonzero gives ys sorted.
"""
import numpy as np
from scipy import fft as sp_fft


def pct(a, p):
    """np.percentile(a, p) for a sorted 1-d integer array, method 'linear', in numpy's float64 steps:
    virtual index (n-1)*q, floor, and _lerp's two-sided form."""
    n = len(a); q = np.float64(p) / 100
    v = (n - 1) * q
    if v >= n - 1:
        return np.float64(a[-1])
    if v < 0:
        return np.float64(a[0])
    lo = np.floor(v); i = int(lo); g = v - lo
    lo_v, hi_v = a[i], a[i + 1]
    d = hi_v - lo_v
    return hi_v - d * (1 - g) if g >= 0.5 else lo_v + d * g


def install(ns):
    W, H, SEARCH, TPL_BOX, TPL = ns['W'], ns['H'], ns['SEARCH'], ns['TPL_BOX'], ns['TPL']
    CK = list(ns['RGB']); CARR = np.array([ns['RGB'][k] for k in CK], np.int16)
    cache = {}

    def mnmx(a):
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        return np.minimum(np.minimum(r, g), b), np.maximum(np.maximum(r, g), b)

    def white(a):
        mn, mx = mnmx(a)
        return ((mn > 190) & ((mx - mn) < 50)).astype(np.float32)

    def locate(fr, pl):
        x0, y0, x1, y1 = TPL_BOX[pl]
        t = TPL[pl]
        X0, Y0 = max(0, x0 - SEARCH), max(0, y0 - SEARCH)
        X1, Y1 = min(W, x1 + SEARCH), min(H, y1 + SEARCH)
        m = white(fr[Y0:Y1, X0:X1])
        s1, s2 = m.shape, t.shape
        shape = [s1[i] + s2[i] - 1 for i in range(2)]
        key = (pl, s1, id(t))
        if key not in cache:
            fshape = [sp_fft.next_fast_len(n, True) for n in shape]
            cache[key] = (fshape, sp_fft.rfftn(t[::-1, ::-1], fshape), float(t.sum()))
        fshape, tf, tsum = cache[key]
        ret = sp_fft.irfftn(sp_fft.rfftn(m, fshape) * tf, fshape)[:shape[0], :shape[1]]
        nv = [s1[i] - s2[i] + 1 for i in range(2)]
        st = [(shape[i] - nv[i]) // 2 for i in range(2)]
        c = ret[st[0]:st[0] + nv[0], st[1]:st[1] + nv[1]]
        iy, ix = np.unravel_index(np.argmax(c), c.shape)
        return X0 + ix - x0, Y0 + iy - y0, float(c[iy, ix] / tsum)

    def classify2(region):
        mn, mx = mnmx(region)
        if np.count_nonzero((mx - mn) > 80) < 15:
            return '-'
        r = region.astype(np.int16)
        d = np.abs(r[:, :, None, :] - CARR); d = d[..., 0] + d[..., 1] + d[..., 2]
        M = d < 110
        n = M.reshape(-1, len(CK)).sum(0)
        i = int(n.argmax())
        if n[i] < 60:
            return '?'
        return CK[i] if shape_of2(M[:, :, i]) == CK[i] else '?'

    SHAPES = ns['SHAPES']

    def shape_of2(m):  # the chain's shape_of with np.percentile replaced by pct()
        ys, xs = np.nonzero(m)
        if len(ys) < 40:
            return None
        xs = np.sort(xs)
        y0, y1 = pct(ys, 2), pct(ys, 98) + 1
        x0, x1 = pct(xs, 2), pct(xs, 98) + 1
        h, w = y1 - y0, x1 - x0
        if h < 3 or w < 3:
            return None
        ar = w / h
        if ar > 3.0:
            return 'I'
        if ar < 1.3:
            return 'O'
        g = []
        for r in range(2):
            row = []
            for c in range(3):
                ya, yb = int(y0 + r * h / 2), int(y0 + (r + 1) * h / 2)
                xa, xb = int(x0 + c * w / 3), int(x0 + (c + 1) * w / 3)
                cell = m[ya:yb, xa:xb]
                row.append(1 if cell.size and cell.mean() > 0.5 else 0)
            g.append(tuple(row))
        g = tuple(g)
        for k, v in SHAPES.items():
            if v == g:
                return k
        return None

    orig = {k: ns[k] for k in ('white', 'locate', 'classify2', 'shape_of')}
    ns.update(white=white, locate=locate, classify2=classify2, shape_of=shape_of2)
    return orig


REPLACED = ('white', 'locate', 'classify2', 'shape_of')
READ = ('read_state', 'frames')
CONSTS = ('RGB', 'SHAPES', 'SEARCH', 'TPL_BOX', 'MIN_SCORE', 'SLOT_Y', 'NEXT_X', 'HOLD_X', 'HOLD_Y', 'W', 'H')
# every corr/tools/nextcount.py in extractor/chain (29 chains) and extractor/amemiya/xKR/check, 2026-11-14
KNOWN = {'46279798'}


def fingerprint(src):
    """md5 (8 hex) of the functions this module replaces or relies on, and the constants they read"""
    import ast, hashlib
    t = ast.parse(src); parts = []
    for n in t.body:
        if isinstance(n, ast.FunctionDef) and n.name in REPLACED + READ:
            parts.append(ast.get_source_segment(src, n))
        if isinstance(n, ast.Assign) and any(getattr(x, 'id', '') in CONSTS for x in n.targets):
            parts.append(ast.get_source_segment(src, n))
    return hashlib.md5('\n'.join(parts).encode()).hexdigest()[:8]
