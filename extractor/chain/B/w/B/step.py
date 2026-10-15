import sys, json, numpy as np
import extract_b as X
L='.GZLOSIJT?'
gid,p,a,b,rows=sys.argv[1],int(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5])
g={x['id']:x for x in json.load(open('/private/tmp/claude-501/sk/games.json'))}[gid]
z=np.load(f'cells2/{gid}.npz'); t0=float(z['t0'])
cls=X.classify(z['cells'][:,p])
def tr(i,B,Qc,sol):
    t=t0+i/30
    if t<a: return
    desc='NOOP' if sol==[] else ('NONE' if sol is None else [ (o['op'], o.get('rows') or o.get('g') or X.shape_of(o.get('piece') or [])) for o in sol[2]])
    print('t=%.2f'%t, desc)
    for row in range(rows,-1,-1): print(''.join('#' if x else '.' for x in B[row]),'  ',''.join(L[x] for x in Qc[row]))
X.analyze_player(cls,int((g['start_s']-t0)*30),int((b-t0)*30),trace=tr)
