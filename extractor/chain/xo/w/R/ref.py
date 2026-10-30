# ref.py VIDEO T0 T1 PLAYER(p1|p2|both) STEP OUT [cols]
# contact sheet of board(+hold+next) crops every STEP frames at 30fps, labelled with t
import sys,subprocess,numpy as np
from PIL import Image,ImageDraw
v,t0,t1,who,step,out=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),sys.argv[4],int(sys.argv[5]),sys.argv[6]
cols=int(sys.argv[7]) if len(sys.argv)>7 else 10
W,H=854,480
cmd=['ffmpeg','-loglevel','error','-ss',str(t0),'-i',f'/tmp/claude-0/xo/video/{v}.mp4','-t',str(t1-t0),'-r','30','-f','rawvideo','-pix_fmt','rgb24','-']
raw=subprocess.run(cmd,capture_output=True).stdout
n=len(raw)//(W*H*3); fr=np.frombuffer(raw,np.uint8)[:n*W*H*3].reshape(n,H,W,3)
boxes={'p1':(85,60,362,392),'p2':(497,60,772,392)}
sel=['p1','p2'] if who=='both' else [who]
tiles=[]
for i in range(0,n,step):
  parts=[Image.fromarray(fr[i][boxes[s][1]:boxes[s][3],boxes[s][0]:boxes[s][2]]) for s in sel]
  w=sum(p.width for p in parts); h=parts[0].height
  im=Image.new('RGB',(w,h+14),(0,0,0)); x=0
  for p in parts: im.paste(p,(x,14)); x+=p.width
  ImageDraw.Draw(im).text((2,1),'%.2f'%(t0+i/30),fill=(255,255,0))
  tiles.append(im)
tw,th=tiles[0].size; sc=float(sys.argv[8]) if len(sys.argv)>8 else 0.6
tw2,th2=int(tw*sc),int(th*sc)
rows=(len(tiles)+cols-1)//cols
sheet=Image.new('RGB',(tw2*cols,th2*rows))
for k,t in enumerate(tiles): sheet.paste(t.resize((tw2,th2)),((k%cols)*tw2,(k//cols)*th2))
sheet.save(out); print(n,'frames',len(tiles),'tiles',sheet.size)
