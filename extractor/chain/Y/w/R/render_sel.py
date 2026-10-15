import pickle,json,subprocess,sys
G={g['id']:g for g in json.load(open('/private/tmp/claude-501/sk/metrics/more/games_YbMeCRhjG1k.json'))}
sel=pickle.load(open('R/sel.pkl','rb'))
for i,(c,x) in enumerate(sel):
  ev=x[3] or x[4]; t=ev['t']; t1=ev.get('tl',t)
  a0=t-1.4; a1=max(t1,t)+0.8
  subprocess.run(['python3','R/ref.py',G[x[0]]['video'],'%.2f'%a0,'%.2f'%a1,x[1],'2',f'R/fr/sel{i:02d}.png','14','0.55'])
  d=pickle.load(open(f'R/ev/{x[0]}.pkl','rb'))
  near=lambda L:[e for e in L if a0-1<=e['t']<=a1+1]
  print(i,c,x[0],x[1],'window %.2f-%.2f'%(a0,a1))
  print('  A',[(e['t'],e.get('kind'),e.get('lines'),e.get('garbage')) for e in near(d['a'][x[1]])])
  print('  B',[(e['t'],e['kind'],e['lines']) for e in near(d['b'][x[1]]['clears'])],'locks',[l for l in d['b'][x[1]]['locks'] if a0-1<=l<=a1+1],'garb',[g for g in d['b'][x[1]]['garbage'] if a0-1<=g[0]<=a1+1],'gaps',[g for g in d['b'][x[1]]['gaps'] if g['t1']>=a0-1 and g['t0']<=a1+1])
