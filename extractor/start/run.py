import sys, json
from bag import settled, nearest
vid=sys.argv[1]; d=json.load(open(f'g_{vid}.json'))
starts=[];z=0
for t,n,g in d:
    if n==0: z+=1
    else:
        if z>=8: starts.append(t)
        z=0
res=[]
for k,s in enumerate(starts):
    bs=settled(f'vid/{vid}.mp4',max(0,s-0.5),7)
    got={}
    for t,n,rows in bs:
        if n in (24,28) and n not in got and not any('G' in r for r in rows):
            got[n]=(t,rows,nearest(rows,2))
        if n>28: break
    print(f'=== {vid} game{k} start={s:.1f}')
    for n,(t,rows,m) in sorted(got.items()):
        print(f'  n={n} t={t:.2f}'); print('\n'.join('    '+r for r in rows)); print('   ',m[0]); print('   ',m[1])
    if not got: print('  no clean board; counts',[n for t,n,r in bs][:30])
    res.append(dict(vid=vid,game=k,start=s,boards={n:dict(t=v[0],rows=v[1],near=v[2]) for n,v in got.items()}))
json.dump(res,open(f'res_{vid}.json','w'),ensure_ascii=False)
