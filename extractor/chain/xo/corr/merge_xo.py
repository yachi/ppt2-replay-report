# [xo] Merge checker proposals (b*), skeptic verdicts (v*) and the hidden-PC frame check -> corr/event-corrections.json + corr/cells.json
import json
O='/tmp/claude-0/xo/corr/out'; C='/tmp/claude-0/xo/corr'
WAS={('u115','p1',7190.3):['?',0,0],('u115','p1',7224.6):['?',0,0]}
def tag(x,s): x=dict(x); x['source']=f"{s}: {x.get('source','')}"; return x
ev,cells=[],[]
for k in range(6):
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
