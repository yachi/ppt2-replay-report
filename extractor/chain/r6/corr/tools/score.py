# usage: python3 score.py T0 T1  -> prints every frame (t, p1 score, p2 score) at 30 fps where either changes; '?' = unreadable digit
import sys,subprocess,numpy as np
sys.path.insert(0,'/tmp/claude-0/r6/w/ocr')
from reader import classify, cells_of
V='/tmp/claude-0/r6/video/'+sys.argv[3]+'.mp4'   # [ach] usage: score.py T0 T1 VIDEO_ID
t0,t1=float(sys.argv[1]),float(sys.argv[2])
p=subprocess.Popen(['ffmpeg','-v','error','-ss',str(t0),'-i',V,'-t',str(t1-t0),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
k=0;prev=None
while True:
    b=p.stdout.read(854*480*3)
    if len(b)<854*480*3:break
    lab,dm=classify(cells_of(np.frombuffer(b,np.uint8).reshape(480,854,3)))
    lab=[c if d<=70 else '?' for c,d in zip(lab,dm)]
    cur=(''.join(lab[:8]),''.join(lab[8:]))
    if cur!=prev or '-a' in sys.argv: print(f'{t0+k/30:.2f}',cur[0],cur[1])
    prev=cur;k+=1
