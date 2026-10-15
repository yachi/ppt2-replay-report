# independent T-spin banner detector (referee). banner.py GID -> R/ban/GID.json
import sys,json,subprocess,numpy as np
from PIL import Image
G={g['id']:g for g in json.load(open('/private/tmp/claude-501/sk/metrics/more/cVO/games.json'))}
Y0,H=306,46
def strip(path,t0,t1):
  cmd=['ffmpeg','-loglevel','error','-ss',str(t0),'-i',path,'-t',str(t1-t0),'-r','30','-vf',f'crop=854:{H}:0:{Y0}','-f','rawvideo','-pix_fmt','rgb24','-']
  raw=subprocess.run(cmd,capture_output=True).stdout
  n=len(raw)//(854*H*3); return np.frombuffer(raw,np.uint8)[:n*854*H*3].reshape(n,H,854,3).astype(np.float32)
def tpl(png,x0,y0,x1,y1):
  return np.asarray(Image.open(png).convert('RGB'),np.float32)[y0:y1,x0:x1]
T_SPIN=tpl('R/fr/b2.png',482,322,511,336)            # '-SPIN' p2 coords
WORDS={'Single':tpl('R/fr/b_single.png',99,320,134,336),'Triple':tpl('R/fr/b2.png',511,320,546,336),'Double':tpl('R/fr/b3.png',511,320,546,336)}
def ncc(patch,t):
  a=patch-patch.mean(); b=t-t.mean(); d=np.sqrt((a*a).sum()*(b*b).sum())+1e-6; return float((a*b).sum()/d)
def best(fr,t,x,y,r=4):
  h,w=t.shape[:2]; bs=-1;bp=None
  for dy in range(-3,4):
    for dx in range(-r,r+1):
      yy=y+dy-Y0; xx=x+dx
      if yy<0 or yy+h>fr.shape[0]: continue
      s=ncc(fr[yy:yy+h,xx:xx+w],t)
      if s>bs: bs,bp=s,(xx,yy+Y0)
  return bs,bp
def run(gid,t0,t1):
  g=G[gid]; F=strip(g['path'],t0,t1); out={}
  for p,off in (('p1',-412),('p2',0)):
    sc=[];pos=[]
    for f in F:
      s,bp=best(f,T_SPIN,482+off,322); sc.append(s); pos.append(bp)
    out[p]=dict(t0=t0,score=[round(s,3) for s in sc],pos=pos)
  return out,F
if __name__=='__main__':
  gid=sys.argv[1]; t0=float(sys.argv[2]); t1=float(sys.argv[3])
  o,F=run(gid,t0,t1)
  for p in o:
    sc=o[p]['score']; hi=[(round(t0+i/30,2),s) for i,s in enumerate(sc) if s>0.5]
    print(p,'max',max(sc),'n>0.5',len(hi),hi[:6],hi[-3:])
