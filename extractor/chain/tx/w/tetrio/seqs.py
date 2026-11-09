# Rebuild the referee's per-lock fused sequence (R/build.py player()) WITHOUT writing reconciled.jsonl,
# carrying line count, pc flag and gclr per clear. Control: counts must reproduce reconciled.jsonl.
import json,pickle,collections,re
src=open('R/build.py').read().split('FIELDS=')[0]
# carry (t, kind, lines, pc, gclr, origin) instead of (t, kind)
src=src.replace("seqitems.append((e['t'],None)); continue","seqitems.append((e['t'],None,0,False,0,'A')); continue")
src=src.replace("seqitems.append((e['t'],k))","seqitems.append((e['t'],k,n,bool(e['pc']),e.get('gclr',0) or 0,'A'))")
src=src.replace("seqitems.append((cl['t'],k))","seqitems.append((cl['t'],k,n,bool(cl.get('pc')),cl.get('gc',0) or 0,'B'))")
src=src.replace("seqitems.append((bn['t'],k))","seqitems.append((bn['t'],k,n2,False,0,'ban'))")
src=src.replace("if t not in clt: seqitems.append((t,None))","if t not in clt: seqitems.append((t,None,0,False,0,'B'))")
src=src.replace("seqitems.append((gp['t0'],'BREAK'))","seqitems.append((gp['t0'],'BREAK',gp['lines'],False,0,'gap'))")
src=src.replace("mc,mb=streaks([k for _,k in seqitems])","mc,mb=streaks([z[1] for z in seqitems]); SEQ[(g,p)]=list(seqitems)")
assert src.count('SEQ[(g,p)]')==1 and src.count("'gap'))")==1
SEQ={}
exec(src)
out={}
for g in sorted(A):
  for p in('p1','p2'):
    v,notes,unres,spl=player(g,p)
    out[(g,p)]=dict(seq=SEQ[(g,p)],v=v,unres=unres,spliced=spl)
pickle.dump(out,open('tetrio/seqs.pkl','wb'))
# control
R={j['id']:j for j in map(json.loads,open('reconciled.jsonl'))}
bad=[]
for (g,p),o in out.items():
  r=R[g][p]; v=o['v']
  for f in ['pieces','lines_cleared','garbage_received_rows','garbage_cleared','max_combo','max_b2b']:
    if v[f]!=r[f]: bad.append((g,p,f,v[f],r[f]))
  for k,x in v['clears'].items():
    if x!=r['clears'][k]: bad.append((g,p,k,x,r['clears'][k]))
  # sequence-level control: clear kinds in seq reproduce clears dict
  c=collections.Counter(z[1] for z in o['seq'] if z[1] not in (None,'BREAK'))
  c['pc']=sum(1 for z in o['seq'] if z[3])
  for k in v['clears']:
    if c[k]!=v['clears'][k]: bad.append((g,p,'seq.'+k,c[k],v['clears'][k]))
print('player-games',len(out),'mismatches vs reconciled',len(bad)); print(bad[:20])
