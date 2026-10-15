# Extractor B, stage 2: cell-accounting event solver.
import numpy as np, sys, json, itertools
from collections import Counter
LETTERS='.GZLOSIJT'   # 0 empty, 1 grey garbage, 2.. piece colours
def hsv(rgb):
    rgb=rgb.astype(float)/255; mx=rgb.max(-1); mn=rgb.min(-1); d=mx-mn
    s=np.where(mx>0,d/np.maximum(mx,1e-9),0); r,g,b=rgb[...,0],rgb[...,1],rgb[...,2]
    dd=np.maximum(d,1e-9)
    h=np.where(mx==r,((g-b)/dd)%6,np.where(mx==g,(b-r)/dd+2,(r-g)/dd+4))*60
    return h,s,mx
def classify(rgb):
    h,s,v=hsv(rgb)
    c=np.full(h.shape,8,np.int8)              # T 250-330
    c[h<250]=7; c[h<200]=6; c[h<150]=5; c[h<70]=4; c[h<35]=3
    c[(h<12)|(h>=330)]=2
    c[s<0.25]=1
    c[v<0.38]=0
    c[(s<0.25)&(v<0.65)]=0                    # dim grey = glow / effects, not a block
    return c
def debounce(cls,k):
    """per-cell debounced class: a cell takes a new class only after it has held it for k frames"""
    n=len(cls); out=np.zeros_like(cls); cur=cls[0].copy(); run=np.ones(cls.shape[1:],int); prev=cls[0].copy()
    for i in range(n):
        x=cls[i]
        same=(x==prev); run=np.where(same,run+1,1); prev=x
        # occupancy change requires k frames; colour change between occupied classes also k frames
        upd=run>=k
        cur=np.where(upd,x,cur)
        out[i]=cur
    return out
def full_rows(occ): return [r for r in range(20) if occ[r].all()]
def components(mask):
    seen=np.zeros_like(mask,bool); comps=[]
    for r in range(20):
        for c in range(10):
            if mask[r,c] and not seen[r,c]:
                st=[(r,c)]; seen[r,c]=True; comp=[]
                while st:
                    a,b=st.pop(); comp.append((a,b))
                    for da,db in ((1,0),(-1,0),(0,1),(0,-1)):
                        x,y=a+da,b+db
                        if 0<=x<20 and 0<=y<10 and mask[x,y] and not seen[x,y]:
                            seen[x,y]=True; st.append((x,y))
                comps.append(comp)
    return comps
def solve(Bo,Bc,Qc,maxg=12):
    """Bo: belief occupancy (20x10 bool), Bc: belief origin (0 empty,1 garbage,2 piece); Qc: snapshot classes.
    returns best (cost, info)"""
    Qo=Qc>0
    cnt=Bo.sum(1)
    cand=[r for r in range(20) if cnt[r]>=4]
    best=None
    for nc in range(0,5):
        for C in itertools.combinations(cand,nc):
            Cs=set(C); fill=sum(10-cnt[r] for r in C)
            if nc and fill>4*2: continue
            # mapping without garbage
            keep=[r for r in range(20) if r not in Cs]
            for g in range(0,maxg+1):
                M=np.zeros((20,10),bool); Mo=np.zeros((20,10),np.int8)
                for i,r in enumerate(keep):
                    nr=i+g
                    if nr<20: M[nr]=Bo[r]; Mo[nr]=Bc[r]
                # rows lost off the top with content -> topout, heavy cost
                over=sum(Bo[r].sum() for i,r in enumerate(keep) if i+g>=20)
                cost=over*5.0
                gcost=0
                for r in range(g):
                    k=Qo[r].sum(); gcost+=abs(k-9)*2+ (0 if (Qc[r][Qo[r]]==1).mean()>0.7 else 3) if k else 20
                cost+=gcost
                lost=(M&~Qo); lost[:g]=False
                add=(Qo&~M); add[:g]=False
                cost+=lost.sum()*3
                # floating groups among added cells = active piece, ignored
                fl=np.zeros((20,10),bool)
                for comp in components(add):
                    sup=False
                    cols=set(Qc[a,b] for a,b in comp)
                    for a,b in comp:
                        if a==0 or (M[a-1,b] or (add[a-1,b] and (a-1,b) not in comp)): sup=True;break
                    if not sup and len(comp)<=4: 
                        for a,b in comp: fl[a,b]=True
                addp=add&~fl
                N=int(addp.sum())+fill
                m=N%4; cost+=min(m,4-m)*2.5
                if nc and N==0: cost+=6
                cost+=0.01*(nc+g)+0.001*N
                if best is None or cost<best[0]:
                    best=(cost,dict(C=list(C),g=g,N=N,lost=int(lost.sum()),M=M,Mo=Mo,add=addp,fl=fl,fill=fill,gcost=gcost))
    return best
def run(gid,pl,k=5,t_from=None,t_to=None,verbose=False):
    z=np.load(f'/private/tmp/claude-501/sk/metrics/B/cells/{gid}.npz'); cells=z['cells'][:,pl]; t0=float(z['t0'])
    cls=np.stack([classify(f) for f in cells])
    db=debounce(cls,k)
    i0=0 if t_from is None else max(0,int((t_from-t0)*30)); i1=len(db) if t_to is None else min(len(db),int((t_to-t0)*30))
    Bo=np.zeros((20,10),bool); Bc=np.zeros((20,10),np.int8); Bcol=np.zeros((20,10),np.int8)
    events=[]; last=None
    for i in range(i0,i1):
        Q=db[i]; key=Q.tobytes()
        if key==last: continue
        last=key
        cost,info=solve(Bo,Bc,Q)
        if not info['C'] and info['g']==0 and info['N']==0 and info['lost']==0: continue
        ev=dict(f=i,t=round(t0+i/30,3),cost=round(cost,2),C=info['C'],g=info['g'],N=info['N'],lost=info['lost'])
        if cost>=3:   # unexplained: skip this snapshot, wait for a later one
            ev['rejected']=True; events.append(ev)
            if verbose: print('REJ',ev)
            continue
        # pre-clear board with new piece: piece cells in pre-mapping coordinates
        keep=[r for r in range(20) if r not in set(info['C'])]
        inv={i2+info['g']:r for i2,r in enumerate(keep)}
        piece=[]
        for a,b in zip(*np.nonzero(info['add'])):
            if a in inv: piece.append((inv[a],b,int(Q[a,b])))
        for r in info['C']:
            for b in range(10):
                if not Bo[r,b]: piece.append((r,b,-1))
        ev['piece']=piece
        ev['garbage_rows_cleared']=sum(1 for r in info['C'] if (Bc[r]==1).sum()>=6)
        ev['pre']=Bo.copy()
        # update belief
        nBo=info['M'].copy(); nBc=info['Mo'].copy()
        for r in range(info['g']):
            nBo[r]=Q[r]>0; nBc[r]=np.where(Q[r]>0,1,0)
        nBo|=info['add']; nBc[info['add']]=2
        nBcol=np.where(nBo,Q,0)
        ev['post']=nBo.copy(); ev['postcol']=nBcol.copy()
        Bo,Bc=nBo,nBc
        events.append(ev)
        if verbose:
            print({k2:v for k2,v in ev.items() if k2 not in('pre','post','postcol')})
    return events,t0,db
if __name__=='__main__':
    gid,pl,a,b=sys.argv[1],int(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])
    run(gid,pl,t_from=a,t_to=b,verbose=True)
