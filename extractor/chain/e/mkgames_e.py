# [e, new file] games.json for amemiya's 2026-11-07 stream W4Sqy2O93fQ (ids e000..), from seg.games() (seg/seg_games.json,
# 100 segments after par.py's menu filter). WIN counters at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png;
# amemiya is the left board (p1). Left out: segment 0 (vs COM2), 3, 21 and 22 (games cut by a disconnect,
# 「インターネットから切断」 at 471, 1364 and 1448 s, no winner) and 55 (menus). Segment 31's winner (4-4 -> 4-5) was
# read off the LOSE/WIN result screen at 1880 s, and segment 54's (14-8 -> 15-8) off its やった! screen at 3216 s before
# the opponent's connection dropped; the other sets' last games fade on the KO and were read off the faded counter.
import json
K = '/tmp/claude-0/e/'; V = 'W4Sqy2O93fQ'
SETS = [  # (opponent, segment indices, counters from 0-0 to the final)
 ('しょうがく6ねんせい', range(1, 3), '0-0 0-1 1-1'),
 ('しょうがく6ねんせい', range(4, 21), '0-0 1-0 2-0 2-1 3-1 4-1 5-1 6-1 6-2 7-2 7-3 8-3 8-4 8-5 9-5 10-5 11-5 12-5'),
 ('しょうがく6ねんせい', range(23, 32), '0-0 0-1 1-1 1-2 2-2 3-2 4-2 4-3 4-4 4-5'),
 ('たわ', range(32, 55), '0-0 1-0 1-1 2-1 2-2 3-2 4-2 5-2 5-3 6-3 6-4 7-4 7-5 7-6 8-6 9-6 9-7 9-8 10-8 11-8 12-8 13-8 14-8 15-8'),
 ('ひかるきし', range(56, 74), '0-0 0-1 1-1 2-1 3-1 4-1 5-1 6-1 7-1 8-1 9-1 9-2 10-2 11-2 12-2 13-2 14-2 14-3 15-3'),
 ('おはゆれ', range(74, 100), '0-0 1-0 1-1 2-1 2-2 2-3 2-4 3-4 3-5 4-5 4-6 5-6 6-6 7-6 8-6 8-7 9-7 9-8 10-8 10-9 11-9 11-10 11-11 12-11 13-11 14-11 15-11'),
]
S = json.load(open(K + 'w/chain/e/seg/seg_games.json'))
out = []; n = 0
for opp, idx, cs in SETS:
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    idx = list(idx); assert len(idx) == len(c) - 1, (opp, len(idx), len(c))
    for j, si in enumerate(idx):
        d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1)), (opp, j)
        out.append(dict(id=f'e{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                        end_upper_s=round(S[si]['end'], 1), dataset='stream-2026-11-07', opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2)); n += 1
    print(opp, len(c) - 1, 'games, set', '%d-%d' % c[-1])
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'amemiya', w.count(1), 'opp', w.count(2))
