"""Run a chain's R/pcscan.py (the PERFECT CLEAR banner scan) with frames streamed in chunks, so one long game no
longer holds every frame as float32 at once. The chain's file is read, never edited; run it where the chain runs it:

    python3 run_pcscan.py [--check] [--chunk N] [--tool PATH] GID...

pcscan.py decodes a whole game into one float32 array: about 5 GB for a long game, which is what got the scan
OOM-killed. This runner reads the same ffmpeg command's output N frames at a time (default 300) and applies the
chain's own feat() to each chunk. Every printed value is a per-frame mean of a boolean mask, i.e. count / pixels,
exact in float64 whatever the chunking, so R/pcban/<first GID>.json comes out byte for byte the same.

It refuses a pcscan.py other than the version checked here (KNOWN, the md5 of the file), unless --force is given.
--check then also runs the chain's own loop on the same games and stops unless the two JSON texts are identical."""
import hashlib, json, os, subprocess, sys
import numpy as np

KNOWN = {'6f7d501ab191eb1a8c7ee36e43c363e1'}
MARK = 'out={}\n'

args = sys.argv[1:]
check = '--check' in args; force = '--force' in args
args = [a for a in args if a not in ('--check', '--force')]
tool, chunk = 'R/pcscan.py', 300
for flag in ('--tool', '--chunk'):
    if flag in args:
        i = args.index(flag)
        if flag == '--tool': tool = args[i + 1]
        else: chunk = int(args[i + 1])
        del args[i:i + 2]
if not args:
    sys.exit(__doc__)
src = open(tool).read()
fp = hashlib.md5(src.encode()).hexdigest()
if fp not in KNOWN and not force:
    sys.exit(f'pcscan-chunked: {tool} differs from the pcscan.py checked here (md5 {fp}); run with --check --force '
             'on a short game and add the md5 to KNOWN once it passes')
cut = src.index(MARK)
sys.argv = [tool] + args
ns = {'__name__': '__main__', '__file__': tool}
exec(compile(src[:cut], tool, 'exec'), ns)
X0, X1, Y0, Y1 = ns['X0'], ns['X1'], ns['Y0'], ns['Y1']


def means(path, t0, t1):
    """The chain's frames() + feat() + per-board means, N frames at a time from one ffmpeg process."""
    cmd = ['ffmpeg', '-v', 'error', '-ss', f'{t0:.2f}', '-i', path, '-t', f'{t1-t0:.2f}', '-r', '10', '-vf',
           f'crop={X1-X0+411}:{Y1-Y0}:{X0-411}:{Y0}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    w = X1 - X0 + 411; h = Y1 - Y0; fb = w * h * 3; W = X1 - X0
    r = {p: dict(o=[], w=[]) for p in ('p1', 'p2')}
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    while True:
        raw = pr.stdout.read(fb * chunk)
        n = len(raw) // fb
        if n:
            F = np.frombuffer(raw, np.uint8)[:n * fb].reshape(n, h, w, 3).astype(np.float32) / 255
            o, wm = ns['feat'](F)
            for p, xs in (('p1', slice(0, W)), ('p2', slice(411, 411 + W))):
                r[p]['o'] += o[:, :, xs].mean((1, 2)).round(3).tolist()
                r[p]['w'] += wm[:, :, xs].mean((1, 2)).round(3).tolist()
        if len(raw) < fb * chunk:
            break
    pr.stdout.close(); pr.wait()
    return r


G, A = ns['G'], ns['A']
out = {}
for gid in args:
    a = A[gid]; t0 = a['start_s'] - 0.5; t1 = a['end_s'] + 1.5
    out[gid] = dict(t0=t0, **means(G[gid]['path'], t0, t1)); print(gid, flush=True)
dest = f'R/pcban/{args[0]}.json'
text = json.dumps(out)
if check:
    exec(compile(src[cut:], tool, 'exec'), ns)   # the chain's own loop; it writes dest
    orig = open(dest).read()
    if orig != text:
        sys.exit(f'pcscan-chunked MISMATCH: {dest} differs from the chain\'s own output')
    print(f'pcscan-chunked check: {len(args)} games, {dest} identical to the chain\'s output', file=sys.stderr)
open(dest, 'w').write(text)
