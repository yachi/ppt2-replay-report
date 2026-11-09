# [uP port, new file] games.json for chain/sy (TJc format, ids l000..) from seg/par.py's segf_games.json,
# with the WIN counter at start+3 s read by eye from seg/np/np_*.png (Read tool), and set-final winners read by eye
# from the KO frames (gate/e_*.png). Winner of game k = the side whose counter rose by 1 at game k+1 (same set).
import json
S = json.load(open('/tmp/claude-0/ak/w/seg/segf_games.json'))
C = ['0-0','1-0','1-1','2-1','2-2','3-2','3-3','4-3','0-0','1-0',
     '2-0','3-0','3-1','4-1','0-0','1-0','1-1','1-2','0-0','0-1',
     '0-2','1-2','1-3','1-4','2-4','3-4','4-4','0-0','0-1','1-1',
     '2-1','2-2','2-3','2-4','0-0','0-1','0-2','0-3','0-4','1-4',
     '2-4','3-4','4-4','0-0','1-0','2-0','3-0','3-1','3-2','4-2',
     '4-3','4-4','0-0','1-0','2-0','2-1','2-2','3-2','4-2','4-3',
     '4-4','0-0','1-0','2-0','3-0','4-0','4-1','0-0','1-0','1-1',
     '2-1','3-1','3-2','4-2','0-0','0-1','0-2','0-3','0-4','1-4',
     '2-4','3-4','4-4','0-0','0-1']
assert len(C) == len(S) == 85
C = [tuple(map(int, c.split('-'))) for c in C]
# set finals read on KO frames (counter shows 5 / WINNER banner): k -> winner (1 = p1 syakegohan, 2 = p2)
KO = {26: 2, 42: 1, 51: 1, 60: 2, 82: 1}
END = {17: 1358.0,   # KO and やった! by 1357.2, then 通信中 dialog and disconnect (set aborted at 2-2); window cut before the dialog
       84: 5520.0}   # last game froze at ~5520 (score stuck 5520-5527.5), then disconnect: no KO, no winner
win = []
for k in range(85):
    a = C[k]; b = C[k + 1] if k + 1 < 85 else None
    if b is not None and b != (0, 0):
        d = (b[0] - a[0], b[1] - a[1]); assert d in ((1, 0), (0, 1)), (k, a, b); win.append(1 if d == (1, 0) else 2)
    elif k in KO: win.append(KO[k])
    elif k == 17: win.append(1)            # 1-2 -> 2-2 on the KO frame at 1357.2, then the disconnect
    elif k == 84: win.append(None)
    else:
        assert 4 in a and a != (4, 4), (k, a); win.append(1 if a[0] == 4 else 2)   # 4-x final: only the side on 4 can end the set
out = []
for k, q in enumerate(S):
    out.append(dict(id=f'l{k:03d}', video='uP3FeprmAGI', path='/tmp/claude-0/ak/video/uP3FeprmAGI.mp4',
                    start_s=q['start'], end_upper_s=END.get(k, q['end']), dataset='stream-2026-10-28', opener='', opponent='ふられ',
                    win_counter_at_start=f'{C[k][0]}-{C[k][1]}', counter_winner=win[k]))
json.dump(out, open('games.json', 'w'), ensure_ascii=False)
sets = []; cur = []
for k in range(85):
    cur.append(k)
    if k + 1 == 85 or C[k + 1] == (0, 0): sets.append(cur); cur = []
for s in sets:
    w = [win[k] for k in s]; print(f'l{s[0]:03d}-l{s[-1]:03d}', len(s), 'games', w.count(1), '-', w.count(2), 'None' if None in w else '')
print('total', len(out), 'syakegohan', win.count(1), 'opp', win.count(2), 'no winner', win.count(None))
