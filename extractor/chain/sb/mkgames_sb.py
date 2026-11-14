# [qh port, new file] games.json for syakegohan's stream kgdvQLQyxp8 (2026-08-20, 「vs あちみつさん 50先」), ids s000..,
# from seg/seg_games.json (84 segments after filt.py). WIN counters at start+3 s and end-0.3 s read by eye from
# seg/cnt/s*.png; syakegohan is the left board (p1). Two rooms: room 1 runs 0-0 to 7-1 (segments 0-7), then segment 8
# (at 7-1) cuts to black at ~714 s and the room select (no result: games_all only); room 2 restarts at 0-0
# (segments 9-83) and ends 49-26 with the WIN screen and 「ありがとうございました」, after which the stream sits in the
# room select until it ends (pk/b.png), so the last game is closed by seg.
import json
K = '/tmp/claude-0/sb/'; V = 'kgdvQLQyxp8'; DS = 'stream-2026-08-20'; OPP = 'あちみつ'
ROOMS = [(0, 'LLLLLLLR', (7, 1)),
         (9, 'LLLLRLRLRLLR' 'LLLLLL' 'R' 'LLLLLLLLL' 'RLLRRLLLRLL' 'RRRRR' 'LLRR' 'LLLL' 'R' 'LLLLL' 'RR' 'LLL' 'RR' 'LLL' 'RRRR' 'LRL',
          (49, 26))]
CUT = {8: (7, 1)}
S = json.load(open(K + 'w/chain/sb/seg/seg_games.json'))
out = []; n = 0; used = set(CUT)
def row(si, c0, w):
    return dict(id=f's{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                end_upper_s=round(S[si]['end'], 1), dataset=DS, opener='', opponent=OPP,
                win_counter_at_start='%d-%d' % c0, counter_winner=w)
for s0, ws, fin in ROOMS:
    c = [0, 0]
    for j, w in enumerate(ws):
        si = s0 + j; assert si not in used, si; used.add(si)
        out.append(row(si, tuple(c), 1 if w == 'L' else 2)); n += 1
        c[0 if w == 'L' else 1] += 1
    assert tuple(c) == fin, (c, fin); print('room', s0, '%d-%d' % tuple(c), len(ws), 'games')
assert used == set(range(len(S))), sorted(set(range(len(S))) - used)
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
extra = []
for si, c0 in CUT.items():
    r = row(si, c0, None); r['id'] = f's_cut_{si}'; r['note'] = 'cut to black and the room select mid-game, no result'
    extra.append(r)
json.dump(out + extra, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'syakegohan', w.count(1), 'opp', w.count(2))
