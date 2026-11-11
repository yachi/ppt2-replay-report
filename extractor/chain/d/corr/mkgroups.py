# [c] frame-check items: every non-PC flag plus the score spots with |unexplained| >= 900, split by game into 4 groups.
import json, os
f=json.load(open('/tmp/claude-0/d/out/flags.json'))
it=[x for x in f if x['field_or_issue']!='PC banner onset']
for s in json.load(open('score/spots.json')):
    if abs(s['unexplained'])>=900:
        it.append(dict(id=s['id'],player=s['player'],field_or_issue='score_spot',detail=f"score rose {s['step']} vs chain prediction; unexplained {s['unexplained']} between {s['t0']} and {s['t1']} s; chain clears near: {s['near']}",t_s=s['t0']))
it.sort(key=lambda x:(x['id'],x['t_s']))
for n,x in enumerate(it): x['n']=n
K=4; G=[[] for _ in range(K)]
ids=sorted({x['id'] for x in it})
for x in it: G[min(K-1,ids.index(x['id'])*K//len(ids))].append(x)
os.makedirs('groups',exist_ok=True)
for k,g in enumerate(G): json.dump(g,open(f'groups/g{k}.json','w'),ensure_ascii=False,indent=1); print(k,len(g),g[0]['id'],g[-1]['id'])
