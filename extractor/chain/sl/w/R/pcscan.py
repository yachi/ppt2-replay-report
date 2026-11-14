# PERFECT CLEAR banner scan (new for cVO2eGipjV0): orange+white fraction in the banner box, 10 fps
import json,subprocess,numpy as np,sys
G={g['id']:g for g in json.load(open('../games.json'))}
A={j['id']:j for j in map(json.loads,open('A/games.jsonl'))}
X0,X1,Y0,Y1=560,705,150,232
def frames(path,t0,t1):
  cmd=['ffmpeg','-v','error','-ss',f'{t0:.2f}','-i',path,'-t',f'{t1-t0:.2f}','-r','10','-vf',f'crop={X1-X0+411}:{Y1-Y0}:{X0-411}:{Y0}','-f','rawvideo','-pix_fmt','rgb24','-']
  raw=subprocess.run(cmd,capture_output=True).stdout; w=X1-X0+411; h=Y1-Y0
  n=len(raw)//(w*h*3); return np.frombuffer(raw,np.uint8)[:n*w*h*3].reshape(n,h,w,3).astype(np.float32)/255
def feat(F):
  mx=F.max(-1); mn=F.min(-1); s=(mx-mn)/np.maximum(mx,1e-6)
  r,g,b=F[...,0],F[...,1],F[...,2]
  orange=(r>0.85)&(g>0.35)&(g<0.7)&(b<0.25)
  white=(s<0.12)&(mx>0.9)
  return orange,white
out={}
for gid in sys.argv[1:]:
  a=A[gid]; t0=a['start_s']-0.5; t1=a['end_s']+1.5
  F=frames(G[gid]['path'],t0,t1); o,w=feat(F); W=X1-X0
  r={}
  for p,xs in (('p1',slice(0,W)),('p2',slice(411,411+W))):
    r[p]=dict(o=o[:,:,xs].mean((1,2)).round(3).tolist(),w=w[:,:,xs].mean((1,2)).round(3).tolist())
  out[gid]=dict(t0=t0,**r); print(gid,flush=True)
json.dump(out,open(f'R/pcban/{sys.argv[1]}.json','w'))
