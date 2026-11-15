# [ap] games.json for syakegohan vs いわしせいじん 15先×2 Part1-2 (two uploads of 2025-06-22, 854x480: Part1 re-fetched at 720p
# and scaled down, Part2 fetched at 480p; replay Ver 3.5, no rescale), ids ap00.. (two letters and two digits, see chain/sp).
# Segments from seg/v_<VID>/seg_games.json (per-video seg); seg never closes a video's last game, so it is appended:
# start = previous end + 1.2 s, end_upper = the video's end less 0.2 s. WIN counters read by eye at each segment's
# start + 3 s and on the video's last frame (cnt/<VID>.png in the scratch tree); syakegohan is the LEFT board (p1), the
# RIGHT nameplate reads いわしせいじん. Both parts are whole sets from 0-0: Part1 15-13, Part2 15-7.
import json, subprocess
K = '/tmp/claude-0/ap/'; PFX = 'ap'; DS = 'upload-2025-06-22'; OPP = 'いわしせいじん'
VIDS = [  # vid, counters (syakegohan-いわしせいじん) at each game's start and after the last one
 ('u6yuJv6hZU4', '0-0 0-1 1-1 2-1 3-1 3-2 3-3 3-4 3-5 3-6 4-6 4-7 5-7 5-8 5-9 6-9 7-9 8-9 8-10 9-10 9-11 10-11 10-12 11-12 11-13 12-13 13-13 14-13 15-13'),
 ('gk-C0KNZVuY', '0-0 0-1 0-2 1-2 2-2 2-3 3-3 4-3 4-4 4-5 5-5 6-5 7-5 8-5 9-5 10-5 11-5 12-5 13-5 13-6 13-7 14-7 15-7'),
]
out = []; n = 0
for V, cs in VIDS:
    p = K + f'video/{V}.mp4'
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
    S = json.load(open(K + f'w/chain/ap/seg/v_{V}/seg_games.json'))
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
