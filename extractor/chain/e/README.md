# chain/e: amemiya's live stream of 2026-11-07 (video `W4Sqy2O93fQ`)

95 games, ids `e000`–`e094`, dataset `stream-2026-11-07`. This tree is a copy of `chain/c` (itself `chain/s`, `chain/oc`)
run on one stream and kept as it ran (its paths point at `/tmp/claude-0/e/`, a cloud session's scratchpad). It adds no
frame image or video to the repo.

## Inputs

amemiya is the LEFT board (p1) throughout.

| ids | opponent | set |
|---|---|---|
| e000–e001 | しょうがく6ねんせい | 1-1, then a disconnect |
| e002–e018 | しょうがく6ねんせい | 12-5, then two disconnects |
| e019–e027 | しょうがく6ねんせい | 4-5, not played out |
| e028–e050 | たわ | 15-8 |
| e051–e068 | ひかるきし | 15-3 |
| e069–e094 | おはゆれ | 15-11 |

amemiya 62-33 over the 95 games. Every winner agrees with the on-screen WIN counter.

- The video: fetched with yt-dlp through a Tailscale exit node, rescaled with `scale=837:470,pad=854:480:8:6` as for c.
- Games: `seg/` as in c (100 segments after the menu filter). `mkgames_e.py` writes `games.json` from the WIN counters
  read by eye and asserts each game moves one counter by one. Left out: segment 0 (vs COM2), 3, 21 and 22 (games cut by
  「インターネットから切断」 with no winner) and 55 (menus). Segment 31's winner was read off its LOSE/WIN screen and
  segment 54's off its やった! screen; the other sets' last games fade on the KO and were read off the faded counter.

## What differs from chain/c

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/e/`, video `W4Sqy2O93fQ` |
| `mkgames_e.py` | this stream's games |
| banner, word and score-digit templates | **c's, reused** (`w/R/fr/*.png`, `w/ocr/T.npy`); not committed |
| `corr/merge_xo.py` | four groups, and the older missed-entry handling (no skeptic filed a `missed` entry, so it makes no difference) |

As for c, `pool/pool.py` needs `pool/out/` to exist and `w/tetrio/metrics.py` needs scipy.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-amemiya/` (appended after the 2026-11-04 stream's).

1. **Flags.** `apply/checks_xo.py` raised 153 flags (`corr/flags.json`): 99 PERFECT CLEAR banner onsets, 29 winner KO
   pieces, 19 gap windows, 4 KO-tail score jumps, 2 T-spins with no banner.
2. **PERFECT CLEARs.** 27 accepted (`corr/pcaccepted.json`). The onsets away from an accepted PC make 43 clusters
   (`corr/pcclusters.json`), drawn as strips with `check/pc/strip2.py`: all are line-clear flashes, so
   `corr/hidden_pc.json` is empty.
3. **Score spots.** `check/score/` found 28 spots (`corr/score/spots.json`).
4. **Frame checks.** 60 items in four groups (`corr/groups/g0-g3`). One agent per group proposed corrections
   (`corr/out/b*.json`), one more per group tried to refute each (`corr/out/v*.json`): 32 kept, 1 amended, none rejected.
   The largest is e037, a REN standoff in which both players stall for seconds at a time with open wells: the chain held
   pieces the frames do not show (p1 146 → 113, p2 154 → 139) and broke p2's REN (19 → 21).
5. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (14: 7 rebuilt windows, 5 added events,
   1 retype, 1 removal) and `corr/cells.json` (19 cells). `corr/fixwas.py` ran `w/tetrio/metrics.py` and needed no repair.
   The corrected event list already gives 6 of the cells, so 13 are hand edits: 11 piece counts and two REN maxima
   (e037 p2 21, e094 p1 7).
6. **NEXT-queue recount** (`corr/drive_nc.sh`, `corr/nc_compare.py`, reference frame 2200 s): of 190 player-games,
   168 agree with the applied table, 21 are one off and 1 (e023 p2) lost the queue; none is two or more off, so there is
   no fifth group (`corr/nc_compare.json`).

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty, as for the other streams).
