import json,subprocess,sys
from PIL import Image,ImageDraw
g=json.load(open('won/start/games_auto.json'))
crops=[]
for x in g:
    t=x['start_s']+2
    f=f"wc/c/{x['id']}.png"
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',x['path'],'-frames:v','1',f])
    im=Image.open(f).crop((330,430,530,462)).resize((400,64))
    crops.append((x['id'],im))
W=Image.new('RGB',(2*480,32*72),'white');d=ImageDraw.Draw(W)
for k,(i,im) in enumerate(crops):
    c,r=k//32,k%32
    W.paste(im,(c*480+70,r*72));d.text((c*480+5,r*72+25),i,fill='black')
W.save('wc/sheet1.png')
