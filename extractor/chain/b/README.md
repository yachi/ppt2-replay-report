# chain/b: amemiya's live stream of 2026-11-01 (video `-d7Nj5pvqPA`)

136 games, ids `b000`–`b135`, dataset `stream-2026-11-01`. This tree is a copy of `chain/r` (itself `chain/p`, `chain/t`,
`chain/d`, `chain/c`, `chain/s`, `chain/oc`) run on one live-stream archive and kept as it ran (its paths point at
`/tmp/claude-0/b/`, a cloud session's scratchpad). It adds no frame image or video to the repo.

## Inputs

amemiya is the LEFT board (p1) throughout. Six first-to-15 sets, all won by amemiya:

| ids | opponent | set |
|---|---|---|
| b000–b019 | ふらいこん | 15-5 |
| b020–b042 | いんたい | 15-8 |
| b043–b069 | お | 15-12 |
| b070–b098 | たわ | 15-14 |
| b099–b119 | ぶぶ | 15-6 |
| b120–b135 | mitomelody | 15-1 |

amemiya 90-46 over the 136 games. Every winner agrees with the on-screen WIN counter; each set's last game fades on the KO
with amemiya's counter at 15.

- The video: fetched with yt-dlp through a Tailscale exit node, rescaled with `scale=837:470,pad=854:480:8:6` as for c.
- Games: `seg/` as in r (138 segments; the first is a COM practice game and the last is the stream after it left PPT2).
  `mkgames_b.py` writes `games.json` from the WIN counters read by eye and asserts each game moves one counter by one.
- b002 is excluded (`unresolved lower bound`): the stream cut to the Switch home menu from about 1623.5 s to 1629.0 s and
  the game ended as soon as play resumed.

## What differs from chain/r

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/b/`, video `-d7Nj5pvqPA` |
| `mkgames_b.py` | this stream's games (in place of `mkgames_r.py`) |
| banner, word and score-digit templates | **c's, reused** through d (`w/R/fr/*.png`, `w/ocr/T.npy`); not committed |
| `corr/tools/nextcount.py` | reference frame 3375 s (mid b030) |
| `corr/BRIEF.md` | this stream's header |

As for r, `pool/pool.py` needs `pool/out/` to exist, `w/tetrio/metrics.py` needs scipy, and `corr/drive_nc.sh` needs
`corr/nc/` to exist.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-amemiya/` (appended after the 2026-10-31 stream's).

1. **Flags.** `apply/checks_xo.py` raised 198 flags (`corr/flags.json`): 104 PERFECT CLEAR banner onsets, 44 winner KO
   pieces, 31 gap windows, 6 T-spins with no banner, 6 banners with no clear, 4 KO-tail score jumps, 2 unresolved lower
   bounds, 1 bad bag.
2. **PERFECT CLEARs.** 35 accepted (`corr/pcaccepted.json`), one of them amemiya's (b004). The onsets away from an accepted
   PC make 37 clusters (`corr/pcclusters.json`), drawn as strips with `check/pc/strip2.py`: all are line-clear flashes or a
   scene change, so `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 51 spots (`corr/score/spots.json`).
4. **Frame checks.** 107 items in four groups (`corr/groups/g0-g3`). One agent per group proposed corrections
   (`corr/out/b*.json`), one more per group tried to refute each (`corr/out/v*.json`). The skeptics rejected 3 proposals,
   each a winner's last piece that locks one frame after the KO (b029, b077, b100); the rest were kept. Most fixes are
   phantom singles and locks that extractor B logged while the stream lagged in slow motion through long REN chains
   (b069, b078, b079, b081, b094, b095, b101), and three zero-line Mini T-spins logged as 1-line. One retype came from a
   skeptic's aside outside its own item and was checked on frames by the session running the merge: b101 p2 8514.97,
   single → double (`corr/out/b3.json` e4, the score rose +1650, a REN5 double).
5. **NEXT-queue recount** (`corr/drive_nc.sh`, `corr/nc_compare.py`, reference frame 3375 s): against the applied table,
   13 player-games were two or more pieces over the recount. They were a fifth group (`corr/groups/g4.json`, briefs
   `corr/CHECKER4.md` and `corr/SKEPTIC4.md`) with its own checker and skeptic, whose nine piece edits were all kept: in
   the lag games the earlier edits had left extractor B's gap estimates in the piece count, while the event list already
   matched the recount one to one. In the other four (b052, b054, b091, b129) the table is right: the recount starts after
   the first spawns under the GO graphic. Final comparison: 226 agree, 40 one off, 2 lost (b002), 4 still two or more off
   for that reason (`corr/nc_compare.json`).
6. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (73: 35 rebuilt windows, 25 removals, 11 retypes,
   2 added events) and `corr/cells.json` (40 cells). `corr/fixwas.py` ran `w/tetrio/metrics.py`. The corrected event list
   already gives the other 22, so 18 cells are hand edits, all piece counts. The largest is b095 p1, 114 → 99.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the other streams).
