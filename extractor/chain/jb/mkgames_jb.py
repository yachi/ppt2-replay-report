# games.json for ナリクラ's stream JBE9iDhAbJI (released 2026-11-10, 【ぷよテト2】 online Tetris 1v1, first to 2 wins,
# some of them in rooms (「ゲームをやめる」 menu); ids d000..), from seg/seg_games.json (98 segments). Segment 92 is the
# character-select / レディ screen of the room against ごはんのおとも (no game; its star read is noise) and is left out.
# The last match's 1-1 decider (vs まきょぽん, ~7984-8030 s) runs to the end of the video and seg missed it: it is
# appended by hand (EXTRA). WIN stars at start+3 s are read by seg/stars_jb.py (yellow pixels in each of the four star
# cells under the boards) into seg/stars_jb.json; every match's last game is won by the side whose WIN!/LOSE screen
# shows at end-0.3 s, read by eye for all 39 finals plus the appended one (WL_EYE; /tmp/claude-0/jb/gl/fin*.png,
# xs.png). A final that started 1-0 or 0-1 must be won by the leader (the next segment is 0-0); the asserts check it.
# Opponent names read off the right name bar at start+3 s (/tmp/claude-0/jb/gl/names*.png). ナリクラ is the left
# board (p1).
import json
K = '/tmp/claude-0/jb/'; V = 'JBE9iDhAbJI'; DS = 'stream-2026-11-10'
SKIP = {92: 'character select / レディ screen before the ごはんのおとも room match, not a game'}
OPP = {0: 'ぬ', 3: 'ぬ', 5: 'いっせい', 8: 'あ', 10: 'Zeiss', 12: 'やきとりのくし', 14: 'あ', 16: 'あ', 19: 'にくうどん',
       21: 'あ', 24: 'あ', 26: 'あ', 29: 'ピロ', 32: 'あ', 34: 'さむい', 36: 'あだぶたー', 39: '「」', 42: 'あ',
       45: 'ちょこみん', 48: 'ちょこみん', 50: 'ちょこみん', 53: 'そやすけ', 56: 'こう', 58: 'きくのした', 60: 'さむい',
       62: 'もみじ', 64: 'みしゅ', 66: 'さむい', 68: 'Uniあお', 71: 'さむい', 74: 'さむい', 76: 'さむい', 79: 'ココシガ',
       81: 'ココシガ', 83: 'ココシガ', 85: 'クッパ', 87: 'キルア', 89: 'クッパ', 93: 'ごはんのおとも', 96: 'まきょぽん'}
WL_EYE = {2: 2, 4: 2, 7: 2, 9: 2, 11: 1, 13: 1, 15: 2, 18: 1, 20: 1, 23: 1, 25: 1, 28: 1, 31: 1, 33: 1, 35: 2,
          38: 2, 41: 1, 44: 1, 47: 2, 49: 1, 52: 2, 55: 2, 57: 1, 59: 1, 61: 2, 63: 2, 65: 1, 67: 2, 70: 1, 73: 2,
          75: 2, 78: 2, 80: 2, 82: 2, 84: 2, 86: 2, 88: 2, 91: 2, 95: 1, 98: 1}
EXTRA = [dict(i=98, start=7984.3, end=8034.8, c=(1, 1))]  # 1-1 decider vs まきょぽん, to the video end (8034.8 s)
S = json.load(open(K + 'w/chain/jb/seg/seg_games.json'))
R = json.load(open(K + 'w/chain/jb/seg/stars_jb.json'))
assert len(S) == len(R) == 98
segs = [dict(i=i, start=s['start'], end=s['end'], c=tuple(r['c'])) for i, (s, r) in enumerate(zip(S, R)) if i not in SKIP]
segs += EXTRA
for q in segs: q['wl'] = WL_EYE.get(q['i'])
starts = [k for k, q in enumerate(segs) if q['c'] == (0, 0)]
assert [segs[k]['i'] for k in starts] == sorted(OPP), [segs[k]['i'] for k in starts]
out = []; mw = [0, 0]; table = []
def row(q, opp, d):
    return dict(id=f'd{len(out):03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(q['start'], 1),
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
