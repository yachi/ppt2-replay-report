import numpy as np
from PIL import Image
OFF=[9,28,46,65,84,102,121,140]
def cells(f):
    out=[]
    for x0 in (135,554):
        for o in OFF:
            out.append((f[397:420,x0+o:x0+o+15].min(2)>190).astype(float).ravel())
    return out
known={5050:('00216332','00230044'),2300:('00057527','00062488'),3100:('00067895','00068398'),4200:('00129198','00140178'),5200:('00000218','00000219')}
X=[];Y=[]
for t,(a,b) in known.items():
    f=np.array(Image.open(f'/tmp/claude-0/xk/ocr/f{t}.png').convert('RGB'))
    for c,l in zip(cells(f),a+b): X.append(c);Y.append(l)
X=np.array(X);Y=np.array(Y)
T={d:X[Y==d].mean(0) for d in sorted(set(Y))}
print(sorted(T), {d:(Y==d).sum() for d in T})
np.save('/tmp/claude-0/xk/ocr/T.npy',np.array([T[d] for d in sorted(T)]));open('/tmp/claude-0/xk/ocr/TL.txt','w').write(''.join(sorted(T)))
# self-consistency: leave-one-out margins
for i,(x,y) in enumerate(zip(X,Y)):
    d={k:((v-x)**2).sum() for k,v in T.items()}
    s=sorted(d,key=d.get)
    if s[0]!=y or d[s[1]]-d[s[0]]<10: print('weak',i,y,s[:2],round(d[s[0]],1),round(d[s[1]],1))
