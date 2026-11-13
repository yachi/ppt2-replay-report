# [u4] NOT RUN: T.npy copied from chain/fs (same digit font); checked by eye on frames 1100, 1500, 2000 s.
# [qh port] original header follows, kept for provenance:
# [qh port] digit templates for u4P57GT3unk (2026-11-09): cells cut from six frames (2245, 2500, 3050, 4700, 6300, 7900 s) whose scores were read by eye
# (s0..s5.png), averaged per digit and thresholded at 0.5 -> T.npy (10,23,16), labels '0'..'9'.
import numpy as np
from PIL import Image
XS=[150,168,186,204,223,242,260,279]
LAB={0:('00020298','00021891'),1:('00057211','00035936'),2:('00035231',None),3:('00038345','00054644'),4:('00009880',None),5:('00011768','00004587')}
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
