import numpy as np, sys
def hsv(rgb):
    rgb=rgb.astype(float)/255; mx=rgb.max(-1); mn=rgb.min(-1); d=mx-mn
    s=np.where(mx>0,d/np.maximum(mx,1e-9),0)
    r,g,b=rgb[...,0],rgb[...,1],rgb[...,2]
    h=np.zeros_like(mx)
    dd=np.maximum(d,1e-9)
    h=np.where(mx==r,((g-b)/dd)%6,np.where(mx==g,(b-r)/dd+2,(r-g)/dd+4))*60
    return h,s,mx
def classify(rgb,vthr=0.38,sthr=0.25):
    h,s,v=hsv(rgb)
    out=np.full(h.shape,'?',dtype='<U1')
    out[:]='T'
    out[h<260]='J'; out[h<210]='I'; out[h<160]='S'; out[h<70]='O'; out[h<40]='L'; out[(h<15)|(h>=330)]='Z'
    out[s<sthr]='G'; out[v<vthr]='.'
    return out
if __name__=='__main__':
    gid,pl,a,b=sys.argv[1],int(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])
    z=np.load(f'/private/tmp/claude-501/sk/metrics/B/cells/{gid}.npz'); C=z['cells']; t0=float(z['t0'])
    last=None
    for i in range(int((a-t0)*30),min(len(C),int((b-t0)*30))):
        g=classify(C[i,pl]); key=g.tobytes()
        if key==last: continue
        last=key
        top=max([r for r in range(20) if (g[r]!='.').any()],default=0)
        print(f'--- f{i} t={t0+i/30:.2f}')
        for r in range(top,-1,-1): print(''.join(g[r]))
