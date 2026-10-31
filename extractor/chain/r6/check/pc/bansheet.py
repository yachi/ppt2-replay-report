import sys,subprocess,numpy as np
from PIL import Image,ImageDraw
from multiprocessing import Pool
K='/tmp/claude-0/r6/'
v=sys.argv[1]; S=np.load(K+f'w/seg/ban_{v}.npy')
items=[]
for k,(p,x0) in enumerate((('p1',30),('p2',442))):
  s=S[k]; on=np.nonzero((s[1:]>0.6)&(s[:-1]<=0.6))[0]+1
  items+=[(i/10+0.5,p,x0) for i in on]
items.sort()
def fr(it):
  t,p,x0=it
  b=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.2f}','-i',K+f'video/{v}.mp4','-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
  return np.frombuffer(b,np.uint8).reshape(480,854,3)[312:346,x0:x0+150]
with Pool(4) as P: F=P.map(fr,items)
cols=3; rows=(len(F)+cols-1)//cols
im=Image.new('RGB',(cols*230,rows*38),'white'); d=ImageDraw.Draw(im)
for i,(it,f) in enumerate(zip(items,F)):
  c,r=i%cols,i//cols; im.paste(Image.fromarray(f),(c*230+75,r*38)); d.text((c*230+2,r*38+12),f'{i} {it[1]} {it[0]:.1f}',fill='black')
im.save(K+f'w/seg/np/bans_{v}.png'); print(len(items))
