# [uP port, new file] merge occ shards (each keeps [i*L, (i+1)*L)) and apply seg.games() unchanged.
# Usage: merge.py N L
import sys, json, numpy as np
sys.path.insert(0, '/tmp/claude-0/xo/w/chain/xo/seg'); import seg
N, L = int(sys.argv[1]), float(sys.argv[2])
T, O = [], []
for i in range(N):
    z = np.load(f'shard{i}.npz'); t = z['times']; m = (t >= i * L - 1e-6) & (t < (i + 1) * L - 1e-6)
    T.append(t[m]); O.append(z['occ'][m])
t = np.concatenate(T); occ = np.concatenate(O)
assert np.allclose(np.diff(t), 0.1, atol=1e-3), 'gap'
print(len(t), t[0], t[-1])
np.savez_compressed('occ_full.npz', times=t, occ=occ)
g = seg.games(occ)
json.dump(g, open('seg.json', 'w')); print(len(g), 'segments')
for q in g: print(q)
