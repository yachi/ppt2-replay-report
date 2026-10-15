import sys, json, numpy as np
sys.path.insert(0,'.')
from seq import frames
R='/Users/yachi/github/tetrio-replay-report/pipeline/openers/'
def occ(rows):
    g=[''.join('#' if c!='.' else '.' for c in r) for r in rows]
    g=['.'*10]*(8-len(g))+g if len(g)<8 else g[-8:]
    return g
def mir(rows): return [r[::-1].translate(str.maketrans('LJSZ','JLZS')) for r in rows]
def dist(a,b): return sum(x!=y for ra,rb in zip(a,b) for x,y in zip(ra,rb))
pages=[]
for p in json.load(open(R+'opener-fields.json'))['pages']:
    n=sum(c!='.' for r in p['rows'] for c in r); pages.append((p['name'],n,occ(p['rows']),occ(mir(p['rows']))))
for o in json.load(open(R+'wiki-openers.json'))['openers']:
    for f in o['fields']:
        pages.append(('WIKI '+o['wiki']+' / '+f['heading'],f['cells'],occ(f['rows']),occ(mir(f['rows']))))
for nm,rows in json.load(open('routeboards.json')):
    if 'bag1' not in nm: continue
    rr=[r.replace('-','.').replace('U','.') for r in rows if r.strip('-')]
    rr=[r for r in rr if r.strip('.')] 
    n=sum(c!='.' for r in rr for c in r)
    pages.append(('ROUTE '+nm,n,occ(rr),occ(mir(rr))))
def nearest(rows,k=4):
    n=sum(c!='.' for r in rows for c in r); g=occ(rows); out=[]
    for name,pn,a,b in pages:
        if pn!=n: continue
        d0,d1=dist(g,a),dist(g,b); out.append((min(d0,d1),name,'mirror' if d1<d0 else 'drawn'))
    out.sort(); return out[:k]
def settled(path,t0,dur,K=9):
    fr=list(frames(path,t0,dur)); boards=[]
    for i in range(len(fr)-K):
        g=[]
        for r in range(20):
            row=''
            for c in range(10):
                v=fr[i][r][c]
                ok=v not in '.G' and all(fr[i+j][r][c]==v for j in range(K))
                row+=v if ok else '.'
            g.append(row)
        n=sum(ch!='.' for row in g for ch in row)
        top=max([r for r in range(20) if g[r]!='.'*10],default=-1)
        rows=[g[r] for r in range(top,-1,-1)]
        if not boards or boards[-1][2]!=rows: boards.append((t0+i/30,n,rows))
    return boards
if __name__=='__main__':
    vid,t0=sys.argv[1],float(sys.argv[2])
    bs=settled(f'vid/{vid}.mp4',t0,float(sys.argv[3]) if len(sys.argv)>3 else 7)
    for t,n,rows in bs:
        print(f'--- t={t:.2f} n={n}'); print('\n'.join(rows))
        if n in (24,28) and all(c not in 'G' for r in rows for c in r):
            for m in nearest(rows): print('   ',m)
