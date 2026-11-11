# [c, new file] games.json for amemiya's 2026-11-04 stream qNc6SS1aEXY (ids c000..), from seg.games() (seg/seg_games.json,
# 128 segments after par.py's menu filter). WIN counters at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png;
# amemiya is the left board (p1). Left out: segments 0-1 (COM2 practice), 20 (a game begun at いんたい 10-8 and abandoned
# after 15 s, room closed, no winner; frames at 1494-1515 s) and 126-127 (another game, after the stream left PPT2).
# Segment 19 is one 400 s game (1094-1493 s), checked frame by frame. Each set's last game fades on the KO; its winner
# was read off the faded counter.
import json
K = '/tmp/claude-0/c/'; V = 'qNc6SS1aEXY'
SETS = [  # (opponent, segment indices, counters from 0-0 to the final)
 ('いんたい', range(2, 20), '0-0 0-1 1-1 2-1 2-2 2-3 3-3 3-4 3-5 3-6 4-6 4-7 5-7 6-7 7-7 8-7 8-8 9-8 10-8'),
 ('OSW', range(21, 52), '0-0 0-1 0-2 1-2 1-3 2-3 3-3 4-3 5-3 6-3 6-4 6-5 7-5 7-6 8-6 9-6 9-7 9-8 10-8 10-9 11-9 12-9 13-9 14-9 14-10 15-10 15-11 16-11 17-11 18-11 19-11 20-11'),
 ('いんたい', range(52, 74), '0-0 0-1 1-1 1-2 2-2 2-3 2-4 3-4 3-5 4-5 5-5 6-5 6-6 7-6 8-6 9-6 10-6 10-7 11-7 12-7 13-7 14-7 15-7'),
 ('おはゆれ', range(74, 99), '0-0 1-0 1-1 2-1 3-1 4-1 5-1 5-2 5-3 5-4 6-4 7-4 7-5 8-5 8-6 8-7 8-8 9-8 10-8 11-8 12-8 12-9 12-10 13-10 14-10 15-10'),
 ('たわ', range(99, 126), '0-0 1-0 2-0 2-1 2-2 3-2 4-2 5-2 6-2 7-2 8-2 9-2 10-2 11-2 11-3 11-4 11-5 11-6 12-6 12-7 12-8 13-8 13-9 13-10 13-11 14-11 14-12 15-12'),
]
S = json.load(open(K + 'w/chain/c/seg/seg_games.json'))
out = []; n = 0
for opp, idx, cs in SETS:
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    idx = list(idx); assert len(idx) == len(c) - 1, (opp, len(idx), len(c))
    for j, si in enumerate(idx):
        d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1)), (opp, j)
        out.append(dict(id=f'c{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                        end_upper_s=round(S[si]['end'], 1), dataset='stream-2026-11-04', opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2)); n += 1
    print(opp, len(c) - 1, 'games, set', '%d-%d' % c[-1])
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'amemiya', w.count(1), 'opp', w.count(2))
