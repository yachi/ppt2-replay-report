# [sa port] games.json for syakegohan vs ドラえもん 15先×3 (three uploads of 2025-08-27, one first-to-15 set each, downscaled 720p→854x480), ids d000..
# Segments from seg/v_<VID>/seg_games.json (per-video seg); seg never closes a video's last game, so it is appended:
# start = previous end + 1.2 s, end_upper = WIN-counter change (read by eye from cnt/<VID>.png) + 9 s, capped at duration.
# WIN counters read by eye at each segment's start + 3 s (cnt/<VID>.png in the scratch tree); syakegohan is p1.
import json, subprocess
K = '/tmp/claude-0/sm/'; PFX = 'd'; DS = 'upload-2025-08-27'; OPP = 'ドラえもん'
VIDS = [  # vid, counters, last-change-s
 ('btWygcgWSOs', '0-0 0-1 1-1 2-1 3-1 4-1 5-1 6-1 7-1 8-1 8-2 9-2 10-2 10-3 10-4 11-4 12-4 13-4 14-4 15-4', 1270),
 ('FsVlPseNc0o', '0-0 0-1 1-1 2-1 3-1 4-1 5-1 6-1 7-1 8-1 9-1 10-1 11-1 12-1 13-1 14-1 14-2 15-2', 805),
 ('o_jajoEdYzA', '0-0 1-0 2-0 3-0 4-0 4-1 5-1 6-1 7-1 8-1 9-1 9-2 10-2 11-2 12-2 12-3 13-3 14-3 15-3', 908),
]
out = []; n = 0
for V, cs, chg in VIDS:
    p = K + f'video/{V}.mp4'
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
    S = json.load(open(K + f'w/chain/sm/seg/v_{V}/seg_games.json'))
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
