# [ak] games.json for syakegohan vs あちみつ 15先×2 (one upload of 2025-07-11, a PS4 capture fetched at 720p and rescaled
# to the Ver 3.5 layout: scale=837:470,pad=854:480:8:6), ids ak00.. (two letters and two digits, see chain/sp).
# Segments from seg/v_<VID>/seg_games.json; seg never closes the video's last game, so it is appended: start = previous
# end + 1.2 s, end_upper = the video's end less 0.2 s. WIN counters read by eye at each segment's start + 3 s and on the
# video's last frame (cnt/<VID>.png in the scratch tree); syakegohan is the LEFT board (p1, nameplate akashirobo1 with
# his icon). The one video holds two whole sets: the counters reset to 0-0 at segment 19. Set 1 15-4, set 2 15-1.
import json, subprocess
K = '/tmp/claude-0/ak/'; PFX = 'ak'; DS = 'upload-2025-07-11'; OPP = 'あちみつ'; V = 'U1yBGMCQR_A'
SETS = [  # counters (syakegohan-あちみつ) at each game's start and after the set's last game
 '0-0 0-1 0-2 0-3 1-3 2-3 3-3 4-3 5-3 6-3 7-3 8-3 9-3 10-3 11-3 12-3 13-3 14-3 14-4 15-4',
 '0-0 1-0 2-0 3-0 4-0 5-0 6-0 6-1 7-1 8-1 9-1 10-1 11-1 12-1 13-1 14-1 15-1',
]
p = K + f'video/{V}.mp4'
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
S = json.load(open(K + f'w/chain/ak/seg/v_{V}/seg_games.json'))
assert sum(len(s.split()) - 1 for s in SETS) == len(S) + 1, len(S)
out = []; n = 0
for k, cs in enumerate(SETS):
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    for j in range(len(c) - 1):
        d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1))
        if n < len(S): st, en = S[n]['start'], S[n]['end']
        else: st, en = S[-1]['end'] + 1.2, dur - 0.2
        g = dict(id=f'{PFX}{n:02d}', video=V, path=p, start_s=round(st, 1), end_upper_s=round(en, 1), dataset=DS,
                 opener='', opponent=OPP, win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2)
        if j == len(c) - 2: g['win_counter_after'] = '%d-%d' % c[-1]
        out.append(g); n += 1
    print('set', k + 1, len(c) - 1, 'games', '%d-%d' % c[-1])
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('total', n, 'syakegohan', w.count(1), 'opp', w.count(2))
