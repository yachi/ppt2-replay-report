# Merge checker proposals (b*), skeptic verdicts (v*) and the hidden-PC frame check -> corr/event-corrections.json + corr/cells.json
import json
O='/tmp/claude-0/ak/corr/out'; C='/tmp/claude-0/ak/corr'
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
    if (e['id'],e['side']) == ('m041','p1') and e['t'] in (861.33, 860.97): continue   # b1 e4 makes it a plain lock; the PC is the 860.97 quad
    if touched(e): continue
    ev.append(tag(e,'hidden-PC frame check'))
ev.append(dict(id='m041',side='p1',op='retype',t=860.97,was=['quad',4,0],kind='quad',lines=4,pc=1,gc=0,
               source='hidden-PC frame check: PERFECT CLEAR banner at 861.4 over an empty board; b1 e4 shows 861.33 is its double-logged half'))
for e in ev:
    e.pop('n',None); e['t']=round(e['t'],2)
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
