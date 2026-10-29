# KO-tail check: score jumps in the last 1.5 s before KO with no chain clear near them.
import json,sys
sys.path.insert(0,'/home/user/ppt2-replay-report/extractor/amemiya/check/ocr')
from deltas3 import stable
def events(seq, th=60):
    st=stable(seq); ev=[]; cur=None
    for i,(t,v) in enumerate(st):
        if cur is None: cur=v; continue
        nxt=[w for _,w in st[i+1:i+4]]
        if v<cur-100 or v-cur>20000: continue
        if nxt and sum(abs(w-v)<200 or w>v for w in nxt)<len(nxt)/2: continue
        d=v-cur
        if d>=th: ev.append((round(t,2),d))
        if d>0 or d<-100: cur=v
        elif d<0: cur=max(cur,v)
    return ev
W='/tmp/claude-0/fr/won/chain/am/w'
J={j['id']:j for j in map(json.loads,open(f'{W}/A/games.jsonl'))}
S=json.load(open(f'{W}/tetrio/cseq.json'))
out=[]
for g in sorted(J):
    r=json.load(open(f'/tmp/claude-0/fr/ocr/tail/{g}.json')); end=J[g]['end_s']
    for p,si in (('p1',1),('p2',3)):
        jumps=[(t,d) for t,d in events([(x[0],x[si]) for x in r]) if end-1.5<t<=end+0.5]
        ch=[z[0] for z in S[f'{g} {p}'] if z[1] not in (None,'BREAK')]
        for t,d in jumps:
            if not any(abs(t-c)<=0.6 for c in ch):
                out.append(dict(id=g,player=p,t=t,score_jump=d,end=end,last_chain=max([c for c in ch if c<=t+0.6],default=None)))
json.dump(out,open('/tmp/claude-0/fr/corr/kotail.json','w'),indent=0)
print(len(out),'KO-tail spots');[print(o) for o in out]
