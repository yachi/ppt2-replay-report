# [d, new file] games.json for amemiya's 2026-11-06 stream FQi9j7_ZJF8 (ids d000..), from seg.games() (seg/seg_games.json,
# 79 segments after par.py's menu filter). WIN counters at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png;
# amemiya is the left board (p1). Left out: segment 0 (COM2 practice), 1-2 (another mode, a "WINS" star counter against
# "Player 2", 963-2367 s) and 78 (another game at 13830 s, after the stream left PPT2). Set 1 is first to 15 and its last
# game (segment 24) cuts to the loading screen before the counter moves; its winner, ふられ, was read off the result screen
# at 3555 s (7-15). Sets 2 and 3 fade on the KO; their winners were read off the faded counter.
import json
K = '/tmp/claude-0/d/'; V = 'FQi9j7_ZJF8'
SETS = [  # (opponent, segment indices, counters from 0-0 to the final)
 ('ふられ', range(3, 25), '0-0 1-0 2-0 2-1 2-2 2-3 3-3 4-3 4-4 4-5 5-5 5-6 5-7 6-7 7-7 7-8 7-9 7-10 7-11 7-12 7-13 7-14 7-15'),
 ('ふられ', range(25, 51), '0-0 1-0 1-1 1-2 2-2 2-3 3-3 4-3 4-4 4-5 4-6 5-6 5-7 5-8 6-8 7-8 7-9 8-9 8-10 9-10 9-11 10-11 10-12 10-13 10-14 11-14 11-15'),
 ('いっせい', range(51, 78), '0-0 0-1 1-1 2-1 3-1 4-1 4-2 5-2 6-2 7-2 7-3 8-3 8-4 9-4 9-5 9-6 9-7 10-7 11-7 12-7 12-8 12-9 13-9 13-10 14-10 14-11 14-12 15-12'),
]
S = json.load(open(K + 'w/chain/d/seg/seg_games.json'))
out = []; n = 0
for opp, idx, cs in SETS:
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    idx = list(idx); assert len(idx) == len(c) - 1, (opp, len(idx), len(c))
    for j, si in enumerate(idx):
        d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1)), (opp, j)
        out.append(dict(id=f'd{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                        end_upper_s=round(S[si]['end'], 1), dataset='stream-2026-11-06', opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2)); n += 1
    print(opp, len(c) - 1, 'games, set', '%d-%d' % c[-1])
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'amemiya', w.count(1), 'opp', w.count(2))
