# [uP port, new file] seg.py, gamefilter.py import `track`, which is not archived in the repo.
# Board constants are B/sample.py's (and start/grid.py's) 15.7-px layout; coords() as in B/sample.py.
import numpy as np
W, H = 854, 480
X0 = {'p1': 142.5, 'p2': 554.0}; Y0 = 389.0; CW = 15.7
def coords(x0):
    xs = np.array([int(round(x0 + CW * (c + .5))) for c in range(10)])
    ys = np.array([int(round(Y0 - CW * (r + .5))) for r in range(20)])
    return xs, ys
