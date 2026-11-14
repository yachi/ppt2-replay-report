import json,collections
A={j['id']:j for j in map(json.loads,open('A/games.jsonl'))}
B={j['id']:j for j in map(json.loads,open('B/games.jsonl'))}
F=['pieces','lines_cleared','garbage_received_rows','garbage_cleared','max_combo','max_b2b','topped_out']
C=['single','double','triple','quad','tss','tsd','tst','tsmini','pc']
st=collections.defaultdict(lambda:[0,0,0,0]); diffs=collections.defaultdict(list)
nulls=[]
for g in sorted(A):
  a,b=A[g],B[g]
  da,db=a.get('duration_s'),b.get('duration_s')
  if da is None or db is None: nulls.append((g,'dur',da,db))
  else:
    d=abs(da-db); k='duration_s'
    st[k][0 if d<0.01 else 1 if d<=0.5 else 2]+=1; diffs[k].append(db-da)
  for p in ('p1','p2'):
    pa,pb=a.get(p) or {},b.get(p) or {}
    for f in F+['clears.'+c for c in C]:
      va=pa.get('clears',{}).get(f[7:]) if f.startswith('clears.') else pa.get(f)
      vb=pb.get('clears',{}).get(f[7:]) if f.startswith('clears.') else pb.get(f)
      if va is None or vb is None: st[f][3]+=1; continue
      if va==vb: st[f][0]+=1
      elif f not in('topped_out',) and abs(va-vb)<=max(1,0.03*max(va,vb)): st[f][1]+=1; diffs[f].append(vb-va)
      else: st[f][2]+=1; diffs[f].append(vb-va)
print('field equal within(±1/3%) disagree null meanB-A')
for f,v in st.items():
  d=diffs[f]; print(f,v, round(sum(d)/len(d),2) if d else 0)
print(nulls)
print('winner agree', sum(A[g]['winner']==B[g]['winner'] for g in A))
