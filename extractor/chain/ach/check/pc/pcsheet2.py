import sys,json,subprocess,numpy as np
from PIL import Image,ImageDraw
from multiprocessing import Pool
K='/tmp/claude-0/ak/'
G={g['id']:g for g in json.load(open(K+'w/chain/sy/games.json'))}
F=[x for x in json.load(open(K+'out/flags.json')) if x['field_or_issue']=='PC banner onset']
acc=sys.argv[1]=='acc'; dt=float(sys.argv[2])
F=[x for x in F if ('rejected' not in x['detail'])==acc]
def fr(x):
  b=subprocess.run(['ffmpeg','-v','error','-ss',f"{x['t_s']+dt:.2f}",'-i',G[x['id']]['path'],'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
  f=np.frombuffer(b,np.uint8).reshape(480,854,3); x0=130 if x['player']=='p1' else 541
  return np.ascontiguousarray(f[60:400:2,x0:x0+180:2])
with Pool(4) as P: I=P.map(fr,F)
cols=12; rows=(len(I)+cols-1)//cols; w,h=90,170
S=Image.new('RGB',(cols*w,rows*(h+12)),'white'); d=ImageDraw.Draw(S)
for i,(x,a) in enumerate(zip(F,I)):
  c,r=i%cols,i//cols; S.paste(Image.fromarray(a),(c*w,r*(h+12)+12)); d.text((c*w+1,r*(h+12)),f"{i}{x['id'][1:]}{x['player'][1]}",fill='black')
S.save(K+f'w/seg/np/pc_{sys.argv[1]}_{dt}.png'); json.dump(F,open(K+f'w/seg/np/pc_{sys.argv[1]}.json','w')); print(len(F))
