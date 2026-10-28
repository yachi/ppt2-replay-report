# Score reader for the uP capture. Templates: k-means centroids (C.npy, cent2.png, labelled by eye) + '1' and '7' cut from
# f170.png, matched with +-2 px shift tolerance (min distance over 5x5 offsets). ' ' = blank, '?' = saturated cell.
import numpy as np
from PIL import Image
D='/private/tmp/claude-501/uP/w/ocr'
XS=[150,168,186,204,223,242,260,279]; P=2
C=np.load(f'{D}/C.npy')
LAB={2:'3',3:'0',11:'2',16:'4',19:'9',21:'8',18:'6',4:'5'}
_f=np.asarray(Image.open(f'{D}/f170.png').convert('RGB'))
def _cell(f,i,dx=0): x=XS[i]+dx; return (f[392:415,x-2:x+14].min(2)>190).astype(float)
T=[C[k].reshape(23,16) for k in LAB]; TL=[LAB[k] for k in LAB]
T+= [_cell(_f,5),_cell(_f,7),np.zeros((23,16)),np.ones((23,16))]; TL+=['7','1',' ','?']
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
