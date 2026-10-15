import pickle,random,json
G={g['id']:g for g in json.load(open('/private/tmp/claude-501/sk/metrics/more/games_YbMeCRhjG1k.json'))}
disp=pickle.load(open('R/disp.pkl','rb'))
cats=[('B_only',None,'quad'),('A_only','single',None),('kind','double','tsd'),('kind','single','double'),('A_only','quad',None),('kind','tsd','quad'),('kind','single','tsmini'),('B_only',None,'single'),('kind','single','orphan')]
random.seed(7); sel=[]
for c in cats:
  xs=[x for x in disp if (x[2],(x[3] or {}).get('kind'),(x[4] or {}).get('kind'))==c]
  random.shuffle(xs); sel+=[(c,x) for x in xs[:2]]
for i,(c,x) in enumerate(sel):
  t=(x[3] or x[4])['t']; t1=(x[3] or {}).get('tl',t)
  print(i,c,x[0],x[1],G[x[0]]['video'],'A',x[3],'B',x[4])
pickle.dump(sel,open('R/sel.pkl','wb'))
