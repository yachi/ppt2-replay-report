# [qh port, new file] games.json for syakegohan's stream T8HfGflEsSc (2026-07-31, 「レート戦⑦」), ids u000..,
# from seg/seg_games.json (34 segments after filt.py), every segment one game. Rate battles are first to 2 (stars);
# syakegohan is the left board (p1). Winners read off the stars at start+3 s and end-0.3 s in seg/cnt/s*.png, and for
# each set-ending game off the WINNER screen at end-3 s (chk/m4.png in the scratch tree: 11 sets won, 3 lost).
# Segment 16's start-frame stars on the sheet looked like 0-1; the counter at 1191 s reads 1-1 (segment 15, won by
# syakegohan, ends on his やった!), so 16 is the decider.
import json
K = '/tmp/claude-0/se/'; V = 'T8HfGflEsSc'; DS = 'stream-2026-07-31'
AM = 'あめみや　はいしん'; SH = 'しょうがく6ねんせい'
SETS = [(AM, 'LL'), (AM, 'LL'), (AM, 'RLR'), (AM, 'LL'), (AM, 'LL'), (AM, 'LRL'), (AM, 'RLR'), (AM, 'LRL'),
        (SH, 'LL'), (AM, 'LL'), (AM, 'LL'), (AM, 'LL'), (AM, 'RLL'), (AM, 'RLR')]
S = json.load(open(K + 'w/chain/se/seg/seg_games.json'))
out = []; si = 0
for opp, ws in SETS:
    c = [0, 0]
    for w in ws:
        out.append(dict(id=f'u{si:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                        end_upper_s=round(S[si]['end'], 1), dataset=DS, opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % tuple(c), counter_winner=1 if w == 'L' else 2)); si += 1
        c[0 if w == 'L' else 1] += 1
    assert max(c) == 2, (opp, ws)
assert si == len(S), (si, len(S))
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', si, 'syakegohan', w.count(1), 'opp', w.count(2))
