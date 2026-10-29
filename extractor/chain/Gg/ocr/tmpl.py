# [Gg port] digit templates for the Gg capture (remapped to uP geometry): cells cut with the uP reader's own rule
# (rows 392:415, left edges XS, p2 = +411, min(RGB) > 190) from 5 hand-read frames; template = per-digit mean.
import numpy as np, json
from PIL import Image
XS=[150,168,186,204,223,242,260,279]
known={300:('00000369','00000402'),900:('00125797',None),1500:('00000110','00000114'),2100:('00022112','00025563'),2700:('00000247','00000248'),3000:('00066426','00076713')}
def cell(f,x,P=0): return (f[392-P:415+P,x-2-P:x+14+P].min(2)>190).astype(float)
X=[];Y=[]
for t,pair in known.items():
    f=np.asarray(Image.open(f'f{t}.png').convert('RGB'))
    for dx,s in zip((0,411),pair):
        if s is None: continue
        for x,ch in zip(XS,s): X.append(cell(f,x+dx).ravel()); Y.append(ch)
X=np.array(X);Y=np.array(Y)
D=sorted(set(Y)); T=np.array([X[Y==d].mean(0) for d in D])
np.save('T.npy',T); open('TL.txt','w').write(''.join(D)); print(D,{d:int((Y==d).sum()) for d in D})
bad=0
for x,y in zip(X,Y):
    d=((T-x)**2).sum(1); o=np.argsort(d)
    if D[o[0]]!=y or d[o[1]]-d[o[0]]<15: bad+=1; print('weak',y,D[o[0]],D[o[1]],round(d[o[0]],1),round(d[o[1]],1))
print('weak',bad,'of',len(X))
