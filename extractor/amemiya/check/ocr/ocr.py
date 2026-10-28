import numpy as np,subprocess,json,sys
A=np.load('/private/tmp/claude-501/am/corr/ocr/samp2.npy');C=np.load('/private/tmp/claude-501/am/corr/ocr/C2.npy')
L=['4','3','6','0','4','0','0','5','?','0','7','6','5','2','4','0','0','0','4','4','1','0','9','3']
d=((A[:,None,:]-C[None])**2).sum(2);lab=d.argmin(1)
T=[];TL=[]
for j in range(24):
    if L[j]=='?':continue
    if L[j]=='3':
        U=A[lab==j].reshape(-1,23,15); f=U[:,4:9,1:5].sum((1,2))+U[:,13:19,1:5].sum((1,2))
        for lb,m in (('3',f<26),('8',f>=26)):
            if m.any(): T.append(U[m].mean(0).ravel());TL.append(lb)
    else: T.append(C[j]);TL.append(L[j])
T=np.array(T)
OFF=[9,28,46,65,84,102,120,140]
def read(f):
    out=[]
    for x0 in (135,554):
        s='';worst=0
        for o in OFF:
            v=(f[397:420,x0+o:x0+o+15].min(2)>190).astype(float).ravel()
            dd=((T-v)**2).sum(1);k=dd.argmin();s+=TL[k];worst=max(worst,dd[k])
        out.append((s,worst))
    return out
if __name__=='__main__':
    V='/private/tmp/claude-501/am/video/full.mp4'
    t0,t1,name=float(sys.argv[1]),float(sys.argv[2]),sys.argv[3]
    p=subprocess.Popen(['ffmpeg','-v','error','-ss',str(t0),'-i',V,'-t',str(t1-t0),'-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    res=[];k=0
    while True:
        b=p.stdout.read(854*480*3)
        if len(b)<854*480*3:break
        f=np.frombuffer(b,np.uint8).reshape(480,854,3)
        r=read(f);res.append((round(t0+k/30,3),r[0][0],float(r[0][1]),r[1][0],float(r[1][1])));k+=1
    json.dump(res,open(f'/private/tmp/claude-501/am/corr/ocr/{name}.json','w'))
