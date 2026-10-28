# Running difference (score seen - clear points predicted) per player-game; report each lasting step
# >= 350 that is not a zero-line T-spin (1200 +- 60) as a spot to frame-check.
import json, sys
sys.path.insert(0, '/private/tmp/claude-501/uP/w/ocrall'); sys.path.insert(0, '/private/tmp/claude-501/uP/corr/score')
from jumps import events
from scoresum import BASE, HARD, L, S, J, W
spots = []
for g in sorted(J):
    if f'{g} p1' not in S: continue
    r = json.load(open(f'{W}/ocrall/{g}.json')); end = J[g]['end_s']
    for p, si in (('p1', 1), ('p2', 3)):
        seq = S[f'{g} {p}']
        if any(z[1] == 'BREAK' for z in seq) or any(z[3] for z in seq): continue   # unmodelled: B gap lines, PC bonus
        pts = []; ren, b2b = -1, False
        for t, k, n, pc, gc in seq:
            if k is None: ren = -1; continue
            ren += 1; q = BASE[k] * L
            if k in HARD:
                q = q * 3 // 2 if b2b else q; b2b = True
            else: b2b = False
            pts.append((t, q + 50 * ren * L, k))
        jumps = [x for x in events([(x[0], x[si]) for x in r]) if x[0] <= end + 0.3]
        # settled points: a jump followed by >= 2 s with no jump; predicted counts clears spawned <= that jump
        settled = []; cum_seen = 0; i = 0; cum_pred = 0
        for k, (tj, d) in enumerate(jumps):
            cum_seen += d
            nxt = jumps[k + 1][0] if k + 1 < len(jumps) else 1e9
            if nxt - tj < 2.0: continue
            while i < len(pts) and pts[i][0] <= tj + 0.05: cum_pred += pts[i][1]; i += 1
            settled.append((tj, cum_seen - cum_pred))
        prev_t, prev = None, 0
        for tj, diff in settled:
            step = diff - prev
            zero_ts = round(step / 1200) if step > 0 else 0
            rest = step - 1200 * zero_ts
            if abs(rest) >= 350:
                spots.append(dict(id=g, player=p, t0=prev_t, t1=tj, step=step, unexplained=rest,
                                  near=[x for x in pts if (prev_t or 0) - 0.5 <= x[0] <= tj + 0.05]))
            prev_t, prev = tj, diff
json.dump(spots, open('/private/tmp/claude-501/uP/corr/score/spots.json', 'w'), ensure_ascii=False, indent=0)
print(len(spots), 'spots in', len({(s['id'], s['player']) for s in spots}), 'player-games')
for s in spots[:12]: print(s)
