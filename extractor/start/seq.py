import subprocess, numpy as np, sys, colorsys
W,H=854,480
X0,Y0,CW=142.5,389.0,15.7
xs=[int(X0+CW*(c+.5)) for c in range(10)]; ys=[int(Y0-CW*(r+.5)) for r in range(20)]
def col(rgb):
    r,g,b=[v/255 for v in rgb]; h,s,v=colorsys.rgb_to_hsv(r,g,b)
    if v<0.38: return '.'
    if s<0.25: return 'G'  # garbage/grey
    h*=360
    if h<15 or h>=330: return 'Z'
    if h<40: return 'L'
    if h<70: return 'O'
    if h<160: return 'S'
    if h<210: return 'I'
    if h<260: return 'J'
    return 'T'
def frames(path,t0,dur,fps=30):
    p=subprocess.Popen(['ffmpeg','-v','error','-ss',str(t0),'-t',str(dur),'-i',path,'-vf',f'fps={fps}','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        a=np.frombuffer(b,np.uint8).reshape(H,W,3)
        yield [[col(a[y-2:y+3,x-2:x+3].reshape(-1,3).mean(0)) for x in xs] for y in ys]
def stable(path,t0,dur,k=4):
    fr=list(frames(path,t0,dur)); out=[]; last=None
    for i in range(len(fr)-k):
        prev=out[-1][1] if out else [['.']*10 for _ in range(20)]
        g=[[fr[i][r][c] if all(fr[i+j][r][c]==fr[i][r][c] for j in range(k)) else prev[r][c] for c in range(10)] for r in range(20)]
        key=tuple(map(tuple,g))
        if key!=last:
            out.append((t0+i/30,g)); last=key
    return out
if __name__=='__main__':
    vid,t0,dur=sys.argv[1],float(sys.argv[2]),float(sys.argv[3])
    for t,g in stable(f'vid/{vid}.mp4',t0,dur):
        n=sum(c!='.' for r in g for c in r)
        top=max([r for r in range(20) if any(c!='.' for c in g[r])],default=-1)
        print(f'--- t={t:.2f} n={n}')
        for r in range(top,-1,-1): print(''.join(g[r]))
