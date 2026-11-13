# [ms, new] set finals of the edited upload: first frame of the end dialog / loading screen (1 s steps), and the WIN pill 0.5 s before
import json, cv2, numpy as np
S=json.load(open('seg_games.json'))
FIN=[20,39,65,88,117,136,155]
cap=cv2.VideoCapture('/tmp/claude-0/ms/video/mtslCN3qVDY.mp4')
def grab(t):
    cap.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok,f=cap.read(); return f if ok else None
info={}; rows=[]
for si in FIN:
    s,e=S[si]['start'],S[si]['end']; t=s+5; tl=e
    while t<e+5:
        f=grab(t)
        if f is None: break
        if f[115:170,170:680].mean()>225 or f[428:472,560:780].mean()>200 or f.mean()<15: tl=t; break
        t+=0.5
    info[si]=tl
    f=grab(tl-1.0); rows.append(cv2.resize(f[428:472,300:780],(480,44)))
    print(si,s,e,tl)
cv2.imwrite('cnt/fin_ms.png',np.vstack(rows)); json.dump(info,open('fin_load.json','w'))
