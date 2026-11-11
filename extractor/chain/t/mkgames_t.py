# [t, new file] games.json for amemiya's upload armDs7VaDyk vs uyeshota (7先 x 6, dataset upload-2025-08-20, ids t000..),
# from seg.games() (seg/seg_games.json, 57 segments). WIN counters at start+3 s and end-0.3 s read by eye from contact
# sheets; amemiya is the left board (p1). The upload is edited, but every set's last game shows the counter move (or the
# WINNER screen) before the cut, so each set-final winner was read there. Totals: 57 games, amemiya 32-25.
import json
K = '/tmp/claude-0/t/'; V = 'armDs7VaDyk'
SETS = [  # (opponent, segment indices, WIN counters from 0-0 to the final); 7先 x 6, all vs uyeshota
 ('uyeshota', range(0, 10), '0-0 1-0 1-1 2-1 3-1 3-2 4-2 5-2 6-2 6-3 7-3'),
 ('uyeshota', range(10, 19), '0-0 0-1 1-1 2-1 3-1 4-1 5-1 6-1 6-2 7-2'),
 ('uyeshota', range(19, 28), '0-0 1-0 1-1 1-2 2-2 3-2 4-2 5-2 6-2 7-2'),
 ('uyeshota', range(28, 36), '0-0 0-1 0-2 0-3 0-4 0-5 1-5 1-6 1-7'),
 ('uyeshota', range(36, 46), '0-0 0-1 0-2 1-2 1-3 1-4 2-4 2-5 3-5 3-6 3-7'),
 ('uyeshota', range(46, 57), '0-0 1-0 1-1 2-1 3-1 4-1 5-1 5-2 5-3 5-4 6-4 7-4'),
]
S = json.load(open(K + 'w/chain/t/seg/seg_games.json'))
out = []; n = 0
for opp, idx, cs in SETS:
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    idx = list(idx); assert len(idx) == len(c) - 1, (opp, len(idx), len(c))
    for j, si in enumerate(idx):
        d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1)), (opp, j)
        out.append(dict(id=f't{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                        end_upper_s=round(S[si]['end'], 1), dataset='upload-2025-08-20', opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2)); n += 1
    print(opp, len(c) - 1, 'games, set', '%d-%d' % c[-1])
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'amemiya', w.count(1), 'opp', w.count(2))
