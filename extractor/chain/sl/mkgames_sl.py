# [sa port] games.json for syakegohan vs あてん 15先×2 (two uploads of 2025-08-20, one first-to-15 set each), ids c000..
# Segments from seg/v_<VID>/seg_games.json (per-video seg); seg never closes a video's last game, so it is appended:
# start = previous end + 1.2 s, end_upper = WIN-counter change (read by eye from cnt/<VID>.png) + 9 s, capped at duration.
# WIN counters read by eye at each segment's start + 3 s (cnt/<VID>.png in the scratch tree); syakegohan is p1.
import json, subprocess
K = '/tmp/claude-0/sl/'; PFX = 'c'; DS = 'upload-2025-08-20'; OPP = 'あてん'
VIDS = [  # vid, counters, last-change-s
 ('sQlnbjbtMhk', '0-0 1-0 1-1 2-1 3-1 4-1 5-1 6-1 6-2 7-2 8-2 9-2 9-3 10-3 11-3 12-3 13-3 14-3 15-3', 1125),
 ('SM694yDT4JE', '0-0 0-1 0-2 1-2 2-2 2-3 3-3 4-3 4-4 5-4 6-4 7-4 7-5 8-5 9-5 10-5 11-5 12-5 12-6 13-6 13-7 14-7 15-7', 1138),
]
out = []; n = 0
for V, cs, chg in VIDS:
    p = K + f'video/{V}.mp4'
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
    S = json.load(open(K + f'w/chain/sl/seg/v_{V}/seg_games.json'))
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    assert max(c[-1]) == 15 and min(c[-1]) < 15 and len(c) - 2 == len(S), (V, len(c), len(S))
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
print('total', n, 'syakegohan', w.count(1), 'opp', w.count(2))
