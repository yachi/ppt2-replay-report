# contact sheets of the WIN counter + opponent nameplate at start+3 s and end-0.3 s of every candidate game
import json, subprocess, numpy as np
from PIL import Image, ImageDraw
from multiprocessing import Pool
V='/tmp/claude-0/xo/video/XoaWLJowuCQ.mp4'
g=json.load(open('seg_games.json'))
def fr(t):
    b=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.2f}','-i',V,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    return np.frombuffer(b,np.uint8).reshape(480,854,3)[428:472,300:780]
ts=[t for q in g for t in (q['start']+3,q['end']-0.3)]
with Pool(4) as P: F=P.map(fr,ts)
for s in range(0,len(g),20):
    im=Image.new('RGB',(1040,20*46),'white'); d=ImageDraw.Draw(im)
    for r,i in enumerate(range(s,min(s+20,len(g)))):
        d.text((2,r*46+15),f'{i} {g[i]["start"]:.0f}',fill='black')
        im.paste(Image.fromarray(F[2*i]),(80,r*46)); im.paste(Image.fromarray(F[2*i+1]),(560,r*46))
    im.save(f'cnt/s{s//20}.png')
print(len(g))
