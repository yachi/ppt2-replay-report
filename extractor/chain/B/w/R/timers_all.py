import json,subprocess
from PIL import Image,ImageDraw
A={j['id']:j for j in map(json.loads,open('A/games.jsonl'))}
G={g['id']:g for g in json.load(open('../games.json'))}
ids=[g for g in sorted(A) if G[g]['video']!='UviTn8au3WE']
rows=[]
for g in ids:
  t=A[g]['end_s']+1.5
  p='R/fr/_t.png'
  subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(t),'-i',G[g]['path'],'-frames:v','1',p])
  im=Image.open(p).convert('RGB').crop((740,440,854,475))
  r=Image.new('RGB',(200,35)); r.paste(im,(86,0)); ImageDraw.Draw(r).text((2,10),g+' %.2f'%A[g]['duration_s'],fill=(255,255,0)); rows.append(r)
cols=3; n=len(rows); h=(n+cols-1)//cols
S=Image.new('RGB',(200*cols,35*h))
for i,r in enumerate(rows): S.paste(r,((i//h)*200,(i%h)*35))
S.save('R/fr/timers_upload.png'); print(n)
