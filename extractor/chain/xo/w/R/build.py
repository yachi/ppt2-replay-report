import json,pickle,collections
exec(open('R/seqfn.py').read())
A={j['id']:j for j in map(json.loads,open('A/games.jsonl'))}
B={j['id']:j for j in map(json.loads,open('B/games.jsonl'))}
F=pickle.load(open('R/fuse.pkl','rb'))
GAP=json.load(open('R/gaps.json')); PART=json.load(open('R/part.json')); BAG=json.load(open('R/bag.json'))
TIMER={'g000':90.36,'g001':67.33,'g002':16.40,'g003':10.45,'g004':56.61,'g005':64.91,'g006':147.45,'g007':47.81,'g008':23.81,'g009':44.33,'g010':55.58,'g011':99.63,'g012':54.31,'g013':31.65,'g014':85.11,'g015':33.01,'g016':90.43,'g017':152.08,'g018':74.21,'g019':20.23,'g020':189.91,'g021':39.76,'g022':211.15,'g023':17.85,'g024':108.68,'g025':45.26,'g026':43.33,'g027':23.40,'g028':21.88,'g029':22.06,'g030':49.33,'g031':18.30,'g032':37.20,'g033':74.76,'g034':34.03,'g035':58.56,'g036':136.78,'g037':17.35,'g038':17.56,'g039':53.05,'g040':125.15,'g041':36.78,'g042':36.05,'g043':103.58,'g044':236.63,'g045':62.00,'g046':63.93,'g047':26.46,'g048':61.70,'g049':88.00,'g050':39.50}
CK=['single','double','triple','quad','tss','tsd','tst','tsmini','pc']
WL={'Single':1,'Double':2,'Triple':3}
TS={1:'tss',2:'tsd',3:'tst'}; PL={1:'single',2:'double',3:'triple',4:'quad'}
GAPMIN=4.0
OVR={('g003','p2'):{'lines_cleared':8,'clears.double':1,'max_combo':2,'max_b2b':1}}
def windows(g,p):
  x=GAP[g][p]; w=[(t,t+L) for t,L in x['big'] if L>GAPMIN]
  return w
def inw(t,W): return any(a-0.05<=t<=b+0.05 for a,b in W)
def player(g,p):
  a=A[g][p]; b=B[g][p]; r=F[(g,p)]; d=pickle.load(open(f'R/ev/{g}.pkl','rb'))
  bev=d['b'][p]; trunc=g in PART['trunc']
  W=windows(g,p); x=GAP[g][p]
  if x['tail']>GAPMIN: W.append((d['a_end']-x['tail'],d['a_end']))
  bend=max([0]+bev['locks']+[c['t'] for c in bev['clears']])
  notes=[]; unres=False
  # --- A + banner fusion outside windows; extras -> nearest non-clearing lock
  evs=[dict(e) for e in r['evs']]
  c=collections.Counter(); lines=0; gclr=0
  seqitems=[]
  extra=[e for e in r['extra'] if not inw(e['t'],W)]
  added=0
  for xb in extra:
    n2=1 if xb['mini'] else WL[xb['word'][0]]
    cand=[k for k,e in enumerate(evs) if not e['lines'] and abs(e['t']-xb['t'])<=1.5 and e.get('ban') is None]
    if cand:
      k=min(cand,key=lambda k:abs(evs[k]['t']-xb['t'])); evs[k]['lines']=n2; evs[k]['ban']=xb; evs[k]['xtra']=True
    else: evs.append(dict(t=xb['t'],tl=xb['t'],lines=n2,akind='extra',pc=False,gclr=0,ban=xb,xtra=True)); added+=1
  for e in evs:
    n=e['lines']
    if not n: seqitems.append((e['t'],None)); continue
    bn=e['ban']
    if bn: k='tsmini' if bn['mini'] else TS[min(n,3)]
    else: k=PL[min(n,4)]
    c[k]+=1; lines+=n; gclr+=e.get('gclr',0) or 0
    if e['pc']: c['pc']+=1
    seqitems.append((e['t'],k))
  nx=sum(1 for e in r['extra'] if not inw(e['t'],W))
  pieces=a['pieces']; garb=a['garbage_received_rows']
  spl=dict(pieces=0,lines=0,garb=0,untyped=0)
  if W:
    ban=[bn for bn in r['ban'] if inw(bn['t'],W)]; used=set()
    for cl in bev['clears']:
      if not inw(cl['t'],W): continue
      m=[i for i,bn in enumerate(ban) if i not in used and cl['t']-0.2<=bn['t']<=cl['t']+1.0]
      n=cl['lines']
      if m: used.add(m[0]); k='tsmini' if ban[m[0]]['mini'] else TS[min(n,3)]
      else: k=PL[min(n,4)] if n>=1 else None
      if k is None: continue
      c[k]+=1; lines+=n; gclr+=cl.get('gc',0) or 0; spl['lines']+=n
      if cl.get('pc'): c['pc']+=1
      seqitems.append((cl['t'],k))
    for i,bn in enumerate(ban):
      if i in used or bn.get('cens'): continue
      n2=1 if bn['mini'] else WL[bn['word'][0]]; k='tsmini' if bn['mini'] else TS[n2]
      c[k]+=1; lines+=n2; spl['lines']+=n2; seqitems.append((bn['t'],k))
    clt={cl['t'] for cl in bev['clears'] if inw(cl['t'],W)}
    for t in bev['locks']:
      if inw(t,W):
        spl['pieces']+=1
        if t not in clt: seqitems.append((t,None))
    for gp in bev['gaps']:
      if inw(gp['t0'],W) or inw(gp['t1'],W):
        spl['pieces']+=gp['pieces']; spl['lines']+=gp['lines']; spl['untyped']+=gp['lines']; lines+=gp['lines']; spl['garb']+=gp['garbage']; garb+=gp['garbage']
        seqitems.append((gp['t0'],'BREAK'))
    for t,n in bev['garbage']:
      if inw(t,W): garb+=n; spl['garb']+=n
    pieces+=spl['pieces']
    cov=(not trunc) or all(b2<=bend+3.0 for _,b2 in W)
    wtxt=', '.join(f'{a1:.2f}-{b2:.2f}s' for a1,b2 in W)
    wl=sum(b2-a1 for a1,b2 in W); outdur=max(1e-6,(d['a_end']-d['a_start'])-wl); est=round(a['pieces']/outdur*wl)
    notes.append(f'cross-check: A pace outside the window x window length = ~{est} pieces vs {spl["pieces"]} spliced')
    notes.append(f'A lost the NEXT-queue read in {wtxt}; spliced B events there (+{spl["pieces"]} pieces, +{spl["lines"]} lines of which {spl["untyped"]} untyped, +{spl["garb"]} garbage), T-spins in the window typed by on-screen banners')
    if not cov: unres=True; notes.append(f'B coverage ends at {bend:.2f}s before the window ends: pieces/lines/garbage are LOWER BOUNDS (unresolved)')
  seqitems.sort(key=lambda z:z[0])
  mc,mb=streaks([k for _,k in seqitems])
  if nx: notes.append(f'{nx} T-spin banner(s) with no A clear added ({added} as new events)')
  return dict(pieces=pieces,lines_cleared=lines,garbage_received_rows=garb,garbage_cleared=gclr,clears={k:c[k] for k in CK},max_combo=mc,max_b2b=mb,topped_out=a['topped_out']),notes,unres,bool(W)
FIELDS=['duration_s','pieces','lines_cleared','garbage_received_rows','garbage_cleared']+['clears.'+k for k in CK]+['max_combo','max_b2b','topped_out']
def get(o,f):
  for k in f.split('.'): o=o[k]
  return o
out=[]; stats=collections.Counter(); unres_pg=[]
for g in sorted(A):
  trunc=g in PART['trunc']; dur=TIMER.get(g,A[g]['duration_s'])
  rec={'id':g,'duration_s':dur,'winner':A[g]['winner'],'source':{}}
  gnotes=[]
  if trunc: gnotes.append('B truncated mid-game (end detector misfire on stream video); B values not used')
  if g in TIMER: gnotes.append(f'duration from frozen in-game timer {dur:.2f}s (A {A[g]["duration_s"]}, B {B[g]["duration_s"]})')
  else: gnotes.append('stream video has no in-game timer; duration from A (first queue shift to end)')
  confs=[]
  for p in('p1','p2'):
    v,notes,unres,spliced=player(g,p); v['duration_s']=dur
    a=A[g][p]; b=B[g][p]; bb=dict(b); bb['duration_s']=B[g]['duration_s']; aa=dict(a); aa['duration_s']=A[g]['duration_s']
    for f in FIELDS:
      fv=get(v,f); av=get(aa,f); bv=get(bb,f)
      if f=='duration_s' and g in TIMER: s='manual'
      elif trunc: s='A' if fv==av else 'manual'
      else: s='both' if fv==av==bv else 'A' if fv==av else 'B' if fv==bv else 'manual'
      rec['source'][f'{p}.{f}']=s
      if f!='duration_s' and av!=bv: stats['dis']+=1; stats['dis_unres' if unres else 'dis_res']+=1
      stats[s]+=1
    conf=a['confidence']
    if spliced: conf=min(conf,0.6)
    if unres: conf=min(conf,0.4); unres_pg.append(f'{g}{p}')
    if BAG[g][p]['bad_bags'] and not spliced: notes.append(f'7-bag check has {len(BAG[g][p]["bad_bags"])} bad bag(s) with no long spawn gap; A piece count kept')
    v['confidence']=round(conf,3); v['notes']='; '.join(notes) if notes else 'A events, T-spin type from on-screen banners'
    ov=OVR.get((g,p))
    if ov:
      for f,val in ov.items():
        o=v
        ks=f.split('.')
        for k in ks[:-1]: o=o[k]
        o[ks[-1]]=val; rec['source'][f'{p}.{f}']='manual'
      v['notes']+='; hand-verified frame by frame (g003 p2: TST 222.0, TSD 223.5, single 224.4, double+PC 225.8; A had a phantom double)'
    rec[p]=v; confs.append(conf)
  rec['confidence']=round(min(confs),3); rec['notes']='; '.join(gnotes)
  rec['source']['winner']='both' if A[g]['winner']==B[g]['winner'] else 'A'
  out.append(rec)
with open('reconciled.jsonl','w') as fh:
  for r in out: fh.write(json.dumps(r,ensure_ascii=False)+'\n')
print(stats); print('unresolved', unres_pg)
json.dump(unres_pg,open('R/unresolved.json','w'))   # [uP run] read by tetrio/metrics.py (TJc pasted the printed list)
