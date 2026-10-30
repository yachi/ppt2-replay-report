import sys, json, subprocess, numpy as np
sys.path.insert(0,'.'); import track as T
def feat(path, t):
    W,H=T.W,T.H
    b=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.2f}','-i',path,'-frames:v','1','-vf',f'scale={W}:{H}','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    a=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(float)
    out=[]
    for pl in ('p1','p2'):
        xs,ys=T.coords(T.X0[pl]); reg=a[ys.min():ys.max(), xs.min():xs.max()]
        out.append(round(reg.mean(),1))
    return out
if __name__=='__main__':
    path, seg = sys.argv[1], sys.argv[2]
    g=json.load(open(seg))
    for q in g:
        q['bright']=feat(path, q['start']+2.0)
    json.dump(g, open(seg,'w'))
