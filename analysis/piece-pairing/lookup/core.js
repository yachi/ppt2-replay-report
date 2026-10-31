// shared by the page and the node cross-check
const SW = { J: 'L', L: 'J', S: 'Z', Z: 'S' };
function heights(b) { // b[r][c], r=0 bottom, length >= 20
  const h = [];
  for (let c = 0; c < 10; c++) { let m = 0; for (let r = 0; r < b.length; r++) if (b[r][c]) m = r + 1; h.push(m); }
  return h;
}
function sgn(v) { return (v >= 0 ? '+' : '-') + Math.abs(v); }
function key1(t, cells, h) {
  let rl = 99, c0 = 99, c1 = -1;
  for (const [r, c] of cells) { rl = Math.min(rl, r); c0 = Math.min(c0, c); c1 = Math.max(c1, c); }
  const s = cells.slice().sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  const shape = s.map(([r, c]) => `${r - rl}${c - c0}`).join('');
  let ctx = '';
  for (let c = c0 - 1; c <= c1 + 1; c++) ctx += (c < 0 || c > 9) ? 'W' : sgn(Math.max(-3, Math.min(3, h[c] - rl)));
  return t + ':' + shape + ':' + ctx;
}
function pkey(t, cells, h) {
  const a = key1(t, cells, h);
  const b = key1(SW[t] || t, cells.map(([r, c]) => [r, 9 - c]), h.slice().reverse());
  return a < b ? a : b; // python min() on str: same codepoint order for these ascii strings
}
function place(b, cells) { // returns {board, lines}; board rows 0..23
  const a = []; for (let r = 0; r < 24; r++) a.push(r < b.length ? b[r].slice() : new Array(10).fill(false));
  for (const [r, c] of cells) a[r][c] = true;
  const keep = a.filter(row => !row.every(Boolean)); const lines = 24 - keep.length;
  while (keep.length < 24) keep.push(new Array(10).fill(false));
  return { board: keep, lines };
}
function evalEl(b, cells) {
  const { board, lines } = place(b, cells);
  const h = heights(board); let holes = 0, bump = 0, sum = 0;
  for (let c = 0; c < 10; c++) { sum += h[c]; for (let r = 0; r < h[c]; r++) if (!board[r][c]) holes++; if (c < 9) bump += Math.abs(h[c] - h[c + 1]); }
  return { score: -0.510066 * sum + 0.760666 * lines - 0.35663 * holes - 0.184483 * bump, holes, bump, lines, board };
}
if (typeof module !== 'undefined') module.exports = { heights, pkey, place, evalEl };
