import subprocess,numpy as np,sys
V='video/XTveY1Z22jU.mp4'
# one frame every 5 s, top strip only
p=subprocess.Popen(['ffmpeg','-loglevel','error','-i',V,'-vf','fps=1/5,crop=320:14:0:0','-f','rawvideo','-pix_fmt','gray','-'],stdout=subprocess.PIPE)
i=0
while True:
    b=p.stdout.read(320*14)
    if len(b)<320*14: break
    a=np.frombuffer(b,np.uint8)
    print(i*5,int((a>150).sum()))
    i+=1
