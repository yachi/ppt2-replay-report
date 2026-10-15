import numpy as np, sys
d=np.load(sys.argv[1]); p=int(sys.argv[2]); a=float(sys.argv[3]); z=float(sys.argv[4]); K=int(sys.argv[5])
t0=float(d['t0']); g=d['grid'][:,p]
P='.GZLOSIJTW?'
i0=int((a-t0)*30); i1=int((z-t0)*30); prev=None
for i in range(i0,i1):
    if not np.all(g[i:i+K]==g[i]): continue
    key=g[i].tobytes()
    if key==prev: continue
    prev=key
    gg=g[i]; top=max([r for r in range(20) if (gg[r]>0).any()],default=-1)
    rows=[''.join(P[x] for x in gg[r]) for r in range(top,-1,-1)]
    print(f'{t0+i/30:6.2f} n={(gg>0).sum():3d} nxt={"".join(P[x] for x in d["nxt"][i,p])} | '+' / '.join(rows))
