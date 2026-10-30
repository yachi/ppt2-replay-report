import pickle,json,glob,collections,sys
P=json.load(open('R/part.json'))
def a_clears(ev):
  out=[];locks=[e for e in ev if e.get('kind')!='hold-empty']
  for i,e in enumerate(locks):
    if e.get('lines'):
      tn=locks[i+1]['t'] if i+1<len(locks) else e['t']+1
      out.append(dict(t=e['t'],tl=tn,lines=e['lines'],kind=e['kind'],pc=e['pc']))
  return out
def ingap(t,gaps): return any(g['t0']-0.3<=t<=g['t1']+0.3 for g in gaps)
stats=collections.Counter(); disp=[]
for f in sorted(glob.glob('R/ev/*.pkl')):
  gid=f.split('/')[-1][:4]
  if gid in P['trunc']: continue
  d=pickle.load(open(f,'rb'))
  for p in('p1','p2'):
    A=a_clears(d['a'][p]); Bc=d['b'][p]['clears']; gaps=d['b'][p]['gaps']
    used=set()
    for a in A:
      m=[j for j,b in enumerate(Bc) if j not in used and a['t']-0.2<=b['t']<=a['tl']+1.2]
      if m:
        j=m[0]; used.add(j); b=Bc[j]
        if b['lines']==a['lines'] and b['kind']==a['kind'] and b['pc']==a['pc']: stats['match']+=1
        else: stats['kinddiff']+=1; disp.append((gid,p,'kind',a,b))
      elif ingap(a['tl'],gaps): stats['A_in_Bgap']+=1
      else: stats['A_only_tracked']+=1; disp.append((gid,p,'A_only',a,None))
    for j,b in enumerate(Bc):
      if j not in used: stats['B_only']+=1; disp.append((gid,p,'B_only',None,b))
print(stats)
pickle.dump(disp,open('R/disp.pkl','wb'))
c=collections.Counter((x[2],(x[3] or {}).get('kind'),(x[4] or {}).get('kind')) for x in disp)
for k,v in c.most_common(40): print(v,k)
