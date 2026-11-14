# [qh port, new file] games.json for syakegohan's stream n0Kbttgv3sQ (2026-08-16, 「わんこそばさんの大会に出る」), ids t000..,
# from seg/seg_games.json (56 segments after filt.py). WIN counters at start+3 s and end-0.3 s read by eye from
# seg/cnt/s*.png; syakegohan is the left board (p1). Opponents are read off the nameplate (Yuukun3798 is ゆうくん, named as in the other sets). Left out:
# segment 0 (menu), 1 and 7-10 (COM1 warm-up games), 28-35 (スラさん plays puyo, so not tetris vs tetris; segments 32
# and 33 also each hold several games). The last game ends with the darkened WIN screen, so seg closed it.
# るる's two sets are first to 10 (the counter shows 0 after the 10th win of the first set); the rest first to 5.
import json
K = '/tmp/claude-0/sc/'; V = 'n0Kbttgv3sQ'; DS = 'stream-2026-08-16'
SETS = [(2, 'ねっぷーさん', 'LLLLL', (5, 0)), (11, 'meah', 'LLLLL', (5, 0)), (16, 'Hirokiはいしん', 'LLLLL', (5, 0)),
        (21, 'ゆうくん', 'RLRLLLL', (5, 2)), (36, 'るる', 'L' * 10, (10, 0)), (46, 'るる', 'L' * 10, (10, 0))]
SKIP = {0: 'menu', 1: 'COM', 7: 'COM', 8: 'COM', 9: 'COM', 10: 'COM'}
SKIP.update({i: 'puyo' for i in range(28, 36)})
S = json.load(open(K + 'w/chain/sc/seg/seg_games.json'))
out = []; n = 0; used = set(SKIP)
for s0, opp, ws, fin in SETS:
    c = [0, 0]
    for j, w in enumerate(ws):
        si = s0 + j; assert si not in used, si; used.add(si)
        out.append(dict(id=f't{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                        end_upper_s=round(S[si]['end'], 1), dataset=DS, opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % tuple(c), counter_winner=1 if w == 'L' else 2)); n += 1
        c[0 if w == 'L' else 1] += 1
    assert tuple(c) == fin, (c, fin); print(opp, '%d-%d' % tuple(c))
assert used == set(range(len(S))), sorted(set(range(len(S))) - used)
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'syakegohan', w.count(1), 'opp', w.count(2))
