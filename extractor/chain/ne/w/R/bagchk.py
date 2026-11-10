import json,sys,time
sys.argv=['x']
exec(open('R/events.py').read().split("if __name__")[0])
import numpy as np
out={}
ids=sorted(G)
t=time.time()
for k,gid in enumerate(ids):
  d=np.load(f'A/feat/{gid}.npz'); meta=G[gid]; FPS=30.0
  lo=max(0,int(round((meta['start_s']-0.3-float(d['t0']))*FPS))); hi=len(d['grid'])
  s0=[]
  for p in (0,1):
    sp,_,_=Am.spawns(d['nxt'][:,p],lo,hi)
    if sp: s0.append(sp[0])
  start=min(s0); end,loser=Am.find_end(d['border'],start+60,hi); end_f=end if end is not None else hi
  r={}
  for p in (0,1):
    sp,seq,anom=Am.spawns(d['nxt'][:,p],start-2,end_f)
    s=''.join(Am.NAMES[x] for x in seq)
    bad=[i for i in range(0,len(s)-6,7) if len(set(s[i:i+7]))!=7]
    full=(len(s))//7
    r['p%d'%(p+1)]=dict(seq=s,nspawn=len(sp),bad_bags=bad,nbags=full,anom=anom)
  out[gid]=r
  print(k+1,'/',len(ids),gid,round(time.time()-t,1),flush=True)
json.dump(out,open('R/bag.json','w'))
