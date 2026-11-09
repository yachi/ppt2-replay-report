# syakegohan (p1, uP3FeprmAGI) pairs & triples of consecutive touching locks
# Inputs: /tmp/uP/uP_table.jsonl (= uP_table.jsonl.gz here) and /tmp/uP/uP_cf.jsonl (scratch, not committed: every legal placement per lock).
import json, sys, collections as C, numpy as np
rows=[json.loads(l) for l in open('/tmp/uP/uP_table.jsonl') if '"p": "p1"' in l]
cf={j['key']:j for j in map(json.loads,open('/tmp/uP/uP_cf.jsonl'))}
MID=int(sys.argv[1]); OUT=sys.argv[2]
SW={'J':'L','L':'J','S':'Z','Z':'S'}
def adj(a,b):
    sa=set(map(tuple,a)); return any((r+dr,c+dc) in sa for r,c in b for dr,dc in((1,0),(-1,0),(0,1),(0,-1)))
def canon(ps):
    out=[]
    for m in(False,True):
        q=[((SW.get(t,t) if m else t),[(r,-c if m else c) for r,c in cs]) for t,cs in ps]
        allc=[x for _,cs in q for x in cs]; r0=min(r for r,_ in allc); c0=min(c for _,c in allc)
        out.append(tuple((t,tuple(sorted((r-r0,c-c0) for r,c in cs))) for t,cs in q))
    return min(out)
def canon1(ps):
    allc=[x for _,cs in ps for x in cs]; r0=min(r for r,_ in allc); c0=min(c for _,c in allc)
    return tuple((t,tuple(sorted((r-r0,c-c0) for r,c in cs))) for t,cs in ps)
def draw(k):
    cells={}
    for j,(t,cs) in enumerate(k):
        for x in cs: cells[x]=t if j%2==0 else t.lower()
    R=max(r for r,_ in cells); c1=max(c for _,c in cells)
    return '\n'.join(''.join(cells.get((r,c),'.') for c in range(c1+1)) for r in range(R,-1,-1))
seq=C.defaultdict(dict)
for r in rows: seq[r['id']][r['i']]=r
pt=C.Counter(); pall=C.Counter(); pexp=C.Counter(); pmot=C.Counter(); board={}; tymot=C.Counter(); tyex=C.defaultdict(list); pex=C.defaultdict(list)
tset=C.Counter(); texp=C.Counter(); tmot=C.Counter(); tex=C.defaultdict(list); npair=0; ntouch=0; nwin=0; ntri=0
games=json.load(open('/private/tmp/claude-501/uP/w/chain/sy/games.json')); st={g['id']:g['start_s'] for g in games}
for gid,s in seq.items():
    for i in sorted(s):
        B=s[i]; A=s.get(i-1)
        ok=lambda A,B: A and A['i']>=MID and A['trusted'] and B['trusted'] and not A['lines'] and not B['garbage_before']
        if not ok(A,B): continue
        npair+=1; tk=''.join(sorted(A['type']+B['type'])); pall[tk]+=1
        c=cf.get(B['key'])
        if c: pexp[tk]+=np.mean([adj(A['cells'],q) for q in c['placements']])
        else: pexp[tk]+=0  # no counterfactual
        if not adj(A['cells'],B['cells']): continue
        ntouch+=1; pt[tk]+=1; k=canon([(A['type'],A['cells']),(B['type'],B['cells'])]); pmot[k]+=1
        bd=dict(pre=A['pre_hex'],pieces=[[A['type'],A['cells']],[B['type'],B['cells']]],url=f"https://youtu.be/uP3FeprmAGI?t={int(A['t'])-2}")
        board.setdefault(('p',k),bd)
        if len(pex[k])<3: pex[k].append(f"https://youtu.be/uP3FeprmAGI?t={int(A['t'])-2}")
        k1=canon1([(A['type'],A['cells']),(B['type'],B['cells'])]); tymot[k1]+=1
        board.setdefault(('y',k1),bd)
        if len(tyex[k1])<3: tyex[k1].append(f"https://youtu.be/uP3FeprmAGI?t={int(A['t'])-2}")
        A2=s.get(i-2)
        if A2 and ok(A2,A) and adj(A2['cells'],A['cells']):
            nwin+=1
            if adj(A2['cells']+A['cells'],B['cells']):
                ntri+=1; ts=''.join(sorted(A2['type']+A['type']+B['type'])); tset[ts]+=1
                k3=canon([(A2['type'],A2['cells']),(A['type'],A['cells']),(B['type'],B['cells'])]); tmot[k3]+=1
                board.setdefault(('t',k3),dict(pre=A2['pre_hex'],pieces=[[A2['type'],A2['cells']],[A['type'],A['cells']],[B['type'],B['cells']]],url=f"https://youtu.be/uP3FeprmAGI?t={int(A2['t'])-2}"))
                if len(tex[k3])<3: tex[k3].append(f"https://youtu.be/uP3FeprmAGI?t={int(A2['t'])-2}")
res=dict(mid=MID,pairs=npair,touch=ntouch,windows3=nwin,triples=ntri,
 pair_types=[[k,n,pall[k],round(n/pall[k],3),round(pexp[k]/pall[k],3)] for k,n in pt.most_common()],
 pair_motifs=[[draw(k),n,pex[k],board[('p',k)]] for k,n in pmot.most_common(15)],
 type_motifs={tk:[[draw(k),n,tyex[k],board[('y',k)]] for k,n in tymot.most_common() if ''.join(sorted(t for t,_ in k))==tk][:3] for tk in pt},
 triple_types=tset.most_common(15),
 triple_motifs=[[draw(k),n,tex[k],board[('t',k)]] for k,n in tmot.most_common(12)])
json.dump(res,open(OUT,'w'),ensure_ascii=False,indent=1)
print({k:v for k,v in res.items() if not isinstance(v,list)})
for x in res['pair_types'][:15]: print(x)
for d,n,e,*_ in res['pair_motifs'][:12]: print(n,e[0]); print(d); print()
print(res['triple_types'])
for d,n,e,*_ in res['triple_motifs'][:10]: print(n,e[0]); print(d); print()
