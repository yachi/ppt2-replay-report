# [ms port, new file] games.json for 8 syakegohan uploads (one 3-win set per video), ids r000..
# Segments from seg/v_<VID>/seg_games.json (per-video seg); seg never closes a video's last game, so it is appended:
# start = previous end + 1.2 s, end_upper = WIN-counter change (read by eye from cnt/<VID>.png) + 9 s, capped at duration.
# WIN counters read by eye from cnt/<VID>.png; syakegohan is p1.
import json, subprocess
K = '/tmp/claude-0/sa/'; PFX = 'r'
VIDS = [  # vid, dataset, opponent, counters, last-change-s
 ('3ZIHXsEMglM', 'upload-2026-07-07', 'あちみつ', '0-0 1-0 1-1 1-2 2-2 3-2', 218),
 ('DiFaYIsoP2Q', 'upload-2026-07-07', 'あちみつ', '0-0 1-0 2-0 3-0', 250),
 ('Llprnzb5HyE', 'upload-2026-07-07', 'あちみつ', '0-0 1-0 1-1 1-2 2-2 2-3', 352),
 ('1H-Nb8dueHI', 'upload-2026-07-07', 'あちみつ', '0-0 0-1 1-1 2-1 3-1', 264),
 ('P-AdNKkIJZg', 'upload-2026-07-17', 'あちみつ', '0-0 1-0 2-0 3-0', 472),
 ('JeHOgt5ZD00', 'upload-2026-07-17', 'あちみつ', '0-0 1-0 1-1 2-1 3-1', 312),
 ('ef8WfxqLWGE', 'upload-2026-07-17', 'あちみつ', '0-0 1-0 2-0 3-0', 168),
 ('lenoq_l7Egw', 'upload-2026-07-28', 'uyeshota', '0-0 1-0 2-0 3-0', 348),
]
out = []; n = 0
for V, DS, OPP, cs, chg in VIDS:
    p = K + f'video/{V}.mp4'
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
    S = json.load(open(K + f'w/chain/sa/seg/v_{V}/seg_games.json'))
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    assert max(c[-1]) == 3 and min(c[-1]) < 3 and len(c) - 2 == len(S), (V, len(c), len(S))
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
