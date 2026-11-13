# [u4 port, new file] games.json for uyeshota's upload u4P57GT3unk (2026-11-03, 名人戦 VS にんまる, one 20先 set),
# ids b000.., from seg/seg_games.json (21 segments after par.py's menu filter, every one a game; the 112-936 s
# segment it drops is the menus). WIN counters at start+3 s and end-0.3 s read by eye from seg/cnt/s*.png;
# uyeshota is p1. The last game ends on the victory banner, so its segment end is its end.
import json
K = '/tmp/claude-0/u4/'; V = 'u4P57GT3unk'; PFX = 'b'; DS = 'upload-2026-11-03'; OPP = 'にんまる'
SETS = [(0, '0-0 ' + ' '.join(f'{i}-0' for i in range(1, 18)) + ' 17-1 18-1 19-1 20-1')]
S = json.load(open(K + 'w/chain/u4/seg/seg_games.json'))
out = []; used = set(); n = 0
for i0, cs in SETS:
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    for j in range(len(c) - 1):
        q = S[i0 + j]; used.add(i0 + j); d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1))
        out.append(dict(id=f'{PFX}{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(q['start'], 1),
                        end_upper_s=round(q['end'], 1), dataset=DS, opener='', opponent=OPP,
                        win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2))
        n += 1
    out[-1]['win_counter_after'] = '%d-%d' % c[-1]
assert used == set(range(len(S)))
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', n, 'uyeshota', w.count(1), 'opp', w.count(2))
