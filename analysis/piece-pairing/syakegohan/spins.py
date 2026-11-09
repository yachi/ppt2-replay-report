# non-T "spins": final placement not reachable by sliding/dropping in its final rotation (needs a rotation under the stack)
import json,gzip,collections as C
rows=[json.loads(l) for l in gzip.open('uP_table.jsonl.gz','rt')]
rows=[r for r in rows if r['p']=='p1']
def grid(h):
    b=bin(int(h,16))[2:].zfill(len(h)*4); return {(r,c) for r in range(len(b)//10) for c in range(10) if b[r*10+c]=='1'}
def slide_only(occ,cells):
    top=max(r for r,_ in occ) if occ else -1
    lift=max(top+2-min(r for r,_ in cells),0)+1
    start=(lift,0); seen={start}; st=[start]; ok=lambda d:all(0<=c+d[1]<10 and r+d[0]>=0 and (r+d[0],c+d[1]) not in occ for r,c in cells)
    # start: shifted up by lift at any column offset that fits
    st=[(lift,dc) for dc in range(-10,11) if ok((lift,dc))]; seen=set(st)
    while st:
        d=st.pop()
        if d==(0,0): return True
        for dd in((-1,0),(0,1),(0,-1)):
            n=(d[0]+dd[0],d[1]+dd[1])
            if n not in seen and ok(n): seen.add(n); st.append(n)
    return False
seq={(r['id'],r['i']):r for r in rows}
out=C.defaultdict(list); tot=C.Counter()
for r in rows:
    if r['type']=='T' or not r['trusted'] or r['i']<14 or r['garbage_before']: continue
    tot[r['type']]+=1
    occ=grid(r['pre_hex'])
    if slide_only(occ,[tuple(x) for x in r['cells']]): continue
    out[r['type']].append(dict(pre=r['pre_hex'],pieces=[[r['type'],r['cells']]],lines=r['lines'],url=f"https://youtu.be/uP3FeprmAGI?t={int(r['t'])-2}",key=r['key']))
print({t:(len(out[t]),tot[t]) for t in 'IJLOSZ'})
for t in 'IJLSZ': print(t,[ (e['key'],e['lines']) for e in out[t][:5]])
d=json.load(open('mid.json')); d['spins']={t:dict(n=len(out[t]),of=tot[t],lines=sum(e['lines']>0 for e in out[t]),examples=out[t]) for t in 'IJLOSZ'}
json.dump(d,open('mid.json','w'),ensure_ascii=False,indent=1)
