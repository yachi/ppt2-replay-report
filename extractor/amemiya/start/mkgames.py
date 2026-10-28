# [am port, new file] games.json for chain/am from the start candidates (starts.py's zero-run rule on grid.py output).
# A candidate is a game when, at start+3 s and start+6 s, A's border reader sees the online PPT2 layout
# (p1 blue frame >= 0.7 and p2 red frame >= 0.7, A geometry) and both NEXT queues read 5 pieces, on >= 3 of 5 probes (+2..+6 s;
# an attack effect can cross a frame border, k-cand 14 at 828 s).
# Candidates that fail are listed with the reason (menus, lobby, pause, Puyo, the offline green-stage layout,
# other games). end_upper_s = min(next candidate - 0.3, start + 330).
import json, subprocess, sys, numpy as np
sys.path.insert(0, '/private/tmp/claude-501/am/w/chain/am/w/A')
import feat as F
V = '/private/tmp/claude-501/am/video/full.mp4'; VID = '4xcAmo-s-Tg'
starts = json.load(open('/private/tmp/claude-501/am/w/start/sheets/starts.json'))
W, H = 854, 480
def frame(t):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t:.3f}', '-i', V, '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8)[:W * H * 3].reshape(H, W, 3)
    return a[F.CY0:F.CY0 + F.CH_, F.CX0:F.CX0 + F.CW_]
games, rej = [], []
for k, s in enumerate(starts):
    ok = 0; info = []
    for o in (2.0, 3.0, 4.0, 5.0, 6.0):
        c = frame(s + o)
        b = [F.border(c, p) for p in range(2)]
        nx = [[F.piece_in_box(c, F.NEXT_X[0] + 419 * p, F.NEXT_X[1] + 419 * p, y0, y1) for y0, y1 in F.NEXT_Y] for p in range(2)]
        good = b[0] >= 0.7 and b[1] >= 0.7 and all(all(0 < x < 9 for x in q) for q in nx)
        info.append((o, [round(x, 2) for x in b], nx))
        ok += good
    ok = ok >= 3
    nxt = starts[k + 1] if k + 1 < len(starts) else s + 330
    rec = dict(cand=k, start_s=round(s, 2), end_upper_s=round(min(nxt - 0.3, s + 330), 2), probe=info)
    (games if ok else rej).append(rec)
    print(k, s, 'GAME' if ok else 'no', info, flush=True)
out = []
for i, g in enumerate(games):
    out.append(dict(id=f'k{i:03d}', video=VID, path=V, dataset='stream-2026-10-27', start_s=g['start_s'],
                    end_upper_s=g['end_upper_s'], opener='', opponent='', cand=g['cand']))
json.dump(out, open('/private/tmp/claude-501/am/w/start/games_auto.json', 'w'), ensure_ascii=False, indent=0)
json.dump(rej, open('/private/tmp/claude-501/am/w/start/rejected.json', 'w'), ensure_ascii=False, indent=0)
print(len(out), 'games', len(rej), 'rejected')
