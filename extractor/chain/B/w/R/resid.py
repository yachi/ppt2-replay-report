import pickle,json,random,subprocess
from PIL import Image,ImageDraw
F=pickle.load(open('R/fuse.pkl','rb')); G={g['id']:g for g in json.load(open('../games.json'))}
WL={'Single':1,'Double':2,'Triple':3}
ex=[(k,b['t'],'extra %s %s'%(b['word'][0],'mini' if b['mini'] else '')) for k,r in F.items() for b in r['extra']]
nob=[(k,e['tl'],'A %s no banner'%e['akind']) for k,r in F.items() for e in r['evs'] if e['akind'] in('tss','tsd','tst','tsmini') and not e['ban']]
wm=[(k,e['ban']['t'],'word %s vs flash %d'%(e['ban']['word'][0],e['lines'])) for k,r in F.items() for e in r['evs'] if e['ban'] and not e['ban']['mini'] and WL[e['ban']['word'][0]]!=e['lines']]
random.seed(11); random.shuffle(ex); random.shuffle(wm)
L=ex[:8]+nob+wm[:4]
S=Image.new('RGB',(6*300,3*270))
for i,((g,p),t,lab) in enumerate(L):
  subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(t+0.35),'-i',G[g]['path'],'-frames:v','1','R/fr/_t.png'])
  x0=20 if p=='p1' else 432
  m=Image.open('R/fr/_t.png').convert('RGB').crop((x0,120,x0+300,390)); ImageDraw.Draw(m).text((2,2),'%d %s %s %.2f %s'%(i,g,p,t,lab),fill=(255,0,0)); S.paste(m,((i%6)*300,(i//6)*270))
  print(i,g,p,t,lab)
S.save('R/fr/resid.png')
