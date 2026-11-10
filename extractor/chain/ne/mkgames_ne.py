# [nc port, new file] games.json for ナリクラ's stream RggpNNKC3uI (2026-11-08, ranked Tetris matches first to 2 wins,
# then a long run of room matches against ちょこみん; ids e000..), from seg.games() (seg/seg_games.json, 114 segments).
# Segment 3 is a Puyo match (character select, two Puyo games) and is not a game here; the stream's other Puyo
# matches fall in par.py's menu segments. Segment 113, the 1-1 decider of the last match, ended when the opponent
# left the room (「たいせん相手が抜けた」), so it has no result: it is in games_all.json only, and the match's
# previous game carries win_counter_after. WIN stars at start+3 s are read by seg/stars.json (yellow score per star);
# a match's last game is won by the side whose WIN!/WINNER screen shows, read by stars.json's 'wl' where it is set
# and by eye on the frames before the loading or save screen where it is not (WL_EYE). ナリクラ is the left board (p1).
import json
K = '/tmp/claude-0/ne/'; V = 'RggpNNKC3uI'
OPP = {0: 'あ', 4: 'C1', 6: 'C1', 8: 'rez102', 10: 'まきょぽん', 13: 'みしゅ', 16: '3000↑いきたい', 18: '3000↑いきたい',
       20: 's0912', 22: 'でんでん', 24: 'まきょぽん', 26: 'さいこう24REN', 29: 'テトリスおもろすぎ', 31: 'さいこう24REN',
       33: 'さいこう24REN', 36: 'さいこう24REN', 38: 'さいこう24REN', 41: 'クッパ', 43: 'しふとへんこう', 46: 'しろぜ',
       48: 'クッパ', 50: 'クッパ', 52: 'クッパ', 54: 'つっちー', 56: 'ちょこみん', 58: 'クッパ', 60: 'よしき',
       63: 'ちょこみん', 66: 'NAOKI'}
# seg 15 (e014) was first read as a p1 win; A's KO winner disagreed and the WINNER screen at 1416 s names みしゅ, so it is 2.
WL_EYE = {2: 1, 5: 1, 7: 1, 9: 1, 12: 1, 15: 2, 17: 2, 19: 1, 21: 2, 23: 1, 25: 1, 28: 1, 30: 1, 32: 1, 35: 1, 37: 1, 40: 2, 42: 2, 45: 1, 47: 1, 49: 1, 51: 2, 53: 2, 55: 1, 57: 2, 59: 1, 62: 1, 65: 1, 67: 1, 69: 2, 71: 2, 74: 1, 76: 2, 79: 1, 82: 2, 84: 2, 87: 1, 89: 1, 92: 2, 95: 2, 97: 1, 100: 1, 103: 2, 106: 2, 108: 2, 110: 1}
PUYO = {3}; LEFT = 113
S = json.load(open(K + 'w/chain/ne/seg/seg_games.json'))
R = json.load(open(K + 'w/chain/ne/seg/stars.json'))
segs = [dict(i=i, start=s['start'], end=s['end'], c=tuple(r['c']), wl=WL_EYE.get(i, r['wl']))
        for i, (s, r) in enumerate(zip(S, R)) if i not in PUYO]
starts = [k for k, q in enumerate(segs) if q['c'] == (0, 0)]
out = []; mw = [0, 0]; extra = []
def row(q, opp, d):
    return dict(id=f'e{len(out):03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(q['start'], 1),
                end_upper_s=round(q['end'], 1), dataset='stream-2026-11-08', opener='', opponent=opp,
                win_counter_at_start='%d-%d' % q['c'], counter_winner=None if d is None else (1 if d == (1, 0) else 2))
for m, a in enumerate(starts):
    b = starts[m + 1] if m + 1 < len(starts) else len(segs)
    si = segs[a]['i']; opp = OPP.get(si, 'ちょこみん' if si >= 68 else None); assert opp, si
    for k in range(a, b):
        q = segs[k]
        if q['i'] == LEFT:
            r = row(q, opp, None); r['id'] = 'e_left'; r['note'] = 'opponent left the room mid-game, no result'
            extra.append(r); out[-1]['win_counter_after'] = '%d-%d' % q['c']; continue
        if k + 1 < b and segs[k + 1]['i'] != LEFT:
            c1 = segs[k + 1]['c']
        elif k + 1 < b:
            c1 = segs[k + 1]['c']
        else:
            w = q['wl']; assert w in (1, 2), (q['i'], w)
            c1 = (q['c'][0] + (w == 1), q['c'][1] + (w == 2)); assert max(c1) == 2, (q['i'], c1); mw[c1[1] == 2] += 1
        d = (c1[0] - q['c'][0], c1[1] - q['c'][1]); assert d in ((1, 0), (0, 1)), (q['i'], d)
        out.append(row(q, opp, d))
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out + extra, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('games', len(out), 'narikura', w.count(1), 'opp', w.count(2), 'matches won-lost', mw, 'extra', len(extra))
