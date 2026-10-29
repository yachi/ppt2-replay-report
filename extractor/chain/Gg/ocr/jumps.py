# Score-jump detector, copied from amemiya check/ocr/deltas3.py (stable) and check/ocrall/compare.py (events, th=60).
def stable(seq, n=3):
    out = []; prev = None; run = 0
    for t, s in seq:
        if s == prev: run += 1
        else: run = 1; prev = s; ts = t
        if run == n and s.isdigit(): out.append((ts, int(s)))
    return out
def events(seq, th=60):
    st = stable(seq); ev = []; cur = None
    for i, (t, v) in enumerate(st):
        if cur is None: cur = v; continue
        nxt = [w for _, w in st[i + 1:i + 4]]
        if v < cur - 100 or v - cur > 20000: continue
        if nxt and sum(abs(w - v) < 200 or w > v for w in nxt) < len(nxt) / 2: continue
        d = v - cur
        if d >= th: ev.append((round(t, 2), d))
        if d > 0 or d < -100: cur = v
        elif d < 0: cur = max(cur, v)
    return ev
