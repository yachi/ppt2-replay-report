"""CI check for run_pcscan.py, with no video: a stand-in `ffmpeg` on PATH writes synthetic rgb24 frames (noise plus
orange and white banner blocks) for whatever -ss / -t it is given. The chain's own pcscan.py (te's copy) and the
runner read the same bytes; run_pcscan.py --check stops unless the two JSON texts are identical. It runs at chunk
sizes that do and do not divide the frame count, then on three planted defects, each of which must be caught."""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RUNNER = os.path.join(HERE, 'run_pcscan.py')
PCSCAN = os.path.join(HERE, '..', 'chain', 'te', 'w', 'R', 'pcscan.py')
FAKE = r'''#!/usr/bin/env python3
import sys, numpy as np
a = sys.argv; ss = float(a[a.index('-ss') + 1]); t = float(a[a.index('-t') + 1])
w, h = [int(v) for v in a[a.index('-vf') + 1].split('=')[1].split(':')[:2]]
n = int(round(t * 10)); rng = np.random.default_rng(int(ss * 100))
F = rng.integers(0, 256, (n, h, w, 3), dtype=np.uint8)
for i in range(n):
    k = int(rng.integers(0, 4))
    x = int(rng.integers(0, w - 40)); y = int(rng.integers(0, h - 20))
    if k == 1: F[i, y:y + 20, x:x + 40] = (240, 140, 20)       # orange
    if k == 2: F[i, y:y + 20, x:x + 40] = (250, 250, 248)      # white
sys.stdout.buffer.write(F.tobytes())
'''
GAMES = (('g1', 100.0, 103.3), ('g2', 200.05, 201.0), ('g3', 300.0, 304.95))


def run(runner, chunk, d):
    p = subprocess.run([sys.executable, runner, '--check', '--chunk', str(chunk), *[g for g, _, _ in GAMES]],
                       cwd=os.path.join(d, 'w'), capture_output=True, text=True,
                       env={**os.environ, 'PATH': os.path.join(d, 'bin') + os.pathsep + os.environ['PATH']})
    return p.returncode == 0, p.stderr.strip().splitlines()[-1:] if p.stderr else []


def main():
    d = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(d, 'bin')); os.makedirs(os.path.join(d, 'w', 'R', 'pcban')); os.makedirs(os.path.join(d, 'w', 'A'))
        fake = os.path.join(d, 'bin', 'ffmpeg'); open(fake, 'w').write(FAKE.replace('/usr/bin/env python3', sys.executable)); os.chmod(fake, 0o755)
        shutil.copy(PCSCAN, os.path.join(d, 'w', 'R', 'pcscan.py'))
        json.dump([dict(id=g, path='synthetic.mp4') for g, _, _ in GAMES], open(os.path.join(d, 'games.json'), 'w'))
        open(os.path.join(d, 'w', 'A', 'games.jsonl'), 'w').write(
            ''.join(json.dumps(dict(id=g, start_s=s, end_s=e)) + '\n' for g, s, e in GAMES))
        for chunk in (1, 7, 50, 1000):
            ok, msg = run(RUNNER, chunk, d)
            if not ok:
                sys.exit(f'pcscan-chunked check FAILED at chunk {chunk}: {msg}')
        out = json.load(open(os.path.join(d, 'w', 'R', 'pcban', 'g1.json')))
        hit = sum(v > 0.05 for g in out.values() for p in ('p1', 'p2') for k in ('o', 'w') for v in g[p][k])
        if hit == 0:
            sys.exit('pcscan-chunked check: the synthetic frames never lit the orange or white masks, so it compared nothing')
        src = open(RUNNER).read()
        mutants = {
            'last partial chunk dropped': ('if n:', 'if n == chunk:'),
            'p2 window one column off': ('slice(411, 411 + W)', 'slice(412, 412 + W)'),
            'white mask read as orange': ("r[p]['w'] += wm", "r[p]['w'] += o"),
        }
        caught = 0
        for name, (a, b) in mutants.items():
            assert src.count(a) == 1, name
            m = os.path.join(d, 'mutant.py'); open(m, 'w').write(src.replace(a, b))
            ok, _ = run(m, 7, d)
            if ok:
                sys.exit(f'pcscan-chunked check: planted defect not caught: {name}')
            caught += 1
        n = sum(len(g['p1']['o']) for g in out.values())
        print(f'pcscan-chunked check: {n} frames over {len(GAMES)} games, JSON identical to the chain\'s pcscan.py at '
              f'chunk 1, 7, 50 and 1000 ({hit} mask means above 0.05); {caught} planted defects caught')
    finally:
        shutil.rmtree(d)


main()
