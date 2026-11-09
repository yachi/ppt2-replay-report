# R/kofinal.py (port addition, run after R/evrun.py): count the winner's last piece, the one locked at or before
# the KO frame. A's last spawn interval (sp[-1], KO) is never tallied by A/analyze.py. The piece counts as locked
# when its clear flashes (white rows from sp[-1] to KO+1 s) or the next spawn shows after sp[-1] and by KO+3 frames.
# Lines = flash rows (cap 4); fuse.py types a T-spin from the banner as for any A clear.
import sys,json,pickle,numpy as np
sys.path.insert(0,'A'); import analyze as Am
A=[json.loads(l) for l in open('A/games.jsonl')]
log=[]
for a in A:
  gid=a['id']; w=a.get('winner')
  if not w or not a.get('end_s'): continue
  ev=pickle.load(open(f'R/ev/{gid}.pkl','rb'))
  if ev.get('kofinal') is not None: continue
  d=np.load(f'A/feat/{gid}.npz'); t0=float(d['t0']); hi=len(d['grid'])
  end=int(round((a['end_s']-t0)*30)); st=int(round((a['start_s']-t0)*30)); p=0 if w=='p1' else 1
  sp,_,_=Am.spawns(d['nxt'][:,p],st-2,end); ls=sp[-1]
  sp2,_,_=Am.spawns(d['nxt'][:,p],st-2,min(hi,end+30))
  nxt=[f for f in sp2 if ls<f<=end+3]
  g=d['grid'][:,p]; wr,_=Am.white_rows(g,ls,min(hi,end+30)); n=min(len(wr),4)
  rec=None
  if n or nxt:
    Bk=Am.board_at(g,ls+1,min(max(ls+2,end-3),ls+12),np.zeros((Am.TOP,10),np.uint8))
    gclr=sum(1 for r in wr[:4] if r<Am.TOP and (Bk[r]==Am.GREY).any())
    kind={0:'lock',1:'single',2:'double',3:'triple',4:'quad'}[n]
    rec=dict(t=round(t0+ls/30,2),lines=n,kind=kind,garbage=0,gclr=gclr,pc=False,ko=True)
    ev['a'][w].append(rec); a[w]['pieces']+=1
  ev['kofinal']=rec; pickle.dump(ev,open(f'R/ev/{gid}.pkl','wb'))
  log.append((gid,w,ls-end,n,nxt and nxt[0]-end,bool(rec)))
  print(gid,w,'last spawn',ls-end,'flash',n,'next spawn',nxt,'-> +1' if rec else '-> none',flush=True)
with open('A/games.jsonl','w') as fh:
  for a in A: fh.write(json.dumps(a,ensure_ascii=False)+'\n')
print(sum(1 for x in log if x[-1]),'of',len(log),'winners gain the KO piece')
