import sys,json,numpy as np
exec(open('R/banner.py').read().split('if __name__')[0])
A={j['id']:j for j in map(json.loads,open('A/games.jsonl'))}
MINI=None   # [aj] set below: p1 only; p2's 'Mini' is under the camera box, so p2_Mini is all zeros (no mini from the banner)
exec(open('R/mini_aj.py').read())
from numpy.lib.stride_tricks import sliding_window_view as sw
def series(F,t,x,y):
  h,w=t.shape[:2]; tt=t-t.mean(); tn=np.sqrt((tt*tt).sum())
  ys=slice(y-3-Y0,y+3-Y0+h); xs=slice(x-4,x+4+w)
  R=F[:,ys,xs,:]                          # n,h+6,w+8,3
  W=sw(R,(h,w),axis=(1,2))                # n,7,9,3,h,w
  W=W-W.mean(axis=(3,4,5),keepdims=True)
  num=(W*tt.transpose(2,0,1)[None,None,None]).sum(axis=(3,4,5))
  den=np.sqrt((W*W).sum(axis=(3,4,5)))*tn+1e-6
  S=num/den; n=S.shape[0]; flat=S.reshape(n,-1); k=flat.argmax(1)
  return flat.max(1),k
for gid in sys.argv[1:]:
  g=G[gid]; t0=A[gid]['start_s']-0.5; t1=(A[gid]['end_s'] or g['end_upper_s'])+0.5
  res={}
  chunk=20.0; tt=t0; parts={p:[] for p in('p1','p2')}; mparts={p:[] for p in('p1','p2')}; wparts={p:{k:[] for k in WORDS} for p in('p1','p2')}
  while tt<t1:
    F=strip(g['path'],tt,min(t1,tt+chunk))
    for p in ('p1','p2'):
      s,k=series(F,T_SPIN_P[p],SPX[p],SPY); parts[p].append(s)
      ms=np.zeros(len(F),np.float32); mparts[p].append(ms)   # [aj] no Mini template (R/mini_aj.py)
      for wn,wt in WORDS_P[p].items():   # [nk] per-side word templates
        ws,_=series(F,wt,WX[p],WY); wparts[p][wn].append(ws)
    tt+=chunk
  # [aj] p2's spin template is only 'IN' (11 px, the rest is under the camera box), and a one-frame clear flash can
  # score 0.6 on it, which banan.py reads as a second onset: p2's series is the min over two consecutive frames.
  q=np.concatenate(parts['p2']); parts['p2']=[np.minimum(q,np.append(q[1:],q[-1:]))]
  np.savez(f'R/ban/{gid}.npz',t0=t0,**{p:np.concatenate(parts[p]) for p in parts},**{p+'_Mini':np.concatenate(mparts[p]) for p in parts},**{p+'_'+w:np.concatenate(wparts[p][w]) for p in wparts for w in WORDS})
  print('done',gid,flush=True)
