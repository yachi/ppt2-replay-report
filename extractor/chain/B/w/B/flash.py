import numpy as np
def ffill(cls):
    cls = cls.copy(); cls[0][cls[0] == 9] = 0
    for i in range(1, len(cls)):
        m = cls[i] == 9; cls[i][m] = cls[i - 1][m]
    return cls
def flash_events(cls, i0, i1, minrun=2, gap=6):
    """rows entirely grey/white (class 1) = clear flash. Returns [(onset_frame, sorted rows)]"""
    full = (cls[i0:i1] == 1).all(-1)    # n,20
    ev = []; active = {}  # row -> run length
    cur = None
    for j in range(len(full)):
        rows = set(np.nonzero(full[j])[0].tolist())
        # require the row to stay flashing minrun frames
        if j + minrun <= len(full):
            rows = {r for r in rows if full[j:j + minrun, r].all()}
        new = {r for r in rows if not (j > 0 and full[j - 1, r])}
        if new:
            f = i0 + j
            if cur and f - cur[0] <= gap: cur[1].update(new)
            else:
                if cur: ev.append(cur)
                cur = [f, set(new)]
    if cur: ev.append(cur)
    return [(f, sorted(r)) for f, r in ev]
def heights(occ):
    """occ: 20x10 bool -> column heights"""
    h = np.zeros(10, int)
    for c in range(10):
        nz = np.nonzero(occ[:, c])[0]
        h[c] = nz.max() + 1 if len(nz) else 0
    return h
def classify_flash(db, ev, pre=3, post=24):
    out = []
    n = len(db)
    for f, rows in ev:
        a = db[max(0, f - pre)] > 0; b = db[min(n - 1, f + post)] > 0
        ha, hb = heights(a), heights(b)
        m = [hb[c] - ha[c] for c in range(10) if ha[c] > max(rows)]  # columns standing above the flash rows
        if not m: m = [hb[c] - ha[c] for c in range(10)]
        d = float(np.median(m))
        # garbage rows count change at the bottom
        def ng(x):
            k = 0
            while k < 20 and (x[k] == 1).sum() >= 8 and (x[k] > 0).sum() == 9: k += 1
            return k
        out.append(dict(f=f, rows=rows, dh=d, g_before=ng(db[max(0, f - pre)]), g_after=ng(db[min(n - 1, f + post)])))
    return out
