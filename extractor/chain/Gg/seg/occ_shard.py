# [uP port, new file] seg.py's occupancy() over one time shard, so the whole video can run as a process pool.
# Usage: occ_shard.py VIDEO T0 DUR OUT.npz  -> times (s, absolute) and occ (n,2,20,10 bool), same rule as seg.occupancy.
import sys, os, subprocess, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import track as T
path, t0, dur, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
W, H, fps = T.W, T.H, 10
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-i', path, '-t', f'{dur:.3f}', '-vf', f'fps={fps},scale={W}:{H}',
                      '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
C = {k: T.coords(v) for k, v in T.X0.items()}; occ = []
while True:
    b = p.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    a = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.int16)
    row = []
    for pl in ('p1', 'p2'):
        xs, ys = C[pl]
        g = np.array([[a[y - 2:y + 3, x - 2:x + 3].mean() for x in xs] for y in ys])
        row.append(g > 90)
    occ.append(np.stack(row))
occ = np.stack(occ); times = t0 + np.arange(len(occ)) / fps
np.savez_compressed(out, times=times, occ=occ); print(out, len(occ))
