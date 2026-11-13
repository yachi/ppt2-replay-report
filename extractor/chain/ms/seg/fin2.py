import json, cv2, numpy as np
S=json.load(open('seg_games.json'))
FIN=[6,15,23,30,35,42,50,56,65,70,79,87,96,104,110,116,125,130,137,145,152,161,168,175]
cap=cv2.VideoCapture('/tmp/claude-0/ms/video/mtslCN3qVDY.mp4')
def grab(t):
    cap.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok,f=cap.read(); return f if ok else None
rows=[];info={}
for si in FIN:
    s,e=S[si]['start'],S[si]['end']
    # find first 'loading' (counter crop bright) scanning forward 1s from start+5
    t=s+5; tl=None
    while t<e+5:
        f=grab(t)
        if f is None: break
        c=f[428:472,560:780]
        if c.mean()>200: tl=t;break
        t+=1
    if tl is None: tl=e
    info[si]=tl
    tiles=[]
    for dt in np.arange(-12,0,1.0):
        f=grab(tl+dt); t2=f[428:472,300:780] if f is not None else np.zeros((44,480,3),np.uint8)
        tiles.append(cv2.resize(t2,(160,15)))
    r=np.vstack([np.hstack(tiles[:6]),np.hstack(tiles[6:])])
    lab=np.full((30,60,3),255,np.uint8); cv2.putText(lab,f'{si}',(2,20),0,0.5,(0,0,0),1)
    rows.append(np.hstack([lab,r]))
cv2.imwrite('cnt/fin2.png',np.vstack(rows)); json.dump(info,open('fin_load.json','w'))
print(info)
