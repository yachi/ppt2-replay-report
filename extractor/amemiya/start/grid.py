import subprocess, numpy as np, sys, json
W,H=854,480
X0,Y0,CW=137.0,391.0,16.0  # [am port: was 142.5,389.0,15.7]
def grids(path,fps=10):
    p=subprocess.Popen(['ffmpeg','-v','error','-i',path,'-vf',f'fps={fps}','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    xs=[int(X0+CW*(c+.5)) for c in range(10)]; ys=[int(Y0-CW*(r+.5)) for r in range(22)]
    i=0
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        a=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(int)
        g=np.zeros((22,10),int)
        for r,y in enumerate(ys):
            for c,x in enumerate(xs):
                g[r,c]=a[y-2:y+3,x-2:x+3].mean()
        yield i/fps,g,a
        i+=1
if __name__=='__main__':
    out=[]
    for t,g,a in grids(sys.argv[1]):
        out.append([t,(g[:20]>90).sum().item(),g[:20].tolist()])
    json.dump(out,open(sys.argv[2],'w'))
