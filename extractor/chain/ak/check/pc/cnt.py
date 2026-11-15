import sys,json,subprocess,numpy as np
from PIL import Image,ImageDraw
from multiprocessing import Pool
K='/tmp/claude-0/ak/'
def fr(a):
  v,t=a
  b=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.2f}','-i',K+'video/'+v+'.mp4','-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
  return np.frombuffer(b,np.uint8).reshape(480,854,3)[420:462,330:530]
v=sys.argv[1]
g=[q for q in json.load(open(K+f'w/seg/{v}_seg.json')) if q['end']-q['start']>5]
jobs=[]
for q in g: jobs+= [(v,q['start']+3),(v,q['end']-0.3)]
with Pool(4) as P: F=P.map(fr,jobs)
H=46; im=Image.new('RGB',(470,H*len(g)),'white'); d=ImageDraw.Draw(im)
for i,q in enumerate(g):
  im.paste(Image.fromarray(F[2*i]),(60,i*H)); im.paste(Image.fromarray(F[2*i+1]),(270,i*H)); d.text((2,i*H+15),f"{i} {q['start']}",fill='black')
im.save(K+f'w/seg/np/cnt_{v}.png'); print(len(g))
