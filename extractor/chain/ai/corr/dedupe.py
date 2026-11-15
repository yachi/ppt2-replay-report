# [ae] drop events and cell edits that two groups proposed for the same spot; the first kept, the second's source appended
import json, csv
C='/tmp/claude-0/ai/corr'
ev=json.load(open(f'{C}/event-corrections.json')); cells=json.load(open(f'{C}/cells.json'))['cells']
out,notes=[],[]
# [ai] ai28 p1: g1 and g2 disagree on which piece made the PERFECT CLEAR at 241.9. The frames (fr/v1/a28pc.png, the
# refuter's) show the Z from hold (the 241.03 event) dropping into the two-row gap at 241.70 and the PC at 241.90, with the
# I still in NEXT; the I locks on the empty floor after. g1 (and its refuter) is right; g2's two retypes are dropped.
for t in (241.03,241.93):
    for e in [e for e in ev if (e['id'],e['side'],e['t'])==('ai28','p1',t) and e['source'].startswith('b2 ')]:
        ev.remove(e); notes.append(f"event ('ai28','p1','retype',{t}): g2's reading dropped, the frames show the Z made the PC (g1)")
for e in ev:
    k=(e['id'],e['side'],e['op'],e['t'])
    p=next((q for q in out if (q['id'],q['side'],q['op'],q['t'])==k),None)
    if p:
        assert {x:e.get(x,0 if x=='pc' else None) for x in ('kind','lines','pc','was')}=={x:p.get(x,0 if x=='pc' else None) for x in ('kind','lines','pc','was')},(k,e,p)  # [ai] a missing pc is 0
        p['source']+=' Also: '+e['source']; notes.append(f"event {k}: duplicate dropped ({e['source'][:30]})")
    else: out.append(e)
# [ai] g0 rebuilt ai14 p1 895.27-895.63 with a replace_window that already sets the PERFECT CLEAR (a triple, as g0's
# refuter amended) and drops the phantom clear; g2's retypes of the same events fall inside it (same verdicts), so they are dropped
W=[e for e in out if e['op']=='replace_window']
def inwin(e): return any(w['id']==e['id'] and w['side']==e['side'] and w['t']<=e['t']<=w['t_end'] for w in W)
for e in [e for e in out if e['op']=='retype' and inwin(e)]:
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
NC={('ai19','p1'):(159,"the NEXT recount reads 159 cleanly (23 whole bags, no unknown stretch; 161 shifts less the first hold of Z at 1193.37 and the unmatched last shift at 1296.20) and the corrected events also number 159, every other shift matched to an event and no event unmatched, so set to 159 (the checkers' 166 counted through the long REN stretch the replace_windows rebuilt)"),
    ('ai19','p2'):(153,"the NEXT recount reads 154 shifts over 22 whole bags with no unknown stretch; less the first hold of L at 1193.84 that is 153, every shift matched to an event (the last shift at 1296.94 matches the last event, so it is not dropped) and the corrected events also number 153, so set to 153 (the checkers' 162 counted through the long REN stretch the replace_windows rebuilt)")}
for (g,p),(v,why) in NC.items():
    c=next((q for q in co if (q['id'],q['player'],q['field'])==(g,p,'pieces')),None)
    if c: notes.append(f"cell {(g,p,'pieces')}: {c['value']} -> {v} by NEXT recount"); c['value']=v; c['source']+=' Then '+why
    else:
        was=int(next(r['pieces'] for r in csv.DictReader(open('/tmp/claude-0/ai/out/chain_games.csv')) if r['id']==g and r['player']==p))
        co.append(dict(id=g,player=p,field='pieces',was=was,value=v,source=why)); notes.append(f"cell {(g,p,'pieces')}: {was} -> {v} by NEXT recount (new)")
# drop cells the corrected events already give (max_combo/max_b2b are recomputed from the events)
CH={(r['id'],r['player']):r for r in csv.DictReader(open('/tmp/claude-0/ai/out/chain_games.csv'))}
keep=[]
for c in co:
    if str(CH[(c['id'],c['player'])][c['field']])==str(c['value']): notes.append(f"cell {(c['id'],c['player'],c['field'])}: chain already gives {c['value']}, dropped")
    else: keep.append(c)
co=keep
json.dump(out,open(f'{C}/event-corrections.json','w'),ensure_ascii=False,indent=1)
json.dump(dict(cells=co),open(f'{C}/cells.json','w'),ensure_ascii=False,indent=1)
print(len(out),len(co)); print('\n'.join(notes))
