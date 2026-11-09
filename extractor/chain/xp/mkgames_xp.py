# [aj port, new file] games.json for ゆうくん's stream xp1R8-_Bi_I (2026-11-09, 「雑談兼てとぼ 強い人と対戦したい」,
# ids a000..), from seg/seg_games.json (292 candidate segments). WIN counters at start+3 s and end-0.3 s read by eye
# from seg/cnt/s*.png (left pair ゆうくん, right the opponent). ゆうくん is the left board (p1).
# Not counted: segments 0-4 (全世界パズルリーグ first-to-2 matches), 5 and 246 (room menus, no game), 49 (クッパ,
# 「通信相手との接続が切断されました」 about 30 s in, no result).
# Sets (room "WIN数" first to N): にくうどん FT5 5-0 (6-10) and FT15 15-6 (11-31); しょうがくよねんせい FT15 15-2
# (32-48); クッパ FT15 15-5 (50-69); syakegohan 24 sets of FT5 (70-245, the same 176 games as syakegohan's own
# stream QheX1_UP5W4, ids q000-q175); あめみや はいしん FT15 15-11 (247-272) and 4-15 (273-291).
# The syakegohan sets are parsed and checked game for game against QheX1 but NOT written: yachi chose (2026-11-09) to
# skip them, as they are already in the syakegohan subject. games.json holds the other 108 games, ids a000-a107.
# Each set's last game runs into the next room, so its end counter reads 0-0 or Now Loading: a final from x-4
# (x<4) is the opponent's 5th win, from 4-x (x<4) ゆうくん's; the six 4-4 finals take the winner from QheX1's
# games.csv (read there from the WIN pill before the loading screen). Every syakegohan game is checked against
# QheX1. The FT15 finals' winners were read off their last frames (18428 s: ゆうくん LOSE, 4-15).
import json, csv
K = '/tmp/claude-0/xp/'; V = 'xp1R8-_Bi_I'; DS = 'stream-2026-11-09'
S = json.load(open(K + 'w/chain/xp/seg/seg_games.json'))
QH = [int(r[2]) for r in csv.reader(open(K + 'w/chain/xp/seg/qh_winners.csv'))]  # ゆうくん won, QheX1 order

def P(s): return tuple(int(x) for x in s.split('-'))
# (opponent, first segment, start counters, winner of the final game: 1 ゆうくん / 2 opponent / None from QheX1)
SETS = [
 ('にくうどん', 6, '0-0 1-0 2-0 3-0 4-0', 1),
 ('にくうどん', 11, '0-0 1-0 2-0 3-0 4-0 5-0 6-0 7-0 8-0 8-1 8-2 9-2 9-3 9-4 10-4 10-5 10-6 11-6 12-6 13-6 14-6', 1),
 ('しょうがくよねんせい', 32, '0-0 1-0 2-0 3-0 4-0 5-0 5-1 6-1 7-1 8-1 8-2 9-2 10-2 11-2 12-2 13-2 14-2', 1),
 ('クッパ', 50, '0-0 0-1 1-1 2-1 3-1 4-1 5-1 6-1 7-1 8-1 8-2 9-2 10-2 11-2 12-2 13-2 13-3 13-4 13-5 14-5', 1),
]
SY = """0-0 1-0 2-0 2-1 2-2 2-3 2-4|0-0 1-0 1-1 1-2 2-2 2-3 2-4 3-4 4-4|0-0 1-0 1-1 2-1 3-1 3-2 3-3 3-4|0-0 0-1 1-1 1-2 1-3 2-3 2-4|
0-0 0-1 0-2 0-3 0-4|0-0 1-0 1-1 2-1 2-2 2-3 2-4|0-0 0-1 0-2 1-2 2-2 2-3 2-4 3-4|0-0 0-1 0-2 1-2 1-3 1-4|
0-0 0-1 0-2 0-3 1-3 1-4 2-4 3-4 4-4|0-0 0-1 0-2 0-3 0-4|0-0 0-1 0-2 0-3 1-3 2-3 3-3 4-3 4-4|0-0 1-0 1-1 1-2 2-2 3-2 3-3 4-3|
0-0 0-1 1-1 2-1 2-2 2-3 3-3 3-4 4-4|0-0 0-1 0-2 1-2 2-2 2-3 3-3 3-4|0-0 1-0 1-1 1-2 1-3 1-4|0-0 0-1 0-2 1-2 1-3 1-4|
0-0 0-1 1-1 1-2 2-2 2-3 2-4 3-4 4-4|0-0 0-1 0-2 0-3 0-4|0-0 1-0 2-0 2-1 2-2 2-3 2-4|0-0 1-0 2-0 3-0 3-1 3-2 3-3 3-4|
0-0 0-1 0-2 0-3 0-4 1-4 2-4|0-0 1-0 1-1 1-2 2-2 2-3 2-4 3-4 4-4|0-0 0-1 1-1 1-2 1-3 2-3 2-4|0-0 0-1 0-2 1-2 2-2 2-3 2-4"""
seg = 70
for s in SY.replace('\n', '').split('|'):
    SETS.append(('syakegohan', seg, s, None)); seg += len(s.split())
assert seg == 246, seg
SETS += [
 ('あめみや　はいしん', 247, '0-0 1-0 2-0 3-0 4-0 4-1 4-2 5-2 5-3 6-3 6-4 6-5 6-6 7-6 8-6 8-7 8-8 9-8 10-8 10-9 11-9 12-9 13-9 '
  '13-10 14-10 14-11', 1),
 ('あめみや　はいしん', 273, '0-0 0-1 0-2 0-3 0-4 1-4 2-4 2-5 2-6 2-7 2-8 3-8 3-9 3-10 3-11 3-12 3-13 4-13 4-14', 2),
]
out = []; qi = 0; sets = []
for opp, first, cs, fin in SETS:
    C = [P(x) for x in cs.split()]
    for k, c in enumerate(C):
        si = first + k
        if k + 1 < len(C):
            d = (C[k+1][0] - c[0], C[k+1][1] - c[1]); assert d in ((1, 0), (0, 1)), (si, c, C[k+1]); w = 1 if d == (1, 0) else 2
        else:
            if opp == 'syakegohan':
                if c[1] == 4 and c[0] < 4: w = 2
                elif c[0] == 4 and c[1] < 4: w = 1
                else: w = 1 if QH[qi] else 2
            else: w = fin
        if opp == 'syakegohan':
            assert (w == 1) == bool(QH[qi]), (si, qi, c, w); qi += 1
        if opp == 'syakegohan': continue   # yachi 2026-11-09: skip these, they are QheX1's q000-q175 from the other side
        g = dict(id=f'a{len(out):03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                 end_upper_s=round(S[si]['end'], 1), dataset=DS, opener='', opponent=opp,
                 win_counter_at_start='%d-%d' % c, counter_winner=w)
        out.append(g)
    after = (C[-1][0] + (w == 1), C[-1][1] + (w == 2))
    if opp != 'syakegohan': out[-1]['win_counter_after'] = '%d-%d' % after
    sets.append((opp, after))
assert qi == 176
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('games', len(out), 'yukun', w.count(1), 'opp', w.count(2))
for o in sorted(set(s[0] for s in sets)):
    print(o, [a for x, a in sets if x == o])
