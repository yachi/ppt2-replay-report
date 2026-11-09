# Score reader for the Gg capture (remapped to uP geometry). [Gg port of the uP reader] Templates: per-digit means from
# tmpl.py (T.npy, TL.txt: 5 hand-read frames) instead of uP's k-means centroids; same cell rule, same +-2 px shift tolerance.
import numpy as np
D='/private/tmp/claude-501/Gg/w/ocr'
XS=[150,168,186,204,223,242,260,279]; P=2
T=list(np.load(f'{D}/T.npy').reshape(-1,23,16)); TL=list(open(f'{D}/TL.txt').read().strip())
T+=[np.zeros((23,16)),np.ones((23,16))]; TL+=[' ','?']
T=np.array(T)
def classify(cells):
    n=len(cells); best=np.full((n,len(T)),1e9)
    for dy in range(2*P+1):
        for dx in range(2*P+1):
            w=cells[:,dy:dy+23,dx:dx+16].reshape(n,1,-1).astype(float)
            best=np.minimum(best,((w-T.reshape(1,len(T),-1))**2).sum(2))
    k=best.argmin(1); return [TL[i] for i in k], best.min(1)
def cells_of(f):
    out=[]
    for dx in (0,411):
        for x in XS: out.append((f[392-P:415+P,x+dx-2-P:x+dx+14+P].min(2)>190))
    return np.array(out)
def read(f):
    lab,dm=classify(cells_of(f))
    return [(''.join(lab[:8]),float(dm[:8].max())),(''.join(lab[8:]),float(dm[8:].max()))]
