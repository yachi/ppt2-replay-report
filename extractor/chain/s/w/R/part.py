import json,collections
A={j['id']:j for j in map(json.loads,open('A/games.jsonl'))}
B={j['id']:j for j in map(json.loads,open('B/games.jsonl'))}
G={g['id']:g for g in json.load(open('../games.json'))}
trunc=[g for g in A if B[g]['duration_s']<A[g]['duration_s']-1.5]
late=[g for g in A if A[g]['start_s']-G[g]['start_s']>1.2]
comp=[g for g in sorted(A) if g not in trunc]
print('trunc',len(trunc),trunc); print('lateA',late)
F=['pieces','lines_cleared','garbage_received_rows','garbage_cleared','max_combo','max_b2b','topped_out']
C=['single','double','triple','quad','tss','tsd','tst','tsmini','pc']
st=collections.defaultdict(lambda:[0,0,0]);dd=collections.defaultdict(list)
for g in comp:
  for p in('p1','p2'):
    for f in F+['clears.'+c for c in C]:
      va=A[g][p]['clears'][f[7:]] if f[:7]=='clears.' else A[g][p][f]
      vb=B[g][p]['clears'][f[7:]] if f[:7]=='clears.' else B[g][p][f]
      if va==vb: st[f][0]+=1
      elif f!='topped_out' and abs(va-vb)<=max(1,0.05*max(va,vb)): st[f][1]+=1
      else: st[f][2]+=1
      if f!='topped_out': dd[f].append(vb-va)
for f in st: d=dd[f]; print(f, st[f], 'meanB-A', round(sum(d)/max(1,len(d)),2))
# internal consistency: lines = sum by type
def lines_typed(c): return c['single']+c['tss']+c['tsmini']+2*(c['double']+c['tsd'])+3*(c['triple']+c['tst'])+4*c['quad']
for X,n in ((A,'A'),(B,'B')):
  r=[X[g][p]['lines_cleared']-lines_typed(X[g][p]['clears']) for g in comp for p in('p1','p2')]
  print(n,'lines - typed lines: mean',sum(r)/len(r),'min',min(r),'max',max(r))
# big piece disagreements
for g in comp:
  for p in('p1','p2'):
    a,b=A[g][p]['pieces'],B[g][p]['pieces']
    if abs(a-b)>0.1*max(a,b): print(g,p,a,b,'Abag',A[g][p]['qa']['bag'],'Aid',A[g][p]['qa']['identity_ok'],A[g][p]['qa']['identity_n'],'Btr',B[g][p]['tracked_pieces'],B[g][p]['resyncs'],G[g]['video'])
json.dump({'trunc':trunc,'late':late,'comp':comp},open('R/part.json','w'))
