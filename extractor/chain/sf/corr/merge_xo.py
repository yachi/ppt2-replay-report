# [xo] Merge checker proposals (b*), skeptic verdicts (v*) and the hidden-PC frame check -> corr/event-corrections.json + corr/cells.json
import json
O='/tmp/claude-0/sf/corr/out'; C='/tmp/claude-0/sf/corr'
WAS={}
def tag(x,s): x=dict(x); x['source']=f"{s}: {x.get('source','')}"; return x
ev,cells=[],[]
import os
for k in range(4):   # [sf] g0-g1 flags, g2 litcount PCs, g3 the w007 p1 follow-up (no skeptic: its counts match extractor A)
    b=json.load(open(f'{O}/b{k}.json'))
    V={v['ref']:v for v in json.load(open(f'{O}/v{k}.json'))} if os.path.exists(f'{O}/v{k}.json') else {f'{p}{i}':dict(verdict='unreviewed') for p,l in (('e','event_corrections'),('c','cell_edits')) for i in range(len(b[l]))}
    for pre,lst,out in (('e','event_corrections',ev),('c','cell_edits',cells)):
        for i,e in enumerate(b[lst]):
            r=V[f'{pre}{i}']
            if r['verdict']=='reject': continue
            x={**e,**(r.get('amended') or {})}
            out.append(tag(x,f"b{k} frame check, {dict(keep='verified',unreviewed='matches extractor A, no skeptic').get(r['verdict'],'amended by skeptic')}"))
    for r in V.values():
        if r['verdict']=='missed':
            p=r['proposal']; out=cells if 'field' in p else ev
            out.append(tag(p,f"v{k} skeptic, missed by b{k}"))
# [sf] groups overlapped: keep one copy of an event correction per (game, side, op, time), and let g3's w007
# piece/max_combo edits (counted over the union of all removals) replace the per-group ones
seen=set(); ev2=[]
for e in ev:
    key=(e['id'],e['side'],e['op'],round(e['t'],2))
    if key in seen: continue
    seen.add(key); ev2.append(e)
ev=ev2
final={(c['id'],c['player'],c['field']) for c in cells if c['source'].startswith('b3 ')}
cells=[c for c in cells if c['source'].startswith('b3 ') or (c['id'],c['player'],c['field']) not in final]
def touched(e):
    keys=set()
    for x in ev:
        if (x['id'],x['side'])!=(e['id'],e['side']): continue
        if x['op']=='replace_window':
            if x['t']<=e['t']<=x['t_end']: return True
        elif abs(x['t']-e['t'])<0.005: return True
    return False
hp=json.load(open(f'{C}/hidden_pc.json'))
for e in hp:
    if touched(e): continue
    ev.append(tag(e,'hidden-PC frame check'))
for e in ev:
    e.pop('n',None); e['t']=round(e['t'],2)
    if e['op']=='retype' and 'was' not in e: e['was']=WAS[(e['id'],e['side'],round(e['t'],2))]
    if e['op']=='retype' and e['was'][0] is None:
        e['op']='replace_window'; e['t_end']=e['t']
        e['events']=[dict(t=e['t'],kind=e.pop('kind'),lines=e.pop('lines'),pc=e.pop('pc',0),gc=e.pop('gc',0))]
        e['was_old']=[[e['t'],None,0]]; e.pop('was')
    if e['op']=='remove' and e['was'][0] in (None,'BREAK'):
        e['op']='replace_window'; e['t_end']=e['t']; e['events']=[]
        e['was_old']=[[e['t'],e['was'][0],e['was'][1]]]; e.pop('was')
x2=[]
for e in ev:
    if e['op']=='replace_window' and not e['was_old']:
        x2+=[dict(id=e['id'],side=e['side'],op='add',t=round(w['t'],2),kind=w['kind'],lines=w['lines'],pc=w['pc'],gc=w['gc'],source=e['source']) for w in e['events']]
    else: x2.append(e)
ev=x2
json.dump(ev,open(f'{C}/event-corrections.json','w'),ensure_ascii=False,indent=1)
# [se] a later edit of the same cell whose `was` is an earlier edit's `value` folds into that edit (one hand edit per cell)
fold=[]
for c in cells:
    p=next((q for q in fold if (q['id'],q['player'],q['field'])==(c['id'],c['player'],c['field']) and q['value']==c['was']),None)
    if p: p['value']=c['value']; p['source']+=' Then '+c['source']
    else: fold.append(c)
cells=fold
json.dump(dict(cells=cells),open(f'{C}/cells.json','w'),ensure_ascii=False,indent=1)
from collections import Counter
print(len(ev),Counter(e['op'] for e in ev),len(cells))
for c in cells: print(c['id'],c['player'],c['field'],c['was'],'->',c['value'])
