import json
wc="""0-0 0-1 1-1 2-1 2-2 3-2 3-3 3-4 3-5 3-6 4-6 5-6 5-7
0-0 0-1 1-1 1-2 1-3 1-4 1-5 2-5 2-6 3-6 4-6 5-6 6-6 7-6 8-6 8-7 8-8 8-9 8-10 9-10 9-11 9-12 10-12 11-12 11-13 11-14 12-14 13-14 14-14
0-0 1-0 1-1 2-1
0-0 1-0 1-1 2-1
0-0 0-1 0-2 1-2 2-2 3-2 4-2 5-2 6-2 7-2 7-3 7-4 7-5 8-5 9-5 9-6 9-7 9-8 10-8 11-8 12-8 12-9 12-10 13-10 13-11 13-12 13-13 14-13 14-14
0-0 1-0 2-0 3-0 3-1 4-1 4-2 5-2 6-2 7-2 7-3 7-4 8-4 9-4 10-4 10-5 11-5 11-6 11-7 12-7 13-7 13-8 14-8
0-0 1-0 1-1 1-2 1-3 2-3 3-3 4-3 5-3 6-3 6-4 7-4 8-4 9-4 10-4 10-5 11-5 11-6 11-7 11-8 11-9 12-9 13-9 13-10 13-11 14-11 14-12""".split()
assert len(wc)==129,len(wc)
g=json.load(open('start/games_auto.json'))
opp=lambda i:'uyeshota' if i<=41 else ('いっせい' if i<=49 else 'ゆうくん')
after={11:'5-7',41:'14-15',45:'3-1',49:'3-1',78:'14-15',101:'15-8',128:'15-12'}
out=[]
for i,x in enumerate(g):
    assert x['id']==f'x{i:03d}'
    if i==12: continue
    x['opponent']=opp(i); x['win_counter_at_start']=wc[i]
    if i in after: x['win_counter_after']=after[i]
    out.append(x)
json.dump(out,open('chain/am/games.json','w'),ensure_ascii=False,indent=1)
print(len(out))
