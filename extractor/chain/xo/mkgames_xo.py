# [xo port, new file] games.json for uyeshota's stream XoaWLJowuCQ (ids u000..), from seg.games() (seg/seg_games.json,
# 139 games after par.py's menu filter). WIN counters at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png;
# six sets, each FT15, each set's final row is the result screen.
import json
K = '/tmp/claude-0/xo/'; V = 'XoaWLJowuCQ'
SETS = [  # (opponent, first game index, counters from 0-0 to the final)
 ('いんたい', 0, '0-0 1-0 2-0 3-0 4-0 4-1 5-1 5-2 5-3 6-3 7-3 8-3 8-4 9-4 9-5 10-5 10-6 11-6 11-7 12-7 13-7 14-7 14-8 14-9 15-9'),
 ('ゆうくん', 24, '0-0 0-1 0-2 1-2 1-3 1-4 2-4 3-4 4-4 5-4 6-4 7-4 7-5 8-5 8-6 8-7 9-7 10-7 10-8 11-8 11-9 11-10 11-11 11-12 12-12 12-13 12-14 13-14 13-15'),
 ('ゆうくん', 52, '0-0 1-0 2-0 3-0 4-0 5-0 5-1 5-2 6-2 6-3 6-4 7-4 7-5 8-5 8-6 9-6 10-6 11-6 11-7 12-7 13-7 13-8 14-8 14-9 15-9'),
 ('ゆうくん', 76, '0-0 0-1 1-1 2-1 2-2 3-2 4-2 5-2 6-2 7-2 8-2 9-2 9-3 9-4 10-4 11-4 12-4 13-4 14-4 15-4'),
 ('お', 95, '0-0 0-1 0-2 1-2 2-2 2-3 3-3 4-3 4-4 5-4 5-5 6-5 7-5 8-5 9-5 10-5 11-5 12-5 12-6 12-7 12-8 13-8 13-9 14-9 15-9'),
 ('お', 119, '0-0 1-0 2-0 2-1 3-1 4-1 4-2 5-2 5-3 6-3 6-4 7-4 8-4 9-4 10-4 11-4 12-4 13-4 13-5 14-5 15-5'),
]
S = json.load(open(K + 'w/chain/xo/seg/seg_games.json'))
out = []; n = 0
for si, (opp, i0, cs) in enumerate(SETS):
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    i1 = SETS[si + 1][1] if si + 1 < len(SETS) else len(S)
    assert i1 - i0 == len(c) - 1, (opp, i0, i1 - i0, len(c))
    for j in range(len(c) - 1):
        q = S[i0 + j]; d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1)), (opp, j)
        out.append(dict(id=f'u{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(q['start'], 1),
                        end_upper_s=round(q['end'], 1), dataset='stream-2026-10-30', opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2))
        n += 1
    print(opp, len(c) - 1, 'games, set', '%d-%d' % c[-1])
assert n == len(S)
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'uyeshota', w.count(1), 'opp', w.count(2))
