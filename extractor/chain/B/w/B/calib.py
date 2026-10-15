# Calibrate the gap estimator on stretches the tracker followed exactly.
import json, numpy as np, sys
import extract_b as X
games={x['id']:x for x in json.load(open('/private/tmp/claude-501/sk/games.json'))}
W=[];tot=[0,0,0]; err=[0,0,0]; n=0; exact=0
for gid in sys.argv[1:]:
    g=games[gid]; z=np.load(f'cells2/{gid}.npz'); t0=float(z['t0'])
    for p in (0,1):
        cls=X.classify(z['cells'][:,p]); i0=int((g['start_s']-t0)*30)
        states=[]  # (frame, B, Bo, cumL, cumC, cumG)
        cum={'L':0,'C':0,'G':0}
        def tr(i,B,Qc,sol):
            if sol:
                for op in sol[2]:
                    if op['op']=='lock': cum['L']+=1
                    if op['op']=='clear': cum['C']+=len(op['rows'])
                    if op['op']=='garbage': cum['G']+=op['g']
                states.append((i,sol[0].copy(),sol[1].copy(),cum['L'],cum['C'],cum['G']))
        res=X.analyze_player(cls,i0,int((g['start_s']+60-t0)*30),trace=tr)
        rs=[r['f'] for r in res['resyncs']]
        off=max(0,i0-10); fev=X.flash_events(X.ffill(cls[off:int((g['start_s']+60-t0)*30)]))
        # windows of 2 s between tracked states, not crossing a resync
        for a in range(0,len(states)):
            for b in range(a+1,len(states)):
                if states[b][0]-states[a][0]>=45: break
            else: continue
            if any(states[a][0]<=r<=states[b][0] for r in rs): continue
            if a%7: continue
            sa,sb=states[a],states[b]
            def bq(B,O): return np.where(B,np.where(O==1,1,2),0)
            fl=[r for f,r in fev if sa[0]-off-3<=f<=sb[0]-off]
            W.append((int(sb[1].sum()-sa[1].sum()),X.n_garbage_rows(bq(sa[1],sa[2])),X.n_garbage_rows(bq(sb[1],sb[2])),sum(len(r) for r in fl),(sb[0]-sa[0])/30,sb[3] and (states[-1][3]/((states[-1][0]-states[0][0])/30)),(sb[3]-sa[3],sb[4]-sa[4],sb[5]-sa[5])))
            est=X.gap_estimate(int(sb[1].sum()-sa[1].sum()),X.n_garbage_rows(bq(sa[1],sa[2])),X.n_garbage_rows(bq(sb[1],sb[2])),sum(len(r) for r in fl))
            pass
            tru=(sb[3]-sa[3],sb[4]-sa[4],sb[5]-sa[5])
            n+=1; exact+= (est[1:]==tru)
            for k in range(3): tot[k]+=tru[k]; err[k]+=est[k+1]-tru[k]
print('windows',n,'exact',exact,'true totals L,C,G',tot,'signed error',err)

import itertools
for wf,wr in itertools.product([0.5,1,3],[0,0.3,1,3]):
    X.W_FLASH=wf;X.W_RATE=wr; e=[0,0,0];ex=0
    for d,a,b,c,dt,rate,tru in W:
        est=X.gap_estimate(d,a,b,c,None if wr==0 else rate*dt)
        ex+=est[1:]==tru
        for k in range(3): e[k]+=est[k+1]-tru[k]
    print(wf,wr,'exact',ex,'err',e)
