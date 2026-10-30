# [xo] banfind.py streamed in 500-frame chunks over [T0, T0+DUR) so a 2.5 h video fits in memory; same template/score rule.
import sys,subprocess,numpy as np
from PIL import Image
from numpy.lib.stride_tricks import sliding_window_view as sw
K='/tmp/claude-0/xo/'
v,T0,DUR=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]); Y0,H=306,46
t=np.asarray(Image.open(K+'video/f1.png').convert('RGB'),np.float32)[322:336,70:99]
tt=t-t.mean(); tn=np.sqrt((tt*tt).sum())
p=subprocess.Popen(['ffmpeg','-v','error','-ss',str(T0),'-i',K+f'video/{v}.mp4','-t',str(DUR),'-r','10','-vf',f'crop=854:{H}:0:{Y0}','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
out=[[],[]]; fs=854*H*3
while True:
  raw=p.stdout.read(fs*500); n=len(raw)//fs
  if n==0: break
  F=np.frombuffer(raw[:n*fs],np.uint8).reshape(n,H,854,3).astype(np.float32)
  for k,x in enumerate((70,482)):
    R=F[:,322-3-Y0:336+3-Y0,x-6:x+6+29]
    W=sw(R,(14,29),axis=(1,2)); W=W-W.mean(axis=(3,4,5),keepdims=True)
    num=(W*tt.transpose(2,0,1)[None,None,None]).sum(axis=(3,4,5)); den=np.sqrt((W*W).sum(axis=(3,4,5)))*tn+1e-6
    out[k].append((num/den).reshape(n,-1).max(1))
S=np.stack([np.concatenate(o) for o in out])
# times are T0 + i/10; bansheet.py reads i/10 as absolute, so pad the front
S=np.concatenate([np.zeros((2,int(round(T0*10))),np.float32),S],1)
np.save(K+f'w/seg/ban_{v}.npy',S)
for k,pl in enumerate(('p1','p2')):
  s=S[k]; on=np.nonzero((s[1:]>0.6)&(s[:-1]<=0.6))[0]+1
  print(pl,len(on))
