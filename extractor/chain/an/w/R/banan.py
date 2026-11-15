import numpy as np,json,pickle,glob,collections,sys
def onsets(s,t0):
  n=len(s); on=s>0.55
  # fill short dips (<=5 frames) to get segments
  seg=on.copy(); i=0
  idx=np.nonzero(on)[0]
  for a,b in zip(idx[:-1],idx[1:]):
    if 1<b-a<=6: seg[a:b]=True
  # candidate onsets: s low (<0.45) then high (>0.6) within 3 frames
  cands=[]
  for i in range(1,n-3):
    if s[i-1]<0.45 and max(s[i:i+4])>0.6: cands.append(i)
  # dedupe
  c2=[]
  for c in cands:
    if not c2 or c-c2[-1]>6: c2.append(c)
  # segment end for each candidate
  ev=[]
  for c in c2:
    st=c
    while st<min(n,c+4) and s[st]<=0.6: st+=1
    seg[st:min(n,st+1)]=True
    j=st
    while j<n and seg[j]: j+=1
    life=(j-st)/30
    ev.append(dict(t=round(t0+c/30,2),life=round(life,2)))
  return ev
def tspins(s,t0,thr=1.15):
  ev=onsets(s,t0); out=[]
  for k,e in enumerate(ev):
    acc=e['life']>=thr
    nx=[f for f in ev[k+1:] if f['t']-e['t']<thr and f['life']>=thr]
    amb= acc and bool(nx)
    e.update(acc=acc,amb=amb); out.append(e)
  return out
