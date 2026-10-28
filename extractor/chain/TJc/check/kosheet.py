import sys,json,pickle,subprocess,numpy as np
from PIL import Image,ImageDraw
W='/tmp/claude-0/chain/kbb/w'; import os; os.chdir(W)
G={g['id']:g for g in json.load(open('../games.json'))}
A={j['id']:j for j in map(json.loads,open('A/games.jsonl'))}
todo=[]
for gid in sorted(A):
  ev=pickle.load(open(f'R/ev/{gid}.pkl','rb'))
  if A[gid].get('winner') and ev.get('kofinal') is None: todo.append(gid)
print(len(todo),todo)
lo,hi=int(sys.argv[1]),int(sys.argv[2])
tiles=[]
for gid in todo[lo:hi]:
  a=A[gid]; p=a['winner']; x0=140 if p=='p1' else 551
  d=np.load(f'A/feat/{gid}.npz'); t0=float(d['t0']); end=int(round((a['end_s']-t0)*30))
  row=Image.new('RGB',(170*4,375),'black')
  for i,df in enumerate((-8,-3,0,3)):
    t=t0+(end+df)/30
    raw=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.3f}','-i',G[gid]['path'],'-frames:v','1','-vf',f'crop=170:354:{x0}:62','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    row.paste(Image.frombytes('RGB',(170,354),raw),(170*i,20))
  ImageDraw.Draw(row).text((4,4),f'{gid} {p} KO-8 / -3 / 0 / +3',fill='yellow'); tiles.append(row)
S=Image.new('RGB',(680*3,375*((len(tiles)+2)//3)))
for i,t in enumerate(tiles): S.paste(t,((i%3)*680,(i//3)*375))
S.save(f'/tmp/claude-0/chain/ko_{lo}.png')
