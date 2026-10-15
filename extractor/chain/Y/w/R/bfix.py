# YbMeCRhjG1k frame-adjudicated corrections to B's tracked clears inside A-dropout windows (see reconcile md).
# Reads R/ev_endfix/*.pkl (end-forced B), writes R/ev/*.pkl.
import pickle, glob, os
DROP = {('j008', 'p1', 1651.73): 'second TETRIS of a double-logged quad (one TETRIS banner at 1651.4, no PC)',
        ('j016', 'p1', 2791.33): 'quad 0.1 s after a single, no TETRIS banner, REN counter 9 unchanged',
        ('j033', 'p2', 4997.13): 'second quad 0.5 s after the first; one TETRIS banner, no I piece in hold/next'}
log = []
for f in sorted(glob.glob('R/ev_endfix/*.pkl')):
    g = os.path.basename(f)[:-4]; d = pickle.load(open(f, 'rb'))
    for p in ('p1', 'p2'):
        b = d['b'][p]; locks = [c for c in b['clears'] if c['src'] == 'lock']
        keep = []
        for c in b['clears']:
            k = (g, p, c['t'])
            if k in DROP:
                log.append((g, p, c['t'], c['kind'], 'dropped: ' + DROP[k]))
                if c['t'] in b['locks']: b['locks'].remove(c['t'])
                continue
            if c['src'] == 'orphan' and any(abs(l['t'] - c['t']) <= 0.1 and l['lines'] == c['lines'] for l in locks):
                log.append((g, p, c['t'], c['kind'], 'dropped: orphan clear duplicating a tracked lock clear at the same frame'))
                continue
            keep.append(c)
        b['clears'] = keep
    pickle.dump(d, open(f'R/ev/{g}.pkl', 'wb'))
for l in log: print(l)
