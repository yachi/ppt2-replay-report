# [e] T.npy is c's (qNc6SS1aEXY, below), reused unchanged: e's frames line up with c's at 0,0 px (NCC 0.77-0.99 over six
# overlay patches) and the reader gave 00012231 / 00022222 at 600 s, as on screen. The banner templates R/fr are c's too.
# [c] digit templates for qNc6SS1aEXY: cells cut from six frames of this video whose scores were read by eye
# (s0..s5.png at 1450, 2300, 3790, 4930, 6420, 8600 s; s3's p2 score sits under a board fragment, left out),
# averaged per digit and thresholded at 0.5 -> T.npy (10,23,16), labels '0'..'9'.
import numpy as np
from PIL import Image
XS=[150,168,186,204,223,242,260,279]
LAB={0:('00413984','00426370'),1:('00000000','00000000'),2:('00000310','00000331'),3:('00050208',None),4:('00018221','00022888'),5:('00062592','00050970')}
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
