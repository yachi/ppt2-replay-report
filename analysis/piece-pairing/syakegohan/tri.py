# per triple type: example real boards (distinct shapes, most common shape first)
import json, gzip, collections as C
rows=[json.loads(l) for l in gzip.open('uP_table.jsonl.gz','rt') if '"p": "p1"' in l]
MID=14; SW={'J':'L','L':'J','S':'Z','Z':'S'}
def adj(a,b):
    sa=set(map(tuple,a)); return any((r+dr,c+dc) in sa for r,c in b for dr,dc in((1,0),(-1,0),(0,1),(0,-1)))
def canon(ps):
    out=[]
    for m in(False,True):
        q=[((SW.get(t,t) if m else t),[(r,-c if m else c) for r,c in cs]) for t,cs in ps]
        allc=[x for _,cs in q for x in cs]; r0=min(r for r,_ in allc); c0=min(c for _,c in allc)
        out.append(tuple((t,tuple(sorted((r-r0,c-c0) for r,c in cs))) for t,cs in q))
    return min(out)
seq=C.defaultdict(dict)
for r in rows: seq[r['id']][r['i']]=r
ok=lambda A,B: A and A['i']>=MID and A['trusted'] and B['trusted'] and not A['lines'] and not B['garbage_before']
ex=C.defaultdict(list); mot=C.Counter(); n=0
for gid,s in seq.items():
    for i in sorted(s):
        B=s[i]; A=s.get(i-1); A2=s.get(i-2)
        if not(ok(A,B) and adj(A['cells'],B['cells']) and ok(A2,A) and adj(A2['cells'],A['cells']) and adj(A2['cells']+A['cells'],B['cells'])): continue
        n+=1; ps=[(A2['type'],A2['cells']),(A['type'],A['cells']),(B['type'],B['cells'])]
        ts=''.join(sorted(x for x,_ in ps)); k=canon(ps); mot[k]+=1
        ex[ts].append(dict(k=k,pre=A2['pre_hex'],pieces=[list(p) for p in ps],url=f"https://youtu.be/uP3FeprmAGI?t={int(A2['t'])-2}"))
out={}
for ts,L in sorted(ex.items(),key=lambda x:-len(x[1])):
    seen=set(); pick=[]
    for e in sorted(L,key=lambda e:-mot[e['k']]):
        if e['k'] in seen: continue
        seen.add(e['k']); pick.append({x:e[x] for x in('pre','pieces','url')})
        if len(pick)==3: break
    out[ts]=dict(n=len(L),examples=pick)
print(n, [(t,v['n']) for t,v in list(out.items())[:8]])
d=json.load(open('mid.json')); d['triple_type_examples']=out; json.dump(d,open('mid.json','w'),ensure_ascii=False,indent=1)
