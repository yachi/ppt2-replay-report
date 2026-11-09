# [uP port, new file] merge occ shards (each keeps [i*630, (i+1)*630)) and apply seg.games() unchanged.
import sys, json, numpy as np
sys.path.insert(0, '/private/tmp/claude-501/Gg/w/chain/yu/seg'); import seg
T, O = [], []
for i in range(6):
    z = np.load(f'shard{i}.npz'); t = z['times']; m = (t >= i * 570 - 1e-6) & (t < (i + 1) * 570 - 1e-6)
    T.append(t[m]); O.append(z['occ'][m])
t = np.concatenate(T); occ = np.concatenate(O)
assert np.allclose(np.diff(t), 0.1, atol=1e-3), 'gap'
print(len(t), t[0], t[-1])
np.savez_compressed('occ_full.npz', times=t, occ=occ)
g = seg.games(occ)   # seg.games uses index/fps; t[0]==0 so start/end are absolute seconds
json.dump(g, open('seg.json', 'w')); print(len(g), 'segments')
for q in g: print(q)
