# [tx port, new file] games.json for amemiya's stream _TXAJq53mWU (ids w000..), from seg.games() (seg/seg_games.json,
# 85 segments after par.py's menu filter). WIN counters at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png;
# amemiya is the left board (p1). Segment 0 is a game against COM2 and segment 84 is not PPT2 (the stream moved to
# another game); neither is counted. 3918-4789 s and 6023 s on are offline local games, not segmented as online play.
# Segment 9 (6-2 in the first set vs ゆうくん) ended in a disconnect (「通信相手との接続が切断されました」, no result);
# the room was remade and the 15先 sets restarted from 0-0. Segments 34, 62 and 83 end on the result screen (read by eye).
import json
K = '/tmp/claude-0/tx/'; V = '_TXAJq53mWU'
SETS = [  # (opponent, segment indices, counters from 0-0 to the final)
 ('ゆうくん', range(1, 9), '0-0 0-1 0-2 1-2 2-2 3-2 4-2 5-2 6-2'),
 ('ゆうくん', range(10, 35), '0-0 1-0 2-0 3-0 4-0 5-0 6-0 6-1 6-2 6-3 7-3 7-4 8-4 9-4 10-4 11-4 11-5 11-6 12-6 12-7 12-8 13-8 13-9 14-9 14-10 15-10'),
 ('ゆうくん', range(35, 63), '0-0 1-0 1-1 2-1 3-1 3-2 3-3 4-3 4-4 4-5 4-6 4-7 4-8 4-9 5-9 5-10 5-11 6-11 6-12 7-12 8-12 9-12 10-12 11-12 12-12 13-12 13-13 14-13 15-13'),
 ('ぶぶ', range(63, 84), '0-0 1-0 2-0 3-0 4-0 5-0 6-0 6-1 6-2 7-2 8-2 9-2 10-2 10-3 10-4 10-5 11-5 12-5 12-6 13-6 14-6 15-6'),
]
END = {}
S = json.load(open(K + 'w/chain/tx/seg/seg_games.json'))
out = []; n = 0
def row(si, opp, c0, d):
    return dict(id=f'w{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                end_upper_s=END.get(si, round(S[si]['end'], 1)), dataset='stream-2026-11-03', opener='',
                opponent=opp, win_counter_at_start='%d-%d' % c0,
                counter_winner=None if d is None else (1 if d == (1, 0) else 2))
for opp, idx, cs in SETS:
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    idx = list(idx); assert len(idx) == len(c) - 1, (opp, len(idx), len(c))
    for j, si in enumerate(idx):
        d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1)), (opp, j)
        out.append(row(si, opp, c[j], d)); n += 1
    print(opp, len(c) - 1, 'games, set', '%d-%d' % c[-1])
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
dis = row(9, 'ゆうくん', (6, 2), None); dis['id'] = 'w_disconnect'; dis['note'] = 'opponent disconnected, no result'
json.dump(out + [dis], open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'amemiya', w.count(1), 'opp', w.count(2))
