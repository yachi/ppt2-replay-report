# [fs port] digit templates for -FTFs2Vv1ZI: cells cut from six frames (343.2, 451.5, 713.1, 942.8, 1358.9, 1597.3 s) whose scores were read by eye
# (s0..s5.png; s0's p1 and both of s2's are hidden by effects and skipped), averaged per digit and thresholded at 0.5 -> T.npy (10,23,16), labels '0'..'9'.
import numpy as np
from PIL import Image
XS=[150,168,186,204,223,242,260,279]
LAB={0:(None,'00038249'),1:('00040740','00041750'),3:('00036528','00064883'),4:('00066654','00070229'),5:('00056350','00054567')}
def cell(f,x): return (f[392:415,x-2:x+14].min(2)>190).astype(float)
acc={str(d):[] for d in range(10)}
for i,(a,b) in LAB.items():
  f=np.asarray(Image.open(f's{i}.png').convert('RGB'))
  for s,dx in ((a,0),(b,411)):
    if s is None: continue
    for x,c in zip(XS,s): acc[c].append(cell(f,x+dx))
T=np.array([(np.mean(acc[str(d)],0)>0.5).astype(float) for d in range(10)])
print({k:len(v) for k,v in acc.items()})
np.save('T.npy',T)
