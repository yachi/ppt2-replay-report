# [xp] digit templates for xp1R8-_Bi_I (frames at 1000, 1500, 2200, 5000, 5500, 8000 s, scores read by eye) (was: [aj], [ach port, new file] the 2026-10-28 uploads): cells cut from six frames whose scores were read by eye
# (s0..s5.png), averaged per digit and thresholded at 0.5 -> T.npy (10,23,16), labels '0'..'9'.
import numpy as np
from PIL import Image
XS=[150,168,186,204,223,242,260,279]
LAB={0:('00005224','00000455'),1:('00053624','00036426'),2:('00000121','00000148'),3:('00005298','00005298'),4:('00077203','00096884'),5:('00005594','00005721')}
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
