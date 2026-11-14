# chain/sl: syakegohan vs あてん, 15先×2 (uploaded 2025-08-20)

40 games, ids `c000`–`c039`, dataset `upload-2025-08-20`, two videos. This tree is a copy of `chain/sj`, run on the
two videos together and kept as it ran (its paths point at `/tmp/claude-0/sl/`, a cloud session's scratchpad). It
adds no frame image or video to the repo.

## Inputs

Each video is one set, first to 15. syakegohan is the LEFT board (p1) throughout.

| ids | video | opponent | score |
|---|---|---|---|
| c000–c017 | `sQlnbjbtMhk` (Part1) | あてん | 15-3 |
| c018–c039 | `SM694yDT4JE` (Part2) | あてん | 15-7 |

syakegohan 30-10 over the 40 games, both sets.

- The videos: native 854x480 h264, the layout ms's and qh's coordinates expect. **No rescale.**
- Games: `seg/` was run per video (`seg/v_<video>/`), as for `chain/sa`. seg never closes a video's last game, so
  `mkgames_sl.py` appends it: start 1.2 s after the previous end, end 9 s after the WIN counter's last change (read by
  eye off a crop at each game's start), capped at the video's length. It asserts each game moves one counter by one
  and each video ends at 15.

## What differs from chain/sj

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/sl/`; `games.json` carries each game's own video `path`; no rescale |
| `mkgames_sl.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `sl` |
| `corr/tools/nextcount.py` | `REF_FRAME_T` 30.0 s, a frame inside the first game of either video |
| `corr/merge_xo.py` | three groups (`range(3)`; g2 = the PC items) |
| `apply/hand_edits_sl.py` | `hand_edits_se.py` reading this set's `corr/cells.json` |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 93 flags: 61 PERFECT CLEAR banner onsets, 11 winner KO pieces,
   9 banner/type disagreements, 6 KO-tail score jumps, 4 banners with no clear, 1 gap window and 1 bad bag.
   `check/score/` added 31 score spots.
2. **PERFECT CLEARs.** 12 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 21 clusters
   (`corr/pcclusters.json`). A lit-cell count of the board after each (`corr/litcount.txt`) left 20 that went to a
   frame check as group g2.
3. **Frame checks.** 39 non-PC items in two groups (`corr/groups/g0.json`, `g1.json`) and the 20 PC items (`g2.json`).
   `extractor/autosettle` settled 4 as no change (`corr/out/auto.json`). One agent per group proposed corrections
   (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`); they kept all 42 (39 events, 3 cells). All 20 PC items were
   real PERFECT CLEARs the chain had logged twice (the clear, then a duplicate clear on the next piece).
4. **Merge.** `corr/merge_xo.py` wrote 39 event corrections. Four g2 windows (c004 p1 273.53, c014 p1 841.93, c026 p1
   453.97, c038 p1 1050.8) repeated, event for event, retypes g0 and g1 had already proposed, so the windows were
   dropped and the retypes kept: 35 corrections. `corr/fixwas.py` ran `w/tetrio/metrics.py` and needed no repair.
5. **Cells.** 3 cell edits; the corrected event list already gives the two max RENs (c014 p1 2, c026 p1 3), so one is
   a hand edit (`corr/hand_edits.csv`): c026 p1 pieces 161 → 162, an S locked before the KO.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted every player-game's spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/nc_compare.json`). Of the 80 player-games 70 agree exactly
and 4 are off by one, all recounting lower (the KO piece). 6 are marked lost (bad bags or long unreadable stretches),
and none was changed: c000 p2 (recount 129, table 126, four bad bags), c002 p2 (66 vs 74), c006 p2, c007 p2, c008 p2
(each one lower) and c014 p2 (205 vs 207; the skeptic counted the 29 spawns of its rebuilt window by eye).

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- c027 p1's table has 69 pieces against 68 chain events; nobody looked into it.
- No opener labels (the `opener` column is empty).
