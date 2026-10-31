# sample score digit cells (padded by 2 px) from frames across the video. uP capture: 8 digits, rows 392:415, left edges XS (p1), p2 = +411
import subprocess,numpy as np,sys
V='/tmp/claude-0/r6/video/6rUc3cXsjbo.mp4'
XS=[150,168,186,204,223,242,260,279]   # digit left edges on f170 (p1 score 00093701)
P=2
def cells(f,pad=P):
    out=[]
    for dx in (0,411):
        for x in XS:
            out.append((f[392-pad:415+pad,x+dx-2-pad:x+dx+14+pad].min(2)>190).astype(np.uint8))
    return out
if __name__=='__main__':
    samp=[]
    for t in np.arange(100,5480,23.7):
        b=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.2f}','-i',V,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
        if len(b)<854*480*3: continue
        f=np.frombuffer(b,np.uint8).reshape(480,854,3); samp+=cells(f)
    A=np.array(samp); np.save('sampP.npy',A); print(A.shape)
