# [sr] drop events and cell edits that two groups proposed for the same spot; the first kept, the second's source appended
import json
C='/tmp/claude-0/sr/corr'
ev=json.load(open(f'{C}/event-corrections.json')); cells=json.load(open(f'{C}/cells.json'))['cells']
out,notes=[],[]
for e in ev:
    k=(e['id'],e['side'],e['op'],e['t'])
    p=next((q for q in out if (q['id'],q['side'],q['op'],q['t'])==k),None)
    if p: p['source']+=' Also: '+e['source']; notes.append(f"event {k}: duplicate dropped ({e['source'][:30]})")
    else: out.append(e)
# cell edits: identical ones merged; conflicting piece counts take the NEXT recount value (decided after drive_nc)
DECIDE={('ac01','p1','pieces'):196,('ac24','p1','pieces'):587}  # ac01 p1 is then set by the NEXT recount below
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
# [sr] NEXT recount (nc_compare): clean reads that disagree with the table by more than one piece
NC={('ac01','p1'):(182,"NEXT recount: 183 shifts, no bad bag block or unknown stretch, every chain event matched; less the first hold = 182. The slow REN duel's gap pieces (BREAK windows) were phantoms."),
    ('ac01','p2'):(183,"NEXT recount: 185 shifts, less the first hold and an unmatched last shift = 183; bag blocks 154-175 are flagged bad (a resync at 520.4), so this is +-1, but 194 kept spliced gap pieces the p1 read rules out."),
    ('ac25','p1'):(253,"NEXT recount: 255 shifts on a clean read, less the first hold and the unmatched last shift = 253; every chain event matched, so the table's 4 extra are pieces extractor B spliced in.")}
for (g,p),(v,why) in NC.items():
    c=next((q for q in co if (q['id'],q['player'],q['field'])==(g,p,'pieces')),None)
    if c: notes.append(f"cell {(g,p,'pieces')}: {c['value']} -> {v} by NEXT recount"); c['value']=v; c['source']+=' Then '+why
    else:
        import csv
        was=int(next(r['pieces'] for r in csv.DictReader(open('/tmp/claude-0/sr/out/chain_games.csv')) if r['id']==g and r['player']==p))
        co.append(dict(id=g,player=p,field='pieces',was=was,value=v,source=why)); notes.append(f"cell {(g,p,'pieces')}: {was} -> {v} by NEXT recount (new)")
# [sr] ac01 p2 478.33: phantom duplicate the frame check missed (outside the g1 window)
k=('ac01','p2','remove',478.33)
if not any((q['id'],q['side'],q['op'],q['t'])==k for q in out):
    out.append(dict(id='ac01',side='p2',op='remove',t=478.33,was=['single',1,0],source='dedupe: phantom duplicate of the single at 479.43 (nextcount unmatched_event 478.33, the ~1.1 s pair pattern of the removed phantoms); p2 score steps run to REN 18 at 482.73 (b1 frame check)'))
    notes.append('event ac01 p2 478.33 remove added')
# [sr] drop cells the corrected events already give (max_combo/max_b2b are recomputed from the events)
import csv
CH={(r['id'],r['player']):r for r in csv.DictReader(open('/tmp/claude-0/sr/out/chain_games.csv'))}
keep=[]
for c in co:
    if str(CH[(c['id'],c['player'])][c['field']])==str(c['value']): notes.append(f"cell {(c['id'],c['player'],c['field'])}: chain already gives {c['value']}, dropped")
    else: keep.append(c)
co=keep
json.dump(out,open(f'{C}/event-corrections.json','w'),ensure_ascii=False,indent=1)
json.dump(dict(cells=co),open(f'{C}/cells.json','w'),ensure_ascii=False,indent=1)
print(len(out),len(co)); print('\n'.join(notes))
