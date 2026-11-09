# [uP port, new file] gamefilter.py + winner.py over a 9-process pool (same feat()/crop rules; the archived scripts loop serially).
# Usage (cwd seg/): par.py VIDEO SEG.json  -> SEG.json gets 'bright'; SEG_games.json = winner.py's filter + dL/dR.
import sys, json, numpy as np
from multiprocessing import Pool
sys.path.insert(0, '.')
import gamefilter as GF
V = sys.argv[1]; SEG = sys.argv[2]
def br(q): return GF.feat(V, q['start'] + 2.0)
def wframe(t):
    import subprocess
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.2f}', '-i', V, '-frames:v', '1', '-vf', 'scale=640:360', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    a = np.frombuffer(b, np.uint8).reshape(360, 640, 3).astype(float)
    return (a[324:341, 268:292].mean(2), a[324:341, 348:372].mean(2))
if __name__ == '__main__':
    g = json.load(open(SEG))
    with Pool(9) as P:
        for q, b in zip(g, P.map(br, g)): q['bright'] = b
        json.dump(g, open(SEG, 'w'))
        k = [q for q in g if max(q['bright']) < 100 and q['end'] - q['start'] > 5]
        crops = P.map(wframe, [q['start'] + 3.0 for q in k] + [k[-1]['end'] - 1.0])
    for i, q in enumerate(k):
        q['dL'] = round(float(np.abs(crops[i + 1][0] - crops[i][0]).mean()), 1); q['dR'] = round(float(np.abs(crops[i + 1][1] - crops[i][1]).mean()), 1)
        print(q['start'], round(q['end'] - q['start'], 1), q['bright'], q['dL'], q['dR'])
    json.dump(k, open(SEG.replace('.json', '_games.json'), 'w'))
    print(len(k), 'games of', len(g), 'segments')
