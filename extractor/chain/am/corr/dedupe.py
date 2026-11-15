# [ae] drop events and cell edits that two groups proposed for the same spot; the first kept, the second's source appended
import json, csv
C='/tmp/claude-0/am/corr'
ev=json.load(open(f'{C}/event-corrections.json')); cells=json.load(open(f'{C}/cells.json'))['cells']
out,notes=[],[]
for e in ev:
    k=(e['id'],e['side'],e['op'],e['t'])
    p=next((q for q in out if (q['id'],q['side'],q['op'],q['t'])==k),None)
    if p:
        if e.get('was') and p.get('was') and e['was'][:2]==p['was'][:2] and e['was']!=p['was']:  # [al] groups read the chain's pc flag differently in `was`; fixwas.py re-reads it
            e=dict(e,was=p['was'])
        assert {x:e.get(x,0 if x=='pc' else None) for x in ('kind','lines','pc','was')}=={x:p.get(x,0 if x=='pc' else None) for x in ('kind','lines','pc','was')},(k,e,p)  # [ai] a missing pc is 0
        p['source']+=' Also: '+e['source']; notes.append(f"event {k}: duplicate dropped ({e['source'][:30]})")
    else: out.append(e)
# [aj] retypes inside a replace_window are dropped (the window already sets those events)
# [al] removes too: g2 rebuilt al44 by per-event removals, g3 by replace_windows over the same REN stretch (both verified,
# same piece counts); g3's windows are kept and g2's removals inside them dropped
W=[e for e in out if e['op']=='replace_window']
def inwin(e): return any(w is not e and w['id']==e['id'] and w['side']==e['side'] and w['t']<=e['t']<=w['t_end'] for w in W)
def point(e): return e['op']=='replace_window' and e['t']==e['t_end'] and len(e['events'])<=1  # a lock/BREAK removal or a single retype
for e in [e for e in out if (e['op'] in ('retype','remove') or point(e)) and inwin(e)]:
    out.remove(e); notes.append(f"event {(e['id'],e['side'],e['op'],e['t'])}: inside a replace_window, dropped ({e['source'][:30]})")
DECIDE={}
co=[]
for c in cells:
    k=(c['id'],c['player'],c['field'])
    p=next((q for q in co if (q['id'],q['player'],q['field'])==k),None)
    if p is None: co.append(c); continue
    if p['value']!=c['value']:
        v=DECIDE[k]; notes.append(f"cell {k}: {p['value']} vs {c['value']} -> {v}")
        if c['value']==v: p['value']=v
    else: notes.append(f"cell {k}: duplicate {c['value']} merged")
    p['source']+=' Also: '+c['source']
NC={}  # NEXT recount decisions, filled after drive_nc
for (g,p),(v,why) in NC.items():
    c=next((q for q in co if (q['id'],q['player'],q['field'])==(g,p,'pieces')),None)
    if c: notes.append(f"cell {(g,p,'pieces')}: {c['value']} -> {v} by NEXT recount"); c['value']=v; c['source']+=' Then '+why
    else:
        was=int(next(r['pieces'] for r in csv.DictReader(open('/tmp/claude-0/am/out/chain_games.csv')) if r['id']==g and r['player']==p))
        co.append(dict(id=g,player=p,field='pieces',was=was,value=v,source=why)); notes.append(f"cell {(g,p,'pieces')}: {was} -> {v} by NEXT recount (new)")
# drop cells the corrected events already give (max_combo/max_b2b are recomputed from the events)
CH={(r['id'],r['player']):r for r in csv.DictReader(open('/tmp/claude-0/am/out/chain_games.csv'))}
keep=[]
for c in co:
    if str(CH[(c['id'],c['player'])][c['field']])==str(c['value']): notes.append(f"cell {(c['id'],c['player'],c['field'])}: chain already gives {c['value']}, dropped")
    else: keep.append(c)
co=keep
json.dump(out,open(f'{C}/event-corrections.json','w'),ensure_ascii=False,indent=1)
json.dump(dict(cells=co),open(f'{C}/cells.json','w'),ensure_ascii=False,indent=1)
print(len(out),len(co)); print('\n'.join(notes))
