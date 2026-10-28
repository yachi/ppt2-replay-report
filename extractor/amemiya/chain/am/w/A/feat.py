"""Extractor A, stage 1: per-frame feature dump (own code, no imports from sk/*.py).

For each frame of a game window, for each player (0 = left/syakegohan, 1 = right):
  grid[20,10]  cell code   0 empty, 1 grey(low sat bright), 2 Z,3 L,4 O,5 S,6 I,7 J,8 T
  val[20,10]   HSV value*255 of the cell patch mean (to tell garbage grey from white flash)
  nxt[5]       NEXT slot piece code (0 = unreadable)
  hold         HOLD box piece code
  border       fraction of frame-border samples showing the player's frame colour
"""
import subprocess, sys, json, numpy as np

W, H = 854, 480
CX0, CY0, CW_, CH_ = 78, 50, 706, 348          # crop box fed by ffmpeg  [am port: old (85,55,690,340) scaled x1.0191]
CELL = 16.0                                     # [am port: 15.7 -> 16.0, gridline fit on 4xcAmo-s-Tg frames 622/640/700]
BX = [137.0, 556.0]                             # board x0 (left, right)  [am port: was 142.5, 553.6; gridline fit]
BY = 391.0                                       # [am port: was 389.0]
DX = BX[1] - BX[0]                              # 411.1
NEXT_X = (316, 354)                             # [am port: old geometry x1.0191 about the board]
NEXT_Y = [(72, 96), (105, 128), (139, 162), (173, 195), (207, 230)]
HOLD_X, HOLD_Y = (86, 126), (84, 109)
BORDER_X = [(132, 133, 300, 301), (552, 553, 719, 720)]
BORDER_Y = [int(round(16 / 15.7 * (y - 389) + 391)) for y in range(95, 385, 12)]

def _idx():
    ys, xs = [], []
    for p in range(2):
        yy = np.array([int(round(BY - CELL * (r + .5))) for r in range(20)])
        xx = np.array([int(round(BX[p] + CELL * (c + .5))) for c in range(10)])
        ys.append(yy); xs.append(xx)
    return ys, xs
CYS, CXS = _idx()

def hsv(rgb):
    """rgb float array (...,3) 0..255 -> h(deg), s, v (0..1)"""
    r, g, b = [rgb[..., i] / 255. for i in range(3)]
    mx = np.maximum(np.maximum(r, g), b); mn = np.minimum(np.minimum(r, g), b)
    d = mx - mn
    s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0)
    h = np.zeros_like(mx)
    dd = np.maximum(d, 1e-9)
    h = np.where(mx == r, ((g - b) / dd) % 6, h)
    h = np.where(mx == g, (b - r) / dd + 2, h)
    h = np.where(mx == b, (r - g) / dd + 4, h)
    return h * 60, s, mx

def hue_code(h):
    c = np.full(h.shape, 8, np.uint8)            # T (purple) default for 260..330
    c[(h < 15) | (h >= 330)] = 2                  # Z red
    c[(h >= 15) & (h < 40)] = 3                   # L orange
    c[(h >= 40) & (h < 70)] = 4                   # O yellow
    c[(h >= 70) & (h < 160)] = 5                  # S green
    c[(h >= 160) & (h < 210)] = 6                 # I cyan
    c[(h >= 210) & (h < 260)] = 7                 # J blue
    return c

OFF = np.arange(-5, 6)

def cells(a, p):
    """code: 0 empty, 1 grey garbage, 2..8 piece colours, 9 white flash, 10 uncertain"""
    ys = CYS[p] - CY0; xs = CXS[p] - CX0
    Y = (ys[:, None] + OFF[None, :]).reshape(-1)
    X = (xs[:, None] + OFF[None, :]).reshape(-1)
    px = a[Y][:, X].reshape(20, 11, 10, 11, 3).astype(np.float32)
    h, s, v = hsv(px)
    vm = v.mean(axis=(1, 3)); vs = v.std(axis=(1, 3)); sm = s.mean(axis=(1, 3))
    mean = px.mean(axis=(1, 3))
    hm, _, _ = hsv(mean)
    code = hue_code(hm)
    code[(sm < 0.5) | (vs > 0.12)] = 10
    grey = (sm < 0.25) & (vs <= 0.075) & (vm >= 0.55)
    code[grey] = 1
    code[grey & (vm > 0.9)] = 9
    code[vm < 0.45] = 0
    return code, (vm * 255).astype(np.uint8)

def piece_in_box(a, x0, x1, y0, y1):
    sub = a[y0 - CY0:y1 - CY0, x0 - CX0:x1 - CX0].reshape(-1, 3).astype(float)
    h, s, v = hsv(sub)
    m = (s > 0.45) & (v > 0.45)
    if m.sum() < 25:
        return 0
    hh = h[m]
    # circular-ish: red wraps; vote by code
    codes = hue_code(hh)
    cnt = np.bincount(codes, minlength=9)
    best = cnt.argmax()
    if cnt[best] < 0.6 * m.sum():
        return 0
    return int(best)

def border(a, p):
    pts = np.array([[a[y - CY0, x - CX0] for x in BORDER_X[p]] for y in BORDER_Y], float)
    h, s, v = hsv(pts)
    if p == 0:
        ok = (h > 180) & (h < 220) & (s > 0.45) & (v > 0.45)
    else:
        ok = ((h < 15) | (h > 330)) & (s > 0.3) & (v > 0.5)
    return float(ok.mean())

def run(path, t0, t1, out):
    cmd = ['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-i', path, '-t', f'{t1 - t0:.3f}',
           '-vf', f'crop={CW_}:{CH_}:{CX0}:{CY0}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    G, V, N, Hd, B = [], [], [], [], []
    fs = CW_ * CH_ * 3
    while True:
        b = pr.stdout.read(fs)
        if len(b) < fs:
            break
        a = np.frombuffer(b, np.uint8).reshape(CH_, CW_, 3)
        g2, v2, n2, h2, b2 = [], [], [], [], []
        for p in range(2):
            c, v = cells(a, p); g2.append(c); v2.append(v)
            dx = int(round(DX)) * p
            n2.append([piece_in_box(a, NEXT_X[0] + dx, NEXT_X[1] + dx, y0, y1) for y0, y1 in NEXT_Y])
            h2.append(piece_in_box(a, HOLD_X[0] + dx, HOLD_X[1] + dx, *HOLD_Y))
            b2.append(border(a, p))
        G.append(g2); V.append(v2); N.append(n2); Hd.append(h2); B.append(b2)
    pr.wait()
    np.savez_compressed(out, grid=np.array(G, np.uint8), val=np.array(V, np.uint8),
                        nxt=np.array(N, np.uint8), hold=np.array(Hd, np.uint8),
                        border=np.array(B, np.float32), t0=t0, fps=30.0)
    return len(G)

if __name__ == '__main__':
    path, t0, t1, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    print(run(path, t0, t1, out))
