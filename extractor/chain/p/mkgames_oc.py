# [oc port, new file] games.json for amemiya's stream 0Akye6ouJbw (2026-11-08, ids o000..), from seg.games()
# (seg/seg_games.json, 131 segments after par.py's menu filter). WIN counters at start+3 s and end-0.3 s read by eye
# from seg/cnt/s*.png; amemiya is the left board (p1). Segment 0 is a COM game (COM1 vs COM2) and is not counted;
# the stream moves to Kirby Air Riders after 8180 s, which was never segmented.
# Segment 54 (3-2 in the second set vs uyeshota) stopped mid-game when the Switch software was restarted, and
# segment 55 (0-0, the remade room) stopped 16 s in with 「インターネットから切断しています」; neither has a result
# (games_all only). The five games before segment 54 ARE counted (tx precedent); the set restarted at segment 56.
import json
K = '/tmp/claude-0/p/'; V = '0Akye6ouJbw'
SETS = [  # (opponent, segment indices, counters from 0-0 to the final)
 ('いんたい', range(1, 28), '0-0 0-1 1-1 2-1 2-2 3-2 4-2 4-3 4-4 4-5 5-5 5-6 6-6 7-6 8-6 8-7 9-7 9-8 9-9 10-9 10-10 11-10 11-11 11-12 12-12 13-12 14-12 15-12'),
 ('uyeshota', range(28, 49), '0-0 1-0 2-0 2-1 2-2 3-2 3-3 4-3 5-3 6-3 7-3 8-3 9-3 10-3 11-3 12-3 12-4 13-4 13-5 13-6 14-6 15-6'),
 ('uyeshota', range(49, 54), '0-0 0-1 1-1 1-2 2-2 3-2'),
 ('uyeshota', range(56, 85), '0-0 0-1 0-2 1-2 1-3 1-4 1-5 2-5 3-5 4-5 5-5 6-5 7-5 8-5 8-6 8-7 9-7 9-8 10-8 10-9 11-9 12-9 12-10 12-11 12-12 13-12 14-12 14-13 14-14 15-14'),
 ('たわ', range(85, 107), '0-0 0-1 0-2 1-2 2-2 2-3 2-4 3-4 4-4 5-4 6-4 6-5 7-5 8-5 9-5 10-5 11-5 12-5 12-6 13-6 13-7 14-7 15-7'),
 ('ふまんなつれ', range(107, 131), '0-0 0-1 0-2 1-2 1-3 2-3 2-4 2-5 2-6 3-6 3-7 4-7 5-7 6-7 7-7 7-8 8-8 8-9 9-9 10-9 11-9 12-9 13-9 14-9 15-9'),
]
END = {}
S = json.load(open(K + 'w/chain/p/seg/seg_games.json'))
out = []; n = 0
def row(si, opp, c0, d):
    return dict(id=f'o{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                end_upper_s=END.get(si, round(S[si]['end'], 1)), dataset='stream-2026-11-08', opener='',
                opponent=opp, win_counter_at_start='%d-%d' % c0,
                counter_winner=None if d is None else (1 if d == (1, 0) else 2))
for opp, idx, cs in SETS:
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    idx = list(idx); assert len(idx) == len(c) - 1, (opp, len(idx), len(c))
    for j, si in enumerate(idx):
        d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1)), (opp, j)
        out.append(row(si, opp, c[j], d)); n += 1
    print(opp, len(c) - 1, 'games, set', '%d-%d' % c[-1])
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
extra = []
for si, c0, note, tag in ((54, (3, 2), 'game stopped mid-play (Switch software restarted), no result', 'o_restart'),
                          (55, (0, 0), 'internet disconnect 16 s in, no result', 'o_disconnect')):
    r = row(si, 'uyeshota', c0, None); r['id'] = tag; r['note'] = note; extra.append(r)
json.dump(out + extra, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'amemiya', w.count(1), 'opp', w.count(2))
