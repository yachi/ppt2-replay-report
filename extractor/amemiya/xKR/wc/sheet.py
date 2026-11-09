import json,subprocess,sys
from PIL import Image,ImageDraw
g=json.load(open('won/start/games_auto.json'))
rows=[]
for x in g:
    f=f"wc/c/{x['id']}.png"
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(x['start_s']+2),'-i',x['path'],'-frames:v','1',f])
    im=Image.open(f); a=im.crop((330,430,530,462)).resize((300,48)); b=im.crop((525,432,745,460)).resize((330,42))
    rows.append((x['id'],a,b))
per=44
for s in range(0,len(rows),per):
    W=Image.new('RGB',(720,per*52),'white');d=ImageDraw.Draw(W)
    for k,(i,a,b) in enumerate(rows[s:s+per]):
        W.paste(a,(60,k*52));W.paste(b,(370,k*52+3));d.text((5,k*52+18),i,fill='black')
    W.save(f'wc/sheet{s//per}.png')
