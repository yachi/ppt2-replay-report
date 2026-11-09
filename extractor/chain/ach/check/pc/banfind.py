import sys,subprocess,numpy as np
from PIL import Image
from numpy.lib.stride_tricks import sliding_window_view as sw
K='/tmp/claude-0/ak/'
v=sys.argv[1]; Y0,H=306,46
t=np.asarray(Image.open(K+'video/f1.png').convert('RGB'),np.float32)[322:336,70:99]
tt=t-t.mean(); tn=np.sqrt((tt*tt).sum())
raw=subprocess.run(['ffmpeg','-v','error','-i',K+f'video/{v}.mp4','-r','10','-vf',f'crop=854:{H}:0:{Y0}','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
n=len(raw)//(854*H*3); F=np.frombuffer(raw,np.uint8)[:n*854*H*3].reshape(n,H,854,3).astype(np.float32)
out=[]
for p,x in (('p1',70),('p2',482)):
  S=[]
  for i0 in range(0,n,500):
    R=F[i0:i0+500,322-3-Y0:336+3-Y0,x-6:x+6+29]
    W=sw(R,(14,29),axis=(1,2)); W=W-W.mean(axis=(3,4,5),keepdims=True)
    num=(W*tt.transpose(2,0,1)[None,None,None]).sum(axis=(3,4,5)); den=np.sqrt((W*W).sum(axis=(3,4,5)))*tn+1e-6
    S.append((num/den).reshape(len(R),-1).max(1))
  S=np.concatenate(S); out.append(S)
np.save(K+f'w/seg/ban_{v}.npy',np.stack(out))
for k,p in enumerate(('p1','p2')):
  S=out[k]; on=np.nonzero((S[1:]>0.6)&(S[:-1]<=0.6))[0]+1
  print(p,len(on),[round(i/10,1) for i in on][:200])
