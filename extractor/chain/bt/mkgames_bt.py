# games.json for ナリクラ's stream 4Btsf0blGBQ (【ぷよテト2】レートでRENするか…♡, online rated Tetris 1v1, first to 2 wins;
# ids f000..), from seg/seg_games.json (78 segments, every one a Tetris-vs-Tetris game: the WIN-star counters chain
# without a break). DS is stream-2026-11-12: the YouTube page's live startDate is 2026-11-12T10:12:51Z (19:12 JST),
# read 2026-11-14. Skipped: nothing
# from seg; the stream's other stretches (0-199 s, 793-1211 s, 4127-4649 s: Puyo-vs-Puyo matches and menus;
# 5993-6268 s: a Tetris-vs-Puyo match; the rest lobby / VS / character select) are not in seg and were checked on
# contact sheets (/tmp/claude-0/bt/gl/g0.png, h*.png). The last match's 1-1 decider (vs かいてと, ゴー! at 7164.6 s,
# opponent's WIN! at ~7248 s) runs to the end of the video (7255.5 s) and seg missed it: appended by hand (EXTRA;
# /tmp/claude-0/bt/gl/g7160.png, b_b.png, b_c.png). WIN stars at start+3 s are read by seg/stars_bt.py (yellow
# pixels in each of the four star cells under the boards; same coordinates as JBE9iDhAbJI's) into seg/stars_bt.json;
# every match's last game is won by the side whose WIN!/LOSE screen shows at end-0.3 s, read by eye for all 32
# finals plus the appended one (WL_EYE; /tmp/claude-0/bt/gl/fin*.png). A final that started 1-0 or 0-1 must be won
# by the leader (the next segment is 0-0); the asserts check it. Opponent names read off the right name bar at
# start+3 s (/tmp/claude-0/bt/gl/names*.png, nz.png); 「???」 is the name as displayed (four matches, possibly
# different players). ナリクラ is the left board (p1).
import json
K = '/tmp/claude-0/bt/'; V = '4Btsf0blGBQ'; DS = 'stream-2026-11-12'
SKIP = {}
OPP = {0: 'ちょこみん', 2: '$さかな$', 4: 'うっみぎうでがうずく', 7: '???', 9: '???', 11: 'うっみぎうでがうずく',
       13: '???', 16: '???', 19: 'たなかてつろう', 21: 'うっみぎうでがうずく', 23: 'うっみぎうでがうずく', 25: 'マエ',
       27: 'のこ', 29: 'おお', 32: 'たなばた', 34: 'にくうどん', 37: 'たなばた', 39: 'け', 42: 'ふかんぜんはんざい',
       44: 'ふかんぜんはんざい', 46: '7「」§¥-/!', 49: 'にんまる', 52: 'udon', 54: '7「」§¥-/!', 57: '7「」§¥-/!',
       60: '7「」§¥-/!', 62: 'Zeiss', 64: 'Zeiss', 67: 'にんまる', 69: 'ヴィヴィアーナ', 71: 'キリー', 74: 'かいてと',
       76: 'かいてと'}
WL_EYE = {1: 2, 3: 1, 6: 1, 8: 2, 10: 2, 12: 2, 15: 1, 18: 1, 20: 1, 22: 1, 24: 1, 26: 1, 28: 1, 31: 1, 33: 1,
          36: 2, 38: 1, 41: 1, 43: 1, 45: 2, 48: 1, 51: 2, 53: 1, 56: 2, 59: 1, 61: 1, 63: 2, 66: 2, 68: 2, 70: 1,
          73: 1, 75: 1, 78: 2}
EXTRA = [dict(i=78, start=7164.6, end=7255.4, c=(1, 1))]  # 1-1 decider vs かいてと, to the video end (7255.5 s)
S = json.load(open(K + 'w/chain/bt/seg/seg_games.json'))
R = json.load(open(K + 'w/chain/bt/seg/stars_bt.json'))
assert len(S) == len(R) == 78
segs = [dict(i=i, start=s['start'], end=s['end'], c=tuple(r['c'])) for i, (s, r) in enumerate(zip(S, R)) if i not in SKIP]
segs += EXTRA
for q in segs: q['wl'] = WL_EYE.get(q['i'])
starts = [k for k, q in enumerate(segs) if q['c'] == (0, 0)]
assert [segs[k]['i'] for k in starts] == sorted(OPP), [segs[k]['i'] for k in starts]
assert sorted(WL_EYE) == [segs[(starts[m + 1] if m + 1 < len(starts) else len(segs)) - 1]['i'] for m in range(len(starts))]
out = []; mw = [0, 0]; table = []
def row(q, opp, d):
    return dict(id=f'f{len(out):03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(q['start'], 1),
                end_upper_s=round(q['end'], 1), dataset=DS, opener='', opponent=opp,
                win_counter_at_start='%d-%d' % q['c'], counter_winner=None if d is None else (1 if d == (1, 0) else 2))
for m, a in enumerate(starts):
    b = starts[m + 1] if m + 1 < len(starts) else len(segs)
    opp = OPP[segs[a]['i']]; first = len(out)
    for k in range(a, b):
        q = segs[k]
        if k + 1 < b:
            c1 = segs[k + 1]['c']; assert q['wl'] is None, q['i']
        else:
            w = q['wl']; assert w in (1, 2), (q['i'], w)
            if q['c'] in ((1, 0), (0, 1)):  # the leader won 2-0: the trailer winning would have made 1-1, not a reset
                assert w == (1 if q['c'] == (1, 0) else 2), (q['i'], w)
            c1 = (q['c'][0] + (w == 1), q['c'][1] + (w == 2)); assert max(c1) == 2, (q['i'], c1); mw[c1[1] == 2] += 1
        d = (c1[0] - q['c'][0], c1[1] - q['c'][1]); assert d in ((1, 0), (0, 1)), (q['i'], d)
        out.append(row(q, opp, d))
    table.append((out[first]['id'], out[-1]['id'], opp, '%d-%d' % c1))
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
for t in table: print(*t)
print('games', len(out), 'narikura', w.count(1), 'opp', w.count(2), 'matches won-lost', mw, 'of', len(starts))
