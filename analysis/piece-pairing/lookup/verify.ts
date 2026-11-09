import { readFileSync, writeFileSync } from 'fs';
import { newEngine, reach, inputsOf } from '/home/user/tetrio-replay-report/pipeline/sim/route-demos.ts';
import { ROWS, WIDTH } from '/home/user/tetrio-replay-report/pipeline/sim/emit-replay.ts';
import { isValidPosition, tryMove, getPieceCells } from '/home/user/tetrio-replay-report/pipeline/sim/vendor/core/srs.ts';
const P = '/tmp/claude-0/pp/';
const src = [P + 'page/srs.js', P + 'page/core.js', P + 'verify/data.js', P + 'verify/logic.js']
  .map(f => readFileSync(f, 'utf8')).join('\n;\n').replace('if (typeof module', 'if (false && typeof module');
(0, eval)(src);
const G: any = globalThis; const A = G.API;
const ROUTES = { source: { fetched: '2026-10-31' } };
const eng0 = newEngine(ROUTES);
const sortC = (c: number[][]) => c.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]);
const tgt = (cells: number[][]) => cells.map(([r, c]) => r * WIDTH + c);
const grid = (b: boolean[][]) => Array.from({ length: ROWS }, (_, y) => Array.from({ length: WIDTH }, (_, x) => (b[y] && b[y][x]) ? 'g' : null));
const occ = (eng: any) => Array.from({ length: 24 }, (_, y) => Array.from({ length: 10 }, (_, x) => !!(eng.board.state[y] && eng.board.state[y][x])));
const bkey = (b: boolean[][]) => b.slice(0, 24).map(r => r.map(v => v ? 1 : 0).join('')).join('/');
// play pieces from a starting board through the real engine (ticks, key events, hard drop)
function play(b: boolean[][], seq: string, paths: { edges: any[] }[]) {
  const eng = newEngine(ROUTES);
  eng.board.state = grid(b).map(r => r.map(c => (c ? { mino: 'gb', connections: 0 } : null)));
  eng.queue.splice(0, eng.queue.length, ...[...seq.slice(1) + 'IJLOSTZIJLOSTZ'].map(c => c.toLowerCase()));
  eng.initiatePiece(seq[0].toLowerCase());
  const { inputs, frames } = inputsOf(paths.map(p => ({ edges: p.edges, hold: false })) as any);
  const by = new Map<number, any[]>();
  for (const [fr, type, k] of inputs) { if (!by.has(fr)) by.set(fr, []); by.get(fr)!.push({ frame: fr, type, data: { key: k, subframe: 0 } }); }
  for (let fr = 0; fr <= frames; fr++) eng.tick(by.get(fr) || []);
  return eng;
}
// every resting position the page's own geometry admits, asked of the engine (independent full set)
function engineSet(b: boolean[][], piece: string) {
  const H = 40; const bb: any = Array.from({ length: H }, () => new Array(10).fill(null));
  for (let r = 0; r < 20; r++) for (let c = 0; c < 10; c++) if (b[r][c]) bb[39 - r][c] = 'G';
  const out = new Set<string>();
  for (let rot = 0; rot < 4; rot++) for (let col = -3; col < 12; col++) for (let row = 0; row < 40; row++) {
    const p = { type: piece, rotation: rot, col, row };
    if (!isValidPosition(bb, p as any) || tryMove(bb, p as any, 0, 1)) continue;
    const cs = sortC(getPieceCells(p as any).map((c: any) => [39 - c.row, c.col]));
    if (cs.some(([r]) => r >= 20)) continue;
    if (reach(eng0, grid(b), piece, tgt(cs), { no180: true }).length) out.add(JSON.stringify(cs));
  }
  return out;
}
const res: any = { singles: 0, singlesBad: [], pairs: 0, pairsBad: [], setDiff: [], samples: 0, unreachableTop: 0 };
for (const [si, s] of G.SAMPLES.entries()) {
  const b = A.unhex(s.b);
  res.samples++;
  // 1) the page's whole candidate list vs the engine's own reachable set
  const page = new Set<string>((G.SRSREACH(b, s.a) as number[][][]).map(c => JSON.stringify(sortC(c))));
  const eng = engineSet(b, s.a);
  const onlyPage = [...page].filter(x => !eng.has(x)), onlyEng = [...eng].filter(x => !page.has(x));
  if (onlyPage.length || onlyEng.length) res.setDiff.push({ si, piece: s.a, onlyPage, onlyEng });
  for (const all of [false, true]) {
    A.set(b, s.a, s.n, all); A.compute();
    // 2) top-8 singles: engine path, then play it and compare the board
    for (const x of A.R1.slice(0, 8)) {
      if (all) break;
      res.singles++;
      const p = reach(eng0, grid(b), s.a, tgt(x.c), { no180: true });
      if (!p.length) { res.singlesBad.push({ si, cells: x.c, why: 'unreachable' }); continue; }
      const e = play(b, s.a + s.n, [p[0]]);
      if (bkey(occ(e)) !== bkey(x.e.board)) res.singlesBad.push({ si, cells: x.c, why: 'board differs' });
    }
    // 3) top-8 pairs (default and all-pairs mode): both pieces through the engine in one run
    for (const q of A.R2) {
      res.pairs++;
      const p1 = reach(eng0, grid(b), s.a, tgt(q.a.c), { no180: true });
      const p2 = p1.length ? reach(eng0, grid(q.b2), s.n, tgt(q.c2), { no180: true }) : [];
      if (!p1.length || !p2.length) { res.pairsBad.push({ si, all, why: !p1.length ? 'first unreachable' : 'second unreachable' }); continue; }
      const e = play(b, s.a + s.n, [p1[0], p2[0]]);
      if (bkey(occ(e)) !== bkey(q.e2.board)) res.pairsBad.push({ si, all, why: 'board differs' });
    }
  }
}
writeFileSync(P + 'verify/result.json', JSON.stringify(res, null, 1));
console.log(JSON.stringify({ samples: res.samples, singles: res.singles, singlesBad: res.singlesBad.length, pairs: res.pairs, pairsBad: res.pairsBad.length, setDiff: res.setDiff.length }));
console.log(JSON.stringify(res.singlesBad.slice(0, 5)), JSON.stringify(res.pairsBad.slice(0, 5)));
console.log(JSON.stringify(res.setDiff.slice(0, 3).map((d: any) => ({ si: d.si, piece: d.piece, onlyPage: d.onlyPage.length, onlyEng: d.onlyEng.length, ex: d.onlyPage[0] || d.onlyEng[0] }))));
