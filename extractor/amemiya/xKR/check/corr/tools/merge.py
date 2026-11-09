import json,sys,re
R='/tmp/claude-0/xk/corr/results/'
groups=[int(a) for a in sys.argv[1:]] or [0,1,2,3,4]
cseq=json.load(open('/tmp/claude-0/xk/won/chain/am/w/tetrio/cseq.json'))
ev,cells,frz,exc,log=[],[],[],[],[]
def tag(o,g,how):
    o=dict(o); n=o.pop('n',None)
    o['source']=f"b{g} frame check, {how}: "+str(o.get('source',''))
    if 'player' in o and 'side' not in o and 'op' in o: o['side']=o.pop('player')
    return o
for g in groups:
    r=json.load(open(R+f'g{g}.json')); s=json.load(open(R+f's{g}.json'))
    V={v['ref']:v for v in s['verdicts']}
    for key,dst in (('event_fixes',ev),('cell_edits',cells),('freezes',frz),('exclude',exc)):
        for i,o in enumerate(r.get(key,[])):
            v=V.get(f'{key}[{i}]')
            if v is None: log.append(f'g{g} {key}[{i}] NO VERDICT'); continue
            if v['verdict']=='reject': log.append(f'g{g} {key}[{i}] rejected: {v["note"][:120]}'); continue
            if v['verdict']=='amend':
                a=v.get('amended') or {}
                o={**o,**a}; o['source']=str(o.get('source',''))+' | skeptic amend: '+v['note']
                dst.append(tag(o,g,'amended')); continue
            dst.append(tag(o,g,'verified'))
    for o in s.get('added',[]):
        (ev if 'op' in o else cells).append(tag(o,g,'added by skeptic'))
# validate events
bykey={}
for e in ev:
    k=f"{e['id']} {e['side']}"; E=cseq[k]
    ts=[round(x[0],2) for x in E]
    if e['op'] in('remove','retype'):
        m=[x for x in E if abs(x[0]-e['t'])<0.006]
        if not m: log.append(f"BAD {k} {e['op']} t {e['t']} not found")
        elif e.get('was') and [m[0][1],m[0][2],m[0][3]]!=list(e['was'])[:3]: log.append(f"BAD {k} {e['op']} was {e['was']} vs {m[0][:4]}")
    elif e['op']=='add':
        if round(e['t'],2) in ts: log.append(f"BAD {k} add collides {e['t']}")
    elif e['op']=='replace_window':
        w=[[x[0],x[1],x[2]] for x in E if e['t']-1e-6<=x[0]<=e['t_end']+1e-6]
        wo=[list(x)[:3] for x in e['was_old']]
        if [[round(a,2),b,c] for a,b,c in w]!=[[round(a,2),b,c] for a,b,c in wo]: log.append(f"BAD {k} rw was_old mismatch {e['t']}-{e['t_end']}: chain {w} vs {wo}")
        for x in e['events']:
            if not(e['t']-1e-6<=x['t']<=e['t_end']+1e-6): log.append(f"BAD {k} rw event outside {x['t']}")
def conv(e):
    if e['op'] in ('retype','remove') and (e.get('was') or [1])[0] in (None,'BREAK'):
        k=f"{e['id']} {e['side']}"; ms=[x for x in cseq[k] if abs(x[0]-e['t'])<0.006]; m=ms[0]
        new=[dict(t=x[0],kind=x[1],lines=x[2],pc=int(x[3]),gc=x[4]) for x in ms[1:]]
        if e['op']=='retype': new=[dict(t=m[0],kind=e['kind'],lines=e['lines'],pc=e.get('pc',0),gc=e.get('gc',0))]+new
        e={k2:v for k2,v in e.items() if k2 not in('was','kind','lines','pc','gc')}
        e.update(op='replace_window',t_end=m[0],t=m[0],events=new,was_old=[[x[0],x[1],x[2]] for x in ms])
        log.append('converted to replace_window: '+k+' '+str(m[0]))
    return e
ev=[conv(e) for e in ev]
json.dump(ev,open('/tmp/claude-0/xk/corr/event-corrections.json','w'),ensure_ascii=False,indent=1)
json.dump(cells,open('/tmp/claude-0/xk/corr/cells.json','w'),ensure_ascii=False,indent=1)
json.dump({'freezes':frz,'exclude':exc},open('/tmp/claude-0/xk/corr/freezes.json','w'),ensure_ascii=False,indent=1)
print(len(ev),'events',len(cells),'cells',len(frz),'freezes',len(exc),'exclude')
print('\n'.join(log))
