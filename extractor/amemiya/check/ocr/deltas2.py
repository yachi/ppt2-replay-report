import json,sys
def stable(seq):
    out=[];prev=None;run=0
    for t,s in seq:
        if s==prev: run+=1
        else: run=1;prev=s;ts=t
        if run==3 and s.isdigit(): out.append((ts,int(s)))
    return out
def events(seq,merge=0.5):
    st=stable(seq);cur=None;ev=[]
    for i,(t,v) in enumerate(st):
        if cur is None: cur=v;continue
        if v<=cur or v-cur>20000: continue
        # require confirmation: next stable reading not below v (glitch filter)
        nxt=[w for _,w in st[i+1:i+3]]
        if nxt and all(w<v for w in nxt): continue
        d=v-cur;cur=v
        if ev and t-ev[-1][2]<=merge: ev[-1][1]+=d;ev[-1][2]=t
        else: ev.append([t,d,t])
    return [(round(a,2),d) for a,d,_ in ev]
if __name__=='__main__':
    for g in sys.argv[1:]:
        r=json.load(open(g+'.json'))
        for p,si in (('p1',1),('p2',3)):
            e=events([(x[0],x[si]) for x in r])
            print(g,p,' '.join(f"{t}:{d}" for t,d in e if d>=200))
