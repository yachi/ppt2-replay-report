# [r6, new file] games.json for syakegohan's stream 6rUc3cXsjbo (vs ふられ, 5先), ids n000.., from seg/seg_games.json
# (101 segments >5 s). WIN counters at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png; each set final's
# winner read off the WIN/LOSE screen (fin/fin.png). Excluded: seg 8, 42, 100 (menus), seg 7 (set 1 at 4-3:
# disconnect ~6 s into the game, no result). Set 6 also ends on a disconnect, after seg 41 finished (2-3).
import json
K = '/tmp/claude-0/r6/'; V = '6rUc3cXsjbo'
SETS = [  # (first segment, counters from 0-0 through the last game's result)
 (0,  '0-0 1-0 1-1 1-2 2-2 2-3 3-3 4-3'),
 (9,  '0-0 1-0 2-0 3-0 3-1 4-1 5-1'),
 (15, '0-0 0-1 1-1 2-1 3-1 3-2 3-3 4-3 5-3'),
 (23, '0-0 1-0 2-0 2-1 2-2 3-2 4-2 5-2'),
 (30, '0-0 1-0 1-1 1-2 2-2 3-2 4-2 5-2'),
 (37, '0-0 0-1 1-1 1-2 1-3 2-3'),
 (43, '0-0 1-0 1-1 2-1 3-1 3-2 4-2 4-3 4-4 5-4'),
 (52, '0-0 1-0 2-0 3-0 3-1 4-1 5-1'),
 (58, '0-0 1-0 1-1 2-1 2-2 3-2 3-3 3-4 3-5'),
 (66, '0-0 1-0 2-0 3-0 4-0 5-0'),
 (71, '0-0 1-0 1-1 1-2 1-3 2-3 3-3 3-4 3-5'),
 (79, '0-0 0-1 1-1 2-1 3-1 3-2 4-2 5-2'),
 (86, '0-0 1-0 2-0 3-0 4-0 5-0'),
 (91, '0-0 0-1 1-1 1-2 1-3 1-4 2-4 3-4 4-4 4-5'),
]
EXCL = {7, 8, 42, 100}
S = json.load(open(K + 'w/chain/r6/seg/seg_games.json'))
out = []; used = set(); n = 0
for si, (i0, cs) in enumerate(SETS):
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    for j in range(len(c) - 1):
        q = S[i0 + j]; used.add(i0 + j); d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1))
        out.append(dict(id=f'n{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(q['start'], 1),
                        end_upper_s=round(q['end'], 1), dataset='stream-2026-10-30', opener='', opponent='ふられ',
                        win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2))
        n += 1
    print('set', si + 1, len(c) - 1, 'games', '%d-%d' % c[-1])
assert used | EXCL == set(range(len(S))) and not used & EXCL
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'syakegohan', w.count(1), 'opp', w.count(2))
