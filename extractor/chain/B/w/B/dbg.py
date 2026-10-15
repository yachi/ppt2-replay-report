import sys, json, numpy as np
from extract_b import *
L='.GZLOSIJT?'
gid,p,a,b=sys.argv[1],int(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])
g={x['id']:x for x in json.load(open('/private/tmp/claude-501/sk/games.json'))}[gid]
z=np.load(f'cells2/{gid}.npz'); t0=float(z['t0'])
cls=classify(z['cells'][:,p])
res=analyze_player(cls,int((g['start_s']-t0)*30),int((b-t0)*30))
for e in res['events']:
    if t0+e['f']/30>=a: print(round(t0+e['f']/30,2),{k:v for k,v in e.items() if k!='f'})
for r in res['resyncs']:
    t=t0+r['f']/30
    if t<a: continue
    print('RESYNC',round(t,2),'since',round(t0+r['since']/30,2),r['delta'])
    for row in range(14,-1,-1):
        print(''.join('#' if x else '.' for x in r['B'][row]),'  ',''.join(L[x] for x in r['Q'][row]))
