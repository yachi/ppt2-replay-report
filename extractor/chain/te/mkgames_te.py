# [te, from pp] games.json for uyeshota's stream 10ell5aAJuo (2026-11-10, てとぼ, 15先 ×5), ids e000..,
# from seg/seg_games.json (115 segments, every one a game). WIN counters at start+3 s and end-0.3 s read by eye
# from seg/cnt/s*.png (seg/cnt.py); uyeshota is the LEFT board (p1). Set 2's last game starts at 14-14 and the
# stream restarts the game right after it: the frames at 2868-2873 s read uyeshota WIN, 15 WIN 14.
import json
K = '/tmp/claude-0/te/'; V = '10ell5aAJuo'
SETS = [  # (first segment, opponent, number of games, final score uyeshota-opp)
 (0,   'あかさ', 18, (15, 3)),
 (18,  'どらえもん', 29, (15, 14)),
 (47,  'どらえもん', 23, (15, 8)),
 (70,  'よわいこん', 23, (15, 8)),
 (93,  'あちみつ', 22, (15, 7)),
]
S = json.load(open(K + 'w/chain/te/seg/seg_games.json'))
READ = [  # start counter of every segment, in order
 '0-0 1-0 1-1 2-1 2-2 3-2 4-2 5-2 6-2 7-2 8-2 9-2 10-2 11-2 11-3 12-3 13-3 14-3',
 '0-0 1-0 2-0 2-1 3-1 3-2 4-2 4-3 5-3 6-3 6-4 6-5 7-5 7-6 7-7 8-7 8-8 8-9 9-9 9-10 10-10 11-10 12-10 13-10'
 ' 13-11 14-11 14-12 14-13 14-14',
 '0-0 1-0 1-1 2-1 2-2 3-2 4-2 4-3 5-3 5-4 6-4 7-4 8-4 9-4 10-4 10-5 11-5 11-6 12-6 12-7 13-7 14-7 14-8',
 '0-0 0-1 0-2 1-2 2-2 3-2 4-2 5-2 6-2 7-2 8-2 8-3 9-3 10-3 10-4 10-5 11-5 11-6 12-6 13-6 13-7 14-7 14-8',
 '0-0 1-0 2-0 3-0 3-1 4-1 4-2 5-2 5-3 6-3 7-3 8-3 9-3 9-4 10-4 11-4 12-4 12-5 12-6 12-7 13-7 14-7',
]
out = []; n = 0
for (i0, opp, k, fin), r in zip(SETS, READ):
    c = [tuple(map(int, x.split('-'))) for x in r.split()] + [fin]
    assert len(c) == k + 1, (opp, len(c), k)
    for j in range(k):
        q = S[i0 + j]; d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1)), (i0 + j, d)
        out.append(dict(id=f'e{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(q['start'], 1),
                        end_upper_s=round(q['end'], 1), dataset='stream-2026-11-10', opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2))
        n += 1
    out[-1]['win_counter_after'] = '%d-%d' % fin
    print(opp, k, '%d-%d' % fin)
assert n == len(S)
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('total', n, 'uyeshota', w.count(1), 'opp', w.count(2))
