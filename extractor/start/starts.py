import json,sys,subprocess
from PIL import Image, ImageDraw
vid=sys.argv[1]; d=json.load(open(f'g_{vid}.json'))
starts=[];z=0
for i,(t,n,g) in enumerate(d):
    if n==0: z+=1
    else:
        if z>=8: starts.append(t)
        z=0
print(vid,[round(s,1) for s in starts])
offs=[1.5,2.5,3.5,4.5,5.5,7.0]
for k,s in enumerate(starts):
    tiles=[]
    for o in offs:
        f=f'/tmp/_f.png'
        subprocess.run(['ffmpeg','-v','error','-ss',str(max(0,s+o)),'-i',f'vid/{vid}.mp4','-frames:v','1','-y',f],check=True)
        im=Image.open(f).crop((85,55,360,400)); dr=ImageDraw.Draw(im); dr.text((5,330),f'+{o}s',fill=(255,0,0))
        tiles.append(im)
    W=sum(t.width for t in tiles); M=Image.new('RGB',(W,345))
    x=0
    for t in tiles: M.paste(t,(x,0)); x+=t.width
    M.save(f'm_{vid}_{k:02d}_{s:.1f}.png')
