# [sp] games.json for syakegohan vs ふれあ 5先あきぬけ Part1-6 (six uploads of 2025-08-16, one first-to-5 set each,
# native 854x480 replay Ver 3.5, no rescale), ids aa00..aa44 (two letters and two digits, so ids stay 4 characters, which R/match.py, tetrio/metrics.py and apply/checks_xo.py slice on; every one-letter prefix a-z is already
# used by syakegohan's earlier datasets). Segments from seg/v_<VID>/seg_games.json (per-video seg); seg never closes a
# video's last game, so it is appended: start = previous end + 1.2 s, end_upper = WIN-counter change (read by eye at
# 1 s steps, cnt/fine_<VID>.png) + 9 s, capped at duration. WIN counters read by eye at each segment's start + 3 s
# (cnt/<VID>.png in the scratch tree); syakegohan is the LEFT board (p1). The opponent's nameplate reads ふられ; the
# video titles name ふれあ.
import json, subprocess
K = '/tmp/claude-0/sp/'; PFX = 'aa'; DS = 'upload-2025-08-16'; OPP = 'ふれあ'; FT = 5
VIDS = [  # vid, counters (syakegohan-ふれあ), last-change-s
 ('qups09IM4MY', '0-0 1-0 1-1 2-1 2-2 2-3 3-3 4-3 4-4 4-5', 918),
 ('jECOZWLWVLA', '0-0 1-0 2-0 2-1 3-1 4-1 4-2 4-3 4-4 5-4', 1058),
 ('4bOgIVzV4NI', '0-0 1-0 2-0 2-1 3-1 4-1 5-1', 516),
 ('Q_k8Xkxb3jU', '0-0 1-0 2-0 3-0 4-0 5-0', 793),
 ('j4G7JcRSOhs', '0-0 0-1 0-2 1-2 2-2 3-2 4-2 5-2', 1515),
 ('kaOfxT1BP-I', '0-0 1-0 1-1 2-1 3-1 3-2 3-3 3-4 4-4 5-4', 1113),
]
out = []; n = 0
for V, cs, chg in VIDS:
    p = K + f'video/{V}.mp4'
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p]))
    S = json.load(open(K + f'w/chain/sp/seg/v_{V}/seg_games.json'))
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    assert max(c[-1]) == FT and min(c[-1]) < FT and len(c) - 2 == len(S), (V, len(c), len(S))
    for j in range(len(c) - 1):
        d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1))
        if j < len(S): st, en = S[j]['start'], S[j]['end']
        else: st, en = S[-1]['end'] + 1.2, min(dur - 0.2, chg + 9)
        g = dict(id=f'{PFX}{n:02d}', video=V, path=p, start_s=round(st, 1), end_upper_s=round(en, 1), dataset=DS,
                 opener='', opponent=OPP, win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2)
        if j == len(c) - 2: g['win_counter_after'] = '%d-%d' % c[-1]
        out.append(g); n += 1
    print(V, len(c) - 1, 'games', '%d-%d' % c[-1])
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('total', n, 'syakegohan', w.count(1), 'opp', w.count(2))
