"""Run a chain's R/banscan.py with series() computed in Rust. The chain's file is read, never edited.

    cd <chain work dir>; python3 <repo>/extractor/banscan-rs/run_banscan.py [--check] GID...

--check also runs the chain's own numpy series() on every call and stops unless both arrays are identical
(max compared bit for bit, argmax exactly)."""
import os, sys, time, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fast

check = '--check' in sys.argv
sys.argv = [a for a in sys.argv if a != '--check']
src = open('R/banscan.py').read()
cut = src.index('for gid in')
g = {'__name__': '__banscan__'}
exec(compile(src[:cut], 'R/banscan.py', 'exec'), g)
numpy_series = g['series']
stats = {'calls': 0, 'frames': 0, 't_rs': 0.0, 't_np': 0.0}


def series(F, t, x, y):
    t0 = time.perf_counter(); m, k = fast.series(F, t, x, y, g['Y0']); stats['t_rs'] += time.perf_counter() - t0
    stats['calls'] += 1; stats['frames'] += len(m)
    if check:
        t0 = time.perf_counter(); m2, k2 = numpy_series(F, t, x, y); stats['t_np'] += time.perf_counter() - t0
        if m.dtype != m2.dtype or not np.array_equal(m.view(np.uint32), m2.view(np.uint32)) or not np.array_equal(k, k2):
            bad = np.flatnonzero((m.view(np.uint32) != m2.view(np.uint32)) | (k != k2))
            sys.exit(f'banscan-rs MISMATCH at x={x} y={y}: frames {bad[:10].tolist()} rs={m[bad[:3]]} np={m2[bad[:3]]}')
    return m, k


g['series'] = series
exec(compile(src[cut:], 'R/banscan.py', 'exec'), g)
print('banscan-rs:', stats['calls'], 'calls,', stats['frames'], 'frames, rust %.1fs' % stats['t_rs'],
      (', numpy %.1fs, all identical' % stats['t_np']) if check else '', flush=True)
