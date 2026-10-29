import subprocess,numpy as np
V='/tmp/claude-0/fr/video/full.mp4'
OFF=[9,28,46,65,84,102,121,140]
samp=[]
for t in np.arange(1515,5560,11.3):
    b=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',V,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    f=np.frombuffer(b,np.uint8).reshape(480,854,3)
    for x0 in (135,554):
        for o in OFF:
            samp.append((f[397:420,x0+o:x0+o+15].min(2)>190).astype(np.uint8).ravel())
A=np.array(samp,float);np.save('samp.npy',A);print(A.shape)
