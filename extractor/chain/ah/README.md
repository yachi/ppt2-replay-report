# chain/ah: syakegohan vs ドラえもん, 15先 Part1-2 (uploaded 2025-06-29)

42 games, ids `ah00`–`ah41`, dataset `upload-2025-06-29`, two videos. This tree is a copy of `chain/sp`, run on the
two videos together and kept as it ran (its paths point at `/tmp/claude-0/ah/`, a cloud session's scratchpad). It
adds no frame image or video to the repo. Ids follow `chain/sp`'s two-letter scheme: this set is `ah`.

## Inputs

syakegohan is the LEFT board (p1) throughout; the opponent is ドラえもん.

| ids | video | WIN counters at the end (syakegohan first) | length |
|---|---|---|---|
| ah00–ah20 | `hEnw7Uj4Jgs` (Part1) | 15-6 | 20:20 |
| ah21–ah41 | `SytEEEZsu8Y` (Part2) | 15-6 | 18:49 |

syakegohan 30-12 over the 42 games; both videos hold a whole set.

- The videos: リプレイVer 3.5, the layout the coordinates expect. `SytEEEZsu8Y` is native 854x480; `hEnw7Uj4Jgs` was
  fetched at 720p and scaled to 854x480 before the chain ran (no layout rescale).
- Games: `seg/` was run per video (`seg/v_<video>/`); `seg` never closes a video's last game, so `mkgames_ah.py`
  appends it (start = previous end + 1.2 s, end = the video's end less 0.2 s) and asserts each game moves one WIN
  counter by one. The chain's winners agree with the counters in all 42 games.

## What differs from chain/sp

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/ah/` |
| `mkgames_ah.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `ah` |
| `corr/merge_xo.py` | three groups (`range(3)`; g2 = the PC items) |
| `corr/dedupe.py` | as in `chain/ag`, plus two rules for this set: a retype inside another group's replace window is dropped, and pc=1 is set on two quads g1 named PERFECT CLEARs; applies the NEXT recount decision (`NC`) and drops cells the corrected events already give |
| `corr/dedupe_note.txt` | what `dedupe.py` dropped and decided |
| `apply/hand_edits_sp.py` | removed: the cell edits go straight to `analysis/ppt2-syakegohan/hand-edits.csv` |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 81 flags: 53 PERFECT CLEAR banner onsets, 13 winner KO pieces, 5
   banner/type disagreements, 3 T-spins with no banner, 3 KO-tail score jumps, 2 gap windows over 4 s and 2 banners
   with no clear. `check/score/` found 33 score spots.
2. **PERFECT CLEARs.** 5 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 22 clusters
   (`corr/pcclusters.json`), and a lit-cell count of the board after each (`corr/litcount.txt`) left 12 that went to
   a frame check as group g2. The chain logs each of these PCs twice: the real clear without the PC flag, then a
   phantom clear on the next piece. Each fix sets pc=1 on the real clear and drops the phantom. The set holds 19 PCs in
   all (syakegohan 16, ドラえもん 3).
3. **Frame checks.** `extractor/autosettle` settled 6 items as no change (`corr/out/auto.json`); the other non-PC
   items went to two groups (`corr/groups/g0.json`, 15 items; `g1.json`, 13) beside the 12 PC items (`g2.json`). One
   agent per group proposed corrections (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`):
   they rejected none and amended none.
4. **Merge.** `corr/merge_xo.py` wrote 38 event corrections; `corr/dedupe.py` dropped 5 (one repeated PC fix, and
   four g2 retypes inside g0's ah00 p1 and ah15 p1 windows, which already set those PCs) and set pc=1 on two quads
   (ah18 p1 1026.33, ah25 p1 234.47) whose +8400 score jumps g1 read as PERFECT CLEARs, leaving 35
   (`corr/dedupe_note.txt`).
5. **Cells.** Six: ah05 p1 119 -> 120, ah08 p2 54 -> 52, ah10 p1 24 -> 25, ah33 p1 206 -> 207 (KO-frame and phantom
   locks), ah08 p1 max_combo 11 -> 19 and ah08 p1 pieces 68 -> 61 (the NEXT recount, below). The checkers also
   proposed four `max_combo` cells (ah08 p2, ah10 p1, ah15 p1, ah35 p1); the chain recomputes REN from the corrected
   events and already gives each one, so `dedupe.py` dropped them.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted all 84 player-games' spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/hand_edits.csv` is the cells without a header, as
`nc_compare.py` reads it). ah08 p1 read 61 cleanly (8 whole bags, no unknown stretch) against the table's 68, and the
corrected events also number 61 with every shift matched (extractor B had counted spawns through the stalled 19-combo
REN stretch), so its cell was set to 61. After that: 69 agree, 10 differ by one, 1 is a lost read (ah25 p2) and 4 read
two or three fewer than the table (ah29 p2, ah33 p2, ah38 p2, ah41 p2): the recount holds as many shifts as the
corrected events have pieces, but the events at the game's start find no shift, so the table is kept. No other piece
count was changed from it.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty).
