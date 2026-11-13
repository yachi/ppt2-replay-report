# [ac, new file] games.json for uyeshota's upload AmcnYVHJOkM (2026-11-10, 「良い動きができたセット VS あちみつ」), ids f000..,
# from seg/seg_games.json (22 segments, every one a game). It is a replay recording: あちみつ is the LEFT board (p1)
# and uyeshota the RIGHT (p2); counters below read left-right; the swap to uyeshota=p1 happens at integration
# (apply/swap_sides.py). Three first-to-5 sets; WIN counters read by eye from seg/cnt/s*.png.
import json
K = '/tmp/claude-0/ac/'; V = 'AmcnYVHJOkM'
SETS = [  # (first segment, opponent, number of games, final score left-right)
 (0,  'あちみつ', 8, (3, 5)),
 (8,  'あちみつ', 7, (2, 5)),
 (15, 'あちみつ', 7, (2, 5)),
]
def seq(*pairs): return pairs
S = json.load(open(K + 'w/chain/ac/seg/seg_games.json'))
READ = [  # start counter of every segment, in order
 '0-0 0-1 0-2 1-2 1-3 2-3 2-4 3-4',
 '0-0 1-0 1-1 2-1 2-2 2-3 2-4',
 '0-0 1-0 1-1 1-2 1-3 2-3 2-4',
]
out = []; n = 0
for (i0, opp, k, fin), r in zip(SETS, READ):
    c = [tuple(map(int, x.split('-'))) for x in r.split()] + [fin]
    assert len(c) == k + 1, (opp, len(c), k)
    for j in range(k):
        q = S[i0 + j]; d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1)), (i0 + j, d)
        out.append(dict(id=f'f{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(q['start'], 1),
                        end_upper_s=round(q['end'], 1), dataset='upload-2026-11-10', opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2))
        n += 1
    out[-1]['win_counter_after'] = '%d-%d' % fin
    print(opp, k, '%d-%d' % fin)
assert n == len(S)
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('total', n, 'left', w.count(1), 'right (uyeshota)', w.count(2))
