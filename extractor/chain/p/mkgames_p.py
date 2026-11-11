# [p, new file] games.json for amemiya's 2026-10-29 stream 0Akye6ouJbw (ids p000..), from seg.games() (seg/seg_games.json,
# 153 segments after par.py's menu filter). WIN counters at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png;
# amemiya is the left board (p1). Left out: segment 0 (COM2 practice). Six first-to-15 sets. Set 4's counter goes
# 12-3 -> 12-4 -> 12-5 in 1.5 s at the end of segment 92: the stream skips from that game's end to the result screen of
# the next one (scores 37614 / 46540, not the 101631 / 161331 on the board 3 s earlier), so the 12-4 -> 12-5 game
# (won by uyeshota) is not in the video and has no id ('|' in its counter string). Each set's last game fades on the
# KO; its winner was read off the faded counter (set 4's at 8059.5 s, 15-13, before the loading screen).
import json
K = '/tmp/claude-0/p/'; V = '0Akye6ouJbw'
SETS = [  # (opponent, segment indices, counters from 0-0 to the final; '|' = a game not in the video)
 ('3200↑てとぼ', range(1, 20), '0-0 0-1 1-1 2-1 2-2 3-2 3-3 4-3 5-3 6-3 7-3 8-3 8-4 9-4 10-4 11-4 12-4 13-4 14-4 15-4'),
 ('Yuukun3798', range(20, 48), '0-0 0-1 0-2 0-3 1-3 1-4 2-4 2-5 2-6 3-6 3-7 3-8 3-9 4-9 5-9 5-10 5-11 5-12 6-12 7-12 8-12 9-12 10-12 10-13 10-14 11-14 12-14 13-14 13-15'),
 ('Yuukun3798', range(48, 77), '0-0 0-1 1-1 2-1 2-2 2-3 2-4 3-4 4-4 5-4 5-5 5-6 6-6 6-7 7-7 8-7 9-7 10-7 10-8 11-8 12-8 12-9 12-10 12-11 13-11 13-12 14-12 14-13 14-14 14-15'),
 ('uyeshota', range(77, 104), '0-0 1-0 2-0 3-0 3-1 4-1 4-2 5-2 6-2 7-2 8-2 9-2 10-2 10-3 11-3 12-3 12-4 | 12-5 13-5 13-6 13-7 13-8 13-9 14-9 14-10 14-11 14-12 14-13 15-13'),
 ('uyeshota', range(104, 127), '0-0 1-0 1-1 2-1 3-1 4-1 4-2 5-2 5-3 6-3 6-4 7-4 7-5 8-5 9-5 10-5 11-5 11-6 12-6 13-6 13-7 14-7 14-8 15-8'),
 ('uyeshota', range(127, 153), '0-0 0-1 1-1 1-2 2-2 2-3 2-4 2-5 2-6 2-7 2-8 2-9 3-9 4-9 5-9 6-9 7-9 7-10 8-10 8-11 9-11 9-12 9-13 9-14 10-14 11-14 11-15'),
]
S = json.load(open(K + 'w/chain/p/seg/seg_games.json'))
out = []; n = 0
for opp, idx, cs in SETS:
    toks = cs.split(); pairs = []  # (from, to) per recorded game
    for a, b in zip(toks, toks[1:]):
        if '|' in (a, b): continue
        pairs.append(tuple(tuple(map(int, x.split('-'))) for x in (a, b)))
    for i, t in enumerate(toks):
        if t == '|':
            x, y = (tuple(map(int, toks[i + k].split('-'))) for k in (-1, 1)); assert (y[0] - x[0], y[1] - x[1]) in ((1, 0), (0, 1))
    idx = list(idx); assert len(idx) == len(pairs), (opp, len(idx), len(pairs))
    for si, (c0, c1) in zip(idx, pairs):
        d = (c1[0] - c0[0], c1[1] - c0[1]); assert d in ((1, 0), (0, 1)), (opp, si)
        out.append(dict(id=f'p{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                        end_upper_s=round(S[si]['end'], 1), dataset='stream-2026-10-29', opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % c0, counter_winner=1 if d == (1, 0) else 2)); n += 1
    print(opp, len(pairs), 'games, set', toks[-1])
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'amemiya', w.count(1), 'opp', w.count(2))
