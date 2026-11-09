#!/usr/bin/env python3
"""List NEXT-queue shifts (and hold-box changes) for one player in [t0,t1].

usage: python3 nextcount.py p1|p2 T0 T1 [--dump]

Decodes only [T0,T1] of the video with ffmpeg (30 fps raw frames, piped, cropped),
classifies the 5 NEXT slots and the HOLD box by colour on every frame, and reports:
  shift  t  k   -- the queue advanced by k pieces between the previous stable state and this one
  hold   t  X   -- the hold box changed to piece X ('-' = empty)
  unk    t0 t1  -- stretches where the queue could not be read (shake, cut-in, freeze, ...)
A state is accepted only when it is read identically on 2 consecutive frames.
"""
import sys, subprocess, colorsys
import numpy as np

VIDEO = '/private/tmp/claude-501/Gg/video/Ggl5NeUAYEA.mp4'
W, H = 854, 480
SLOT_Y = [(73, 100), (106, 134), (139, 166), (171, 200), (205, 234)]
NEXT_X = {'p1': 314, 'p2': 724}
HOLD_X = {'p1': 92, 'p2': 506}   # hold box piece area x..x+40, y 90..115
HOLD_Y = (88, 118)
# reference hues (degrees) and colours
REF = {'I': 197, 'J': 220, 'O': 47, 'L': 24, 'Z': 358, 'S': 95, 'T': 302}


def classify(region):
    r = region.reshape(-1, 3).astype(int)
    mx = r.max(1); mn = r.min(1)
    s = (mx - mn) > 80
    n = int(s.sum())
    if n < 60:
        return '-' if n < 15 else '?'
    med = np.median(r[s], 0) / 255.0
    h, sat, v = colorsys.rgb_to_hsv(*med)
    hd = h * 360
    best, bd = None, 999
    for k, ref in REF.items():
        d = min(abs(hd - ref), 360 - abs(hd - ref))
        if d < bd:
            best, bd = k, d
    if bd > 11:
        return '?'
    return best


RGB = {'I': (31, 142, 190), 'O': (229, 191, 35), 'Z': (185, 33, 39), 'S': (102, 173, 42),
       'T': (134, 23, 130), 'L': (218, 91, 25), 'J': (15, 62, 149)}
SHAPES = {'T': ((0, 1, 0), (1, 1, 1)), 'J': ((1, 0, 0), (1, 1, 1)), 'L': ((0, 0, 1), (1, 1, 1)),
          'S': ((0, 1, 1), (1, 1, 0)), 'Z': ((1, 1, 0), (0, 1, 1))}


def shape_of(m):
    ys, xs = np.nonzero(m)
    if len(ys) < 40:
        return None
    # trim stray pixels: use 3..97 percentiles for bbox
    y0, y1 = np.percentile(ys, 2), np.percentile(ys, 98) + 1
    x0, x1 = np.percentile(xs, 2), np.percentile(xs, 98) + 1
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


def classify2(region):
    """piece in a NEXT/HOLD slot: colour and shape must agree; '-' empty, '?' unreadable"""
    r = region.astype(np.int16)
    sat = (r.max(2) - r.min(2)) > 80
    if sat.sum() < 15:
        return '-'
    best, bn, bm = None, 0, None
    for k, c in RGB.items():
        d = np.abs(r - np.array(c, np.int16)).sum(2)
        m = d < 110
        n = int(m.sum())
        if n > bn:
            best, bn, bm = k, n, m
    if bn < 60:
        return '?'
    sh = shape_of(bm)
    return best if sh == best else '?'


def frames(t0, t1):
    n = int(round((t1 - t0) * 30)) + 1
    cmd = ['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-i', VIDEO, '-frames:v', str(n),
           '-r', '30', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    sz = W * H * 3
    i = 0
    while True:
        b = p.stdout.read(sz)
        if len(b) < sz:
            break
        yield t0 + i / 30.0, np.frombuffer(b, np.uint8).reshape(H, W, 3)
        i += 1
    p.wait()


REF_FRAME_T = 400.0   # a clean frame: both boards at rest
TPL = {}
SEARCH = 48           # +- pixels searched around the rest position
TPL_BOX = {'p1': (306, 58, 362, 240), 'p2': (716, 58, 772, 240)}


def white(a):
    a = a.astype(np.int16)
    return ((a.min(2) > 190) & ((a.max(2) - a.min(2)) < 50)).astype(np.float32)


def init_templates():
    if TPL:
        return
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{REF_FRAME_T:.3f}', '-i', VIDEO, '-frames:v', '1',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    fr = np.frombuffer(b, np.uint8).reshape(H, W, 3)
    for pl, (x0, y0, x1, y1) in TPL_BOX.items():
        TPL[pl] = white(fr[y0:y1, x0:x1])


def locate(fr, pl):
    """offset (dx,dy) of the NEXT column against the rest position, and match score 0..1"""
    from scipy.signal import fftconvolve
    x0, y0, x1, y1 = TPL_BOX[pl]
    t = TPL[pl]
    X0, Y0 = max(0, x0 - SEARCH), max(0, y0 - SEARCH)
    X1, Y1 = min(W, x1 + SEARCH), min(H, y1 + SEARCH)
    m = white(fr[Y0:Y1, X0:X1])
    c = fftconvolve(m, t[::-1, ::-1], mode='valid')
    iy, ix = np.unravel_index(np.argmax(c), c.shape)
    return X0 + ix - x0, Y0 + iy - y0, float(c[iy, ix] / t.sum())


MIN_SCORE = 0.6


def read_state(fr, pl):
    dx, dy, sc = locate(fr, pl)
    if sc < MIN_SCORE:
        return '?????', '?', (dx, dy, sc)
    x = NEXT_X[pl] + dx
    q = ''.join(classify2(fr[y0 + dy:y1 + dy, x - 2:x + 42]) for y0, y1 in SLOT_Y)
    hx = HOLD_X[pl] + dx
    hd = classify2(fr[HOLD_Y[0] + dy:HOLD_Y[1] + dy, hx - 2:hx + 42])
    return q, hd, (dx, dy, sc)


def shift_k(a, b):
    """smallest k in 0..4 with b[:5-k] == a[k:]"""
    for k in range(0, 5):
        if b[:5 - k] == a[k:]:
            return k
    return None


def cands(stable, q):
    """shift amounts k (0..4) consistent with reading q (wildcard '?') against stable (may hold '?').
    Each candidate needs >= 2 compared positions (k=4: the single position must match and k is only
    accepted when the 4 newly revealed slots are read)."""
    out = []
    for k in range(0, 5):
        n = 0; ok = True
        for i in range(5 - k):
            if q[i] == '?' or stable[i + k] == '?':
                continue
            n += 1
            if q[i] != stable[i + k]:
                ok = False; break
        if ok and n >= 2:
            out.append(k)
    return out[:1]      # smallest consistent shift (a real shift between two readable frames is 1)


def merge(a, b):
    return ''.join(y if y != '?' else x for x, y in zip(a, b))


def agree(a, b):
    """slots read identically in two readings; others '?'"""
    return ''.join(x if x == y else '?' for x, y in zip(a, b))


def cands_weak(stable, q):
    """cands(), and if none, retry trusting fewer of the newest slots (a misread tail slot must not
    lock the reader out for the rest of the game)"""
    c = cands(stable, q)
    if c:
        return c, 0
    for j in (1, 2):
        c = cands(stable[:5 - j] + '?' * j, q)
        if c:
            return c, j
    return [], 0


SEQ = {}        # absolute queue index -> piece, filled by run()
CONFLICT = []   # (t, index, old, new) a slot read two different ways


def bag_check(seq, n):
    """best 7-bag alignment over indices 0..n-1: (offset, bad blocks, blocks checked)"""
    best = None
    for o in range(7):
        bad = []; tot = 0
        j = o
        while j + 7 <= n:
            blk = [seq.get(i) for i in range(j, j + 7)]
            if None not in blk:
                tot += 1
                if len(set(blk)) != 7:
                    bad.append(j)
            j += 7
        if best is None or len(bad) < len(best[1]):
            best = (o, bad, tot)
    return best


def run(pl, t0, t1, dump=False):
    init_templates()
    events = []
    stable = None       # last accepted queue ('?' = slot not read since it appeared)
    pend = None         # (t, k, q) candidate shift seen on the previous frame
    prev_full = None
    stable_hold = None
    prev_hold = None
    unk_start = None
    hist = []
    base = 0
    SEQ.clear(); CONFLICT.clear()
    t = t0
    for t, fr in frames(t0, t1):
        q, hd, loc = read_state(fr, pl)
        q = q.replace('-', '?')
        if dump:
            print(f'{t:.3f} {q} {hd} st={stable} dx={loc[0]} dy={loc[1]} sc={loc[2]:.2f}')
        known = sum(c != '?' for c in q)
        if stable is None:
            if known == 5 and prev_full == q:
                stable = q
                events.append(('init', t, q))
            prev_full = q if known == 5 else None
        elif known < 3:
            if unk_start is None:
                unk_start = t
            pend = None
        else:
            c, weak = cands_weak(stable, q)
            if len(c) == 1:
                hist = []
                if unk_start is not None:
                    if t - unk_start >= 0.2:
                        events.append(('unk', unk_start, t))
                    unk_start = None
                k = c[0]
                if k == 0:
                    if weak:
                        pend = None       # a misread slot; keep the state as it is
                    else:
                        # confirmed slots overwrite; a slot never read so far is filled at once
                        if pend is not None and pend[1] == 0:
                            stable = merge(stable, agree(pend[2], q))
                        stable = ''.join(y if x == '?' and y != '?' else x for x, y in zip(stable, q))
                        pend = (t, 0, q)
                elif pend is not None and pend[1] == k and cands_weak(stable, pend[2])[0] == [k]:
                    if weak:
                        events.append(('weak', pend[0], weak))
                    new = (stable[k:] + '?' * k) if not weak else (stable[:5 - weak] + '?' * weak)[k:] + '?' * k
                    events.append(('shift', pend[0], k, stable + '>' + merge(new, agree(pend[2], q))))
                    base += k
                    stable = merge(new, agree(pend[2], q))
                    pend = None
                else:
                    pend = (t, k, q)
            else:
                if unk_start is None:
                    unk_start = t
                pend = None
                # resync: three identical full readings that match nothing
                if known == 5:
                    hist.append(q)
                    if len(hist) >= 3 and hist[-1] == hist[-2] == hist[-3]:
                        k1 = None
                        for k in range(0, 5):
                            if all(q[i] == stable[i + k] or stable[i + k] == '?' for i in range(5 - k)) and \
                                    any(stable[i + k] != '?' for i in range(5 - k)):
                                k1 = k; break
                        events.append(('resync', unk_start, t, k1, stable + '>' + q))
                        base += (k1 or 0)
                        stable = q; hist = []
                        unk_start = None
                else:
                    hist = []
        if stable is not None:
            for i, ch in enumerate(stable):
                if ch != '?':
                    j = base + i
                    if j in SEQ and SEQ[j] != ch:
                        CONFLICT.append((round(t, 3), j, SEQ[j], ch))
                    SEQ[j] = ch
        if prev_hold is not None and prev_hold == hd and hd != '?' and hd != stable_hold:
            events.append(('hold', t - 1 / 30.0, hd))
            stable_hold = hd
        prev_hold = hd
    if unk_start is not None and t - unk_start >= 0.2:
        events.append(('unk', unk_start, t))
    return events


def summary(events):
    return sum(e[2] for e in events if e[0] == 'shift')


if __name__ == '__main__' and sys.argv[1] != '--game':
    pl, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    ev = run(pl, t0, t1, dump='--dump' in sys.argv)
    for e in ev:
        if e[0] == 'shift':
            print(f'shift {e[1]:.3f} {e[2]} {e[3]}')
        elif e[0] == 'hold':
            print(f'hold  {e[1]:.3f} {e[2]}')
        elif e[0] == 'resync':
            print(f'resync {e[1]:.3f} {e[2]:.3f} k={e[3]} {e[4]}')
        elif e[0] == 'unk':
            print(f'unk   {e[1]:.3f} {e[2]:.3f} ({e[2]-e[1]:.2f}s)')
        else:
            print(e[0], *[f'{x:.3f}' if isinstance(x, float) else x for x in e[1:]])
    print('TOTAL_SHIFTS', summary(ev))


# ---------------------------------------------------------------- game mode
GAMES = '/private/tmp/claude-501/Gg/w/chain/yu/w/A/games.jsonl'
CSEQ = '/private/tmp/claude-501/Gg/w/chain/yu/w/tetrio/cseq.json'


def game(gid, pl, tol=0.12):
    """python3 nextcount.py --game y005 p1  -> shifts in the game window matched to chain events"""
    import json
    g = [json.loads(l) for l in open(GAMES) if json.loads(l)['id'] == gid][0]
    s0, s1 = g['start_s'], g['end_s']
    ev = [e for e in json.load(open(CSEQ))[f'{gid} {pl}'] if e[1] != 'BREAK']
    out = run(pl, s0 - 1.5, s1 + 1.0)
    sh = []           # (t, k)
    resyncs = []
    for e in out:
        if e[0] == 'shift':
            sh.append((round(e[1], 3), e[2]))
        elif e[0] == 'resync':
            resyncs.append((round(e[1], 3), round(e[2], 3), e[3], e[4]))
            if e[3]:
                sh.append((round(e[2], 3), e[3]))
    sh.sort()
    holds = [(round(e[1], 3), e[2]) for e in out if e[0] == 'hold']
    unk = [(round(e[1], 3), round(e[2], 3)) for e in out if e[0] == 'unk' and e[2] - e[1] >= 0.5]
    inwin = [x for x in sh if x[0] <= s1 + 1e-6]
    after = [x for x in sh if x[0] > s1 + 1e-6]
    tot = sum(k for _, k in inwin)
    et = [e[0] for e in ev]
    # monotone alignment (DP) of spawns after the first against chain events; an event may lead its
    # spawn by up to ~0.75 s (line-clear delay) or trail it slightly. Unpaired items cost GAP.
    singles = [t for t, k in inwin for _ in range(k)][1:]
    GAP = 0.6

    def cost(st, et_):
        d = st - et_
        if -0.45 <= d <= 0.9:
            return abs(d - 0.1) * 0.5
        return None
    n, m = len(singles), len(et)
    INF = 1e18
    D = [[INF] * (m + 1) for _ in range(n + 1)]
    P = [[None] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            v = D[i][j]
            if v >= INF:
                continue
            if i < n and v + GAP < D[i + 1][j]:
                D[i + 1][j] = v + GAP; P[i + 1][j] = (i, j, 's')
            if j < m and v + GAP < D[i][j + 1]:
                D[i][j + 1] = v + GAP; P[i][j + 1] = (i, j, 'e')
            if i < n and j < m:
                c = cost(singles[i], et[j])
                if c is not None and v + c < D[i + 1][j + 1]:
                    D[i + 1][j + 1] = v + c; P[i + 1][j + 1] = (i, j, 'p')
    i, j = n, m; unmatched_sh = []; unmatched_ev = []
    while (i, j) != (0, 0):
        pi, pj, w = P[i][j]
        if w == 's':
            unmatched_sh.append(round(singles[pi], 3))
        elif w == 'e':
            unmatched_ev.append(round(et[pj], 2))
        i, j = pi, pj
    unmatched_sh.reverse(); unmatched_ev.reverse()
    first_hold = next((h for h in holds if h[1] not in '-?' and h[0] >= s0 - 0.5), None)
    nsp = sum(k for _, k in inwin)
    bag = bag_check(SEQ, nsp)
    missing = [i for i in range(nsp) if i not in SEQ]
    return dict(bag_offset=bag[0], bag_bad_blocks=bag[1], bag_blocks=bag[2], seq_missing=missing,
                seq_conflicts=CONFLICT[:20],
                id=gid, player=pl, start=s0, end=s1, shifts_total=tot, first_shift=inwin[0] if inwin else None,
                multi=[x for x in inwin if x[1] != 1], shifts_after_end=after[:3], events=len(ev),
                first_hold=first_hold, unmatched_shifts=unmatched_sh, unmatched_events=unmatched_ev,
                long_unknown=unk, resyncs=resyncs, weak=[round(e[1], 3) for e in out if e[0] == 'weak'], last_shift=inwin[-1] if inwin else None, last_event=et[-1] if et else None)


if __name__ == '__main__' and sys.argv[1] == '--game':
    import json as _j
    print(_j.dumps(game(sys.argv[2], sys.argv[3]), indent=1))


def cumdiff(gid, pl, step=0.5):
    """print where cumulative(shift spawns) - cumulative(events) changes; a k-shift is put at its time"""
    import json
    g = [json.loads(l) for l in open(GAMES) if json.loads(l)['id'] == gid][0]
    s0, s1 = g['start_s'], g['end_s']
    ev = [e[0] for e in json.load(open(CSEQ))[f'{gid} {pl}'] if e[1] != 'BREAK']
    out = run(pl, s0 - 1.5, s1 + 1.0)
    sh = [(e[1], e[2]) for e in out if e[0] == 'shift' and e[1] <= s1 + 1e-6]
    hold = next((e[1] for e in out if e[0] == 'hold' and e[2] not in '-?' and e[1] >= s0 - 0.5), None)
    pts = sorted([(t, k, 's') for t, k in sh] + [(t, 1, 'e') for t in ev])
    d = 0; last = None; rows = []
    for t, k, w in pts:
        d += k if w == 's' else -1
        rows.append((t, k, w, d))
    return sh, ev, hold, rows
