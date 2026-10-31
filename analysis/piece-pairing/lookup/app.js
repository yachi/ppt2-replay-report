const VID=['XoaWLJowuCQ','h3FUsPBZmzE'], VNAME=['uyeshota 直播','amemiya 直播'];
const PIECES='IOTSZJL';
const css=n=>getComputedStyle(document.documentElement).getPropertyValue(n).trim();
let board=Array.from({length:20},()=>new Array(10).fill(false));
let p1='T', p2='S', sel=null, si=0, sample=null, R1=[], R2=[];
const sortC=c=>c.slice().sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
const cj=c=>JSON.stringify(sortC(c));
function unhex(h){const b=[];for(let r=0;r<20;r++){const row=[];for(let c=0;c<10;c++){const i=r*10+c;row.push(!!(parseInt(h[i>>2],16)&(8>>(i&3))));}b.push(row);}return b;}
function stat(k){const s=RATES.k[k];return s?{av:s[0],ch:s[1],ex:s.slice(2)}:{av:0,ch:0,ex:[]};}
function rate(s){return (s.ch+RATES.A*RATES.p0)/(s.av+RATES.A);}
function compute(){
  const h=heights(board);
  const P=SRSREACH(board,p1);
  R1=P.map(c=>{const k=pkey(p1,c,h),s=stat(k),e=evalEl(board,c);return {c,k,s,r:rate(s),e};});
  R1.sort((a,b)=>b.r-a.r||b.e.score-a.e.score);
  const grI=R1.reduce((m,x,i)=>x.e.score>R1[m].e.score?i:m,0);
  R1.forEach((x,i)=>x.gr=i===grI);
  const h0=holesOf(board), bump0=bumpOf(board);
  const pairs=[];
  for(const x of R1){
    const b2=x.e.board, h2=heights(b2);
    for(const c2 of SRSREACH(b2,p2)){const s2=stat(pkey(p2,c2,h2));const e2=evalEl(b2,c2);
      const touch=!x.e.lines&&adjacent(x.c,c2);const m=touch?motif(p1,x.c,p2,c2):null;
      const L=m?(m[0]+2)/(m[1]+2):0.67;
      pairs.push({a:x,c2,s2,e2,b2,touch,m,newHoles:e2.holes-h0,r:x.r*rate(s2)*(touch?L*Math.exp(-0.2*(e2.bump-bump0)):1)});}
  }
  let pool=pairs;
  if(!ALLPAIRS){pool=pairs.filter(p=>p.touch&&p.newHoles<=0);if(!pool.length)pool=pairs.filter(p=>p.touch);}
  pool.sort((a,b)=>b.r-a.r||a.e2.bump-b.e2.bump);
  R2=pool.slice(0,8);
}
let ALLPAIRS=false;
function holesOf(b){const h=heights(b);let n=0;for(let c=0;c<10;c++)for(let r=0;r<h[c];r++)if(!b[r][c])n++;return n;}
function bumpOf(b){const h=heights(b);let n=0;for(let c=0;c<9;c++)n+=Math.abs(h[c]-h[c+1]);return n;}
function adjacent(a,b){const s=new Set(a.map(([r,c])=>r*10+c));return b.some(([r,c])=>[[1,0],[-1,0],[0,1],[0,-1]].some(([dr,dc])=>c+dc>=0&&c+dc<10&&s.has((r+dr)*10+c+dc)));}
const MSW={J:'L',L:'J',S:'Z',Z:'S'};
function motif(ta,A,tb,B){
  for(const m of [false,true]){
    const a=A.map(([r,c])=>[r,m?-c:c]), b=B.map(([r,c])=>[r,m?-c:c]);
    const r0=Math.min(...a.map(x=>x[0])), c0=Math.min(...a.map(x=>x[1]));
    const f=v=>v.map(([r,c])=>[r-r0,c-c0]).sort((x,y)=>x[0]-y[0]||x[1]-y[1]).map(([r,c])=>`${r},${c};`).join('');
    const k=(m?(MSW[ta]||ta):ta)+f(a)+(m?(MSW[tb]||tb):tb)+f(b);
    if(MOTIFS[k])return MOTIFS[k];
  }
  return null;
}
function shade(hex,f){const n=parseInt(hex.slice(1),16);let r=n>>16,g=n>>8&255,b=n&255;const t=f>0?255:0,a=Math.abs(f);r=Math.round(r+(t-r)*a);g=Math.round(g+(t-g)*a);b=Math.round(b+(t-b)*a);return `rgb(${r},${g},${b})`;}
function mino(ctx,x,y,w,col,k=.32){const e=Math.max(1.5,w*0.14);ctx.fillStyle=col;ctx.fillRect(x,y,w,w);
  ctx.fillStyle=shade(col,k);ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+w,y);ctx.lineTo(x+w-e,y+e);ctx.lineTo(x+e,y+e);ctx.lineTo(x+e,y+w-e);ctx.lineTo(x,y+w);ctx.closePath();ctx.fill();
  ctx.fillStyle=shade(col,-k);ctx.beginPath();ctx.moveTo(x+w,y+w);ctx.lineTo(x,y+w);ctx.lineTo(x+e,y+w-e);ctx.lineTo(x+w-e,y+w-e);ctx.lineTo(x+w-e,y+e);ctx.lineTo(x+w,y);ctx.closePath();ctx.fill();}
function drawCells(ctx,b,cs,ov){
  const cv=ctx.canvas,W=cv.width/10,H=cv.height/b.length,y=r=>(b.length-1-r)*H;
  ctx.fillStyle=css('--well');ctx.fillRect(0,0,cv.width,cv.height);
  ctx.strokeStyle=css('--grid');ctx.lineWidth=Math.max(1,W/30);
  for(let c=1;c<10;c++){ctx.beginPath();ctx.moveTo(c*W,0);ctx.lineTo(c*W,cv.height);ctx.stroke();}
  for(let r=1;r<b.length;r++){ctx.beginPath();ctx.moveTo(0,r*H);ctx.lineTo(cv.width,r*H);ctx.stroke();}
  const g=Math.max(0.5,W*0.04),gcol=css('--G');
  for(let r=0;r<b.length;r++)for(let c=0;c<10;c++)if(b[r][c])mino(ctx,c*W+g,y(r)+g,W-2*g,gcol,.16);
  for(const o of ov){const col=css('--'+o.t);
    for(const [r,c] of o.c){if(r>=b.length)continue;const x=c*W+g,yy=y(r)+g,w=W-2*g;
      if(o.dash){ctx.globalAlpha=.55;mino(ctx,x,yy,w,col);ctx.globalAlpha=1;ctx.strokeStyle=col;ctx.lineWidth=Math.max(2,W*0.12);const k=ctx.lineWidth/2;ctx.strokeRect(x+k,yy+k,w-2*k,w-2*k);}
      else mino(ctx,x,yy,w,col);}}
}
function crop(b){let m=0;for(let r=0;r<b.length;r++)if(b[r].some(Boolean))m=r+1;return Math.min(b.length,Math.max(8,m+4));}
function thumb(b,ov){const top=Math.max(...ov.flatMap(o=>o.c.map(x=>x[0])));const lo=Math.max(0,Math.min(...ov.flatMap(o=>o.c.map(x=>x[0])))-3);const n=Math.min(b.length,Math.max(lo+8,top+3));const sub=b.slice(lo,n);const ov2=ov.map(o=>({...o,c:o.c.map(([r,c])=>[r-lo,c])}));const cv=document.createElement('canvas');cv.width=240;cv.height=Math.round(240/10*sub.length);drawCells(cv.getContext('2d'),sub,20,ov2);return cv;}
function tags(isPro,isCC,isGr){let s='';if(isPro)s+='<span class="tag pro">高手實際</span> ';if(isCC)s+='<span class="tag cc">Cold Clear</span> ';if(isGr)s+='<span class="tag gr">El-Tetris</span>';return s;}
function exl(ex){return ex.map(([v,t])=>`<a href="https://youtu.be/${VID[v]}?t=${t}" target="_blank" rel="noopener">▶ ${VNAME[v]} ${Math.floor(t/60)}:${String(t%60).padStart(2,'0')}</a>`).join('');}
function pct(s){return s.av?`${s.ch}/${s.av} 次（${Math.round(100*s.ch/s.av)}%）`:'冇見過呢個情況';}
function render(){
  const maxr=Math.max(...R1.map(x=>x.r),0.0001);
  const c1=document.getElementById('c1');c1.innerHTML='';
  const proK=sample&&sample.a===p1?cj(sample.pro):null, ccK=sample&&sample.cc&&sample.a===p1?cj(sample.cc):null;
  document.getElementById('n1').textContent=R1.length?`${p1} 有 ${R1.length} 個可以擺嘅位。顯示頭 8 個，加埋其他標記咗嘅。`:`${p1} 喺呢個 board 擺唔落。`;
  const show=R1.filter((x,i)=>i<8||x.gr||cj(x.c)===proK||cj(x.c)===ccK);
  show.forEach(x=>{const i=R1.indexOf(x);const b=document.createElement('button');b.className='cand';b.setAttribute('aria-pressed',sel&&sel.k==='1'&&sel.i===i?'true':'false');
    b.innerHTML=`<span class="rk">${i+1}</span><span class="th"></span><span class="meta"><span class="num">${pct(x.s)}</span><span class="bar"><i style="width:${100*x.r/maxr}%"></i></span><span>${tags(cj(x.c)===proK,cj(x.c)===ccK,x.gr)}</span><span class="ex">${exl(x.s.ex)}</span></span>`;
    b.querySelector('.th').appendChild(thumb(board,[{c:x.c,t:p1}]));
    b.onclick=e=>{if(e.target.closest('a'))return;sel={k:'1',i};render();const bd=document.getElementById('board').getBoundingClientRect();if(bd.bottom<0||bd.top>innerHeight)document.getElementById('board').scrollIntoView({behavior:'smooth',block:'center'});};c1.appendChild(b);});
  const c2=document.getElementById('c2');c2.innerHTML='';
  const pro2K=sample&&sample.pro2&&sample.a===p1&&sample.n===p2?cj(sample.pro2):null;
  document.getElementById('n2').textContent=!R2.length?'冇得計。':ALLPAIRS?'包埋唔痴埋嘅組合，按兩粒各自嘅揀率排。第一粒清行嘅話，縮圖畫清行之後嘅 board。':'淨係列第二粒痴住第一粒、又唔會整多個窿嘅擺法。排法：兩粒各自嘅揀率，再乘高手痴埋擺呢個形嘅次數比隨機多幾多倍，擺完愈凹凸就扣分愈多。';
  const maxp=Math.max(...R2.map(x=>x.r),1e-9);
  R2.forEach((x,i)=>{const b=document.createElement('button');b.className='cand';b.setAttribute('aria-pressed',sel&&sel.k==='2'&&sel.i===i?'true':'false');
    const pro=proK&&cj(x.a.c)===proK&&pro2K&&cj(x.c2)===pro2K&&!x.a.e.lines;
    b.innerHTML=`<span class="rk">${i+1}</span><span class="th"></span><span class="meta"><span class="num">${p1}：${pct(x.a.s)}</span><span class="num">${p2}：${pct(x.s2)}</span><span class="bar"><i style="width:${100*x.r/maxp}%"></i></span><span>${tags(pro,false,false)}${x.a.e.lines?` <span class="note">第一粒清 ${x.a.e.lines} 行</span>`:''}</span><span class="note">${x.touch?(x.m?`高手痴埋擺呢個形 ${x.m[0]} 次（隨機預期 ${x.m[1]} 次）`:'高手未痴埋擺過呢個形'):'兩粒冇痴埋'}・凹凸 ${bumpOf(board)} → ${x.e2.bump}${x.newHoles>0?`・多咗 ${x.newHoles} 個窿`:''}</span></span>`;
    b.querySelector('.th').appendChild(thumb(...pairView(x)));
    b.onclick=()=>{sel={k:'2',i};render();const bd=document.getElementById('board').getBoundingClientRect();if(bd.bottom<0||bd.top>innerHeight)document.getElementById('board').scrollIntoView({behavior:'smooth',block:'center'});};c2.appendChild(b);});
  drawMain();
}
function pairView(x){return x.a.e.lines?[x.b2,[{c:x.c2,t:p2,dash:true}]]:[board,[{c:x.a.c,t:p1},{c:x.c2,t:p2,dash:true}]];}
function drawMain(){const ctx=document.getElementById('board').getContext('2d');let b=board,ov=[];
  if(sel&&sel.k==='1'&&R1[sel.i])ov=[{c:R1[sel.i].c,t:p1}];
  if(sel&&sel.k==='2'&&R2[sel.i]){[b,ov]=pairView(R2[sel.i]);b=b.slice(0,20);}
  drawCells(ctx,b,30,ov);const sh=document.getElementById('showing');sh.textContent=sel&&sel.k==='2'?`而家畫緊：兩粒組合第 ${sel.i+1} 個（${p1} 實色，${p2} 半透明框）`:sel?`而家畫緊：第一粒第 ${sel.i+1} 個位（淨係 ${p1}）`:'';}
function refresh(keepSel){compute();if(!keepSel)sel=R2.length?{k:'2',i:0}:R1.length?{k:'1',i:0}:null;render();}
function pickers(){for(const [id,get,set] of [['p1',()=>p1,v=>p1=v],['p2',()=>p2,v=>p2=v]]){const el=document.getElementById(id);el.innerHTML='';
  for(const t of PIECES){const b=document.createElement('button');b.className='pc';b.textContent=t;b.style.background=css('--'+t);b.setAttribute('aria-pressed',get()===t?'true':'false');b.setAttribute('aria-label',`${id==='p1'?'第一粒':'第二粒'} ${t}`);
    b.onclick=()=>{set(t);pickers();showSample();refresh();};el.appendChild(b);}}}
function showSample(){const el=document.getElementById('samp');if(!sample){el.hidden=true;return;}el.hidden=false;
  const [v,t]=sample.src;const same=sample.a===p1&&sample.n===p2;
  el.innerHTML=`<b>例子 ${si+1}/${SAMPLES.length}</b>：${VNAME[v]} <a href="https://youtu.be/${VID[v]}?t=${t}" target="_blank" rel="noopener">${Math.floor(t/60)}:${String(t%60).padStart(2,'0')}</a>。高手擺咗 ${sample.a}，跟住擺 ${sample.n}。`+(same?'清單入面標咗佢實際擺嘅位同 Cold Clear 揀嘅位。':'你改咗方塊，所以唔再標實際擺法。');}
function load(i){si=(i+SAMPLES.length)%SAMPLES.length;sample=SAMPLES[si];board=unhex(sample.b);p1=sample.a;p2=sample.n;pickers();showSample();refresh();}
// editor
(function(){const cv=document.getElementById('board');let mode=null;
  const cell=e=>{const r=cv.getBoundingClientRect();const c=Math.floor((e.clientX-r.left)/r.width*10),row=19-Math.floor((e.clientY-r.top)/r.height*20);return c>=0&&c<10&&row>=0&&row<20?[row,c]:null;};
  cv.addEventListener('pointerdown',e=>{const p=cell(e);if(!p)return;cv.setPointerCapture(e.pointerId);mode=!board[p[0]][p[1]];board[p[0]][p[1]]=mode;sample=null;showSample();drawCells(cv.getContext('2d'),board,30,[]);});
  cv.addEventListener('pointermove',e=>{if(mode===null)return;const p=cell(e);if(p&&board[p[0]][p[1]]!==mode){board[p[0]][p[1]]=mode;drawCells(cv.getContext('2d'),board,30,[]);}});
  const up=()=>{if(mode!==null){mode=null;refresh();}};cv.addEventListener('pointerup',up);cv.addEventListener('pointercancel',up);})();
document.getElementById('allp').onchange=e=>{ALLPAIRS=e.target.checked;refresh(true);};
document.getElementById('clear').onclick=()=>{board=board.map(r=>r.map(()=>false));sample=null;showSample();refresh();};
document.getElementById('prev').onclick=()=>load(si-1);document.getElementById('next').onclick=()=>load(si+1);
document.getElementById('rand').onclick=()=>load(Math.floor(Math.random()*SAMPLES.length));
// accuracy table
(function(){const t=document.getElementById('acc');t.innerHTML='<tr><th>方法</th><th>睇到乜</th><th>第一選擇同高手一樣</th></tr>'+ACC.rows.map(r=>`<tr><td>${r[0]}</td><td>${r[1]}</td><td class="n">${r[2]}</td></tr>`).join('');
  document.getElementById('accnote').textContent=ACC.note;document.getElementById('caveats').innerHTML=ACC.caveats.map(c=>`<li>${c}</li>`).join('');})();
const rerender=()=>{pickers();render();};
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',rerender);
new MutationObserver(rerender).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
load(0);
