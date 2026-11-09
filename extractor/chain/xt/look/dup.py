import json,subprocess,numpy as np
from concurrent.futures import ThreadPoolExecutor
g=json.load(open('w/chain/xt/seg/seg_games.json'))
V='video/XTveY1Z22jU.mp4'
def fr(t):
    b=subprocess.run(['ffmpeg','-loglevel','error','-ss',str(t),'-i',V,'-frames:v','1','-vf','crop=700:300:77:90,scale=70:30','-f','rawvideo','-pix_fmt','gray','-'],capture_output=True).stdout
    return np.frombuffer(b,np.uint8).astype(float)
def sig(x):
    return np.concatenate([fr(x['start']+o) for o in (8,14,20)])
with ThreadPoolExecutor(4) as ex: S=list(ex.map(sig,g))
S=np.array(S)
for j in range(len(g)):
    dd=[np.abs(S[j]-S[i]).mean() for i in range(len(g)) if i!=j]
    idx=[i for i in range(len(g)) if i!=j]
    k=int(np.argmin(dd)); print(j,round(g[j]['start']),idx[k],round(g[idx[k]]['start']),round(dd[k],1))
