"""Self-check without a video: the Rust series against banscan.py's numpy series on synthetic frames.
Integer-valued float32 frames (as ffmpeg rgb24 gives), random templates of banscan's sizes, plus constant
frames (all-zero scores: argmax must be the first window) and a frame with a repeated pattern (ties).
Then plants two defects and requires the comparison to catch each."""
import os, sys, numpy as np
from numpy.lib.stride_tricks import sliding_window_view as sw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fast
Y0 = 306


def series(F, t, x, y):  # verbatim from extractor/chain/te/w/R/banscan.py
  h,w=t.shape[:2]; tt=t-t.mean(); tn=np.sqrt((tt*tt).sum())
  ys=slice(y-3-Y0,y+3-Y0+h); xs=slice(x-4,x+4+w)
  R=F[:,ys,xs,:]
  W=sw(R,(h,w),axis=(1,2))
  W=W-W.mean(axis=(3,4,5),keepdims=True)
  num=(W*tt.transpose(2,0,1)[None,None,None]).sum(axis=(3,4,5))
  den=np.sqrt((W*W).sum(axis=(3,4,5)))*tn+1e-6
  S=num/den; n=S.shape[0]; flat=S.reshape(n,-1); k=flat.argmax(1)
  return flat.max(1),k


def same(a, b):
    return np.array_equal(a[0].view(np.uint32), b[0].view(np.uint32)) and np.array_equal(a[1], b[1])


rng = np.random.default_rng(1)
F = rng.integers(0, 256, (300, 46, 854, 3)).astype(np.float32)
F[10:20] = 7.0                                   # constant: every score 0, argmax 0
F[20:30] = np.tile(rng.integers(0, 256, (46, 2, 3)), (1, 427, 1))[None]  # period 2 in x: tied windows
src = rng.integers(0, 256, (480, 854, 3)).astype(np.float32)
cases = [(14, 29, 482, 322), (14, 29, 70, 322), (13, 20, 473, 325), (16, 35, 511, 320), (16, 35, 99, 320)]
n = 0
for h, w, x, y in cases:
    t = src[y:y + h, x:x + w]                    # a non-contiguous slice, as tpl() returns
    a = fast.series(F, t, x, y, Y0); b = series(F, t, x, y)
    assert same(a, b), (h, w, x, y)
    assert (b[1][10:20] == 0).all()
    n += 1
    tc = t.copy(); tc[2, 3, 1] = 255 - tc[2, 3, 1]   # the template as the series must not see it
    assert not same(fast.series(F, tc, x, y, Y0), b), 'template mutant survived'
fast.THREADS = 1
assert same(fast.series(F, src[322:336, 482:511], 482, 322, Y0), series(F, src[322:336, 482:511], 482, 322)), 'threads=1'
bad = fast.series(F, src[322:336, 482:511], 482, 322, Y0); bad[0][5] = np.nextafter(bad[0][5], np.float32(9))
assert not same(bad, series(F, src[322:336, 482:511], 482, 322)), '1-ulp mutant survived'
print(f'banscan-rs check: {n} templates x {len(F)} frames identical; 1-ulp and template mutants caught')
