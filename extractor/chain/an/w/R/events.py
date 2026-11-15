import sys,json,importlib.util,numpy as np
sys.path.insert(0,'A'); sys.path.insert(0,'B')
def load(name,path):
  s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
Am=load('A_an','A/analyze.py'); Bm=load('B_ex','B/extract_b.py')
G={g['id']:g for g in json.load(open('../games.json'))}
def a_events(gid):
  d=np.load(f'A/feat/{gid}.npz'); t0=float(d['t0'])
  meta=G[gid]
  # replicate analyse() but keep events
  r=Am.analyse.__wrapped__(f'A/feat/{gid}.npz',meta) if hasattr(Am.analyse,'__wrapped__') else None
  return t0
def a_run(gid):
  import io,contextlib
  meta=G[gid]; d=np.load(f'A/feat/{gid}.npz'); t0=float(d['t0'])
  # monkeypatch pop of events: call analyse_player directly like analyse()
  FPS=Am.FPS; lo=max(0,int(round((meta['start_s']-0.3-t0)*FPS))); hi=len(d['grid'])
  s0=[]
  for p in (0,1):
    sp,_,_=Am.spawns(d['nxt'][:,p],lo,hi)
    if sp: s0.append(sp[0])
  start=min(s0); end,loser=Am.find_end(d['border'],start+60,hi); end_f=end if end is not None else hi
  out={}
  for p in (0,1):
    st,sp=Am.analyse_player(d,p,start-2,end_f,[])
    out['p%d'%(p+1)]=[dict(t=round(t0+e['t']/FPS,2),**{k:v for k,v in e.items() if k not in('t','cells','j')}) for e in st['_events']]
  return out,t0+start/FPS,t0+end_f/FPS
def b_run(gid):
  g=G[gid]; o,det=Bm.run_game(g); z=np.load(f'B/cells2/{gid}.npz'); t0=float(z['t0'])
  out={}
  for k in('p1','p2'):
    r=det[k]; ev=[]
    for e in r['events']: ev.append(dict(t=round(t0+e['f']/30,2),**{x:y for x,y in e.items() if x!='f'}))
    for gp in r['gaps']: ev.append(dict(t=round(t0+gp['f']/30,2),kind='GAP',since=round(t0+gp['since']/30,2),pieces=gp['pieces'],lines=gp['lines'],garbage=gp['garbage'],flash=gp['flash']))
    for L in r['locks']:
      pass
    ev.sort(key=lambda e:e['t']); out[k]=ev
  return out,o
if __name__=='__main__':
  gid=sys.argv[1]; who=sys.argv[2] if len(sys.argv)>2 else 'p1'
  a,s,e=a_run(gid); print('A start %.2f end %.2f'%(s,e))
  for x in a[who]:
    if x.get('kind')!='lock' or x.get('garbage') or x.get('flag'): print('A',x)
  b,o=b_run(gid)
  for x in b[who]:
    if x['kind']!='lock': print('B',x)
