# Game segmentation for a 360p video with no games.csv rows: occupancy of both boards at 10 fps.
# A game starts when both boards have been empty for >= 0.8 s and one fills; it ends when both are empty again.
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import track as T
def occupancy(path, fps=10):
    W, H = T.W, T.H
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'fps={fps},scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    C = {k: T.coords(v) for k, v in T.X0.items()}; out = []
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        a = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.int16)
        row = []
        for pl in ('p1', 'p2'):
            xs, ys = C[pl]
            g = np.array([[a[y - 2:y + 3, x - 2:x + 3].mean() for x in xs] for y in ys])
            row.append(g > 90)
        out.append(np.stack(row))
    return np.stack(out)   # n,2,20,10 bool
def games(occ, fps=10):
    n = occ.sum((2, 3)); empty = (n == 0).all(1); res = []; z = 0; cur = None
    for i in range(len(n)):
        if empty[i]:
            z += 1
            if cur is not None and z >= 8:
                s, = cur; e = i - z
                h = [int(occ[e, k].any(1).nonzero()[0].max() + 1) if occ[e, k].any() else 0 for k in range(2)]
                # loser = the board that is higher (topped out) in the last frames
                hh = [max(int(occ[j, k].any(1).nonzero()[0].max() + 1) if occ[j, k].any() else 0 for j in range(max(s, e - 10), e + 1)) for k in range(2)]
                res.append(dict(start=s / fps, end=e / fps, h=hh)); cur = None
        else:
            if cur is None and z >= 8: cur = (i,)
            z = 0
    return res
if __name__ == '__main__':
    path, out = sys.argv[1], sys.argv[2]
    occ = occupancy(path); np.save(out + '.npy', np.packbits(occ, axis=-1))
    g = games(occ); json.dump(g, open(out, 'w')); print(len(g), 'games')
