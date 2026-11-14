"""ctypes wrapper for the Rust NCC series. series(F,t,x,y,Y0) returns what a chain's R/banscan.py series() returns,
bit for bit: (max per frame, float32) and (first argmax per frame, int64)."""
import ctypes, os, subprocess, numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, 'target', 'release', 'libbanscan_ncc.so')


def _stale():
    if not os.path.exists(LIB):
        return True
    t = os.path.getmtime(LIB)
    srcs = [os.path.join(HERE, 'Cargo.toml')] + [os.path.join(HERE, 'src', f) for f in os.listdir(os.path.join(HERE, 'src'))]
    return any(os.path.getmtime(s) > t for s in srcs)


def _load():
    if _stale():
        subprocess.run(['cargo', 'build', '--release', '--quiet'], cwd=HERE, check=True)
    lib = ctypes.CDLL(LIB)
    P = ctypes.c_void_p
    lib.ncc_series.argtypes = [P, ctypes.c_size_t, ctypes.c_size_t, ctypes.c_size_t, P, ctypes.c_size_t, ctypes.c_size_t,
                               ctypes.c_float, ctypes.c_int64, ctypes.c_int64, P, P, ctypes.c_size_t]
    lib.ncc_series.restype = ctypes.c_int
    return lib


_lib = None
THREADS = int(os.environ.get('BANSCAN_THREADS', os.cpu_count() or 1))


def series(F, t, x, y, Y0):
    global _lib
    if _lib is None:
        _lib = _load()
    # the template half exactly as banscan.py computes it, in numpy
    h, w = t.shape[:2]; tt = t - t.mean(); tn = np.sqrt((tt * tt).sum())
    if F.dtype != np.float32 or tt.dtype != np.float32 or np.asarray(tn).dtype != np.float32:
        raise TypeError('banscan-rs reproduces the float32 path only')
    F = np.ascontiguousarray(F); tt = np.ascontiguousarray(tt)
    n = F.shape[0]
    mx = np.empty(n, np.float32); k = np.empty(n, np.int64)
    rc = _lib.ncc_series(F.ctypes.data, n, F.shape[1], F.shape[2], tt.ctypes.data, h, w, float(tn),
                         y - 3 - Y0, x - 4, mx.ctypes.data, k.ctypes.data, THREADS)
    if rc:
        raise ValueError(f'ncc_series rc={rc} (window outside the frame or bad shape)')
    return mx, k
