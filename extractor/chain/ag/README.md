# chain/ag: syakegohan vs ドラえもん, 15先 Part1-2 (uploaded 2025-07-17)

41 games, ids `ag00`–`ag40`, dataset `upload-2025-07-17`, two videos. This tree is a copy of `chain/sp`, run on the
two videos together and kept as it ran (its paths point at `/tmp/claude-0/ag/`, a cloud session's scratchpad). It
adds no frame image or video to the repo. Ids follow `chain/sp`'s two-letter scheme: this set is `ag`.

## Inputs

syakegohan is the LEFT board (p1) throughout; the opponent is ドラえもん.

| ids | video | WIN counters at the end (syakegohan first) | length |
|---|---|---|---|
| ag00–ag20 | `nYKv827YLg8` (Part1) | 15-6 | 21:09 |
| ag21–ag40 | `op-Tc_IVY8w` (Part2) | 15-5 | 21:33 |

syakegohan 30-11 over the 41 games; both videos hold a whole set.

- The videos: native 854x480, リプレイVer 3.5, the layout the coordinates expect. **No rescale.**
- Games: `seg/` was run per video (`seg/v_<video>/`); `seg` never closes a video's last game, so `mkgames_ag.py`
  appends it (start = previous end + 1.2 s, end = the video's end less 0.2 s) and asserts each game moves one WIN
  counter by one. The chain's winners agree with the counters in all 41 games.

## What differs from chain/sp

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/ag/` |
| `mkgames_ag.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `ag` |
| `corr/merge_xo.py` | three groups (`range(3)`; g2 = the PC items) |
| `corr/dedupe.py` | as in `chain/ae`: run after `merge_xo.py`; drops repeated proposals (asserting they agree), joins overlapping replace windows, applies the NEXT recount decision (`NC`) and drops cells the corrected events already give |
| `corr/dedupe_note.txt` | what `dedupe.py` dropped and decided |
| `apply/hand_edits_sp.py` | removed: the cell edits go straight to `analysis/ppt2-syakegohan/hand-edits.csv` |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 67 flags: 39 PERFECT CLEAR banner onsets, 13 winner KO pieces, 5
   banner/type disagreements, 4 KO-tail score jumps, 3 gap windows over 4 s, 2 T-spins with no banner and 1 banner
   with no clear. `check/score/` found 41 score spots.
2. **PERFECT CLEARs.** 8 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 15 clusters
   (`corr/pcclusters.json`), and a lit-cell count of the board after each (`corr/litcount.txt`) left 10 that went to
   a frame check as group g2. All 10 were real PERFECT CLEARs that the chain had logged as a plain clear; each was
   retyped. The set holds 18 PCs in all (syakegohan 14, ドラえもん 4).
3. **Frame checks.** `extractor/autosettle` settled 3 items as no change (`corr/out/auto.json`); the other non-PC
   items went to two groups (`corr/groups/g0.json`, 14 items; `g1.json`, 15) beside the 10 PC items (`g2.json`). One
   agent per group proposed corrections (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`):
   they rejected none and amended none. g0's refuter gave no verdict for e7 (ag16 p2's replace window); its own
   evidence on that window covers it, and a keep verdict was added to `v0.json` by hand.
4. **Merge.** `corr/merge_xo.py` wrote 39 event corrections; `corr/dedupe.py` dropped 9 that repeated another group's
   fix (four PC retypes proposed by g0 or g1 and by g2, and the overlapping ag16 p1 windows, joined into one over
   913.8–929.3 s), leaving 30 (`corr/dedupe_note.txt`).
5. **Cells.** Six, all piece counts: ag08 p1 103 -> 104, ag16 p2 110 -> 108, ag21 p1 97 -> 98, ag29 p2 203 -> 204,
   ag31 p1 38 -> 39 (KO-frame and phantom locks) and ag16 p1 131 -> 122 (the NEXT recount, below). The checkers also
   proposed two `max_combo` cells (ag16 p2, ag38 p1); the chain recomputes REN from the corrected events and already
   gives each one, so `dedupe.py` dropped them.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted all 82 player-games' spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table. ag16 p1 read 122 cleanly (17 whole bags, no unknown stretch) against
128 after the frame check, and the corrected events also number 122 (extractor B had counted spawns through the
stalled REN stretch), so its cell was set to 122. After that: 71 agree, 9 differ by one, 1 is a lost read (ag08 p2) and
ag21 p1 reads 96 against 98, the two pieces locked on the KO frame that the recount does not see; the table keeps 98.
No other piece count was changed from it.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty).
