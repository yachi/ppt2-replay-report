# ocr_game.py GID: read both scores at 30 fps over [start-1, A end+1.5] -> ocrall/GID.json [(t, s1, d1, s2, d2), ...]
# (amemiya check/ocrall/ocr_all.py, re-templated for the uP capture: ocr/reader.py). A cell with distance > 70 reads '?'.
import sys, json, subprocess, numpy as np
sys.path.insert(0, '/tmp/claude-0/r6/w/ocr')
from reader import classify, cells_of
G = {g['id']: g for g in json.load(open('/tmp/claude-0/r6/w/chain/r6/games.json'))}   # [ach port] one video per game
D = '/tmp/claude-0/r6/w/ocrall'
A = {j['id']: j for j in map(json.loads, open('/tmp/claude-0/r6/w/chain/r6/w/A/games.jsonl'))}
def read(f):
    lab, dm = classify(cells_of(f)); lab = [c if d <= 70 else '?' for c, d in zip(lab, dm)]
    return ''.join(lab[:8]), float(dm[:8].max()), ''.join(lab[8:]), float(dm[8:].max())
for g in sys.argv[1:]:
    t0 = A[g]['start_s'] - 1.0; t1 = A[g]['end_s'] + 1.5
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-i', G[g]['path'], '-t', f'{t1 - t0:.3f}', '-vf', 'crop=854:40:0:385',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    res = []; k = 0; FB = 854 * 40 * 3
    while True:
        b = p.stdout.read(FB)
        if len(b) < FB: break
        f = np.zeros((480, 854, 3), np.uint8); f[385:425] = np.frombuffer(b, np.uint8).reshape(40, 854, 3)
        s1, d1, s2, d2 = read(f); res.append((round(t0 + k / 30, 3), s1, round(d1, 1), s2, round(d2, 1))); k += 1
    json.dump(res, open(f'{D}/{g}.json', 'w')); print(g, len(res), flush=True)
