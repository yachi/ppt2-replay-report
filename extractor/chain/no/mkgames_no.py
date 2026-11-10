# [ne port, new file] games.json for ナリクラ's stream QZzZ6dWVqYk (2026-11-01, 「パズルリーグ」 ranked Tetris matches,
# first to 2 wins; ids b..), from seg.games() (seg/seg_games.json, 82 game segments; par.py's other segments are
# Puyo matches and menus, checked on a contact sheet). WIN stars at start+3 s are read by seg/stars.json; a match's
# last game is won by the side whose WIN!/WINNER screen shows: every final that started 1-1, and three that looked
# odd, are read by eye (WL_EYE, ws*.png sheets); a final that started 1-0 or 0-1 must be won by the leader (the
# next segment is 0-0), which the asserts check. ナリクラ is the left board (p1).
import json
K = '/tmp/claude-0/no/'; V = 'QZzZ6dWVqYk'
OPP = {0: 'こざとへん', 3: 'こざとへん', 5: 'Yuio', 8: 'Yuio', 10: 'ゆうれい', 13: 'いか', 16: 'いか', 18: 'イチゴだいふく',
       21: 'すっきーに', 23: 'てらこ', 26: 'こまる', 29: 'みしゅ', 31: 'たむら', 34: 'ゆきかき', 36: 'ゆきかき',
       38: 'ゆきかき', 41: 'みしゅ', 43: 'ゆきかき', 45: 'ぬろ', 48: 'ゆうれい', 51: 'ゆうれい', 53: 'ゆうれい',
       55: 'こまる', 58: 'さむい', 60: 'さむい', 63: 'さむい', 65: 'さむい', 68: 'NAOKI', 71: 'ゆきかき', 74: 'Aloud',
       76: 'Ando', 79: 'おーわ'}
WL_EYE = {2: 1, 7: 1, 12: 1, 15: 2, 20: 2, 25: 2, 28: 2, 33: 1, 35: 1, 37: 1, 40: 2, 47: 1, 50: 2, 57: 1, 62: 2,
          67: 1, 70: 1, 73: 1, 78: 1, 81: 1}
S = json.load(open(K + 'w/chain/no/seg/seg_games.json'))
R = json.load(open(K + 'w/chain/no/seg/stars.json'))
segs = [dict(i=i, start=s['start'], end=s['end'], c=tuple(r['c']), wl=WL_EYE.get(i, r['wl']))
        for i, (s, r) in enumerate(zip(S, R))]
starts = [k for k, q in enumerate(segs) if q['c'] == (0, 0)]
out = []; mw = [0, 0]
def row(q, opp, d):
    return dict(id=f'b{len(out):03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(q['start'], 1),
                end_upper_s=round(q['end'], 1), dataset='stream-2026-11-01', opener='', opponent=opp,
                win_counter_at_start='%d-%d' % q['c'], counter_winner=None if d is None else (1 if d == (1, 0) else 2))
for m, a in enumerate(starts):
    b = starts[m + 1] if m + 1 < len(starts) else len(segs)
    opp = OPP[segs[a]['i']]
    for k in range(a, b):
        q = segs[k]
        if k + 1 < b:
            c1 = segs[k + 1]['c']
        else:
            w = q['wl']
            if q['c'] in ((1, 0), (0, 1)):  # the leader won 2-0: the trailer winning would have made 1-1, not a reset
                lead = 1 if q['c'] == (1, 0) else 2; assert w in (None, lead), (q['i'], w); w = lead
            assert w in (1, 2), (q['i'], w)
            c1 = (q['c'][0] + (w == 1), q['c'][1] + (w == 2)); assert max(c1) == 2, (q['i'], c1); mw[c1[1] == 2] += 1
        d = (c1[0] - q['c'][0], c1[1] - q['c'][1]); assert d in ((1, 0), (0, 1)), (q['i'], d)
        out.append(row(q, opp, d))
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('games', len(out), 'narikura', w.count(1), 'opp', w.count(2), 'matches won-lost', mw)
