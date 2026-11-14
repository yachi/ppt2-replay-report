# [sf port] games.json for syakegohan's stream GC9tyaPCEk8 (2026-04-19, 「レート戦②」), ids a000..,
# from seg/seg_games.json (36 segments after filt.py), every segment one game. Rate battles are first to 2 (stars);
# syakegohan is the left board (p1). Winners read off the stars at start+3 s and end-0.3 s in seg/cnt/s*.png, and for each
# 1-1 decider off the WIN/LOSE and WINNER screens at end-4..0 s (chk/m4.png in the scratch tree: all six deciders won by
# syakegohan). Opponent names as the nameplate prints them.
import json
K = '/tmp/claude-0/sj/'; V = 'GC9tyaPCEk8'; DS = 'stream-2026-04-19'
DO = 'どらさ'; NN = 'になな'; YU = 'Yuukun3798'; A = 'あ'
SETS = [(DO, 'LRL'), (DO, 'LL'), (NN, 'LL'), (DO, 'LL'), (DO, 'LL'), (YU, 'RLL'), (YU, 'LL'), (YU, 'LRL'),
        (A, 'RR'), (A, 'LL'), (A, 'RLL'), (A, 'LRL'), (A, 'LL'), (A, 'RLL'), (A, 'LL')]
S = json.load(open(K + 'w/chain/sj/seg/seg_games.json'))
out = []; si = 0
for opp, ws in SETS:
    c = [0, 0]
    for w in ws:
        out.append(dict(id=f'a{si:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(S[si]['start'], 1),
                        end_upper_s=round(S[si]['end'], 1), dataset=DS, opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % tuple(c), counter_winner=1 if w == 'L' else 2)); si += 1
        c[0 if w == 'L' else 1] += 1
    assert max(c) == 2, (opp, ws)
assert si == len(S), (si, len(S))
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', si, 'syakegohan', w.count(1), 'opp', w.count(2))
