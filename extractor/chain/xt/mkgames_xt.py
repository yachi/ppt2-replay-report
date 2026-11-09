# [xt port, new file] games.json for uyeshota's stream XTveY1Z22jU (ids v000..), from seg.games() (seg/seg_games.json,
# 137 segments after par.py's menu filter). WIN counters at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png.
# The streamer twice seeks back in his own YouTube archive (the win-prediction tool he was trying) and replays a set:
# segments 17-26 replay set 1's games 7-16 and 44-60 replay set 2's 27-43 (board-matched, w/look/dup.py). Near the end
# he seeks back during the fifth Solitar game: segment 132 is that game's live start, 133-135 replay 129-131, and 136
# is the replayed copy of 132 that runs to the result screen, so 136 stands for it. Segment 126 ended in a disconnect
# (「通信相手との接続が切断されました」, no result) and 127 is a game against COM1; neither is counted.
import json
K = '/tmp/claude-0/xt/'; V = 'XTveY1Z22jU'
SETS = [  # (opponent, segment indices, counters from 0-0 to the final)
 ('あ', range(0, 17), '0-0 1-0 2-0 2-1 3-1 4-1 5-1 6-1 7-1 7-2 8-2 9-2 10-2 11-2 12-2 13-2 14-2 15-2'),
 ('ふらいこん', range(27, 44), '0-0 0-1 1-1 2-1 3-1 4-1 5-1 6-1 7-1 7-2 8-2 9-2 10-2 11-2 12-2 13-2 14-2 15-2'),
 ('???', range(61, 76), ' '.join('%d-0' % i for i in range(16))),
 ('おはゆれ', range(76, 100), '0-0 1-0 1-1 2-1 3-1 4-1 4-2 4-3 4-4 4-5 5-5 5-6 6-6 7-6 8-6 8-7 9-7 9-8 10-8 11-8 12-8 12-9 13-9 14-9 15-9'),
 ('ろうがい', range(100, 124), '0-0 1-0 2-0 2-1 3-1 4-1 4-2 5-2 5-3 6-3 7-3 8-3 9-3 9-4 9-5 10-5 11-5 11-6 11-7 11-8 11-9 12-9 13-9 14-9 15-9'),
 ('Solitar', [124, 125], '0-0 1-0 2-0'),
 ('Solitar', [128, 129, 130, 131, 136], '0-0 1-0 2-0 3-0 4-0 5-0'),
]
END = {136: 7790.0}  # the replay leaves the result screen for the room select by 7792 (frames read by eye)
S = json.load(open(K + 'w/chain/xt/seg/seg_games.json'))
out = []; n = 0
def row(q, si, opp, c0, d):
    return dict(id=f'v{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                end_upper_s=END.get(si, round(S[si]['end'], 1)), dataset='stream-2026-11-02', opener='',
                opponent=opp, win_counter_at_start='%d-%d' % c0,
                counter_winner=None if d is None else (1 if d == (1, 0) else 2))
for opp, idx, cs in SETS:
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    idx = list(idx); assert len(idx) == len(c) - 1, (opp, len(idx), len(c))
    for j, si in enumerate(idx):
        d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1)), (opp, j)
        out.append(row(None, si, opp, c[j], d)); n += 1
    print(opp, len(c) - 1, 'games, set', '%d-%d' % c[-1])
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
dis = row(None, 126, 'Solitar', (2, 0), None); dis['id'] = 'v_disconnect'; dis['note'] = 'opponent disconnected, no result'
json.dump(out + [dis], open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'uyeshota', w.count(1), 'opp', w.count(2))
