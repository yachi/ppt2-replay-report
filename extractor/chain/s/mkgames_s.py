# [s, new file] games.json for amemiya's upload 6nzD6OsKuuY (「VS uyeshota！15先×3回」, uploaded 2025-07-05, ids s000..),
# from seg.games() (seg/seg_games.json, 75 segments after par.py's menu filter). WIN counters at start+3 s and end-0.3 s
# read by eye from seg/cnt/s*.png; amemiya is the left board (p1). The upload is edited: each set's last game cuts to the
# loading screen, so its winner was read off the result screen just before the cut (1496 s: amemiya WINNER at 15-8;
# 2774 s: uyeshota WIN! at 8-15).
import json
K = '/tmp/claude-0/s/'; V = '6nzD6OsKuuY'
SETS = [  # (opponent, segment indices, counters from 0-0 to the final)
 ('uyeshota', range(0, 23), '0-0 0-1 1-1 2-1 3-1 4-1 5-1 6-1 6-2 7-2 7-3 7-4 8-4 9-4 9-5 9-6 10-6 10-7 11-7 12-7 12-8 13-8 14-8 15-8'),
 ('uyeshota', range(23, 46), '0-0 0-1 1-1 1-2 1-3 2-3 2-4 2-5 2-6 2-7 2-8 2-9 3-9 3-10 4-10 5-10 5-11 6-11 6-12 6-13 7-13 8-13 8-14 8-15'),
 ('uyeshota', range(46, 75), '0-0 1-0 1-1 2-1 2-2 3-2 3-3 3-4 4-4 5-4 5-5 5-6 5-7 5-8 5-9 5-10 6-10 7-10 7-11 7-12 7-13 8-13 9-13 10-13 11-13 12-13 13-13 14-13 14-14 15-14'),
]
S = json.load(open(K + 'w/chain/s/seg/seg_games.json'))
out = []; n = 0
for opp, idx, cs in SETS:
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    idx = list(idx); assert len(idx) == len(c) - 1, (opp, len(idx), len(c))
    for j, si in enumerate(idx):
        d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1)), (opp, j)
        out.append(dict(id=f's{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                        end_upper_s=round(S[si]['end'], 1), dataset='upload-2025-07-05', opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2)); n += 1
    print(opp, len(c) - 1, 'games, set', '%d-%d' % c[-1])
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'amemiya', w.count(1), 'opp', w.count(2))
