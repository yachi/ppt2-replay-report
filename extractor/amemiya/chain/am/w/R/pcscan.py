# PERFECT CLEAR banner scanner (referee addition for lgszEWNFSx0): NCC of the 'PERFECT' word template per board, every frame at 30 fps.
import sys,json,subprocess,numpy as np
from PIL import Image
from numpy.lib.stride_tricks import sliding_window_view as sw
V='/private/tmp/claude-501/am/video/full.mp4'  # [am port]
A={j['id']:j for j in map(json.loads,open('A/games.jsonl'))}
G={g['id']:g for g in json.load(open('../games.json'))}
TX0,TY0,TX1,TY1=570,150,702,180   # [am port] 'PERFECT' word on p2, frame 828.6 s (k011); lg used p1 158,158,282,188
T=np.asarray(Image.open('../chk/t_pc.png').convert('RGB'),np.float32)[TY0:TY1,TX0:TX1]
OFF={'p1':-419,'p2':0}; M=8   # [am port] was {'p1':0,'p2':411}
def scan(gid):
  g=G[gid]; t0=A[gid]['start_s']-0.5; t1=(A[gid]['end_s'] or g['end_upper_s'])+2.0
  out={}
  y0=TY0-M; y1=TY1+M
  cmd=['ffmpeg','-loglevel','error','-ss',str(t0),'-i',V,'-t',str(t1-t0),'-r','30','-vf',f'crop=854:{y1-y0}:0:{y0}','-f','rawvideo','-pix_fmt','rgb24','-']
  raw=subprocess.run(cmd,capture_output=True).stdout; H=y1-y0
  n=len(raw)//(854*H*3); F=np.frombuffer(raw,np.uint8)[:n*854*H*3].reshape(n,H,854,3).astype(np.float32)
  h,w=T.shape[:2]; tt=T-T.mean(); tn=np.sqrt((tt*tt).sum())
  for p,o in OFF.items():
    R=F[:,:,TX0+o-M:TX1+o+M,:]; S=[]
    for k in range(0,n,60):
      Wn=sw(R[k:k+60],(h,w),axis=(1,2)); Wn=Wn-Wn.mean(axis=(3,4,5),keepdims=True)
      num=(Wn*tt.transpose(2,0,1)[None,None,None]).sum(axis=(3,4,5)); den=np.sqrt((Wn*Wn).sum(axis=(3,4,5)))*tn+1e-6
      S.append((num/den).reshape(len(Wn),-1).max(1))
    out[p]=np.concatenate(S)
  np.savez(f'R/pc/{gid}.npz',t0=t0,**out)
for gid in sys.argv[1:]: scan(gid); print('done',gid,flush=True)
