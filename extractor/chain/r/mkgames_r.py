# [r, new file] games.json for amemiya's 2026-10-31 stream bExpa2eFlOw (ids r000..), from seg.games() (seg/seg_games.json,
# 102 segments after par.py's menu filter). WIN counters at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png;
# amemiya is the left board (p1). Left out: segment 0 (COM2 practice). Four first-to-15 sets. Each set's last game fades
# on the KO; its winner was read off the faded counter, except set 2's, whose counter resets to 0-0 before the next set;
# it was read off the result screen at 4320 s (12-15, ゆうくん).
import json
K = '/tmp/claude-0/r/'; V = 'bExpa2eFlOw'
SETS = [  # (opponent, segment indices, counters from 0-0 to the final)
 ('どらえもん', range(1, 24), '0-0 1-0 2-0 3-0 4-0 4-1 4-2 5-2 6-2 7-2 8-2 9-2 9-3 9-4 10-4 11-4 11-5 12-5 13-5 13-6 13-7 13-8 14-8 15-8'),
 ('ゆうくん', range(24, 51), '0-0 0-1 0-2 1-2 1-3 2-3 2-4 2-5 2-6 3-6 4-6 4-7 4-8 4-9 5-9 6-9 7-9 7-10 8-10 9-10 9-11 10-11 10-12 11-12 11-13 11-14 12-14 12-15'),
 ('ゆうくん', range(51, 76), '0-0 1-0 1-1 2-1 3-1 4-1 5-1 6-1 7-1 8-1 9-1 10-1 10-2 11-2 11-3 12-3 12-4 12-5 12-6 12-7 13-7 13-8 13-9 14-9 14-10 15-10'),
 ('てつ', range(76, 102), '0-0 0-1 1-1 1-2 2-2 2-3 3-3 3-4 3-5 4-5 5-5 5-6 6-6 6-7 6-8 7-8 7-9 8-9 8-10 9-10 10-10 11-10 12-10 13-10 14-10 14-11 15-11'),
]
S = json.load(open(K + 'w/chain/r/seg/seg_games.json'))
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
        out.append(dict(id=f'r{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                        end_upper_s=round(S[si]['end'], 1), dataset='stream-2026-10-31', opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % c0, counter_winner=1 if d == (1, 0) else 2)); n += 1
    print(opp, len(pairs), 'games, set', toks[-1])
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'amemiya', w.count(1), 'opp', w.count(2))
