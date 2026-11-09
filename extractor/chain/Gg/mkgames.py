# [Gg port of uP's mkgames.py] games.json for chain/yu (ids y000..) from seg/par.py's segf_games.json,
# with the WIN counter at start+3 s read by eye from seg/np/sheet*.png (Read tool), and the two set-final winners read by eye
# from the KO frames (gate/e_*.png). Winner of game k = the side whose counter rose by 1 at game k+1 (same set).
import json
S = json.load(open('/private/tmp/claude-501/Gg/w/seg2/segf_games.json'))   # seg2 = the segmenter re-run on the remapped video
assert S[0]['start'] < 31; S = S[1:]   # 30.1-119.5 is the room-setup menu (gate/e_35.png), not a game
C = ['0-0','0-1','1-1','1-2','2-2','2-3','2-4','3-4','3-5','3-6',
     '3-7','4-7','4-8','5-8','6-8','6-9','7-9','7-10','8-10','8-11',
     '9-11','9-12','9-13','10-13','0-0','0-1','1-1','1-2','1-3','2-3',
     '2-4','2-5','2-6','2-7','3-7','4-7','5-7','5-8','5-9','6-9',
     '6-10','6-11','6-12','6-13','7-13','8-13','8-14','9-14','10-14','11-14',
     '12-14']
assert len(C) == len(S) == 51
C = [tuple(map(int, c.split('-'))) for c in C]
# set finals read on KO frames: k -> winner (1 = p1 Yuukun3798, 2 = p2 uyeshota)
KO = {23: 1,   # やった! on the left at 1717.5 with 11-13, then 通信中 at 1718.0 and the opponent disconnects (FT15 set aborted at 11-13)
      50: 2}   # the counter reads 12-15 on the last frame of the game (3132.1): uyeshota takes the set 15-12
END = {23: 1717.6}   # window cut before the 通信中 dialog
win = []
for k in range(51):
    a = C[k]; b = C[k + 1] if k + 1 < 51 else None
    if k in KO: win.append(KO[k]); continue
    d = (b[0] - a[0], b[1] - a[1]); assert d in ((1, 0), (0, 1)), (k, a, b); win.append(1 if d == (1, 0) else 2)
out = []
for k, q in enumerate(S):
    out.append(dict(id=f'y{k:03d}', video='Ggl5NeUAYEA', path='/private/tmp/claude-501/Gg/video/Ggl5NeUAYEA.mp4',
                    start_s=q['start'], end_upper_s=END.get(k, q['end']), dataset='stream-2026-10-29', opener='', opponent='uyeshota',
                    win_counter_at_start=f'{C[k][0]}-{C[k][1]}', counter_winner=win[k]))
json.dump(out, open('games.json', 'w'), ensure_ascii=False)
for s in (range(0, 24), range(24, 51)):
    w = [win[k] for k in s]; print(f'y{s[0]:03d}-y{s[-1]:03d}', len(w), 'games', w.count(1), '-', w.count(2))
print('total', len(out), 'Yuukun3798', win.count(1), 'opp', win.count(2))
