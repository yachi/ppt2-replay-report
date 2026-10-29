# usage: python3 sheet.py OUT.png T0 T1 STEP [p1|p2|both] -> contact sheet of frames T0..T1 every STEP s, each labelled with its time
import sys,subprocess,numpy as np
from PIL import Image,ImageDraw
out,t0,t1,st=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]);side=sys.argv[5] if len(sys.argv)>5 else 'both'
box={'p1':(90,40,400,430),'p2':(510,40,820,430),'both':(0,0,854,480)}[side]
ims=[];t=t0
while t<=t1+1e-6:
    b=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.3f}','-i','/tmp/claude-0/fr/video/full.mp4','-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    im=Image.fromarray(np.frombuffer(b,np.uint8).reshape(480,854,3)).crop(box);ImageDraw.Draw(im).text((4,4),f'{t:.2f}',fill=(255,255,0));ims.append(im);t+=st
w,h=ims[0].size;cols=min(len(ims),6 if side!='both' else 3);rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(w*cols,h*rows))
for i,im in enumerate(ims): S.paste(im,((i%cols)*w,(i//cols)*h))
S.save(out);print(out,len(ims),'frames')
