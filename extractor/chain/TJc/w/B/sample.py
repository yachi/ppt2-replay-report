# Extractor B, stage 1: decode a game window at 30 fps and store per-cell mean RGB for both boards.
import subprocess, numpy as np, sys, json, os
W,H=854,480
X0={'p1':142.5,'p2':554.0}; Y0=389.0; CW=15.7
def coords(x0):
    xs=np.array([int(round(x0+CW*(c+.5))) for c in range(10)])
    ys=np.array([int(round(Y0-CW*(r+.5))) for r in range(20)])
    return xs,ys
def sample(g,outdir,pad=1.0):
    t0=max(0.0,g['start_s']-pad); t1=g['end_upper_s']+pad
    cmd=['ffmpeg','-v','error','-ss',f'{t0:.3f}','-i',g['path'],'-t',f'{t1-t0:.3f}','-vf','fps=30','-f','rawvideo','-pix_fmt','rgb24','-']
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE)
    C={k:coords(v) for k,v in X0.items()}
    outs=[]; borders=[]
    BY=np.arange(85,381,12)
    off=np.arange(-3,4)
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        a=np.frombuffer(b,np.uint8).reshape(H,W,3)
        fr=np.zeros((2,20,10,3),np.uint8)
        for k,pl in enumerate(('p1','p2')):
            xs,ys=C[pl]
            Y=(ys[:,None]+off[None,:])  # 20x7
            X=(xs[:,None]+off[None,:])  # 10x7
            patch=a[Y[:,None,:,None],X[None,:,None,:]]  # 20,10,7,7,3
            fr[k]=patch.reshape(20,10,49,3).mean(2).astype(np.uint8)
        outs.append(fr)
        bd=np.zeros((2,2,BY.size,3),np.uint8)
        for k,pl in enumerate(('p1','p2')):
            for side,xx in enumerate((int(X0[pl]-4),int(X0[pl]+157+3))):
                pt=a[BY[:,None]+np.array([-1,0,1])[None,:]][:,:,xx-1:xx+2]  # n,3,3,3
                bd[k,side]=pt.reshape(BY.size,9,3).mean(1).astype(np.uint8)
        borders.append(bd)
    p.wait()
    arr=np.stack(outs) if outs else np.zeros((0,2,20,10,3),np.uint8)
    np.savez_compressed(os.path.join(outdir,g['id']+'.npz'),cells=arr,borders=np.stack(borders) if borders else np.zeros((0,2,2,25,3),np.uint8),t0=t0,fps=30)
    return arr.shape
if __name__=='__main__':
    games={g['id']:g for g in json.load(open('/tmp/claude-0/chain/kbb/games.json'))}
    outdir='/tmp/claude-0/chain/kbb/w/B/cells2'
    for gid in sys.argv[1:]:
        if os.path.exists(os.path.join(outdir,gid+'.npz')): continue
        print(gid,sample(games[gid],outdir),flush=True)
