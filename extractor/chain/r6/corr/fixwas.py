# [xo] re-run metrics; where a retype/remove 'was' disagrees with the chain only in the third slot (checker wrote gc, overlay wants pc) or was unknown ('?'), take the chain's value. Logs each fix.
import json,subprocess,re,ast,sys
F='/tmp/claude-0/r6/corr/event-corrections.json'
for it in range(40):
    r=subprocess.run(['python3','tetrio/metrics.py'],capture_output=True,text=True)
    if r.returncode==0: open('tetrio/metrics.out','w').write(r.stdout+r.stderr); print('OK after',it); sys.exit()
    m2=re.search(r"AssertionError: \('OVERLAY replace_window was_old mismatch', (\{.*\}), (\[.*\])\)\s*$",r.stderr.strip(),re.S)
    if m2:
        c=ast.literal_eval(m2.group(1)); old=ast.literal_eval(m2.group(2)); ev=json.load(open(F))
        assert c['t']==c['t_end'] and all(z[1] is None and round(z[0],2)==c['t'] for z in old) and len(c['was_old'])==1, (c,old)
        for e in ev:
            if (e['id'],e['side'],e['op'],e['t'])==(c['id'],c['side'],c['op'],c['t']):
                e['was_old']=[[round(z[0],2),None,0] for z in old]
                e['events']+= [dict(t=c['t'],kind=None,lines=0,pc=0,gc=0)]*(len(old)-1)
                print('widened',e['id'],e['side'],e['t'],len(old))
        json.dump(ev,open(F,'w'),ensure_ascii=False,indent=1); continue
    m=re.search(r"AssertionError: \('OVERLAY was-mismatch', (\{.*\}), (\(.*\))\)\s*$",r.stderr.strip(),re.S)
    if not m: print(r.stderr[-1500:]); sys.exit(1)
    c=ast.literal_eval(m.group(1)); z=ast.literal_eval(m.group(2).replace('False','False'))
    ev=json.load(open(F))
    for e in ev:
        if (e['id'],e['side'],e['op'],e['t'])==(c['id'],c['side'],c['op'],c['t']):
            w=e['was']
            if w[0]!='?' and (w[0],int(w[1]))!=(z[1],z[2]): print('REAL MISMATCH',c,z); sys.exit(1)
            e['was']=[z[1],z[2],int(bool(z[3]))]; print('fixed',e['id'],e['side'],e['t'],w,'->',e['was'])
    json.dump(ev,open(F,'w'),ensure_ascii=False,indent=1)
