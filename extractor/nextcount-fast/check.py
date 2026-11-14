"""Self-check without a video: a chain's nextcount.py read_state() with the original helpers against fastnc's,
on synthetic frames (a white-outlined NEXT column and hold box, pieces drawn in the queue's colours and shapes,
noise, random offsets, blank and saturated frames), plus pct() against np.percentile. Then plants three defects
and requires each to be caught."""
import os, sys, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import fastnc
TOOL = os.path.join(HERE, '..', 'chain', 'te', 'corr', 'tools', 'nextcount.py')
src = open(TOOL).read()
assert fastnc.fingerprint(src) in fastnc.KNOWN
ns = {'__name__': 'nextcount'}
exec(compile(src[:src.index("if __name__ == '__main__'")], TOOL, 'exec'), ns)
W, H = ns['W'], ns['H']
rng = np.random.default_rng(3)
CELL = 8


def draw_piece(fr, k, x, y):
    c = np.array(ns['RGB'][k], np.int16)
    if k == 'I':
        cells = [(0, i) for i in range(4)]
    elif k == 'O':
        cells = [(0, 0), (0, 1), (1, 0), (1, 1)]
    else:
        cells = [(r, cc) for r in range(2) for cc in range(3) if ns['SHAPES'][k][r][cc]]
    for r, cc in cells:
        blk = c + rng.integers(-12, 13, (CELL, CELL, 3))
        fr[y + r * CELL:y + (r + 1) * CELL, x + cc * CELL:x + (cc + 1) * CELL] = np.clip(blk, 0, 255)


def frame(pl, dx, dy, q, hold, noise):
    fr = rng.integers(0, noise + 1, (H, W, 3)).astype(np.int16)
    x0, y0, x1, y1 = ns['TPL_BOX'][pl]
    o = (slice(y0 + dy, y1 + dy), slice(x0 + dx, x1 + dx))
    box = np.zeros((y1 - y0, x1 - x0), bool); box[:2] = box[-2:] = True; box[:, :2] = box[:, -2:] = True
    box[60:62] = True
    fr[o][box] = 230
    for (ya, yb), k in zip(ns['SLOT_Y'], q):
        if k != '-':
            draw_piece(fr, k, ns['NEXT_X'][pl] + dx + 4, ya + dy + 6)
    if hold != '-':
        draw_piece(fr, hold, ns['HOLD_X'][pl] + dx + 4, ns['HOLD_Y'][0] + dy + 6)
    return np.clip(fr, 0, 255).astype(np.uint8)


P = list(ns['RGB']) + ['-']
ns['TPL'].update({pl: ns['white'](frame(pl, 0, 0, '-----', '-', 0)[y0:y1, x0:x1])
                  for pl, (x0, y0, x1, y1) in ns['TPL_BOX'].items()})
cases = []
for i in range(400):
    pl = ('p1', 'p2')[i % 2]
    cases.append(frame(pl, int(rng.integers(-20, 21)), int(rng.integers(-20, 21)),
                       ''.join(rng.choice(P, 5)), str(rng.choice(P)), int(rng.choice([0, 40, 120, 255]))))
cases += [np.zeros((H, W, 3), np.uint8), np.full((H, W, 3), 255, np.uint8)]


def readall(funcs):
    keep = {k: ns[k] for k in funcs}
    ns.update(funcs)
    try:
        return [(ns['read_state'](fr, ('p1', 'p2')[i % 2])) for i, fr in enumerate(cases)]
    finally:
        ns.update(keep)


def helpers(mutate=None):
    """fastnc's helpers installed on a copy of the module namespace, optionally with one defect planted"""
    g = dict(ns); fastnc.install(g)
    if mutate:
        mutate(g)
    return {k: g[k] for k in fastnc.REPLACED}


def pct_ok(pct):
    r2 = np.random.default_rng(0); n = 0
    for _ in range(20000):
        a = np.sort(r2.integers(0, int(r2.integers(1, 60)), int(r2.integers(1, 700))))
        for p in (2, 98):
            if pct(a, p) != np.percentile(a, p):
                return False, n
            n += 1
    return True, n


want = readall({k: ns[k] for k in fastnc.REPLACED})
got = readall(helpers())
assert got == want, [i for i, (a, b) in enumerate(zip(got, want)) if a != b][:10]
read = sum(q.count('?') < 5 for q, _, _ in want); kinds = {c for q, _, _ in want for c in q}
assert read > 200 and kinds >= set('IJLOSZT'), (read, kinds)
ok, n = pct_ok(fastnc.pct)
assert ok

# planted defects, each caught by the comparison that guards it
loc_off = lambda g: g.update(locate=(lambda lo: lambda fr, pl: (lambda d: (d[0], d[1], np.nextafter(d[2], 2.0)))(lo(fr, pl)))(g['locate']))  # 1 ulp in the score
s_as_t = lambda g: g.update(classify2=(lambda c2: lambda r: (lambda v: 'T' if v == 'S' else v)(c2(r)))(g['classify2']))
caught = [readall(helpers(loc_off)) != want, readall(helpers(s_as_t)) != want,
          not pct_ok(lambda a, p: (lambda v: v + (1e-9 if p == 98 else 0))(fastnc.pct(a, p)))[0]]
assert all(caught), caught
print(f'nextcount-fast check: {len(cases)} frames, read_state identical ({read} with a queue read, pieces '
      f'{"".join(sorted(kinds - {"?"}))}); pct == np.percentile on {n} arrays; 3 planted defects caught')
