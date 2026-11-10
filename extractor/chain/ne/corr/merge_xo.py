# [xo] Merge checker proposals (b*), skeptic verdicts (v*) and the hidden-PC frame check -> corr/event-corrections.json + corr/cells.json
import json
O='/tmp/claude-0/ne/corr/out'; C='/tmp/claude-0/ne/corr'
WAS={}
def tag(x,s): x=dict(x); x['source']=f"{s}: {x.get('source','')}"; return x
ev,cells=[],[]
for k in range(5):   # [nc] five groups
    b=json.load(open(f'{O}/b{k}.json')); V={v['ref']:v for v in json.load(open(f'{O}/v{k}.json'))}
    for pre,lst,out in (('e','event_corrections',ev),('c','cell_edits',cells)):
        for i,e in enumerate(b[lst]):
            r=V[f'{pre}{i}']
            if r['verdict']=='reject': continue
            x={**e,**(r.get('amended') or {})}
            out.append(tag(x,f"b{k} frame check, {'verified' if r['verdict']=='keep' else 'amended by skeptic'}"))
    for r in V.values():
        if r['verdict']=='missed':
            p=r['proposal']; out=cells if 'field' in p else ev
            out.append(tag(p,f"v{k} skeptic, missed by b{k}"))
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
# [nc] c085 p1 6572.47 was proposed by both b2 and b3: keep one
seen=set(); d=[]
for e in ev:
    k=(e['id'],e['side'],e['op'],e['t'])
    if k in seen: continue
    seen.add(k); d.append(e)
ev=d
# [ne] e033 p1 cells proposed by both b0/v0 and b1: keep one
seen=set(); cd=[]
for c in cells:
    k=(c['id'],c['player'],c['field'])
    if k in seen: continue
    seen.add(k); cd.append(c)
cells=cd
# [ne] e108 p2 7438.43: A logged a single and B a quad at the same t; drop the quad only
for e in ev:
    if e['id']=='e108' and e['op']=='remove' and e['t']==7438.43:
        e['op']='replace_window'; e['t_end']=e['t']; e.pop('was')
        e['events']=[dict(t=7438.43,kind='single',lines=1,pc=0,gc=1)]
        e['was_old']=[[7438.43,'single',1],[7438.43,'quad',4]]
x2=[]
for e in ev:
    if e['op']=='replace_window' and not e['was_old']:
        x2+=[dict(id=e['id'],side=e['side'],op='add',t=round(w['t'],2),kind=w['kind'],lines=w['lines'],pc=w['pc'],gc=w['gc'],source=e['source']) for w in e['events']]
    else: x2.append(e)
ev=x2
json.dump(ev,open(f'{C}/event-corrections.json','w'),ensure_ascii=False,indent=1)
json.dump(dict(cells=cells),open(f'{C}/cells.json','w'),ensure_ascii=False,indent=1)
from collections import Counter
print(len(ev),Counter(e['op'] for e in ev),len(cells))
for c in cells: print(c['id'],c['player'],c['field'],c['was'],'->',c['value'])
