import json,pickle,collections,numpy as np
exec(open('R/banan.py').read())
A={j['id']:j for j in map(json.loads,open('A/games.jsonl'))}
WL={'Single':1,'Double':2,'Triple':3}
def a_locks(ev):
  return [e for e in ev if e.get('kind')!='hold-empty']
def fuse(gid,p):
  z=np.load(f'R/ban/{gid}.npz'); t0=float(z['t0']); d=pickle.load(open(f'R/ev/{gid}.pkl','rb'))
  T1=tspins(z[p],t0); M1=tspins(z[p+'_Mini'],t0)
  def repl(e,other):  # segment cut by the other banner type taking over
    end=e['t']+e['life']; return any(abs(o['t']-end)<=0.3 for o in other)
  ts=[dict(e,mini=False) for e in T1 if e['acc'] or (e['life']>=0.3 and repl(e,M1))]
  ms=[dict(e,mini=True) for e in M1 if e['acc'] or (e['life']>=0.3 and repl(e,T1))]
  tend=t0+len(z[p])/30   # censored-banner rule (endfix rebuild)
  cens=lambda e: (not e['acc']) and e['life']>=0.3 and e['t']+e['life']>=tend-0.15
  ts+=[dict(e,mini=False,cens=True) for e in T1 if not(e['acc'] or (e['life']>=0.3 and repl(e,M1))) and cens(e)]
  ms+=[dict(e,mini=True,cens=True) for e in M1 if not(e['acc'] or (e['life']>=0.3 and repl(e,T1))) and cens(e)]
  # drop mini onsets coinciding with full onsets (should not happen)
  ban=sorted(ts+ms,key=lambda e:e['t'])
  for e in ban:
    i=int(round((e['t']-t0)*30))
    if e['mini']: e['word']=('Single',1.0)
    else:
      w=max(WL,key=lambda w:z[p+'_'+w][i:i+15].max()); e['word']=(w,round(float(z[p+'_'+w][i:i+15].max()),2))
  L=a_locks(d['a'][p]); evs=[]
  for k,e in enumerate(L):
    tn=L[k+1]['t'] if k+1<len(L) else e['t']+1
    evs.append(dict(t=e['t'],tl=tn,lines=e.get('lines',0),akind=e.get('kind'),pc=e.get('pc',False),gclr=e.get('gclr',0),ban=None))
  extra=[]
  for b in ban:
    m=[k for k,e in enumerate(evs) if e['lines'] and e['ban'] is None and e['t']-0.1<=b['t']<=e['tl']+0.7]
    if not m:
      m=[k for k,e in enumerate(evs) if e['lines'] and e['ban'] is None and abs(e['tl']-b['t'])<=1.5]
      m=sorted(m,key=lambda k:abs(evs[k]['tl']-b['t']))[:1]
      if m: b['loose']=True
    if m: evs[m[-1]]['ban']=b
    elif not b.get('cens'): extra.append(b)
  return evs,extra,ban
def kinds(evs,extra,use_extra=True):
  c=collections.Counter(); lines=0; seq=[]
  for e in evs:
    n=e['lines']
    if not n: seq.append(None); continue
    b=e['ban']
    if b:
      if b['mini']: k='tsmini'
      else: k={1:'tss',2:'tsd',3:'tst'}[WL[b['word'][0]]]
      n2=n
      if not b['mini']: k={1:'tss',2:'tsd',3:'tst'}[min(n,3)]
    else: k={1:'single',2:'double',3:'triple',4:'quad'}[min(n,4)]; n2=n
    c[k]+=1; lines+=n2; seq.append((e['t'],k,n2,e['pc']))
    if e['pc']: c['pc']+=1
  if use_extra:
    for b in extra:
      k='tsmini' if b['mini'] else {1:'tss',2:'tsd',3:'tst'}[WL[b['word'][0]]]; n2=1 if b['mini'] else WL[b['word'][0]]
      c[k]+=1; lines+=n2
      # insert into seq by time
      seq.append((b['t'],k,n2,False))
  return c,lines,seq
if __name__=='__main__':
  out={}
  for gid in sorted(A):
    for p in('p1','p2'):
      evs,extra,ban=fuse(gid,p); out[(gid,p)]=dict(evs=evs,extra=extra,ban=ban)
  pickle.dump(out,open('R/fuse.pkl','wb'))
  tot=collections.Counter()
  for (g,p),r in out.items():
    tot['ban']+=len(r['ban']); tot['extra']+=len(r['extra']); tot['mini']+=sum(b['mini'] for b in r['ban'])
    tot['A_ts_nob']+=sum(1 for e in r['evs'] if e['akind'] in('tss','tsd','tst','tsmini') and not e['ban'])
    tot['wordmismatch']+=sum(1 for e in r['evs'] if e['ban'] and not e['ban']['mini'] and WL[e['ban']['word'][0]]!=e['lines'])
  print(tot)
