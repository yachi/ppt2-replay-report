import json,pickle,collections
exec(open('R/banan.py').read())
P=json.load(open('R/part.json'))
A={j['id']:j for j in map(json.loads,open('A/games.jsonl'))}
B={j['id']:j for j in map(json.loads,open('B/games.jsonl'))}
def a_clears(ev):
  out=[];locks=[e for e in ev if e.get('kind')!='hold-empty']
  for i,e in enumerate(locks):
    if e.get('lines'):
      tn=locks[i+1]['t'] if i+1<len(locks) else e['t']+1
      out.append(dict(t=e['t'],tl=tn,lines=e['lines'],kind=e['kind'],pc=e['pc']))
  return out
R={}
for gid in sorted(A):
  z=np.load(f'R/ban/{gid}.npz'); d=pickle.load(open(f'R/ev/{gid}.pkl','rb'))
  for p in('p1','p2'):
    ts=tspins(z[p],float(z['t0'])); t0=float(z['t0'])
    tsacc=[e for e in ts if e['acc']]
    ac=a_clears(d['a'][p]); used=set(); res=collections.Counter(); unmatched=[]
    for e in tsacc:
      i=int(round((e['t']-t0)*30)); wd=max(['Single','Double','Triple'],key=lambda w:z[p+'_'+w][i:i+15].max()); wv=z[p+'_'+wd][i:i+15].max()
      m=[k for k,a in enumerate(ac) if k not in used and a['t']-0.1<=e['t']<=a['tl']+0.7]
      if m:
        k=m[-1]; used.add(k); L=ac[k]['lines']; e['A']=ac[k]['kind']
      else: L=None; unmatched.append(e)
      e['word']=(wd,round(float(wv),2)); e['L']=L
    # A tspin events without banner
    a_ts_nob=[a for k,a in enumerate(ac) if a['kind'] in('tss','tsd','tst','tsmini') and k not in used]
    R[(gid,p)]=dict(ts=tsacc,unmatched=unmatched,a_ts_nob=a_ts_nob,amb=sum(e['amb'] for e in tsacc))
pickle.dump(R,open('R/bancmp.pkl','wb'))
# summary: banner count vs A,B T-spin totals (full games only for B)
rows=[]
for (gid,p),r in R.items():
  nb=len(r['ts']); na=sum(A[gid][p]['clears'][k] for k in('tss','tsd','tst','tsmini')); nbB=sum(B[gid][p]['clears'][k] for k in('tss','tsd','tst','tsmini'))
  rows.append((gid,p,nb,na,nbB,len(r['unmatched']),len(r['a_ts_nob']),r['amb'],gid in P['trunc']))
import statistics
c=[r for r in rows if not r[8]]
print('comparable: banner==A',sum(r[2]==r[3] for r in c),'banner==B',sum(r[2]==r[4] for r in c),'of',len(c))
print('all: banner==A',sum(r[2]==r[3] for r in rows),len(rows))
print('sum banner',sum(r[2] for r in rows),'A',sum(r[3] for r in rows),'unmatched',sum(r[5] for r in rows),'A tspin w/o banner',sum(r[6] for r in rows),'amb',sum(r[7] for r in rows))
for r in rows[:30]: print(r)
