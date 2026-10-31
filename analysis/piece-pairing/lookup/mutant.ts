import { readFileSync } from 'fs';
import { newEngine, reach } from '/home/user/tetrio-replay-report/pipeline/sim/route-demos.ts';
import { ROWS, WIDTH } from '/home/user/tetrio-replay-report/pipeline/sim/emit-replay.ts';
const P='/tmp/claude-0/pp/';
(0,eval)([P+'page/srs.js',P+'page/core.js',P+'verify/data.js',P+'verify/logic.js'].map(f=>readFileSync(f,'utf8')).join('\n;\n').replace('if (typeof module','if (false && typeof module'));
const G:any=globalThis,A=G.API,eng=newEngine({source:{fetched:'2026-10-31'}});
const grid=(b:boolean[][])=>Array.from({length:ROWS},(_,y)=>Array.from({length:WIDTH},(_,x)=>(b[y]&&b[y][x])?'g':null));
let n=0,caught=0;
for(const s of G.SAMPLES){const b=A.unhex(s.b);A.set(b,s.a,s.n,false);A.compute();
 for(const x of A.R1.slice(0,8)){ for(const d of [[1,0],[0,1],[0,-1]]){n++;const t=x.c.map(([r,c]:any)=>(r+d[0])*WIDTH+c+d[1]);if(!reach(eng,grid(b),s.a,t,{no180:true}).length)caught++;}}}
console.log('shifted placements rejected',caught,'of',n);
