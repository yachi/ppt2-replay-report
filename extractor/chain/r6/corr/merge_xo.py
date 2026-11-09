# [xo, r6: twelve groups plus the PC group; a hidden PC on an event a checker also corrected sets pc on that correction] Merge checker proposals (b*), skeptic verdicts (v*) and the hidden-PC frame check -> corr/event-corrections.json + corr/cells.json
import json
O='/tmp/claude-0/r6/corr/out'; C='/tmp/claude-0/r6/corr'
WAS={}
def tag(x,s): x=dict(x); x['source']=f"{s}: {x.get('source','')}"; return x
ev,cells=[],[]
for k in [str(i) for i in range(12)]+['pc']:
    b=json.load(open(f'{O}/b{k}.json')); V={v['ref']:v for v in json.load(open(f'{O}/v{k}.json'))}
    for pre,lst,out in (('e','event_corrections',ev),('c','cell_edits',cells)):
        for i,e in enumerate(b[lst]):
            r=V[f'{pre}{i}']
            if r['verdict']=='reject': continue
            x={**e,**(r.get('amended') or {})}
            out.append(tag(x,f"b{k} frame check, {'verified' if r['verdict']=='keep' else 'amended by skeptic'}"))
    for r in V.values():
        if r['verdict']=='missed':
            p=r['proposal']; src=f"v{k} skeptic, missed by b{k}"
            if (r['ref'],p.get('field'))==('n327','pieces'): print('dropped (B splice already counted):',p); continue
            if 'field' in p: cells.append(tag(p,src)); continue
            if p.get('op')=='add_multi':
                ev.extend(tag(dict(id=p['id'],side=p['side'],op='add',**w,source=p.get('source','')),src) for w in p['events']); continue
            if 'edits' in p:
                ev.extend(tag(dict(id='n005',side='p2',**w,source=p.get('source','')),src) for w in p['edits']); assert r['ref']=='n216'; continue
            ev.append(tag(p,src))
def touched(e):
    keys=set()
    for x in ev:
        if (x['id'],x['side'])!=(e['id'],e['side']): continue
        if x['op']=='replace_window':
            if x['t']<=e['t']<=x['t_end']: return True
        elif abs(x['t']-e['t'])<0.005: return True
    return False
big=json.load(open(f'{O}/big.json'))
for lst,out in (('event_corrections',ev),('cell_edits',cells)):
    out+=[tag(e,'big-jump frame check (one reader, no skeptic)') for e in big[lst]]
hp=json.load(open(f'{C}/hidden_pc.json'))
for e in hp:
    hit=[x for x in ev if (x['id'],x['side'])==(e['id'],e['side']) and x['op']!='replace_window' and abs(x['t']-e['t'])<0.005]
    if hit:
        for x in hit:
            if x['op']=='retype': x['pc']=1; x['source']+=f"; PC: {e['source']}"
        continue
    if touched(e): print('hidden PC inside a replaced window, check by hand:',e['id'],e['side'],e['t']); continue
    ev.append(tag(e,'hidden-PC frame check'))
for e in ev:
    e.pop('n',None); e['t']=round(e['t'],2)
    if e['op']=='retype' and 'was' not in e: e['was']=WAS[(e['id'],e['side'],round(e['t'],2))]
    if e['op']=='retype' and e['was'][0] in (None,'BREAK'):
        e['op']='replace_window'; e['t_end']=e['t']
        e['events']=[dict(t=e['t'],kind=e.pop('kind'),lines=e.pop('lines'),pc=e.pop('pc',0),gc=e.pop('gc',0))]
        e['was_old']=[[e['t'],e['was'][0],e['was'][1]]]; e.pop('was')
    if e['op']=='remove' and e['was'][0] in (None,'BREAK'):
        e['op']='replace_window'; e['t_end']=e['t']; e['events']=[]
        e['was_old']=[[e['t'],e['was'][0],e['was'][1]]]; e.pop('was')
PRE=json.load(open('/tmp/claude-0/r6/w/chain/r6/w/tetrio/cseq.json'))
for e in ev:
    if e['op']=='replace_window' and 'was_old' not in e:
        for f in ('kind','lines','pc','gc','was'): e.pop(f,None)
        e['was_old']=[[z[0],z[1],z[2]] for z in PRE[f"{e['id']} {e['side']} pre"] if e['t']-0.005<=z[0]<=e['t_end']+0.005]
        print('was_old filled from chain:',e['id'],e['side'],e['t'],e['was_old'])
x2=[]
for e in ev:
    if e['op']=='replace_window' and not e['was_old']:
        x2+=[dict(id=e['id'],side=e['side'],op='add',t=round(w['t'],2),kind=w['kind'],lines=w['lines'],pc=w['pc'],gc=w['gc'],source=e['source']) for w in e['events']]
    else: x2.append(e)
ev=x2
# [r6, after validate.py] (1) bpc corrections that another group already made: inside its replace_window, or an add of
# the same kind within 0.15 s of its add. Both groups read the same frames; keep one.
def grp(e): return e['source'].split(' ')[0]
def dup(e):
    if grp(e)!='bpc': return False
    for w in ev:
        if w is e or grp(w)=='bpc' or (w['id'],w['side'])!=(e['id'],e['side']): continue
        if w['op']=='replace_window' and w['t_end']>w['t'] and w['t']-0.005<=e['t']<=w['t_end']+0.005: return True
        if w['op']=='add' and e['op']=='add' and w['kind']==e['kind'] and abs(w['t']-e['t'])<0.15: return True
    return False
for e in [e for e in ev if dup(e)]: print('dropped, made by another group:',e['id'],e['side'],e['op'],e['t']); ev.remove(e)
# (2) the chain holds several events at one t. A one-event replace_window keeps the others; retypes/removes that cannot
# pick their event are folded into one replace_window over that t, each applied to the first event its 'was' matches.
def at(e): return [[z[0],z[1],z[2],z[3],z[4]] for z in PRE[f"{e['id']} {e['side']} pre"] if abs(z[0]-e['t'])<0.005]
for e in ev:
    if e['op']=='replace_window' and e['t_end']==e['t'] and len(e['was_old'])==1:
        cur=at(e)
        if len(cur)>1:
            k=next(i for i,z in enumerate(cur) if [z[1],z[2]]==e['was_old'][0][1:])
            e['events']+= [dict(t=z[0],kind=z[1],lines=z[2],pc=z[3],gc=z[4]) for i,z in enumerate(cur) if i!=k]
            e['was_old']=[[z[0],z[1],z[2]] for z in cur]; print('same-t window widened to the chain events:',e['id'],e['side'],e['t'])
amb={}
for e in ev:
    if e['op'] in ('retype','remove') and len([z for z in at(e) if z[1] not in (None,'BREAK')])>1: amb.setdefault((e['id'],e['side'],e['t']),[]).append(e)
for (g,p,t),es in amb.items():
    cur=at(es[0]); done=set()
    for e in es:
        k=next(i for i,z in enumerate(cur) if i not in done and [z[1],z[2],z[3]]==[e['was'][0],e['was'][1],e['was'][2]]); done.add(k)
        cur[k]=None if e['op']=='remove' else [t,e['kind'],e['lines'],e.get('pc',cur[k][3]),e.get('gc',cur[k][4])]
    w=dict(id=g,side=p,op='replace_window',t=t,t_end=t,events=[dict(t=z[0],kind=z[1],lines=z[2],pc=z[3],gc=z[4]) for z in cur if z],
           was_old=[[z[0],z[1],z[2]] for z in at(es[0])],source=' + '.join(e['source'] for e in es))
    ev[ev.index(es[0])]=w
    for e in es[1:]: ev.remove(e)
    print('same-t retypes folded into one window:',g,p,t,[(z['kind']) for z in w['events']])
# (3) n092 p2 8011.97: the skeptic's 'was' says pc 1; the chain event has pc 0 (the PC is elsewhere)
for e in ev:
    if (e['id'],e['side'],e['t'],e['op'])==('n092','p2',8011.97,'retype') and e['was'][2]==1: e['was'][2]=0; print('was pc fixed: n092 p2 8011.97')
json.dump(ev,open(f'{C}/event-corrections.json','w'),ensure_ascii=False,indent=1)
# pieces edits that compared NEXT spawns with the chain's EVENT count inside a B-splice window: rr['pieces'] already
# holds B's pieces for those windows (reconciled.jsonl notes), so the edit would count them twice. Left to the recount.
SPLICE_DROP={('n018','p2'),('n020','p2'),('n035','p1'),('n027','p1')}
for c in [c for c in cells if c['field']=='pieces' and (c['id'],c['player']) in SPLICE_DROP]:
    print('dropped pieces edit inside a B splice window:',c['id'],c['player'],c['was'],'->',c['value']); cells.remove(c)
json.dump(dict(cells=cells),open(f'{C}/cells.json','w'),ensure_ascii=False,indent=1)
from collections import Counter
print(len(ev),Counter(e['op'] for e in ev),len(cells))
for c in cells: print(c['id'],c['player'],c['field'],c['was'],'->',c['value'])
