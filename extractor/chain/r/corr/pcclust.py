# [c] PC-onset clusters (as for s): PC banner onsets not within -0.5..+3 s of an accepted PC, onsets < 2 s after a
# cluster's first merged into it -> corr/pcclusters.json, drawn with check/pc/strip2.py.
import json
f=json.load(open('/tmp/claude-0/r/out/flags.json'))
pc=[x for x in f if x['field_or_issue']=='PC banner onset']
acc=[(x['id'],x['player'],x['t_s']) for x in pc if 'PC = clear at' in x['detail']]
rest=sorted([(x['id'],x['player'],x['t_s']) for x in pc if 'PC = clear at' not in x['detail']],key=lambda z:(z[0],z[1],z[2]))
cl=[]
for g,p,t in rest:
    if any(g==a and p==b and -0.5<=t-c<=3 for a,b,c in acc): continue
    if cl and cl[-1][1]==g and cl[-1][2]==p and t-cl[-1][3]<2: continue
    cl.append([f'c{len(cl)}',g,p,t])
json.dump(cl,open('corr/pcclusters.json','w'));print(len(cl),'clusters;',len(acc),'accepted PCs')
json.dump(acc,open('corr/pcaccepted.json','w'))
from collections import Counter; print('accepted by player',Counter(p for _,p,_ in acc)); print('clusters by player',Counter(p for _,_,p,_ in cl))
