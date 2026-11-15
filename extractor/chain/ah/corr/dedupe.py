# [ae] drop events and cell edits that two groups proposed for the same spot; the first kept, the second's source appended
import json, csv
C='/tmp/claude-0/ah/corr'
ev=json.load(open(f'{C}/event-corrections.json')); cells=json.load(open(f'{C}/cells.json'))['cells']
out,notes=[],[]
for e in ev:
    k=(e['id'],e['side'],e['op'],e['t'])
    p=next((q for q in out if (q['id'],q['side'],q['op'],q['t'])==k),None)
    if p:
        assert {x:e.get(x) for x in ('kind','lines','pc','was')}=={x:p.get(x) for x in ('kind','lines','pc','was')},(k,e,p)
        p['source']+=' Also: '+e['source']; notes.append(f"event {k}: duplicate dropped ({e['source'][:30]})")
    else: out.append(e)
# [ah] g0 rebuilt ah00 p1 and ah15 p1 with replace_windows that already set the PC and drop the phantom clear;
# g2's retypes of the same events fall inside those windows, so they are dropped (same verdicts)
W=[e for e in out if e['op']=='replace_window']
def inwin(e): return any(w['id']==e['id'] and w['side']==e['side'] and w['t']<=e['t']<=w['t_end'] for w in W)
for e in [e for e in out if e['op']=='retype' and inwin(e)]:
    out.remove(e); notes.append(f"event {(e['id'],e['side'],e['op'],e['t'])}: inside a replace_window, dropped ({e['source'][:30]})")
# [ah] g1 found the ah18 p1 1026.33 quad and the ah25 p1 234.47 quad were PERFECT CLEARs (it retyped their duplicates,
# 1026.6 and 234.73, and left the pc flag to the PC group, which did not get them); set pc=1 on the real clears
for g,t,why in [('ah18',1026.33,"one score jump of +8400 at 1026.53 (a PC-sized jump; a plain B2B quad is far smaller), the board empty after it"),
                ('ah25',234.47,"one score jump of +8400 at 234.67, the PC-sized jump g1 and its refuter both read")]:
    out.append(dict(id=g,side='p1',op='retype',t=t,was=['quad',4,0],kind='quad',lines=4,pc=1,gc=0,
        source=f"b1 frame check (g1 named this quad a PERFECT CLEAR while retyping its duplicate; v1 kept that retype on the same jump): {why}."))
    notes.append(f"event ({g!r}, 'p1', 'retype', {t}): pc=1 added from g1's finding")
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
NC={('ah08','p1'):(61,"the NEXT recount reads 61 cleanly (8 whole bags, no unknown stretch; 62 shifts less the first hold of Z at 531.43) and the corrected events also number 61, every shift matched to an event and no event unmatched, so set to 61 (the table's 68 came from extractor B, which counted spawns through the stalled 19-combo REN stretch)")}  # NEXT recount decisions, filled after drive_nc
for (g,p),(v,why) in NC.items():
    c=next((q for q in co if (q['id'],q['player'],q['field'])==(g,p,'pieces')),None)
    if c: notes.append(f"cell {(g,p,'pieces')}: {c['value']} -> {v} by NEXT recount"); c['value']=v; c['source']+=' Then '+why
    else:
        was=int(next(r['pieces'] for r in csv.DictReader(open('/tmp/claude-0/ah/out/chain_games.csv')) if r['id']==g and r['player']==p))
        co.append(dict(id=g,player=p,field='pieces',was=was,value=v,source=why)); notes.append(f"cell {(g,p,'pieces')}: {was} -> {v} by NEXT recount (new)")
# drop cells the corrected events already give (max_combo/max_b2b are recomputed from the events)
CH={(r['id'],r['player']):r for r in csv.DictReader(open('/tmp/claude-0/ah/out/chain_games.csv'))}
keep=[]
for c in co:
    if str(CH[(c['id'],c['player'])][c['field']])==str(c['value']): notes.append(f"cell {(c['id'],c['player'],c['field'])}: chain already gives {c['value']}, dropped")
    else: keep.append(c)
co=keep
json.dump(out,open(f'{C}/event-corrections.json','w'),ensure_ascii=False,indent=1)
json.dump(dict(cells=co),open(f'{C}/cells.json','w'),ensure_ascii=False,indent=1)
print(len(out),len(co)); print('\n'.join(notes))
