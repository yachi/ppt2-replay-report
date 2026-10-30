import sys,json,subprocess,numpy as np
from PIL import Image,ImageDraw
from multiprocessing import Pool
K='/tmp/claude-0/ak/'
G={g['id']:g for g in json.load(open(K+'w/chain/sy/games.json'))}
C=json.load(open(sys.argv[1])) # list of [label,id,player,t]
OFF=[-1.5,-1.0,-0.6,-0.3,-0.1,0.05,0.2,0.4,0.7,1.0,1.5]
def fr(a):
  (lab,gid,p,t),o=a
  b=subprocess.run(['ffmpeg','-v','error','-ss',f"{t+o:.2f}",'-i',G[gid]['path'],'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
  f=np.frombuffer(b,np.uint8).reshape(480,854,3); x0=130 if p=='p1' else 541
  return np.ascontiguousarray(f[60:400:2,x0:x0+180:2])
jobs=[(c,o) for c in C for o in OFF]
with Pool(4) as P: I=P.map(fr,jobs)
w,h=90,170; S=Image.new('RGB',(len(OFF)*w,len(C)*(h+12)),'white'); d=ImageDraw.Draw(S)
for k,((c,o),a) in enumerate(zip(jobs,I)):
  r,col=k//len(OFF),k%len(OFF); S.paste(Image.fromarray(a),(col*w,r*(h+12)+12))
  if col==0: d.text((1,r*(h+12)),f"{c[0]} {c[1]}{c[2]} {c[3]}",fill='black')
  else: d.text((col*w+2,r*(h+12)),f"{o:+.2f}",fill='blue')
S.save(sys.argv[2])
