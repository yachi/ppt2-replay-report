import json
D='/private/tmp/claude-501/sk/endfix/combo3/apply'
c=json.load(open(f'{D}/corrections2.json')); assert len(c)==30
h=[i for i,r in enumerate(c) if r['id']=='h017' and r['side']=='p1' and r['op']=='add' and r['t']==1493.733]; assert len(h)==1
r=c[h[0]]; assert r['gc']==0; r['gc']=1
r['source']+='; gc 1: the S fills the col-6 hole of the top grey row, the 1493.800 band covers rows 5 (grey) and 6 (coloured); combo3/gc/c_h017.png, out_h017_p1_1493.txt'
w=[i for i,r in enumerate(c) if r['id']=='i015' and r['side']=='p2' and r['op']=='replace_window' and r['t']==1605.0]; assert len(w)==1
ev=[e for e in c[w[0]]['events'] if e['t']==1626.267]; assert len(ev)==1 and ev[0]['kind']=='single' and ev[0]['gc']==0
ev[0]['gc']=1
c[w[0]]['source']+='; 1626.267 single clears the one grey row GGGGGG.GGG; combo3/gc/c_i015_1626a.png, i015_mid2.txt'
sp=[i for i,r in enumerate(c) if r['id']=='g070' and r['op']=='setpc' and r['t']==1716.57]; assert len(sp)==1
c.insert(sp[0]+1, {"id":"g070","side":"p1","op":"retype","t":1716.57,"was":["double",2,1],"kind":"double","lines":2,"gc":0,"source":"PC double at video 1716.5 clears two coloured rows, no grey on the board 1710-1719; combo3/gc/c_g070.png, out_g070_p1_1716.txt"})
assert len(c)==31
json.dump(c,open(f'{D}/corrections3.json','w'),ensure_ascii=False,indent=1)
print('ok',len(c))
