# [ae] drop events and cell edits that two groups proposed for the same spot; the first kept, the second's source appended
import json, csv
C='/tmp/claude-0/af/corr'
ev=json.load(open(f'{C}/event-corrections.json')); cells=json.load(open(f'{C}/cells.json'))['cells']
out,notes=[],[]
for e in ev:
    k=(e['id'],e['side'],e['op'],e['t'])
    p=next((q for q in out if (q['id'],q['side'],q['op'],q['t'])==k),None)
    if p:
        assert {x:e.get(x) for x in ('kind','lines','pc','was')}=={x:p.get(x) for x in ('kind','lines','pc','was')},(k,e,p)
        p['source']+=' Also: '+e['source']; notes.append(f"event {k}: duplicate dropped ({e['source'][:30]})")
    else: out.append(e)
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
NC={('af29','p1'):(78,'the NEXT recount reads 78 cleanly (11 whole bags, no unknown stretch, every spawn matched to a corrected lock event), so set to 78.')}  # NEXT recount decisions, filled after drive_nc
for (g,p),(v,why) in NC.items():
    c=next((q for q in co if (q['id'],q['player'],q['field'])==(g,p,'pieces')),None)
    if c: notes.append(f"cell {(g,p,'pieces')}: {c['value']} -> {v} by NEXT recount"); c['value']=v; c['source']+=' Then '+why
    else:
        was=int(next(r['pieces'] for r in csv.DictReader(open('/tmp/claude-0/af/out/chain_games.csv')) if r['id']==g and r['player']==p))
        co.append(dict(id=g,player=p,field='pieces',was=was,value=v,source=why)); notes.append(f"cell {(g,p,'pieces')}: {was} -> {v} by NEXT recount (new)")
# drop cells the corrected events already give (max_combo/max_b2b are recomputed from the events)
CH={(r['id'],r['player']):r for r in csv.DictReader(open('/tmp/claude-0/af/out/chain_games.csv'))}
keep=[]
for c in co:
    if str(CH[(c['id'],c['player'])][c['field']])==str(c['value']): notes.append(f"cell {(c['id'],c['player'],c['field'])}: chain already gives {c['value']}, dropped")
    else: keep.append(c)
co=keep
json.dump(out,open(f'{C}/event-corrections.json','w'),ensure_ascii=False,indent=1)
json.dump(dict(cells=co),open(f'{C}/cells.json','w'),ensure_ascii=False,indent=1)
print(len(out),len(co)); print('\n'.join(notes))
