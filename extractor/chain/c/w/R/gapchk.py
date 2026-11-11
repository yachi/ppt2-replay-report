import json,sys
sys.argv=['x']
exec(open('R/events.py').read().split("if __name__")[0])
import numpy as np
out={}
for gid in sorted(G):
  d=np.load(f'A/feat/{gid}.npz'); meta=G[gid]; FPS=30.0; t0=float(d['t0'])
  lo=max(0,int(round((meta['start_s']-0.3-t0)*FPS))); hi=len(d['grid'])
  s0=[]
  for p in (0,1):
    sp,_,_=Am.spawns(d['nxt'][:,p],lo,hi)
    if sp: s0.append(sp[0])
  start=min(s0); end,loser=Am.find_end(d['border'],start+60,hi); end_f=end if end is not None else hi
  r={}
  for p in (0,1):
    sp,seq,anom=Am.spawns(d['nxt'][:,p],start-2,end_f)
    gaps=[(sp[i+1]-sp[i])/30 for i in range(len(sp)-1)]
    big=[(round(t0+sp[i]/30,2),round(g,2)) for i,g in enumerate(gaps) if g>2.5]
    tail=(end_f-sp[-1])/30 if sp else None
    r['p%d'%(p+1)]=dict(big=big,tail=round(tail,2),head=round((sp[0]-start)/30,2) if sp else None)
  out[gid]=r
json.dump(out,open('R/gaps.json','w'))
for g in out:
  for p in out[g]:
    x=out[g][p]
    if x['big'] or x['tail']>2.5 or x['head']>1: print(g,p,x)
