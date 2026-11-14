import json, cv2, numpy as np
S=json.load(open('seg_games.json'))
FIN=[6,15,23,30,35,42,50,56,65,70,79,87,96,104,110,116,125,130,137,145,152,161,168,175]
cap=cv2.VideoCapture('/tmp/claude-0/yk/video/YkPw_o7t6no.mp4')
rows=[]
for si in FIN:
    e=S[si]['end']; tiles=[]
    for dt in (-2.0,-1.0,-0.3,0.5,1.5,3.0):
        cap.set(cv2.CAP_PROP_POS_MSEC,(e+dt)*1000); ok,f=cap.read()
        t=f[428:472,300:780] if ok else np.zeros((44,480,3),np.uint8)
        tiles.append(cv2.resize(t,(240,22)))
    r=np.hstack(tiles); lab=np.full((22,60,3),255,np.uint8); cv2.putText(lab,str(si),(2,16),0,0.5,(0,0,0),1)
    rows.append(np.hstack([lab,r]))
cv2.imwrite('cnt/fin.png',np.vstack(rows))
