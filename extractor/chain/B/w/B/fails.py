import sys, json, numpy as np
import extract_b as X
L='.GZLOSIJT?'
gid,p,lim=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
g={x['id']:x for x in json.load(open('/private/tmp/claude-501/sk/games.json'))}[gid]
z=np.load(f'cells2/{gid}.npz'); t0=float(z['t0'])
cls=X.classify(z['cells'][:,p])
st={'ep':None,'n':0,'snaps':[]}
def show(i,B,Qc):
    top=max([r for r in range(20) if B[r].any() or (Qc[r]>0).any()]+[0])
    print('  t=%.2f'%(t0+i/30))
    for row in range(top,-1,-1): print(''.join('#' if x else '.' for x in B[row]),'  ',''.join(L[x] for x in Qc[row]))
def tr(i,B,Qc,sol):
    if sol is None:
        if st['ep'] is None: st['ep']=i; st['snaps']=[]
        st['snaps'].append((i,B.copy(),Qc.copy()))
    else:
        if st['ep'] is not None and i-st['ep']>=25 and st['n']<lim:
            st['n']+=1; print('EPISODE %.2f-%.2f'%(t0+st['ep']/30,t0+i/30))
            s=st['snaps']; 
            for k in (0,len(s)//2,len(s)-1): show(*s[k])
        st['ep']=None
X.analyze_player(cls,int((g['start_s']-t0)*30),int((float(sys.argv[4])-t0)*30),trace=tr)
