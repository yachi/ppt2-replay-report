# Score reader for the 2026-10-28 uploads ([ach port]: uP's k-means C.npy replaced by T.npy from mktpl.py, digits
# labelled by eye on s0..s5.png). Same cell geometry as uP: 8 digits, rows 392:415, left edges XS (p1), p2 = +411;
# matched with +-2 px shift tolerance (min distance over 5x5 offsets). ' ' = blank, '?' = saturated cell.
import numpy as np
D='/tmp/claude-0/r6/w/ocr'
XS=[150,168,186,204,223,242,260,279]; P=2
T=list(np.load(f'{D}/T.npy')); TL=[str(d) for d in range(10)]
T+= [np.zeros((23,16)),np.ones((23,16))]; TL+=[' ','?']
T=np.array(T)
def classify(cells):
    """cells: n,27,20 binary (padded). -> labels, min distance"""
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
