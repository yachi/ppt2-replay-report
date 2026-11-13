# [qv, new file] games.json for uyeshota's upload qvB4pt22yPw (2026-11-03, vs ゆうくん), ids d000..,
# from seg/seg_games.json (23 segments, every one a game). uyeshota is the LEFT board (p1). One set; the video ends
# during the 24th game at 14-9, which has no winner and is not a segment. WIN counters read by eye from seg/cnt/s*.png.
import json
K = '/tmp/claude-0/qv/'; V = 'qvB4pt22yPw'
S = json.load(open(K + 'w/chain/qv/seg/seg_games.json'))
READ = ('0-0 1-0 2-0 3-0 4-0 5-0 5-1 5-2 6-2 6-3 6-4 7-4 7-5 8-5 8-6 9-6 10-6 11-6 11-7 12-7 13-7 13-8 14-8', (14, 9))
c = [tuple(map(int, x.split('-'))) for x in READ[0].split()] + [READ[1]]
assert len(c) == len(S) + 1
out = []
for j, q in enumerate(S):
    d = (c[j+1][0] - c[j][0], c[j+1][1] - c[j][1]); assert d in ((1, 0), (0, 1)), (j, d)
    out.append(dict(id=f'd{j:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(q['start'], 1),
                    end_upper_s=round(q['end'], 1), dataset='upload-2026-11-03', opener='', opponent='ゆうくん',
                    win_counter_at_start='%d-%d' % c[j], counter_winner=1 if d == (1, 0) else 2))
out[-1]['win_counter_after'] = '%d-%d' % READ[1]
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('total', len(out), 'uyeshota', w.count(1), 'ゆうくん', w.count(2))
