# [wr, new file] games.json for amemiya's stream wrUXrGsHWLU (2026-11-11, 「超久しぶりの連勝企画」, first-to-5 sets
# against whoever joined), ids g000.., from seg/seg_games.json (185 segments). WIN counters at start+3 s and
# end-0.3 s read by eye from seg/cnt/s*.png; amemiya is the left board (p1). Segment 0 is a COM game, not counted.
# Segments 88 (vs だいご at 1-0) and 112 (vs リミレ at 2-0) end in 「通信相手との接続が切断されました」 mid-game:
# no result (games_all only); the games before them in those sets ARE counted (tx/oc precedent). Segments 82 and
# 102 end under the Switch's pause menu; their winner is read off the next segment's starting counter.
import json
K = '/tmp/claude-0/wr/'; V = 'wrUXrGsHWLU'
SETS = [  # (opponent, first segment, winners in order: L = amemiya, R = opponent)
 ('むぎ　りは', 1, 'LLRLLL'), ('にゃんにゃん', 7, 'LLLLRRL'), ('sa', 14, 'LLLLRL'), ('むぎ　りは', 20, 'RLLLLL'),
 ('なかあけいいちろう', 26, 'LLLLL'), ('むぎ　りは', 31, 'LLLLL'), ('チアオパンクス', 36, 'LLLLL'),
 ('なかあけいいちろう', 41, 'LLLLL'), ('つかこ', 46, 'LLLLL'), ('2Sぜいみしゅ', 51, 'LLLLL'), ('カットトマト', 56, 'LLLLL'),
 ('ユウソル', 61, 'LLLLL'), ('めんこ', 66, 'LLLLL'), ('あ', 71, 'LLLLL'), ('せきりゅう', 76, 'LLRLLL'),
 ('リミレ', 82, 'LLLLL'), ('だいご', 87, 'L'), ('チアオパンクス', 89, 'LLLLL'), ('リミレ', 94, 'LLLLL'),
 ('わんこそば　ようつべ', 99, 'LLLLRL'), ('めんこ', 105, 'LLLLL'), ('リミレ', 110, 'LL'), ('はるま', 113, 'LLLLRL'),
 ('リミレ', 119, 'LLLLL'), ('せと　27↑', 124, 'LLLLL'), ('あ', 129, 'LRLLLL'), ('はるま', 135, 'LLLLRL'),
 ('カットトマト', 141, 'LRLLLRL'), ('はるま', 148, 'LLLLL'), ('α', 153, 'LLLLRL'), ('Rii', 159, 'LLLLL'),
 ('molmottoo', 164, 'LLLRLL'), ('はるま', 170, 'LLLLL'), ('はるま', 175, 'LLLLL'), ('まくまくさん', 180, 'LLLLL'),
]
CUT = {88: ('だいご', (1, 0)), 112: ('リミレ', (2, 0))}
S = json.load(open(K + 'w/chain/wr/seg/seg_games.json'))
out = []; n = 0; used = {0, *CUT}
def row(si, opp, c0, w):
    return dict(id=f'g{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                end_upper_s=round(S[si]['end'], 1), dataset='stream-2026-11-11', opener='',
                opponent=opp, win_counter_at_start='%d-%d' % c0, counter_winner=w)
for opp, s0, ws in SETS:
    c = [0, 0]
    for j, w in enumerate(ws):
        si = s0 + j; assert si not in used, si; used.add(si)
        out.append(row(si, opp, tuple(c), 1 if w == 'L' else 2)); n += 1
        c[0 if w == 'L' else 1] += 1
    assert opp in ('だいご', 'リミレ') and max(c) < 5 or max(c) == 5, (opp, c)
    print(opp, '%d-%d' % tuple(c))
assert used == set(range(len(S))), sorted(set(range(len(S))) - used)
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
extra = []
for si, (opp, c0) in CUT.items():
    r = row(si, opp, c0, None); r['id'] = f'g_disconnect_{si}'; r['note'] = 'opponent disconnected mid-game, no result'
    extra.append(r)
json.dump(out + extra, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'amemiya', w.count(1), 'opp', w.count(2))
