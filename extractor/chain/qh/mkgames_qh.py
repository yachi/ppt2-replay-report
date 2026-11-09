# [qh port, new file] games.json for syakegohan's stream QheX1_UP5W4 (2026-11-09, vs ゆうくん / Yuukun3798, 5先あきぬけ),
# ids q000.., from seg.games() (seg/seg_games.json, 176 segments after par.py's menu filter, every one a game).
# WIN counters at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png; syakegohan is the left board (p1).
# A set's last game runs into the next set's room: its end-0.3 s counter is already the next set's 0-0 (or the
# Now Loading screen), so its winner is read off the WIN pill 3-9 s before that loading screen (seg/fin3*.png,
# fin4.png; seg/fin_load.json holds each loading time, used as that game's end_upper_s).
import json
K = '/tmp/claude-0/qh/'; V = 'QheX1_UP5W4'
SETS = [  # (first segment, counters from 0-0 through the last game's result)
 (0,   '0-0 0-1 0-2 1-2 2-2 3-2 4-2 5-2'),
 (7,   '0-0 0-1 1-1 2-1 2-2 3-2 4-2 4-3 4-4 5-4'),
 (16,  '0-0 0-1 1-1 1-2 1-3 2-3 3-3 4-3 5-3'),
 (24,  '0-0 1-0 1-1 2-1 3-1 3-2 4-2 5-2'),
 (31,  '0-0 1-0 2-0 3-0 4-0 5-0'),
 (36,  '0-0 0-1 1-1 1-2 2-2 3-2 4-2 5-2'),
 (43,  '0-0 1-0 2-0 2-1 2-2 3-2 4-2 4-3 5-3'),
 (51,  '0-0 1-0 2-0 2-1 3-1 4-1 5-1'),
 (57,  '0-0 1-0 2-0 3-0 3-1 4-1 4-2 4-3 4-4 5-4'),
 (66,  '0-0 1-0 2-0 3-0 4-0 5-0'),
 (71,  '0-0 1-0 2-0 3-0 3-1 3-2 3-3 3-4 4-4 4-5'),
 (80,  '0-0 0-1 1-1 2-1 2-2 2-3 3-3 3-4 3-5'),
 (88,  '0-0 1-0 1-1 1-2 2-2 3-2 3-3 4-3 4-4 5-4'),
 (97,  '0-0 1-0 2-0 2-1 2-2 3-2 3-3 4-3 5-3'),
 (105, '0-0 0-1 1-1 2-1 3-1 4-1 5-1'),
 (111, '0-0 1-0 2-0 2-1 3-1 4-1 5-1'),
 (117, '0-0 1-0 1-1 2-1 2-2 3-2 4-2 4-3 4-4 5-4'),
 (126, '0-0 1-0 2-0 3-0 4-0 5-0'),
 (131, '0-0 0-1 0-2 1-2 2-2 3-2 4-2 5-2'),
 (138, '0-0 0-1 0-2 0-3 1-3 2-3 3-3 4-3 5-3'),
 (146, '0-0 1-0 2-0 3-0 4-0 4-1 4-2 5-2'),
 (153, '0-0 0-1 1-1 2-1 2-2 3-2 4-2 4-3 4-4 5-4'),
 (162, '0-0 1-0 1-1 2-1 3-1 3-2 4-2 5-2'),
 (169, '0-0 1-0 2-0 2-1 2-2 3-2 4-2 5-2'),
]
S = json.load(open(K + 'w/chain/qh/seg/seg_games.json'))
LOAD = {int(k): v for k, v in json.load(open(K + 'w/chain/qh/seg/fin_load.json')).items()}
out = []; used = set(); n = 0; sw = [0, 0]
for si, (i0, cs) in enumerate(SETS):
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    assert max(c[-1]) == 5 and min(c[-1]) < 5
    for j in range(len(c) - 1):
        q = S[i0 + j]; used.add(i0 + j); d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1))
        last = j == len(c) - 2
        if last: assert i0 + j in LOAD
        out.append(dict(id=f'q{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(q['start'], 1),
                        end_upper_s=round(LOAD[i0 + j] if last else q['end'], 1), dataset='stream-2026-11-09',
                        opener='', opponent='ゆうくん', win_counter_at_start='%d-%d' % c[j],
                        counter_winner=1 if d == (1, 0) else 2))
        if last: out[-1]['win_counter_after'] = '%d-%d' % c[-1]
        n += 1
    sw[c[-1][1] == 5] += 1
    print('set', si + 1, len(c) - 1, 'games', '%d-%d' % c[-1])
assert used == set(range(len(S)))
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('total', n, 'syakegohan', w.count(1), 'opp', w.count(2), 'sets', sw)
