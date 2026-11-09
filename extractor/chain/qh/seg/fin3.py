import json, cv2, numpy as np
info={int(k):v for k,v in json.load(open('fin_load.json')).items()}
cap=cv2.VideoCapture('/tmp/claude-0/qh/video/QheX1_UP5W4.mp4')
rows=[]
for si,tl in info.items():
    tiles=[]
    for dt in (-9,-7,-5,-3):
        cap.set(cv2.CAP_PROP_POS_MSEC,(tl+dt)*1000); ok,f=cap.read()
        tiles.append(cv2.resize(f[430:470,415:600],(240,52)))
    lab=np.full((52,70,3),255,np.uint8); cv2.putText(lab,str(si),(2,30),0,0.7,(0,0,0),2)
    rows.append(np.hstack([lab]+tiles))
a=np.vstack(rows); cv2.imwrite('cnt/fin3a.png',a[:52*12]); cv2.imwrite('cnt/fin3b.png',a[52*12:])
