import numpy as np,subprocess,json,sys,os
T=np.load('/tmp/claude-0/fr/ocr/T.npy');TL=open('/tmp/claude-0/fr/ocr/TL.txt').read()
OFF=[9,28,46,65,84,102,121,140]
V='/tmp/claude-0/fr/video/full.mp4'
def read(f):
    out=[]
    for x0 in (135,554):
        s='';worst=0
        for o in OFF:
            v=(f[397:420,x0+o:x0+o+15].min(2)>190).astype(float).ravel()
            dd=((T-v)**2).sum(1);k=dd.argmin();s+=TL[k] if dd[k]<80 else '?';worst=max(worst,dd[k])
        out.append((s,worst))
    return out
if __name__=='__main__':
  J={j['id']:j for j in map(json.loads,open('/tmp/claude-0/fr/won/chain/am/w/A/games.jsonl'))}
  os.makedirs('/tmp/claude-0/fr/ocr/tail',exist_ok=True)
  for g in sys.argv[1:]:
      end=J[g]['end_s'];t0=end-4
      p=subprocess.Popen(['ffmpeg','-v','error','-ss',str(t0),'-i',V,'-t','4.6','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
      res=[];k=0
      while True:
          b=p.stdout.read(854*480*3)
          if len(b)<854*480*3:break
          f=np.frombuffer(b,np.uint8).reshape(480,854,3)
          r=read(f);res.append((round(t0+k/30,3),r[0][0],float(r[0][1]),r[1][0],float(r[1][1])));k+=1
      json.dump(res,open(f'/tmp/claude-0/fr/ocr/tail/{g}.json','w'))
