# [xp] Hidden PCs from the strips of corr/pcclusters.json (look/pc/s0..s5.png): 24 of the 42 clusters show a PERFECT CLEAR
# banner on that board, 18 are clear effects over garbage. Board crops around each pair were checked by eye.
import json
C='/tmp/claude-0/xp/w/chain/xp/w/tetrio/cseq.json'
cs=json.load(open(C)); cl={x[0]:x for x in json.load(open('/tmp/claude-0/xp/corr/pcclusters.json'))}
def ev(g,p,t): return next(e for e in cs[f'{g} {p}'] if abs(e[0]-t)<0.005)
SRC="hidden PERFECT CLEAR banner on the {p} board right after this clear (pcmap rejected it: its onsets were split by clear effects); corr/pcclusters.json {c}"
# cluster: (pc event t, earlier half t or None, how the earlier half is handled, extra phantom events after the PC)
PLAN={'c3':(1049.07,None,None,[]),'c5':(1297.2,1296.33,'lock',[]),'c6':(1362.13,None,None,[]),
 'c7':(1448.9,1448.63,'dup',[1449.17]),'c8':(1636.87,None,None,[]),'c12':(2539.5,2539.17,'dup',[]),
 'c13':(2560.63,None,None,[]),'c14':(2708.33,2708.03,'dup',[]),'c15':(2980.3,2979.37,'lock',[]),
 'c16':(3004.07,None,None,[]),'c17':(3079.57,3078.57,'lock',[]),'c18':(3088.27,None,None,[]),
 'c19':(3150.53,3150.27,'dup',[]),'c20':(3398.17,3397.93,'dup',[]),'c21':(3448.7,3448.4,'dup',[]),
 'c24':(16219.97,16219.63,'dup',[]),'c25':(16322.2,16321.77,'dup',[]),'c28':(16784.3,16783.83,'dup',[]),
 'c31':(17214.0,17213.83,'dup',[]),'c32':(17451.97,17451.5,'dup',[]),'c34':(17605.5,17605.17,'dup',[]),
 'c38':(18006.87,18006.33,'dup',[]),'c39':(18012.77,18012.53,'dup',[18013.1,18013.6]),'c40':(18292.23,None,None,[])}
out=[]
for c,(t,t0,how,ph) in PLAN.items():
    _,g,p,_=cl[c]; e=ev(g,p,t)
    out.append(dict(id=g,side=p,op='retype',t=t,was=[e[1],e[2],e[4]],kind=e[1],lines=e[2],pc=1,gc=e[4],source=SRC.format(p=p,c=c)))
    if t0 is not None:
        e0=ev(g,p,t0)
        if how=='dup':
            out.append(dict(id=g,side=p,op='remove',t=t0,was=[e0[1],e0[2],e0[4]],source=f"double-logged half of the hidden PC at {t:.2f} (same clear logged twice; board empty after the PC)"))
        else:
            out.append(dict(id=g,side=p,op='retype',t=t0,was=[e0[1],e0[2],e0[4]],kind=None,lines=0,pc=0,gc=0,source=f"this lock cleared nothing: the board keeps the same rows until the PC at {t:.2f} (frame crops)"))
    for tp in ph:
        e1=ev(g,p,tp)
        out.append(dict(id=g,side=p,op='remove',t=tp,was=[e1[1],e1[2],e1[4]],source=f"phantom after the hidden PC at {t:.2f}: the board is empty, so nothing could clear (frame crops)"))
json.dump(out,open('/tmp/claude-0/xp/corr/hidden_pc.json','w'),ensure_ascii=False,indent=1)
print(len(out),'ops,',sum(1 for x in out if x.get('pc')),'PCs')
