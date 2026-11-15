# [ag] games.json for syakegohan vs ドラえもん 15先×2 Part1-2 (two uploads of 2025-07-17, native 854x480,
# replay Ver 3.5, no rescale), ids ag00.. (two letters and two digits, see chain/sp). Segments from
# seg/v_<VID>/seg_games.json (per-video seg); seg never closes a video's last game, so it is appended: start = previous
# end + 1.2 s, end_upper = the video's end less 0.2 s. WIN counters read by eye at each segment's start + 3 s and on the
# video's last frame (cnt/<VID>.png in the scratch tree); syakegohan is the LEFT board (p1). The opponent's nameplate
# reads ドラえもん. Each video is a whole set: Part1 15-6, Part2 15-5.
import json, subprocess
K = '/tmp/claude-0/ag/'; PFX = 'ag'; DS = 'upload-2025-07-17'; OPP = 'ドラえもん'
VIDS = [  # vid, counters (syakegohan-ドラえもん) at each game's start and after the last one
 ('nYKv827YLg8', '0-0 0-1 1-1 1-2 2-2 3-2 4-2 5-2 6-2 7-2 7-3 8-3 8-4 9-4 10-4 11-4 11-5 12-5 12-6 13-6 14-6 15-6'),
 ('op-Tc_IVY8w', '0-0 1-0 2-0 3-0 4-0 5-0 6-0 7-0 8-0 8-1 9-1 10-1 11-1 11-2 11-3 12-3 13-3 13-4 14-4 14-5 15-5'),
]
out = []; n = 0
for V, cs in VIDS:
    p = K + f'video/{V}.mp4'
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
    S = json.load(open(K + f'w/chain/ag/seg/v_{V}/seg_games.json'))
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    assert len(c) - 2 == len(S), (V, len(c), len(S))
    for j in range(len(c) - 1):
        d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1))
        if j < len(S): st, en = S[j]['start'], S[j]['end']
        else: st, en = S[-1]['end'] + 1.2, dur - 0.2
        g = dict(id=f'{PFX}{n:02d}', video=V, path=p, start_s=round(st, 1), end_upper_s=round(en, 1), dataset=DS,
                 opener='', opponent=OPP, win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2)
        if j == len(c) - 2: g['win_counter_after'] = '%d-%d' % c[-1]
        out.append(g); n += 1
    print(V, len(c) - 1, 'games', '%d-%d' % c[-1])
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('total', n, 'syakegohan', w.count(1), 'opp', w.count(2))
