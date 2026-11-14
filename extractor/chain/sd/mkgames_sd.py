# [qh port, new file] games.json for syakegohan's stream UKNJ3gWqqkU (2026-08-16, 「練習【ぷよぷよテトリス２】」), ids v000..,
# from seg/seg_games.json (144 segments). WIN counters at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png;
# syakegohan is the left board (p1). Sets are first to 3. When a set is won without leaving the room the counter
# resets to 0-0 on the deciding game's end frame (e.g. segment 8: 2-0 -> 0-0); from 2-0 only syakegohan can reach 3,
# so those deciders are his. A Now Loading / cloud / darkened end frame means the room was left after the set.
# Opponent names read off a 480p nameplate (kana and punctuation as they appear there). The nameplate of segments
# 6-11 is empty ('-----'), so that opponent is '' (the page shows 對手未知).
# Left out (one mid-game frame per set, start+15 s, chk/mid*.png in the scratch tree):
#   18-24 ☆つぶあんばんまん☆ plays puyo (segment 23, 2-0 -> 2-2, also holds two games);
#   38-43 あっきーみゃーさ, 80-85 スーホ, 98-103 わあい, 117-124 ヤマダ: all play puyo (segment 121, 2-2 -> 0-0, is
#   ambiguous too), so none is tetris vs tetris.
# Segment 111 (あちみつ set 2, 2-2 -> 0-0 on the sheet): the frame at 6203 s shows syakegohan LOSE / opponent WIN, so
# that set is 2-3. Segment 137 (カワウソ, 0-0) is one game: the frame at 7640 s shows やった! and the counter 1-0, then
# the stream leaves the room, so that set stops at 1-0.
# No menu or COM segment is in seg_games.json; every remaining segment holds exactly one game.
import json
K = '/tmp/claude-0/sd/'; V = 'UKNJ3gWqqkU'; DS = 'stream-2026-08-16'
SETS = [(0, 'カワウソ', 'LLL', (3, 0)), (3, 'カワウソ', 'LLL', (3, 0)),
        (6, '', 'LLL', (3, 0)), (9, '', 'LLL', (3, 0)),
        (12, 'ちぃちゃちゃもん', 'LLL', (3, 0)), (15, 'ちぃちゃちゃもん', 'LLL', (3, 0)),
        (25, 'くくすす', 'LLL', (3, 0)), (28, 'くくすす', 'RLLL', (3, 1)),
        (32, 'Fumi´∀`', 'LLL', (3, 0)), (35, 'Fumi´∀`', 'LLL', (3, 0)),
        (44, 'アベル', 'LLL', (3, 0)), (47, 'アベル', 'LLL', (3, 0)),
        (50, 'カワウソ', 'LLL', (3, 0)), (53, 'カワウソ', 'LLL', (3, 0)),
        (56, 'ににな', 'LLL', (3, 0)), (59, 'ににな', 'LLL', (3, 0)),
        (62, 'KinoKo', 'LLL', (3, 0)), (65, 'KinoKo', 'LLL', (3, 0)),
        (68, '」', 'LLL', (3, 0)), (71, '」', 'LLL', (3, 0)),
        (74, 'リュウ2サンズ', 'LLL', (3, 0)), (77, 'リュウ2サンズ', 'LLL', (3, 0)),
        (86, 'あおりーん！_！', 'LLL', (3, 0)), (89, 'あおりーん！_！', 'LLL', (3, 0)),
        (92, 'Uniあお', 'LLL', (3, 0)), (95, 'Uniあお', 'LLL', (3, 0)),
        (104, 'あちみつ', 'LLL', (3, 0)), (107, 'あちみつ', 'LLRRR', (2, 3)), (112, 'あちみつ', 'LRRLR', (2, 3)),
        (125, 'コルティ', 'LLL', (3, 0)), (128, 'コルティ', 'LLL', (3, 0)),
        (131, 'ヤ', 'LLL', (3, 0)), (134, 'ヤ', 'LLL', (3, 0)),
        (137, 'カワウソ', 'L', (1, 0)),
        (138, 'コルティ', 'LLL', (3, 0)), (141, 'コルティ', 'LLL', (3, 0))]
SKIP = {i: 'puyo' for r in [(18, 25), (38, 44), (80, 86), (98, 104), (117, 125)] for i in range(*r)}
S = json.load(open(K + 'w/chain/sd/seg/seg_games.json'))
out = []; n = 0; used = set(SKIP)
for s0, opp, ws, fin in SETS:
    c = [0, 0]
    for j, w in enumerate(ws):
        si = s0 + j; assert si not in used, si; used.add(si)
        out.append(dict(id=f'v{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                        end_upper_s=round(S[si]['end'], 1), dataset=DS, opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % tuple(c), counter_winner=1 if w == 'L' else 2)); n += 1
        c[0 if w == 'L' else 1] += 1
    assert tuple(c) == fin, (c, fin)
    assert max(c) == 3 or s0 == 137, (s0, c)
    print('%3d-%3d %s %d-%d' % (s0, s0 + len(ws) - 1, opp, *c))
assert used == set(range(len(S))), sorted(set(range(len(S))) - used)
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'syakegohan', w.count(1), 'opp', w.count(2), 'sets', len(SETS))
