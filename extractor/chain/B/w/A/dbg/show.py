import numpy as np, sys
d=np.load(sys.argv[1]); p=int(sys.argv[2]); a=float(sys.argv[3]); z=float(sys.argv[4]); K=int(sys.argv[5]) if len(sys.argv)>5 else 1
t0=float(d['t0']); g=d['grid'][:,p]; v=d['val'][:,p]
P='.GZLOSIJT'
i0=int((a-t0)*30); i1=int((z-t0)*30); prev=None
for i in range(i0,i1):
    ok=np.all(g[i:i+K]==g[i],axis=0)
    gg=np.where(ok,g[i],255)
    key=gg.tobytes()
    if key==prev: continue
    prev=key
    top=max([r for r in range(20) if (gg[r]>0).any()],default=-1)
    print(f'--- {t0+i/30:.2f} i={i} n={(g[i]>0).sum()} nxt={"".join(P[x] for x in d["nxt"][i,p])}')
    for r in range(top,-1,-1): print(''.join(P[x] if x<9 else '?' for x in gg[r]), ' '.join(f'{x:3d}' for x in v[i,r]) if '-v' in sys.argv else '')
