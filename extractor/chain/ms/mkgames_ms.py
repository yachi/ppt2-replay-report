# [ms port, new file] games.json for syakegohan's upload mtslCN3qVDY (uploaded 2026-11-10, 「vs ドラえもんさん 15先あきぬけ」,
# nameplate どらえもん), ids p000.., from seg/seg_games.json (156 segments after par.py's menu filter, every one a game).
# WIN counters at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png; syakegohan is p1. The upload is edited:
# every set's last game cuts straight to the next set's room, so its end is the first end-dialog / loading frame
# (seg/fin_ms.py -> seg/fin_load.json) and its winner is the WIN pill 1 s before it (seg/cnt/fin_ms.png).
import json
K = '/tmp/claude-0/ms/'; V = 'mtslCN3qVDY'; PFX = 'p'; DS = 'upload-2026-11-10'; OPP = 'どらえもん'
SETS = [
 (0,   '0-0 1-0 2-0 3-0 4-0 4-1 4-2 5-2 5-3 6-3 6-4 7-4 8-4 9-4 10-4 10-5 11-5 12-5 13-5 14-5 14-6 15-6'),
 (21,  '0-0 1-0 2-0 2-1 2-2 3-2 4-2 5-2 5-3 5-4 6-4 7-4 8-4 9-4 10-4 11-4 12-4 13-4 14-4 15-4'),
 (40,  '0-0 1-0 1-1 1-2 2-2 2-3 3-3 4-3 4-4 5-4 6-4 6-5 7-5 7-6 7-7 8-7 9-7 9-8 10-8 11-8 12-8 13-8 13-9 14-9 14-10 14-11 15-11'),
 (66,  '0-0 0-1 1-1 2-1 3-1 4-1 4-2 5-2 6-2 6-3 7-3 7-4 8-4 9-4 10-4 10-5 11-5 11-6 11-7 12-7 13-7 14-7 14-8 15-8'),
 (89,  '0-0 0-1 0-2 1-2 2-2 3-2 4-2 4-3 5-3 5-4 5-5 6-5 6-6 7-6 8-6 8-7 9-7 10-7 10-8 11-8 11-9 11-10 11-11 11-12 12-12 12-13 13-13 14-13 14-14 14-15'),
 (118, '0-0 0-1 1-1 2-1 3-1 4-1 5-1 6-1 7-1 8-1 9-1 10-1 11-1 12-1 12-2 12-3 13-3 14-3 14-4 15-4'),
 (137, '0-0 0-1 1-1 2-1 2-2 3-2 4-2 5-2 5-3 6-3 7-3 8-3 8-4 9-4 10-4 11-4 12-4 13-4 14-4 15-4'),
]
S = json.load(open(K + 'w/chain/ms/seg/seg_games.json'))
LOAD = {int(k): v for k, v in json.load(open(K + 'w/chain/ms/seg/fin_load.json')).items()}
out = []; used = set(); n = 0
for si, (i0, cs) in enumerate(SETS):
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    assert max(c[-1]) == 15 and min(c[-1]) < 15
    for j in range(len(c) - 1):
        q = S[i0 + j]; used.add(i0 + j); d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1))
        last = j == len(c) - 2
        if last: assert i0 + j in LOAD
        out.append(dict(id=f'{PFX}{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(q['start'], 1),
                        end_upper_s=round(LOAD[i0 + j] if last else q['end'], 1), dataset=DS,
                        opener='', opponent=OPP, win_counter_at_start='%d-%d' % c[j],
                        counter_winner=1 if d == (1, 0) else 2))
        if last: out[-1]['win_counter_after'] = '%d-%d' % c[-1]
        n += 1
    print('set', si + 1, len(c) - 1, 'games', '%d-%d' % c[-1])
assert used == set(range(len(S)))
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('total', n, 'syakegohan', w.count(1), 'opp', w.count(2))
