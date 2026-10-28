# Verbatim copy of the inline heredoc that wrote analysis/ppt2-syakegohan/games.csv
# (main transcript 436947ab..., 2026-10-14T09:38:53Z), with ALLROWS and OUTCSV parameterised.
import csv,json,glob,sys
# [am port, uP paths] games come from the one set's games.json; ALLROWS/OUTCSV are required arguments
ALLROWS=sys.argv[1]
OUTCSV=sys.argv[2]
G={g['id']:g for g in json.load(open('/private/tmp/claude-501/uP/w/chain/sy/games.json'))}
R=list(csv.DictReader(open(ALLROWS)))
opp={r['id']:r['opponent'] for r in R if r['player']=='p2' and r['opponent']}
def op(s):
    s=s.strip(); unsure=s.endswith('*'); s=s.rstrip('*').strip()
    m={'honeycup':'Honey Cup','gamushiro':'Gamushiro','meisou':'Stray Cannon','other':'Other'}
    s=m.get(s.lower(),s)
    if s.endswith('(deviated)'): s=s.replace(' (deviated)',''); unsure=True
    return s+(' (?)' if unsure and s else '')
KEEP=['id','dataset','video','start_s','opener','opponent','player','who','won','excluded','reason','duration_s','pieces','lines_cleared','attack','garbage_cleared','garbage_received_rows','single','double','triple','quad','tss','tsd','tst','tsmini','pc','max_combo','max_b2b']
out=[]
for r in R:
    g=G[r['id']]
    row={k:r.get(k,'') for k in KEEP}
    row['video']=g['video']; row['start_s']=g['start_s']; row['opener']=op(r['opener'])
    row['opponent']=opp.get(r['id'],'') ; row['reason']=r['reason'].strip()
    if r['player']=='p2' and not r['who']: row['who']=row['opponent']
    out.append(row)
out.sort(key=lambda r:(r['dataset'],float(r['start_s']),r['player']))
with open(OUTCSV,'w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,KEEP,lineterminator='\n'); w.writeheader(); w.writerows(out)
