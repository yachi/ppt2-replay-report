# [pp, new file] games.json for uyeshota's stream Pp-m3oLlOBM (2026-11-08, てとぼ, 15先 ×6), ids c000..,
# from seg/seg_games.json (123 segments, every one a game). WIN counters at start+3 s and end-0.3 s read by eye
# from seg/cnt/s*.png (seg/cnt.py); uyeshota is the LEFT board (p1). Set 1's last game starts at 14-14 and its
# end counter is already set 2's 0-0: its result screen (frame at 1580 s) reads どらえもん WINNER, 14 WIN 15.
import json
K = '/tmp/claude-0/pp/'; V = 'Pp-m3oLlOBM'
SETS = [  # (first segment, opponent, number of games, final score uyeshota-opp)
 (0,   'どらえもん', 29, (14, 15)),
 (29,  'どらえもん', 24, (15, 9)),
 (53,  'ひかるきし　はいしん', 18, (15, 3)),
 (71,  'せい', 16, (15, 1)),
 (87,  'ふらいこん', 20, (15, 5)),
 (107, 'さむい', 16, (15, 1)),
]
# counters at each segment's start, as read (left-right); the last game's winner comes from the next set / result
START = {}
def seq(*pairs): return pairs
S = json.load(open(K + 'w/chain/pp/seg/seg_games.json'))
READ = [  # start counter of every segment, in order
 '0-0 0-1 1-1 2-1 3-1 3-2 4-2 5-2 6-2 7-2 7-3 7-4 8-4 8-5 8-6 9-6 10-6 11-6 12-6 12-7 12-8 12-9 12-10 12-11 12-12'
 ' 12-13 12-14 13-14 14-14',
 '0-0 0-1 1-1 2-1 2-2 2-3 2-4 3-4 3-5 4-5 5-5 6-5 6-6 7-6 8-6 9-6 9-7 10-7 10-8 11-8 12-8 13-8 14-8 14-9',
 '0-0 0-1 1-1 1-2 2-2 3-2 4-2 5-2 5-3 6-3 7-3 8-3 9-3 10-3 11-3 12-3 13-3 14-3',
 '0-0 1-0 2-0 3-0 4-0 5-0 6-0 7-0 8-0 9-0 10-0 11-0 12-0 12-1 13-1 14-1',
 '0-0 1-0 1-1 2-1 3-1 4-1 5-1 6-1 7-1 7-2 8-2 9-2 9-3 10-3 11-3 11-4 12-4 13-4 13-5 14-5',
 '0-0 1-0 2-0 3-0 3-1 4-1 5-1 6-1 7-1 8-1 9-1 10-1 11-1 12-1 13-1 14-1',
]
out = []; n = 0
for (i0, opp, k, fin), r in zip(SETS, READ):
    c = [tuple(map(int, x.split('-'))) for x in r.split()] + [fin]
    assert len(c) == k + 1, (opp, len(c), k)
    for j in range(k):
        q = S[i0 + j]; d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1)), (i0 + j, d)
        out.append(dict(id=f'c{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(q['start'], 1),
                        end_upper_s=round(q['end'], 1), dataset='stream-2026-11-08', opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2))
        n += 1
    out[-1]['win_counter_after'] = '%d-%d' % fin
    print(opp, k, '%d-%d' % fin)
assert n == len(S)
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('total', n, 'uyeshota', w.count(1), 'opp', w.count(2))
