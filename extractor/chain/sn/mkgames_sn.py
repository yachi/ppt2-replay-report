# [sm port] games.json for syakegohan vs あてん 5先あきぬけ Part1-3 (three uploads of 2025-12-22, one first-to-5 set each,
# 854x480 replay Ver 4.0 with larger boards, RESCALED scale=836:470,pad=854:480:9:5 as se), ids e000.. Segments from seg/v_<VID>/seg_games.json (per-video seg); seg never closes a video's last
# game, so it is appended: start = previous end + 1.2 s, end_upper = WIN-counter change (read by eye, 1 s steps) + 9 s,
# capped at duration. WIN counters read by eye at each segment's start + 3 s (cnt/<VID>.png in the scratch tree).
# AS FILMED: あてん is the LEFT board (p1) and syakegohan the RIGHT (p2) in all three videos; apply/swap_sides.py turns
# the table, hand edits and event corrections round so that p1 is syakegohan in analysis/.
import json, subprocess
K = '/tmp/claude-0/sn/'; PFX = 'e'; DS = 'upload-2025-12-22'; OPP = 'あてん'; FT = 5
VIDS = [  # vid, counters (left-right), last-change-s
 ('ewFgsvZkuII', '0-0 1-0 1-1 2-1 2-2 2-3 2-4 2-5', 341),
 ('jeH2N-kjDUw', '0-0 0-1 0-2 0-3 0-4 0-5', 392),
 ('lK7Nd8Nqh1c', '0-0 0-1 0-2 0-3 0-4 0-5', 237),
]
out = []; n = 0
for V, cs, chg in VIDS:
    p = K + f'video/{V}.mp4'
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
    S = json.load(open(K + f'w/chain/sn/seg/v_{V}/seg_games.json'))
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
print('total', n, 'あてん (left)', w.count(1), 'syakegohan (right)', w.count(2))
