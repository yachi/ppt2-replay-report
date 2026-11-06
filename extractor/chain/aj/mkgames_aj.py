# [nk port, new file] games.json for ゆうくん's stream aajsP06utaU (2026-11-06, 「VSどらえもんガチ連戦 30先」, one
# first-to-30 set against どらえもん in a private room; ids z000..), from seg.games() (seg/seg_games.json, 63
# segments). WIN counters at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png (left pair ゆうくん, right
# どらえもん). Segment 0 is a COM1 game before the set; segments 59-62 are Puzzle League ranked matches after
# it (first to 2, どらえもん on 1P in at least one), not counted. The set's last game (58) ends 28-30, read off
# its WIN/LOSE screen at 3244 s. ゆうくん is the left board (p1).
import json
K = '/tmp/claude-0/aj/'; V = 'aajsP06utaU'
FIRST, LAST = 1, 58
# winner of each game, from the counters: 1 = ゆうくん (left), 2 = どらえもん
C = [(0,0),(1,0),(2,0),(3,0),(4,0),(4,1),(4,2),(4,3),(4,4),(5,4),(5,5),(5,6),(6,6),(6,7),(6,8),(7,8),(7,9),(8,9),
     (8,10),(9,10),(9,11),(9,12),(10,12),(11,12),(12,12),(13,12),(13,13),(13,14),(14,14),(15,14),(16,14),(16,15),
     (17,15),(17,16),(17,17),(18,17),(18,18),(19,18),(19,19),(19,20),(19,21),(19,22),(19,23),(20,23),(21,23),
     (21,24),(22,24),(22,25),(22,26),(23,26),(24,26),(25,26),(25,27),(26,27),(27,27),(28,27),(28,28),(28,29),(28,30)]
S = json.load(open(K + 'w/chain/aj/seg/seg_games.json'))
assert len(C) - 1 == LAST - FIRST + 1
out = []
for n, si in enumerate(range(FIRST, LAST + 1)):
    d = (C[n+1][0] - C[n][0], C[n+1][1] - C[n][1]); assert d in ((1, 0), (0, 1)), n
    out.append(dict(id=f'z{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                    end_upper_s=round(S[si]['end'], 1), dataset='stream-2026-11-06', opener='',
                    opponent='どらえもん', win_counter_at_start='%d-%d' % C[n],
                    counter_winner=1 if d == (1, 0) else 2))
out[-1]['win_counter_after'] = '28-30'
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('games', len(out), 'yukun', w.count(1), 'opp', w.count(2))
