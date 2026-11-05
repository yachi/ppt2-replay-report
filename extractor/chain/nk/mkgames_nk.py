# [tx port, new file] games.json for ナリクラ's stream m2-MB304ydQ (2026-11-04, 全世界パズルリーグ ranked Tetris
# matches, first to 2 wins; ids y000..), from seg.games() (seg/seg_games.json, 67 segments after par.py's menu
# filter; every one is a Tetris game). WIN stars at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png
# (left pair narikura, right pair the opponent); a match's last game is read off its WIN/LOSE screen
# (seg/cnt/all*.png). ナリクラ is the left board (p1). The Puyo matches of the stream fall in par.py's menu
# segments (bright) and are not games here.
import json
K = '/tmp/claude-0/nk/'; V = 'm2-MB304ydQ'
MATCHES = [  # (opponent, first and last game index into seg_games.json, star counters 0-0 .. final)
 ('にくうどん', 0, 2, '0-0 0-1 1-1 1-2'), ('にくうどん', 3, 4, '0-0 0-1 0-2'), ('にくうどん', 5, 6, '0-0 0-1 0-2'),
 ('にくうどん', 7, 9, '0-0 1-0 1-1 1-2'), ('かにずし', 10, 11, '0-0 1-0 2-0'), ('のこ', 12, 13, '0-0 1-0 2-0'),
 ('ずみ', 14, 16, '0-0 1-0 1-1 2-1'), ('マサムネ', 17, 19, '0-0 1-0 1-1 2-1'), ('sa', 20, 21, '0-0 0-1 0-2'),
 ('harukun101', 22, 23, '0-0 0-1 0-2'), ('あ', 24, 25, '0-0 1-0 2-0'), ('パルスィ', 26, 27, '0-0 1-0 2-0'),
 ('まきょぽん', 28, 29, '0-0 1-0 2-0'), ('まきょぽん', 30, 32, '0-0 0-1 1-1 2-1'), ('まきょぽん', 33, 34, '0-0 1-0 2-0'),
 ('まきょぽん', 35, 36, '0-0 0-1 0-2'), ('ゆづり〜ん', 37, 38, '0-0 1-0 2-0'), ('ゆづり〜ん', 39, 41, '0-0 0-1 1-1 2-1'),
 ('ゆづり〜ん', 42, 43, '0-0 0-1 0-2'), ('ゆづり〜ん', 44, 45, '0-0 0-1 0-2'), ('ゆづり〜ん', 46, 47, '0-0 0-1 0-2'),
 ('まきょぽん', 48, 49, '0-0 0-1 0-2'), ('ピロ', 50, 52, '0-0 0-1 1-1 2-1'), ('ayt', 53, 55, '0-0 0-1 1-1 2-1'),
 ('ゆづり〜ん', 56, 58, '0-0 0-1 1-1 1-2'), ('ゆづり〜ん', 59, 60, '0-0 1-0 2-0'), ('ゆづり〜ん', 61, 63, '0-0 0-1 1-1 1-2'),
 ('テトリスおもろすぎ', 64, 66, '0-0 1-0 1-1 2-1'),
]
END = {}
S = json.load(open(K + 'w/chain/nk/seg/seg_games.json'))
out = []; n = 0; nxt = 0
def row(si, opp, c0, d):
    return dict(id=f'y{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                end_upper_s=END.get(si, round(S[si]['end'], 1)), dataset='stream-2026-11-04', opener='',
                opponent=opp, win_counter_at_start='%d-%d' % c0,
                counter_winner=None if d is None else (1 if d == (1, 0) else 2))
mw = [0, 0]
for opp, a, b, cs in MATCHES:
    assert a == nxt, (opp, a, nxt); nxt = b + 1
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    assert len(c) - 1 == b - a + 1 and max(c[-1]) == 2 and max(c[-2]) == 1 or c[-1] in ((2, 0), (0, 2)), (opp, cs)
    for j, si in enumerate(range(a, b + 1)):
        d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1)), (opp, j)
        out.append(row(si, opp, c[j], d)); n += 1
    mw[c[-1][1] == 2] += 1
assert nxt == len(S)
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('games', n, 'narikura', w.count(1), 'opp', w.count(2), 'matches won-lost', mw)
