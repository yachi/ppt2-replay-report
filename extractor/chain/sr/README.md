# chain/sr: syakegohan vs あめみや, 15先 Part1-2 (uploaded 2025-08-15)

38 games, ids `ac00`–`ac37`, dataset `upload-2025-08-15`, two videos. This tree is a copy of `chain/sp`, run on the
two videos together and kept as it ran (its paths point at `/tmp/claude-0/sr/`, a cloud session's scratchpad). It
adds no frame image or video to the repo. Ids follow `chain/sp`'s two-letter scheme: this set is `ac`.

## Inputs

syakegohan is the LEFT board (p1) throughout. The opponent's nameplate reads あめみや　はいしん, the name the earlier
あめみや datasets use.

| ids | video | WIN counters at the end (syakegohan first) | length |
|---|---|---|---|
| ac00–ac16 | `0XVKmFHsMkw` (Part1) | 12-5 | 30:28 |
| ac17–ac37 | `tJsRm74phxQ` (Part2) | 15-6 | 27:58 |

syakegohan 27-11 over the 38 games. Part1's replay stops at 12-5 (the WIN screen of that game ends the video), so its
set is not complete here; Part2 is a whole set.

- The videos: native 854x480, リプレイVer 3.5, the layout the coordinates expect. **No rescale.**
- Games: `seg/` was run per video (`seg/v_<video>/`); `seg` never closes a video's last game, so `mkgames_sr.py`
  appends it (start = previous end + 1.2 s, end = the video's end less 0.2 s) and asserts each game moves one WIN
  counter by one. Extractor A's winners agree with the counters in all 38 games.

## What differs from chain/sp

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/sr/` |
| `mkgames_sr.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `sr` |
| `corr/merge_xo.py` | five groups (`range(5)`; g4 = the PC items) |
| `corr/dedupe.py` | **new**: run after `merge_xo.py`; drops repeated proposals, settles cell conflicts, applies the NEXT recount and drops cells the corrected events already give |
| `corr/dedupe_note.txt` | what `dedupe.py` dropped and decided |
| `apply/hand_edits_sp.py` | removed: the cell edits go straight to `analysis/ppt2-syakegohan/hand-edits.csv` |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 109 flags: 47 PERFECT CLEAR banner onsets, 35 gap windows over 4 s, 9
   banner/type disagreements, 8 winner KO pieces, 5 KO-tail score jumps, 3 banners with no clear and 2 T-spins with no
   banner. `check/score/` found 37 score spots.
2. **PERFECT CLEARs.** 12 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 18 clusters
   (`corr/pcclusters.json`), and a lit-cell count of the board after each (`corr/litcount.txt`) left 6 that went to a
   frame check as group g4. All 6 were real PERFECT CLEARs (syakegohan, in ac00, ac05, ac06, ac09, ac15 and ac35) that
   the chain had logged as a clear plus a phantom second piece.
3. **Frame checks.** 67 non-PC items; `extractor/autosettle` settled 4 as no change (`corr/out/auto.json`), and the
   other 63 went to four groups (`corr/groups/g0.json`–`g3.json`) beside the 6 PC items (`g4.json`). One agent per
   group proposed corrections (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`): they
   rejected 2, amended 6 and added 2 the checker had missed.
4. **Merge.** `corr/merge_xo.py` wrote 47 event corrections; `corr/dedupe.py` dropped 7 that repeated another group's
   fix and added one (ac01 p2 478.33, a phantom single just past a group's window; the score steps put the REN peak
   at 18), leaving 41 (`corr/dedupe_note.txt`). `corr/fixwas.py` repaired one `was` (ac35 p1 1518.8, after the
   retype before it).
5. **Cells.** 10 piece counts. The checkers also proposed `max_combo` cells; the chain recomputes REN from the
   corrected events and already gives each of them, so `dedupe.py` dropped them.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted all 76 player-games' spawns with `corr/tools/nextcount.py --game` (the 4-of-5-frame
template from `chain/sp`), and `corr/nc_compare.py` compared them with the table after the cell edits: 69 agree, 4
differ by one, 2 are lost reads and 1 differs by more (ac13 p2, a read that starts late; table kept). Three piece
cells were set from clean recounts where the readers disagreed: ac01 p1 182, ac01 p2 183 and ac25 p1 253.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty).
