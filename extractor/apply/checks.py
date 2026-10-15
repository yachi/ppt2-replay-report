import csv, sys
sys.path.insert(0, '/Users/yachi/github/tetrio-replay-report')
from pipeline.ppt2_page import apply_hand_edits, _video, _game_key
from collections import defaultdict
D='/private/tmp/claude-501/sk/endfix/combo3/apply'; R='/Users/yachi/github/tetrio-replay-report/analysis/ppt2-syakegohan'
def rows(p): return list(csv.DictReader(open(p,encoding='utf-8',newline='')))
# writer control: ctrl chain + repo hand-edits through apply_hand_edits must reproduce the repo games.csv bytes
import io, hashlib
c=rows(f'{D}/ctrl/games.csv'); cols=list(c[0].keys()); apply_hand_edits(c, rows(f'{R}/hand-edits.csv'))
b=io.StringIO(); w=csv.DictWriter(b,fieldnames=cols,lineterminator='\n'); w.writeheader(); w.writerows(c)
print('writer control md5', hashlib.md5(b.getvalue().encode()).hexdigest(), '(repo bdd89d7be3038b2eab688a60168ffe14)')
def games(rs):
    g=defaultdict(dict)
    for r in rs: g[r['id']][r['player']]=r
    return g
old=games(rows(f'{R}/games.csv')); new=games(rows(f'{D}/fin/games.csv'))
for gid in ['h004','h006','h017','g060','g083','g086']:
    a,b=old[gid]['p1'],new[gid]['p1']
    lab=lambda r:f"{int(float(r['start_s'])//60)}:{int(float(r['start_s'])%60):02d}"
    print(gid, _video(a).split('t=')[1], '->', _video(b).split('t=')[1], lab(a),'->',lab(b), 'dur', a['duration_s'], b['duration_s'])
oo=sorted(old,key=lambda k:_game_key(old[k])); nn=sorted(new,key=lambda k:_game_key(new[k]))
print('order unchanged', oo==nn, len(oo))
