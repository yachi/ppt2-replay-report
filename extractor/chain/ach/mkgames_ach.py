# [ach port, new file] games.json for the five 2026-10-28 uploads vs あちみつ (ids m000..), from seg.games() per video
# plus each video's last game (closed by the end screen, not by empty boards). WIN counters at start+3 s and
# end-0.3 s read by eye from w/seg/np/cnt_<video>.png; the final row is the set result.
import json
K = '/tmp/claude-0/ak/'
C = {
 'FAsKhtwulHA': '0-0 1-0 2-0 3-0 4-0 4-1 5-1 6-1 7-1 7-2 8-2 8-3 8-4 8-5 8-6 8-7 8-8 9-8 10-8 11-8 12-8 13-8 13-9 14-9 15-9',
 'IJGqwSdiKwk': '0-0 1-0 1-1 2-1 3-1 3-2 3-3 3-4 3-5 4-5 5-5 5-6 6-6 7-6 7-7 8-7 9-7 10-7 11-7 12-7 12-8 13-8 14-8 15-8',
 '-zR8CNrXdCI': '0-0 0-1 0-2 0-3 0-4 0-5 0-6 1-6 1-7 2-7 3-7 4-7 4-8 4-9 5-9 6-9 7-9 8-9 8-10 8-11 9-11 10-11 11-11 11-12 11-13 12-13 12-14 13-14 13-15',
 'b-o1kjuoygk': '0-0 1-0 2-0 3-0 4-0 5-0 6-0 6-1 6-2 6-3 7-3 8-3 9-3 9-4 10-4 11-4 12-4 12-5 12-6 13-6 14-6 15-6',
 'pUZUSoR6VSU': '0-0 1-0 2-0 3-0 3-1 4-1 5-1 5-2 6-2 6-3 7-3 8-3 9-3 10-3 10-4 11-4 12-4 13-4 14-4 14-5 14-6 15-6',
}
out = []; k = 0
for v, cs in C.items():
    c = [tuple(map(int, x.split('-'))) for x in cs.split()]
    S = [q for q in json.load(open(K + f'w/seg/{v}_seg.json')) if q['end'] - q['start'] > 5]
    assert len(S) == len(c) - 1, (v, len(S), len(c))
    for i, q in enumerate(S):
        d = (c[i+1][0] - c[i][0], c[i+1][1] - c[i][1]); assert d in ((1, 0), (0, 1)), (v, i)
        out.append(dict(id=f'm{k:03d}', video=v, path=K + f'video/{v}.mp4', start_s=round(q['start'], 1),
                        end_upper_s=round(q['end'], 1), dataset='upload-2026-10-28', opener='', opponent='あちみつ',
                        win_counter_at_start='%d-%d' % c[i], counter_winner=1 if d == (1, 0) else 2))
        k += 1
    print(v, len(S), 'games, set', '%d-%d' % c[-1])
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]; print('total', len(out), 'syakegohan', w.count(1), 'あちみつ', w.count(2))
