"""Render page.html (a study-page fragment for bin/build-docs) from mid.json, all.json and tpl.html."""
import json,html,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
D=str(HERE)+'/'
m=json.load(open(D+'mid.json')); a=json.load(open(D+'all.json'))
def board(s):
    rows=s.split('\n'); w=max(len(r) for r in rows)
    out=[f'<div class="bd" style="grid-template-columns:repeat({w},var(--c))">']
    for r in rows:
        for ch in r.ljust(w):
            if ch=='.': out.append('<i></i>')
            else:
                cls=('p-'+ch.upper())+(' b' if ch.islower() else '')
                out.append(f'<i class="{cls}"></i>')
    out.append('</div>'); return ''.join(out)
def real(bd):
    bits=bin(int(bd['pre'],16))[2:].zfill(len(bd['pre'])*4)
    g={}
    for r in range(len(bits)//10):
        for c in range(10):
            if bits[r*10+c]=='1': g[(r,c)]='g'
    for j,(t,cs) in enumerate(bd['pieces']):
        for r,c in cs: g[(r,c)]='p-'+t+(' b' if j%2 else '')
    top=max(r for r,_ in g)+1
    out=['<div class="bd real">']
    for r in range(top,-1,-1):
        for c in range(10):
            v=g.get((r,c)); out.append(f'<i class="{v}"></i>' if v else '<i></i>')
    out.append('</div>'); return ''.join(out)
def tsec(u): t=int(u.split('t=')[1]); return f'{t//60}:{t%60:02d}'
def links(us): return ' '.join(f'<a href="{u}" target="_blank" rel="noopener">{tsec(u)}</a>' for u in us)
rows=[]
for ty,n,c,r,u in [x for x in m['pair_types'] if x[2]>=50]:
    d=r-u; cls='up' if d>=0.05 else ('down' if d<=-0.05 else '')
    rows.append(f'<tr class="{cls}"><td class="ty">{ty[0]} + {ty[1]}</td><td class="n">{n}</td><td class="n">{c}</td>'
      f'<td><div class="bar"><span class="r" style="width:{r*100:.0f}%"></span><span class="u" style="left:{u*100:.0f}%"></span></div></td>'
      f'<td class="n">{r*100:.0f}%</td><td class="n mut">{u*100:.0f}%</td></tr>')
    ex=''.join(f'<figure class="sm">{board(d)}{real(bd)}<figcaption><b>{k} 次</b><span>{links(us[:2])}</span></figcaption></figure>' for d,k,us,bd in m['type_motifs'][ty] if k>=3)
    rows.append(f'<tr class="ex"><td colspan="6"><div class="exs">{ex}</div></td></tr>')
pm=''.join(f'<figure><div class="two">{board(s)}{real(bd)}</div><figcaption><b>{n} 次</b><span>{links(us)}</span></figcaption></figure>' for s,n,us,bd in m['pair_motifs'][:12])
def shape(ps):
    cells={}
    for j,(t,cs) in enumerate(ps):
        for r,c in cs: cells[(r,c)]=t if j%2==0 else t.lower()
    r0=min(r for r,_ in cells);r1=max(r for r,_ in cells);c0=min(c for _,c in cells);c1=max(c for _,c in cells)
    return '\n'.join(''.join(cells.get((r,c),'.') for c in range(c0,c1+1)) for r in range(r1,r0-1,-1))
tex=''
for ts,v in m['triple_type_examples'].items():
    if v['n']<6: continue
    cards=''.join(f'<figure class="sm">{board(shape(e["pieces"]))}{real(e)}<figcaption><span>{links([e["url"]])}</span></figcaption></figure>' for e in v['examples'])
    tex+=f'<div class="tri"><h3>{"+".join(ts)}<span>{v["n"]} 次</span></h3><div class="exs">{cards}</div></div>'
sp='';
for t in 'JLSZIO':
    v=m['spins'][t]
    if not v['n']:
        sp+=f'<div class="tri"><h3>{t}<span>0 / {v["of"]}</span></h3></div>'; continue
    cards=''.join(f'<figure class="sm">{real(e)}<figcaption><span>{links([e["url"]])}</span><span>{"清 "+str(e["lines"])+" 行" if e["lines"] else "冇清行"}</span></figcaption></figure>' for e in v['examples'])
    sp+=f'<div class="tri"><h3>{t}<span>{v["n"]} / {v["of"]} 粒</span></h3><div class="exs">{cards}</div></div>'
tt=''.join(f'<li><b>{"+".join(t)}</b><span>{n}</span></li>' for t,n in m['triple_types'][:15])
tm=''.join(f'<figure><div class="two">{board(s)}{real(bd)}</div><figcaption><b>{n} 次</b><span>{links(us)}</span></figcaption></figure>' for s,n,us,bd in m['triple_motifs'] if n>=3)
allt=', '.join(f'{t[0]}+{t[1]} {n}' for t,n,*_ in sorted(a['pair_types'],key=lambda x:-x[1])[:5])
tpl=open(HERE/'tpl.html').read()
for k,v in dict(ROWS=''.join(rows),PM=pm,TT=tt,SP=sp,SPN=str(sum(v['n'] for v in m['spins'].values())),SPOF=str(sum(v['of'] for v in m['spins'].values())),TEX=tex,TM=tm,ALLT=allt,PAIRS=str(m['pairs']),TOUCH=str(m['touch']),
  TR=f"{m['touch']/m['pairs']*100:.0f}",TRIP=str(m['triples']),APAIRS=str(a['pairs']),ATOUCH=str(a['touch'])).items():
    tpl=tpl.replace('{{'+k+'}}',v)
# bin/build-docs wraps a fragment: drop the document start and end here
frag=re.sub(r'^<!doctype html><html[^>]*><head><meta charset="utf-8">\n<meta name="viewport"[^>]*>\n','',tpl)
assert frag!=tpl and frag.rstrip().endswith('</html>')
frag=frag.rstrip()[:-len('</html>')].rstrip()+'\n'
open(HERE/'page.html','w').write(frag)
