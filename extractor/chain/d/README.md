# chain/d: amemiya's live stream of 2026-11-06 (video `FQi9j7_ZJF8`)

75 games, ids `d000`–`d074`, dataset `stream-2026-11-06`. This tree is a copy of `chain/c` (itself `chain/s`, `chain/oc`)
run on one stream and kept as it ran (its paths point at `/tmp/claude-0/d/`, a cloud session's scratchpad). It adds no
frame image or video to the repo.

## Inputs

amemiya is the LEFT board (p1) throughout. The opponent's in-game name is ふられ (the video title writes ふれあ).

| ids | opponent | set |
|---|---|---|
| d000–d021 | ふられ | 7-15 |
| d022–d047 | ふられ | 11-15 |
| d048–d074 | いっせい | 15-12 |

amemiya 33-42 over the 75 games. Every winner agrees with the on-screen WIN counter.

- The video: fetched with yt-dlp through a Tailscale exit node, rescaled with `scale=837:470,pad=854:480:8:6` as for c.
- Games: `seg/` as in c (79 segments after the menu filter). `mkgames_d.py` writes `games.json` from the WIN counters
  read by eye and asserts each game moves one counter by one. Left out: segment 0 (vs COM2), 1-2 (another mode, a
  「WINS」 star counter against 「Player 2」) and 78 (another game, after the stream left PPT2). The first set's last game
  cuts to the loading screen before the counter moves; its winner was read off the result screen. The other two sets
  fade on the KO and were read off the faded counter.

## What differs from chain/c

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/d/`, video `FQi9j7_ZJF8` |
| `mkgames_d.py` | this stream's games |
| banner, word and score-digit templates | **c's, reused** (`w/R/fr/*.png`, `w/ocr/T.npy`); not committed |
| `corr/tools/nextcount.py` | reference frame 2410 s (mid d000). c's 2200 s falls in the other mode at the start of this stream and gave no shifts |
| `corr/merge_xo.py` | four groups plus a fifth (below), and one patch: at d041 p2 4425.63 the chain holds a no-clear lock and a single at the same t, so the checker's retype is merged as a window over both |
| `corr/pcclust.py`, `corr/mkgroups.py` | copies of c's scripts with paths set to d (c ran them from its scratchpad) |

As for c, `pool/pool.py` needs `pool/out/` to exist and `w/tetrio/metrics.py` needs scipy.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-amemiya/` (appended after the 2026-11-07 stream's).

1. **Flags.** `apply/checks_xo.py` raised 103 flags (`corr/flags.json`): 62 PERFECT CLEAR banner onsets, 20 winner KO
   pieces, 10 gap windows, 5 T-spins with no banner, 3 KO-tail score jumps, 1 bad bag, 1 banner with no clear,
   1 banner/type disagreement.
2. **PERFECT CLEARs.** 28 accepted (`corr/pcaccepted.json`). The onsets away from an accepted PC make 15 clusters
   (`corr/pcclusters.json`), drawn as strips with `check/pc/strip2.py`: all are line-clear flashes, so
   `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 22 spots (`corr/score/spots.json`).
4. **Frame checks.** 45 items in four groups (`corr/groups/g0-g3`). One agent per group proposed corrections
   (`corr/out/b*.json`), one more per group tried to refute each (`corr/out/v*.json`): all 32 kept. During these checks
   `nextcount.py` still had c's reference frame and read no NEXT shifts, so the checkers counted pieces from the score
   (drop points per lock) and contact sheets.
5. **NEXT-queue recount** (`corr/drive_nc.sh`, `corr/nc_compare.py`, reference frame 2410 s): against the applied
   table, 9 player-games were two or more pieces off. They were a fifth group (`corr/groups/g4.json`, brief
   `corr/CHECKER4.md`) with its own checker and skeptic, both of whose proposals were kept. d000 p1 has a 10 s stream lag
   in which one Z falls in slow motion; the chain logged two pieces there that the frames do not show (55 → 53). d019 p1's
   last J spawned into a blocked board and never locked (82 → 80). In the other seven the table is right: the recount
   starts after the first one or two spawns under READY/GO. Final comparison: 114 agree, 28 one off, 1 lost, and 7 still
   two off for that reason (`corr/nc_compare.json`).
6. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (16: 7 rebuilt windows, 4 removals, 3 added
   events, 2 retypes) and `corr/cells.json` (20 cells, two of them g4's second edit of a cell g0-g3 already changed).
   `corr/fixwas.py` ran `w/tetrio/metrics.py` and needed no repair. The corrected event list already gives the 5 REN
   maxima, so 13 are hand edits, all piece counts. The largest is d041 p2 (243 → 240).

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the other streams).
