import sys,json,numpy as np
sys.path.insert(0,'.')
import analyze as A
d=np.load(sys.argv[1]); p=int(sys.argv[2]); js=[int(x) for x in sys.argv[3].split(',')]
meta=json.load(open('../../games.json'))[int(sys.argv[4])]
t0=float(d['t0']); lo=int((meta['start_s']-1-t0)*30)
sp,seq,an=A.spawns(d['nxt'][:,p],lo,len(d['grid'])); print(an[:5])
grid=d['grid'][:,p]; prev=np.zeros((18,10),np.uint8)
iv=[(sp[j],sp[j+1]) for j in range(len(sp)-1)]
bs=[]
for a,b in iv:
    B=A.board_at(grid,a+1,min(max(a+2,b-3),a+12),prev); bs.append(B); prev=B
for j in js:
    a,b=iv[j]
    print(f'j={j} frames {a}-{b} t={t0+a/30:.2f} n={(bs[j]>0).sum()}')
    top=max([r for r in range(18) if bs[j][r].any()],default=0)
    for r in range(top,-1,-1): print('   ',''.join(A.NAMES[x] for x in bs[j][r]))
