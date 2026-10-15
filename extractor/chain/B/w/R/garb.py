import json,pickle,numpy as np,collections
exec(open('R/fuse.py').read().split("if __name__")[0])
B={j['id']:j for j in map(json.loads,open('B/games.jsonl'))}
P=json.load(open('R/part.json')); bag=json.load(open('R/bag.json')); gaps=json.load(open('R/gaps.json'))
F=pickle.load(open('R/fuse.pkl','rb'))
rows=[]
for gid in sorted(A):
  w=A[gid]['winner']; p=w
  if gid in P['trunc']: continue
  if bag[gid][p]['bad_bags'] or gaps[gid][p]['big'] or gaps[gid][p]['tail']>2.5: continue
  d=np.load(f'A/feat/{gid}.npz'); t0=float(d['t0'])
  ef=int(round((A[gid]['end_s']-t0)*30))-6
  pi=0 if p=='p1' else 1
  g=d['grid'][ef-10:ef,pi]           # codes
  occ=np.median(((g!=0)&(g!=10)).sum(axis=(1,2)))
  c,lines,seq=kinds(F[(gid,p)]['evs'],F[(gid,p)]['extra'])
  P_=A[gid][p]['pieces']+1   # +1 active piece visible at end
  Gid=(occ-4*P_+10*lines)/9
  rows.append((gid,p,round(Gid,1),A[gid][p]['garbage_received_rows'],B[gid][p]['garbage_received_rows'],lines,A[gid][p]['lines_cleared'],B[gid][p]['lines_cleared']))
ea=[abs(r[2]-r[3]) for r in rows]; eb=[abs(r[2]-r[4]) for r in rows]
print(len(rows),'median |Gid-A|',np.median(ea),'|Gid-B|',np.median(eb),'A closer',sum(a<b for a,b in zip(ea,eb)),'B closer',sum(b<a for a,b in zip(ea,eb)))
for r in rows[:25]: print(r)
