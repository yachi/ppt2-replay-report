import json,sys,pickle
sys.argv=['x']
exec(open('R/events.py').read().split("if __name__")[0])
import numpy as np
NAME={1:'single',2:'double',3:'triple',4:'quad'}
def b_clears(gid):
  g=G[gid]; o,det=Bm.run_game(g); t0=float(np.load(f'B/cells2/{gid}.npz')['t0'])
  res={}
  for k in('p1','p2'):
    r=det[k]; ev=[]
    for L in r['locks']:
      n=L['lines']
      if not n: continue
      ts=Bm.tspin_kind(L['piece'],L['pre'],n) if L['type']=='T' else None
      if ts=='mini' and n==1: kind='tsmini'
      elif ts: kind={1:'tss',2:'tsd',3:'tst'}.get(n,'tst')
      else: kind=NAME[min(n,4)]
      ev.append(dict(t=round(t0+L['f']/30,2),lines=n,kind=kind,pc=bool(L.get('pc')),gc=L.get('gc',0),src='lock'))
    for e in r['events']:
      if e['kind']=='clear' and e.get('orphan'): ev.append(dict(t=round(t0+e['f']/30,2),lines=e['lines'],kind='orphan',pc=e['pc'],gc=e['garbage_cleared'],src='orphan'))
    gaps=[dict(t0=round(t0+gp['since']/30,2),t1=round(t0+gp['f']/30,2),pieces=gp['pieces'],lines=gp['lines'],garbage=gp['garbage'],flash=gp['flash']) for gp in r['gaps']]
    locks=[round(t0+L['f']/30,2) for L in r['locks']]
    res[k]=dict(clears=sorted(ev,key=lambda e:e['t']),gaps=gaps,locks=locks,garbage=[(round(t0+e['f']/30,2),e['g']) for e in r['events'] if e['kind']=='garbage'])
  return res,o
gid_list=sys.argv[1:] if len(sys.argv)>1 else sorted(G)
