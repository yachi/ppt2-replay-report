import json,subprocess,numpy as np
g=json.load(open('w/chain/xt/seg/seg_games.json'))
V='video/XTveY1Z22jU.mp4'
def fr(t):
    b=subprocess.run(['ffmpeg','-loglevel','error','-ss',str(t),'-i',V,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    return np.frombuffer(b,np.uint8).reshape(480,854,3).astype(int)
for i,x in enumerate(g):
    out=[]
    for t in (x['start']+2,(x['start']+x['end'])/2):
        f=fr(t); r=f[440:478]
        red=((r[...,0]>170)&(r[...,1]<70)&(r[...,2]<90)).sum(axis=1).max()
        out.append(int(red))
    print(i,x['start'],x['end'],out,flush=True)
