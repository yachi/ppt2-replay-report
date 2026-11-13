# [fs port, new file] games.json for syakegohan's stream -FTFs2Vv1ZI (2026-10-30, the first part, before 6rUc3cXsjbo;
# vs ふられ, 5先あきぬけ), ids o000.., from seg.games() (seg/seg_games.json, 21 segments after par.py's menu filter,
# every one a game). WIN counters at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png; syakegohan is p1.
# Set finals (segments 8, 14): winner off the WIN pill before the loading screen (seg/cnt/fin3a.png, seg/fin_load.json).
# The stream ends during set 3 at 3-3.
import json
K = '/tmp/claude-0/fs/'; V = '-FTFs2Vv1ZI'; PFX = 'o'; DS = 'stream-2026-10-30'; OPP = 'ふられ'
SETS = [
 (0,  '0-0 1-0 1-1 2-1 2-2 3-2 3-3 4-3 4-4 4-5'),
 (9,  '0-0 0-1 1-1 2-1 3-1 4-1 5-1'),
 (15, '0-0 1-0 1-1 2-1 2-2 3-2 3-3'),
]
S = json.load(open(K + 'w/chain/fs/seg/seg_games.json'))
LOAD = {int(k): v for k, v in json.load(open(K + 'w/chain/fs/seg/fin_load.json')).items()}
out = []; used = set(); n = 0
for si, (i0, cs) in enumerate(SETS):
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    fin = max(c[-1]) == 5
    for j in range(len(c) - 1):
        q = S[i0 + j]; used.add(i0 + j); d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1))
        last = fin and j == len(c) - 2
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
