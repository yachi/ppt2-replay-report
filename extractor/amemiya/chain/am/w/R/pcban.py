# [am port, new file] R/pc/<id>.npz (pcscan.py NCC series, 30 fps) -> R/pcban.json {id: {p: [(t_onset, dur_s), ...]}}.
# The lg step that wrote its pcban.json is not archived; lg's metrics.py uses segments with dur >= 0.5 s.
# A segment = run of frames with NCC > 0.6, gaps <= 3 frames bridged. Noise max on boards without a banner: 0.49 (k011 p1).
import json, glob, numpy as np
THR, BRIDGE = 0.6, 3
out = {}
for f in sorted(glob.glob('R/pc/*.npz')):
    g = f.split('/')[-1][:-4]; z = np.load(f); t0 = float(z['t0']); out[g] = {}
    for p in ('p1', 'p2'):
        on = np.nonzero(z[p] > THR)[0]; segs = []
        for i in on:
            if segs and i - segs[-1][1] <= BRIDGE + 1: segs[-1][1] = i
            else: segs.append([i, i])
        out[g][p] = [(round(t0 + a / 30, 2), round((b - a + 1) / 30, 2)) for a, b in segs]
json.dump(out, open('R/pcban.json', 'w'))
n = sum(1 for g in out for p in out[g] for t, d in out[g][p] if d >= 0.5)
print('banners >= 0.5 s:', n, '| shorter segments:', sum(1 for g in out for p in out[g] for t, d in out[g][p] if d < 0.5))
