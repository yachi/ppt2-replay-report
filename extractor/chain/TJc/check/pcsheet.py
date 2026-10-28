import sys,json,subprocess,numpy as np
from PIL import Image,ImageDraw
sys.argv=sys.argv; W='/tmp/claude-0/chain/kbb/w'
import os; os.chdir(W)
exec(open('R/pcon.py').read().split("if __name__")[0])
G={g['id']:g for g in json.load(open('../games.json'))}
items=[(g,p,e) for (g,p),v in sorted(PC.items()) for e in v]
lo,hi=int(sys.argv[1]),int(sys.argv[2]); items=items[lo:hi] if len(sys.argv)<4 else [x for x in items if f"{x[0]}{x[1]}{x[2]['t']}" in sys.argv[3].split(",")]
tiles=[]
for g,p,e in items:
  x0=140 if p=='p1' else 551
  ims=[]
  for dt in (-0.4,0.3):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',f"{e['t']+dt:.2f}",'-i',G[g]['path'],'-frames:v','1','-vf',f'crop=170:330:{x0}:70','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    ims.append(Image.frombytes('RGB',(170,330),raw))
  t=Image.new('RGB',(340,350),'black'); t.paste(ims[0],(0,20)); t.paste(ims[1],(170,20))
  ImageDraw.Draw(t).text((4,4),f"{g} {p} {e['t']} len{e['len']}",fill='yellow'); tiles.append(t)
cols=6; rows=(len(tiles)+cols-1)//cols
S=Image.new('RGB',(340*cols,350*rows))
for i,t in enumerate(tiles): S.paste(t,((i%cols)*340,(i//cols)*350))
S.save(f'/tmp/claude-0/chain/pc_{lo}.png'); print(len(items))
