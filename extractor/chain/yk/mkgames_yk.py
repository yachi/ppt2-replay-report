# [yk, new file] games.json for amemiya's stream YkPw_o7t6no (2026-11-12, 【VS最強格テトラー】uyeshota！テトリス15先×2回),
# two first-to-15 sets against uyeshota, ids a000.., from seg/seg_games.json (55 segments). WIN counters at start+3 s and
# end-0.3 s read by eye from seg/cnt/s*.png; amemiya is the left board (p1). Segment 0 is a COM game, and the first
# 47 minutes (one long segment outside seg_games) are local games against 「Player 2」: neither is counted.
# Segments 52-54 are Kirby Air Riders after the stream's PPT2 part. Each set's last game is uyeshota's 15th win
# (the counter resets to 0-0 after it).
import json
K = '/tmp/claude-0/yk/'; V = 'YkPw_o7t6no'
# counter at the start of each segment, read off the sheets
SETS = [('uyeshota', 1, ['0-0','1-0','1-1','1-2','1-3','2-3','3-3','3-4','3-5','4-5','5-5','6-5','7-5','7-6','7-7','8-7',
                         '9-7','9-8','9-9','9-10','10-10','10-11','10-12','10-13','11-13','11-14','12-14'], (12, 15)),
        ('uyeshota', 28, ['0-0','0-1','0-2','0-3','0-4','1-4','2-4','2-5','2-6','2-7','2-8','2-9','3-9','4-9','4-10',
                          '4-11','5-11','6-11','7-11','7-12','7-13','8-13','8-14','9-14'], (9, 15))]
S = json.load(open(K + 'w/chain/yk/seg/seg_games.json'))
out = []; n = 0
for opp, s0, cs, fin in SETS:
    cs = [tuple(map(int, c.split('-'))) for c in cs] + [fin]
    for j in range(len(cs) - 1):
        a, b = cs[j], cs[j + 1]
        assert (b[0] - a[0], b[1] - a[1]) in ((1, 0), (0, 1)), (j, a, b)
        si = s0 + j
        out.append(dict(id=f'a{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                        end_upper_s=round(S[si]['end'], 1), dataset='stream-2026-11-12', opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % a, counter_winner=1 if b[0] > a[0] else 2))
        n += 1
assert out[-1]['start_s'] == round(S[51]['start'], 1)
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'amemiya', w.count(1), 'opp', w.count(2))
