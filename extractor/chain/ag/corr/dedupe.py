# [ae] drop events and cell edits that two groups proposed for the same spot; the first kept, the second's source appended
import json, csv
C='/tmp/claude-0/ag/corr'
ev=json.load(open(f'{C}/event-corrections.json')); cells=json.load(open(f'{C}/cells.json'))['cells']
out,notes=[],[]
for e in ev:
    k=(e['id'],e['side'],e['op'],e['t'])
    p=next((q for q in out if (q['id'],q['side'],q['op'],q['t'])==k),None)
    if p:
        assert {x:e.get(x) for x in ('kind','lines','pc','was')}=={x:p.get(x) for x in ('kind','lines','pc','was')},(k,e,p)
        p['source']+=' Also: '+e['source']; notes.append(f"event {k}: duplicate dropped ({e['source'][:30]})")
    else: out.append(e)
# [ag] ag16 p1: g0 (913.8-922.83) and g1 (921.1-929.3) both rebuilt the stalled REN stretch with overlapping windows;
# they agree on the real locks (S single, J double into the garbage well, then g1's O single, I tetris, I single).
# One window over the union replaces both; the S single keeps g0's spawn time.
W=[e for e in out if (e['id'],e['side'],e['op'])==('ag16','p1','replace_window')]
assert len(W)==2,W
U=dict(W[0]); U['t']=913.8; U['t_end']=929.3
U['events']=[dict(t=913.8,kind='single',lines=1,pc=0,gc=0)]+[x for x in W[1]['events'] if x['t']>=926]
U['was_old']=W[0]['was_old']+[x for x in W[1]['was_old'] if x[0]>922.83]
U['source']='Union of two groups\' windows. '+W[0]['source']+' Also: '+W[1]['source']
out=[e for e in out if e not in W]+[U]; notes.append('event ag16 p1: g0 and g1 replace_windows overlapped; replaced by one window 913.8-929.3 (5 locks)')
DECIDE={('ag16','p1','pieces'):128}  # 8 chain piece events in 913.8-929.3 (922.83 double+quad one piece), 5 real locks
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
NC={('ag16','p1'):(122,"the NEXT recount reads 122 cleanly (17 whole bags, no unknown stretch; 124 shifts less the first hold and the KO-frame shift) and the corrected events also number 122, every spawn matched to a lock except the O held at 922.77 / the J from hold at 926.6, so set to 122 (the table's 131 came from extractor B, which counted spawns through the stalled REN stretch)")}  # NEXT recount decisions, filled after drive_nc
for (g,p),(v,why) in NC.items():
    c=next((q for q in co if (q['id'],q['player'],q['field'])==(g,p,'pieces')),None)
    if c: notes.append(f"cell {(g,p,'pieces')}: {c['value']} -> {v} by NEXT recount"); c['value']=v; c['source']+=' Then '+why
    else:
        was=int(next(r['pieces'] for r in csv.DictReader(open('/tmp/claude-0/ag/out/chain_games.csv')) if r['id']==g and r['player']==p))
        co.append(dict(id=g,player=p,field='pieces',was=was,value=v,source=why)); notes.append(f"cell {(g,p,'pieces')}: {was} -> {v} by NEXT recount (new)")
# drop cells the corrected events already give (max_combo/max_b2b are recomputed from the events)
CH={(r['id'],r['player']):r for r in csv.DictReader(open('/tmp/claude-0/ag/out/chain_games.csv'))}
keep=[]
for c in co:
    if str(CH[(c['id'],c['player'])][c['field']])==str(c['value']): notes.append(f"cell {(c['id'],c['player'],c['field'])}: chain already gives {c['value']}, dropped")
    else: keep.append(c)
co=keep
json.dump(out,open(f'{C}/event-corrections.json','w'),ensure_ascii=False,indent=1)
json.dump(dict(cells=co),open(f'{C}/cells.json','w'),ensure_ascii=False,indent=1)
print(len(out),len(co)); print('\n'.join(notes))
