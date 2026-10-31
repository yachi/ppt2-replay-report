# [r6 port] digit templates for 6rUc3cXsjbo (syakegohan stream; was: [xo port] for uyeshota, before that [ach port, new file] the 2026-10-28 uploads): cells cut from eight frames whose scores were read by eye (s6, s7 added after the first held-out check misread two 6s)
# (s0..s5.png), averaged per digit and thresholded at 0.5 -> T.npy (10,23,16), labels '0'..'9'.
import numpy as np
from PIL import Image
XS=[150,168,186,204,223,242,260,279]
LAB={0:('00039511','00040137'),1:(None,'00123857'),2:(None,'00193282'),3:('00064945','00078758'),4:('00372483',None),5:('00075793','00079846'),6:(None,'00084611'),7:('00070428','00065736')}
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
