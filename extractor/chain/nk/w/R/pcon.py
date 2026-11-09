import json,glob
def onsets(o,w,t0):
  pres=[(a>=0.08 and b>=0.15) for a,b in zip(o,w)]
  ev=[]
  for i in range(len(o)):
    if not pres[i]: continue
    newseg = i==0 or not pres[i-1]
    spike = w[i]>=0.33 and i>0 and w[i]-w[i-1]>=0.08
    if newseg or (spike and ev and t0+i/10-ev[-1]['t']>0.5):
      # segment length
      j=i
      while j<len(o) and pres[j]: j+=1
      ev.append(dict(t=round(t0+i/10,1),len=round((j-i)/10,1),w=w[i]))
  # merge: newseg right after a spike-onset within 0.3s is same banner
  return [e for e in ev]
PC={}
for f in sorted(glob.glob('R/pcban/*.json')):
  d=json.load(open(f))
  for g,r in d.items():
    for p in ('p1','p2'):
      PC[(g,p)]=onsets(r[p]['o'],r[p]['w'],r['t0'])
if __name__=='__main__':
  for k,v in sorted(PC.items()):
    if v: print(k,v)
  print(sum(len(v) for v in PC.values()))
