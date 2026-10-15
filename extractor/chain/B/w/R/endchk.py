import json,subprocess,sys
from PIL import Image,ImageDraw
A={j['id']:j for j in map(json.loads,open('A/games.jsonl'))}
B={j['id']:j for j in map(json.loads,open('B/games.jsonl'))}
G={g['id']:g for g in json.load(open('../games.json'))}
ids=sys.argv[2:]; out=sys.argv[1]
rows=[]
for g in ids:
  tb=G[g]['start_s']+B[g]['duration_s']; ta=A[g]['end_s']
  ts=[('B_end',tb),('A-1.0',ta-1.0),('A_end',ta),('A+1.5',ta+1.5)]
  ims=[]
  for lab,t in ts:
    subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(t),'-i',G[g]['path'],'-frames:v','1','R/fr/_t.png'])
    im=Image.open('R/fr/_t.png').convert('RGB').crop((80,40,780,420)).resize((350,190))
    ImageDraw.Draw(im).text((3,3),'%s %s %.2f'%(g,lab,t),fill=(255,0,0)); ims.append(im)
  r=Image.new('RGB',(1400,190))
  for i,im in enumerate(ims): r.paste(im,(350*i,0))
  rows.append(r)
S=Image.new('RGB',(1400,190*len(rows)))
for i,r in enumerate(rows): S.paste(r,(0,190*i))
S.save(out)
