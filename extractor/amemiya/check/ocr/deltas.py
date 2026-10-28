import json,sys
def steps(seq):
    # seq list of (t,s,w); stable value = same for >=3 consecutive frames
    out=[];cur=None;run=0;prev=None
    for i,(t,s,w) in enumerate(seq):
        if s==prev: run+=1
        else: run=1;prev=s;tstart=t
        if run==3 and s.isdigit():
            v=int(s)
            if cur is None: cur=v; out.append((tstart,v,0))
            elif v!=cur: out.append((tstart,v,v-cur)); cur=v
    return out
for g in sys.argv[1:]:
    r=json.load(open(g+'.json'))
    for p,(si,wi) in (('p1',(1,2)),('p2',(3,4))):
        st=steps([(x[0],x[si],x[wi]) for x in r])
        print(g,p,' '.join(f"{t:.2f}:+{d}" for t,v,d in st if d>=60 or d<0), '| final',st[-1][1])
