# [nk port, new file] games.json for ナリクラ's stream QvoCgqvJ6MY (2026-11-06, 全世界マトリックスリーグ ranked Tetris
# matches, first to 2 wins; ids c000..), from seg.games() (seg/seg_games.json, 98 segments after par.py's menu
# filter, every one a Tetris game) plus the stream's last game, which seg.games() never closed (the WINNER screen
# follows it with no empty board): EXTRA. WIN stars at start+3 s are read by seg/stars.json (yellow score per star,
# checked by eye on seg/cnt/s*.png); a match's last game is won by the side whose WIN! banner shows at end-0.3 s
# (the same file's 'wl'), which the next match's 0-0 cannot tell. ナリクラ is the left board (p1).
import json
K = '/tmp/claude-0/nc/'; V = 'QvoCgqvJ6MY'
OPP = [  # (first segment index of the match, opponent as on the nameplate)
 (0, '¤やなせたかしす¤'), (2, 'o'), (5, 'あ'), (7, '???'), (10, 'いっせい'), (12, 'いっせい'), (14, 'Xenon/キセノン'),
 (17, '???'), (19, '???'), (22, 'たわ'), (24, 'あ'), (26, 'ひろ'), (29, 'ひろ'), (31, 'ひろ'), (34, 'くくすす'),
 (37, 'くくすす'), (40, 'さむい'), (42, 'ぬ'), (44, 'くくすす'), (46, 'SEGA'), (48, 'ゆび'), (50, 'たわ'), (52, 'たわ'),
 (55, 'SEGA'), (58, 'ks'), (60, 'ぬ'), (63, 'いけとろ'), (65, 'SEGA'), (68, 'SEGA'), (71, 'まきょぽん'), (73, 'まきょぽん'),
 (76, 'くくすす'), (78, 'くくすす'), (81, 'たなばた'), (84, 'ks'), (87, 'razania'), (90, 'フォス'), (92, 'manato'),
 (95, 'manato'), (97, 'manato'),
]
EXTRA = dict(start=7402.7, end=7449.4, c=[1, 0], wl=1)   # the last game: occ_full.npz, stars and WINNER screen by eye
S = json.load(open(K + 'w/chain/nc/seg/seg_games.json'))
R = json.load(open(K + 'w/chain/nc/seg/stars.json'))
segs = [dict(start=s['start'], end=s['end'], c=r['c'], wl=r['wl']) for s, r in zip(S, R)] + [EXTRA]
starts = {a for a, _ in OPP}
assert all((tuple(q['c']) == (0, 0)) == (i in starts) for i, q in enumerate(segs)), 'match starts'
out = []; mw = [0, 0]
for k, (a, opp) in enumerate(OPP):
    b = OPP[k + 1][0] if k + 1 < len(OPP) else len(segs)
    for i in range(a, b):
        c0 = tuple(segs[i]['c'])
        if i + 1 < b:
            c1 = tuple(segs[i + 1]['c']); d = (c1[0] - c0[0], c1[1] - c0[1])
        else:
            w = segs[i]['wl']; d = (1, 0) if w == 1 else (0, 1)
            assert max(c0[0] + d[0], c0[1] + d[1]) == 2, (opp, i)
            mw[d[1]] += 1
        assert d in ((1, 0), (0, 1)), (opp, i, d)
        n = len(out)
        out.append(dict(id=f'c{n:03d}', video=V, path=K + f'video/{V}.mp4', start_s=round(segs[i]['start'], 1),
                        end_upper_s=round(segs[i]['end'], 1), dataset='stream-2026-11-06', opener='', opponent=opp,
                        win_counter_at_start='%d-%d' % c0, counter_winner=1 if d == (1, 0) else 2))
json.dump(out, open('games.json', 'w'), ensure_ascii=False, indent=1)
json.dump(out, open('games_all.json', 'w'), ensure_ascii=False, indent=1)
w = [g['counter_winner'] for g in out]
print('games', len(out), 'narikura', w.count(1), 'opp', w.count(2), 'matches won-lost', mw)
