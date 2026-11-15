# [an] games.json for syakegohan vs uyeshota 15先×2 Part1-2 (two uploads of 2025-06-29, 854x480: Part1 re-fetched at 720p
# and scaled down, Part2 fetched at 480p; replay Ver 3.5, no rescale), ids an00.. (two letters and two digits, see chain/sp).
# Segments from seg/v_<VID>/seg_games.json (per-video seg); seg never closes a video's last game, so it is appended:
# start = previous end + 1.2 s, end_upper = the video's end less 0.2 s. WIN counters read by eye at each segment's
# start + 3 s and on the video's last frame (cnt/<VID>.png in the scratch tree); syakegohan is the LEFT board (p1), the
# RIGHT nameplate reads uyeshota. Part1 stops at 11-6 (its last frame shows the replay menu with マッチポイント, so the
# upload does not hold the rest of that set); Part2 is a whole set from 0-0, 15-11.
import json, subprocess
K = '/tmp/claude-0/an/'; PFX = 'an'; DS = 'upload-2025-06-29'; OPP = 'uyeshota'
VIDS = [  # vid, counters (syakegohan-uyeshota) at each game's start and after the last one
 ('K4vvl7e2Ea4', '0-0 1-0 1-1 1-2 2-2 3-2 4-2 5-2 5-3 6-3 6-4 7-4 7-5 8-5 8-6 9-6 10-6 11-6'),
 ('kADGVeU2Miw', '0-0 0-1 1-1 1-2 2-2 2-3 2-4 2-5 3-5 4-5 4-6 5-6 6-6 7-6 8-6 8-7 9-7 10-7 11-7 11-8 11-9 12-9 12-10 13-10 14-10 14-11 15-11'),
]
out = []; n = 0
for V, cs in VIDS:
    p = K + f'video/{V}.mp4'
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
    S = json.load(open(K + f'w/chain/an/seg/v_{V}/seg_games.json'))
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
