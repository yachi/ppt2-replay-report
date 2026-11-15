import pickle,json
exec(open('R/pcon.py').read().split("if __name__")[0])
S=pickle.load(open('tetrio/seqs.pkl','rb'))
PCS={}
for k,v in PC.items():
  longs=[]
  for e in v:
    if e['len']>=0.9 and not any(0<e['t']-l<=1.5 for l in longs): longs.append(e['t'])
  if longs: PCS[k]=longs
out={}
for k in sorted(PCS):
  if k not in S: print('noseq',k); continue
  seq=[z for z in S[k]['seq'] if z[1] not in (None,'BREAK')]
  for b in PCS[k]:
    near=[(z[0],z[1],z[2],z[5]) for z in seq if b-2.0<=z[0]<=b+0.3]
    print(k,b,near)
json.dump({f'{k[0]}|{k[1]}':v for k,v in PCS.items()},open('../pcs.json','w'))
print(sum(len(v) for v in PCS.values()),'PCs')
# --- PCDEC: PC = clear nearest (banner-0.2) at or before banner+0.2; drop same-lines clears <=0.6 s before it
# and any clear <=0.5 s after it (the board is empty after a PC, so these are A's double-logged flash).
DEC={}
for k in sorted(PCS):
  seq=[z for z in S[k]['seq'] if z[1] not in (None,'BREAK')]
  for b in PCS[k]:
    c=[z for z in seq if b-2.0<=z[0]<=b+0.2]
    if not c: print('NO CLEAR',k,b); continue
    pc=min(c,key=lambda z:abs(z[0]-(b-0.2)))
    drops=[z[0] for z in seq if (0<pc[0]-z[0]<=0.65 and z[2]==pc[2]) or 0<z[0]-pc[0]<=0.5]
    DEC.setdefault(k,[]).append((pc[0],drops))
for k,v in DEC.items(): print(k,v)
json.dump([[k[0],k[1],v] for k,v in DEC.items()],open('../pcdec.json','w'))
