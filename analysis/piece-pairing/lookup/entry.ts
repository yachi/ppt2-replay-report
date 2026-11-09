import { isValidPosition, tryMove, tryRotate, getPieceCells } from '/home/user/tetrio-replay-report/pipeline/sim/vendor/core/srs.ts';
// board: boolean[20][10] with row0 = bottom. returns list of placements [[r,c]x4] sorted
export function reach(occ: boolean[][], piece: string): number[][][] {
  const H = 40;
  const b: (string|null)[][] = Array.from({ length: H }, () => new Array(10).fill(null));
  for (let r = 0; r < occ.length && r < 40; r++) for (let c = 0; c < 10; c++) if (occ[r][c]) b[39 - r][c] = 'G';
  const spawn: any = { type: piece, rotation: 0, col: 3, row: 18 };
  const out = new Map<string, number[][]>();
  if (!isValidPosition(b as any, spawn)) return [];
  const k = (p: any) => `${p.rotation}:${p.col}:${p.row}`;
  const seen = new Set([k(spawn)]); const q: any[] = [spawn];
  for (let h = 0; h < q.length && h < 60000; h++) {
    const cur = q[h];
    if (!tryMove(b as any, cur, 0, 1)) {
      const cs = getPieceCells(cur).map((c: any) => [39 - c.row, c.col]).sort((a, z) => a[0]-z[0] || a[1]-z[1]);
      out.set(JSON.stringify(cs), cs);
    }
    for (const [dx, dy] of [[-1,0],[1,0],[0,1]] as const) { const n = tryMove(b as any, cur, dx, dy); if (n && !seen.has(k(n))) { seen.add(k(n)); q.push(n); } }
    for (const d of [1, -1] as const) { const n = tryRotate(b as any, cur, d); if (n && !seen.has(k(n))) { seen.add(k(n)); q.push(n); } }
  }
  return [...out.values()];
}
(globalThis as any).SRSREACH = reach;
