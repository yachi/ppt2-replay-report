import subprocess,numpy as np
V='/private/tmp/claude-501/am/video/full.mp4'
OFF=[9,28,46,65,84,102,121,140]
def digits(f):
    out=[]
    for x0 in (135,554):
        for o in OFF:
            c=f[397:420,x0+o:x0+o+15].min(2)
            out.append((c>190).astype(np.uint8))
    return out
if __name__=='__main__':
    samp=[]
    for t in np.arange(170,9170,37.3):
        b=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',V,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
        f=np.frombuffer(b,np.uint8).reshape(480,854,3)
        samp+=digits(f)
    A=np.array(samp).reshape(len(samp),-1).astype(float)
    np.save('ocr/samp.npy',A)
    print(A.shape)
