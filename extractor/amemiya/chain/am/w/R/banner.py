# independent T-spin banner detector (referee). banner.py GID -> R/ban/GID.json
import sys,json,subprocess,numpy as np
from PIL import Image
G={g['id']:g for g in json.load(open('/private/tmp/claude-501/am/w/chain/am/games.json'))}
Y0,H=306,46
def strip(path,t0,t1):
  cmd=['ffmpeg','-loglevel','error','-ss',str(t0),'-i',path,'-t',str(t1-t0),'-r','30','-vf',f'crop=854:{H}:0:{Y0}','-f','rawvideo','-pix_fmt','rgb24','-']
  raw=subprocess.run(cmd,capture_output=True).stdout
  n=len(raw)//(854*H*3); return np.frombuffer(raw,np.uint8)[:n*854*H*3].reshape(n,H,854,3).astype(np.float32)
def tpl(png,x0,y0,x1,y1):
  return np.asarray(Image.open(png).convert('RGB'),np.float32)[y0:y1,x0:x1]
# [am port] templates re-cut from 4xcAmo-s-Tg frames (the archived R/fr/*.png are not in the repo):
# b2.png = 168.72 s (k000 p2 T-SPIN Triple), b3.png = 179.68 s (k000 p1 T-SPIN Double),
# b_single.png = 175.05 s (k000 p2 T-SPIN Single), b_mini2.png = 3205.48 s (k038 p2 Mini T-SPIN Single).
# Boxes located on these frames; the banner sits ~6 px lower than the old layout x1.0191.
T_SPIN=tpl('R/fr/b2.png',482,328,512,342)            # '-SPIN' p2 coords
WORDS={'Single':tpl('R/fr/b_single.png',512,323,547,339),'Triple':tpl('R/fr/b2.png',512,325,547,341),'Double':tpl('R/fr/b3.png',92,325,127,341)}
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
  for p,off in (('p1',-420),('p2',0)):   # [am port] p1 offset -412 -> -420
    sc=[];pos=[]
    for f in F:
      s,bp=best(f,T_SPIN,482+off,328); sc.append(s); pos.append(bp)
    out[p]=dict(t0=t0,score=[round(s,3) for s in sc],pos=pos)
  return out,F
if __name__=='__main__':
  gid=sys.argv[1]; t0=float(sys.argv[2]); t1=float(sys.argv[3])
  o,F=run(gid,t0,t1)
  for p in o:
    sc=o[p]['score']; hi=[(round(t0+i/30,2),s) for i,s in enumerate(sc) if s>0.5]
    print(p,'max',max(sc),'n>0.5',len(hi),hi[:6],hi[-3:])
