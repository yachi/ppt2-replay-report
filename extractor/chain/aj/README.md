# chain/aj: ゆうくん's stream of 2026-11-06 (「VSどらえもんガチ連戦 30先」)

58 games, ids `z000`–`z057`, dataset `stream-2026-11-06`, video `aajsP06utaU`. This tree is a copy of
`chain/nk`, run on one live-stream archive and kept as it ran (its paths point at `/tmp/claude-0/aj/`, a cloud
session's scratchpad). It adds no frame image or video to the repo.

## Inputs

One first-to-30 set against どらえもん in a private room; ゆうくん is the LEFT board (p1). どらえもん won it 30–28.

- The video: fetched with yt-dlp through a Tailscale exit node (as for tx and nk). 480p (format 135) exists for
  this archive, so no transcode was needed beyond the rescale.
- **Rescale.** As in nk, the layout is larger than xt's. `scale=818:460,pad=854:480:26:7` puts every board cell
  where xt's coordinates expect it; check the gridlines before running A.
- Games: `seg/` as in nk (63 segments, `seg/seg_games.json`). Segment 0 is a COM game before the set and
  segments 59–62 are ranked Puzzle League matches after it; neither is counted. `mkgames_aj.py` writes
  `games.json` and `games_all.json` (the same 58 games) from the WIN counters read by eye off contact sheets,
  and asserts each game moves one counter by one and the set ends 28–30.
- Winners: A's KO winner agrees with the WIN counter on all 58 games.

## What differs from chain/nk

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/aj/`, video `aajsP06utaU`, subject yukun |
| `mkgames_aj.py`, `drive_aj1.sh` | this stream's games and stage-1 driver |
| `w/A/analyze.py` | **NEXT-queue I-flash stalls.** Attack effects flash over the queue and read as I in queue slots for 3–40 frames, so `spawns()` stalled (34 gap windows, one 44 s long) and bags went out of phase. Four rules: drop a short state sandwiched between two equal readings that differs from them only by reading I; a state equal to the reference except where the reference reads I is a re-read (no spawn); within 3 s of the reference queue, a shift whose overlap differs in one slot the reference reads I is accepted and that slot corrected; a 15+ frame state with `ref[4] == new[0]` is a four-piece shift (a cut-in covered the queue). 34 gap windows became 12 short ones, with no bad bag. The 3 s limit matters: after a longer stall a one-slot overlap matched by chance (z051 p2 2707.3) |
| `w/R/banner.py`, `w/R/banscan.py` | **the streamer's camera box** (x 377–497, y 215–371) covers the left part of p2's banner ("T-SP"), so p2's spin template is cut from the visible "IN" only (`T_SPIN_P`, one spin template per side); banner geometry measured on this video ("-SPIN" p1 x=70 y=322, word p1 x=99 y=320, p2 = p1 + 410). p2's spin series is the minimum over two consecutive frames, because a one-frame clear flash scored 0.6 on the 11-pixel "IN" and read as a second onset |
| `w/R/mini_aj.py`, `w/R/banscan.py` | no "Mini" banner was seen: all six of A's mini guesses show the full "T-SPIN Single", and p2's Mini spot is under the camera box. No Mini template is cut; the Mini series are zeros, so a mini reaches the table only through the frame checks |
| banner, word and score-digit templates | **recut from this video** (`w/R/fr/`, `check/ocr/mktpl.py`'s six frames). Not committed |
| `check/pc/strip2.py` | `pcstrip.py` with offsets −0.4 to +2.2 s, for the hidden-PC strips |

As for nk, `pool/pool.py` needs `pool/out/` to exist and `w/tetrio/metrics.py` needs scipy.

## Corrections

All event corrections and hand edits are in `analysis/ppt2-yukun/`.

1. **Flags.** `apply/checks_xo.py` raised 106 flags (`corr/flags.json`): 60 PERFECT CLEAR banner onsets,
   18 winner KO pieces, 12 T-spins with no banner, 9 KO-tail score jumps, 5 gap windows, 1 banner with no
   clear, 1 banner/type disagreement. No structural failure.
2. **PERFECT CLEARs.** `pcmap` accepted 12 PCs; all show the banner. The 22 clusters of short onsets away from
   an accepted PC (`corr/pcclusters.json`) were drawn as strips, and **7 of them are real PCs** whose banner
   onsets were split by a cut-in or clear effect, so `pcmap` rejected them: z003 p1 390.8, z004 p1 435.57,
   z009 p1 764.67, z015 p2 996.4, z018 p1 1100.23, z020 p1 1153.77, z022 p1 1240.67. Six of them were logged
   twice (an earlier half that is the same clear); `corr/hidden_pc.json` retypes the later half to the PC and
   removes the earlier one (13 operations).
3. **Score spots.** `check/score/` found 58 spots (`corr/score/spots.json`); the 17 with an unexplained score
   change of 900 or more were kept as items (smaller ones are drop points and REN rounding).
4. **Frame checks.** The 46 non-PC flags and the 17 spots made 63 items in three groups (`corr/groups/`).
   One agent per group proposed corrections (`corr/out/b*.json`: 25 event corrections, 14 cell edits), one
   more per group tried to refute each (`corr/out/v*.json`). The skeptics kept every proposal, amended one and
   added one the checker had left: z012 p2's last double locks one frame after the KO (event removed, pieces
   41 → 40). The amendment is z051 p1: the checker removed the double at 2763.37, but the clear the chain put
   on the O at 2762.63 is the phantom; the S at 2763.37 made the double and took the garbage row.
5. **Merge.** `corr/merge_xo.py` writes `corr/event-corrections.json` (18 retypes, 9 rebuilt windows,
   9 removals, 2 added events) and `corr/cells.json` (15 cells). `corr/fixwas.py` ran `w/tetrio/metrics.py`
   and repaired one `was` field (z004 p1's triple, gc 3 → 0).
6. **Cells.** Of the 15 cell edits, the corrected event list already gives the 7 REN and back-to-back
   maxima, so 8 are hand edits, all piece counts.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game` (one worker at a
time here, because the frame-check agents shared the four cores), and `corr/nc_compare.py` compared them with the
final table (`corr/nc_compare.json`). Of the 116 player-games, 108 agree exactly, 4 differ by one piece and 3 are
lost reads (bad bags or long unknown stretches: z000 p2, z055 p2, z056 p2). Three of the four one-piece
differences are games whose piece count the frame checks changed (z012 p2, z030 p2, z048 p1): the recount sides
with the chain's count, and the frame checks looked at the KO frame or the duplicated events directly. One differs
by more on a clean read: z034 p1, where the recount is 2 lower than the table's 54. The frame check raised that
count by one for an I locked on the KO frame. No piece count was changed from the recount alone, as for xo, xt,
tx and nk.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No Mini banner template: a mini T-spin the frame checks did not look at is counted as a plain clear (one
  was found, z023 p1 1278.53).
- No opener labels (the `opener` column is empty, as for the streams).
