# [so] games.json for syakegohan vs kazu 15先×2 Part1-2 (two uploads of 2025-08-22, one first-to-15 set each,
# native 854x480 replay Ver 3.5, NO rescale), ids f000.. Segments from seg/v_<VID>/seg_games.json (per-video seg); seg never closes a video's last
# game, so it is appended: start = previous end + 1.2 s, end_upper = WIN-counter change (read by eye, 1 s steps) + 9 s,
# capped at duration. WIN counters read by eye at each segment's start + 3 s (cnt/<VID>.png in the scratch tree).
# AS FILMED: kazu is the LEFT board (p1) and syakegohan the RIGHT (p2) in both videos; apply/swap_sides.py turns
# the table, hand edits and event corrections round so that p1 is syakegohan in analysis/.
import json, subprocess
K = '/tmp/claude-0/so/'; PFX = 'f'; DS = 'upload-2025-08-22'; OPP = 'kazu'; FT = 15
VIDS = [  # vid, counters (left-right), last-change-s
 ('Pjn05duM_gQ', '0-0 0-1 0-2 1-2 1-3 1-4 1-5 1-6 1-7 1-8 1-9 2-9 2-10 2-11 3-11 4-11 4-12 5-12 6-12 6-13 7-13 8-13 9-13 9-14 10-14 11-14 11-15', 1608),
 ('r4sZZlfYNqI', '0-0 1-0 1-1 1-2 1-3 1-4 2-4 2-5 2-6 2-7 2-8 2-9 2-10 2-11 2-12 3-12 3-13 3-14 3-15', 1602),
]
out = []; n = 0
for V, cs, chg in VIDS:
    p = K + f'video/{V}.mp4'
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
    S = json.load(open(K + f'w/chain/so/seg/v_{V}/seg_games.json'))
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    assert max(c[-1]) == FT and min(c[-1]) < FT and len(c) - 2 == len(S), (V, len(c), len(S))
    for j in range(len(c) - 1):
        d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1))
        if j < len(S): st, en = S[j]['start'], S[j]['end']
        else: st, en = S[-1]['end'] + 1.2, min(dur - 0.2, chg + 9)
        g = dict(id=f'{PFX}{n:03d}', video=V, path=p, start_s=round(st, 1), end_upper_s=round(en, 1), dataset=DS,
                 opener='', opponent=OPP, win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2)
        if j == len(c) - 2: g['win_counter_after'] = '%d-%d' % c[-1]
        out.append(g); n += 1
    print(V, len(c) - 1, 'games', '%d-%d' % c[-1])
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('total', n, 'kazu (left)', w.count(1), 'syakegohan (right)', w.count(2))
