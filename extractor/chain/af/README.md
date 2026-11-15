# chain/af: syakegohan vs ドラえもん, 15先 Part1-2 (uploaded 2025-07-26)

37 games, ids `af00`–`af36`, dataset `upload-2025-07-26`, two videos. This tree is a copy of `chain/sp`, run on the
two videos together and kept as it ran (its paths point at `/tmp/claude-0/af/`, a cloud session's scratchpad). It
adds no frame image or video to the repo. Ids follow `chain/sp`'s two-letter scheme: this set is `af`.

## Inputs

syakegohan is the LEFT board (p1) throughout; the opponent is ドラえもん.

| ids | video | WIN counters at the end (syakegohan first) | length |
|---|---|---|---|
| af00–af17 | `nRLujpF_i5Y` (Part1) | 13-5 | 20:03 |
| af18–af36 | `_LqGJguhTEo` (Part2) | 15-4 | 21:28 |

syakegohan 28-9 over the 37 games. Part1's replay stops at 13-5 (the set is not finished in the video); Part2 is a
whole set.

- The videos: native 854x480, リプレイVer 3.5, the layout the coordinates expect. **No rescale.**
- Games: `seg/` was run per video (`seg/v_<video>/`); `seg` never closes a video's last game, so `mkgames_af.py`
  appends it (start = previous end + 1.2 s, end = the video's end less 0.2 s) and asserts each game moves one WIN
  counter by one. The chain's winners agree with the counters in all 37 games.

## What differs from chain/sp

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/af/` |
| `mkgames_af.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `af` |
| `corr/merge_xo.py` | three groups (`range(3)`; g2 = the PC items) |
| `corr/dedupe.py` | **new** (as in `chain/ss`): run after `merge_xo.py`; drops repeated proposals (asserting they agree), applies the NEXT recount decision (`NC`) and drops cells the corrected events already give |
| `corr/dedupe_note.txt` | what `dedupe.py` dropped and decided |
| `apply/hand_edits_sp.py` | removed: the cell edits go straight to `analysis/ppt2-syakegohan/hand-edits.csv` |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 91 flags: 58 PERFECT CLEAR banner onsets, 11 winner KO pieces, 8
   banner/type disagreements, 6 KO-tail score jumps, 5 T-spins with no banner and 3 gap windows over 4 s.
   `check/score/` found 26 score spots, 3 of them taken as frame-check items.
2. **PERFECT CLEARs.** 17 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 18 clusters
   (`corr/pcclusters.json`), and a lit-cell count of the board after each (`corr/litcount.txt`) left 11 that went to
   a frame check as group g2. All 11 were real PERFECT CLEARs (7 syakegohan, 4 ドラえもん) that the chain had logged
   as a plain clear; each was retyped.
3. **Frame checks.** 36 non-PC items; `extractor/autosettle` settled 1 as no change (`corr/out/auto.json`), and the
   other 35 went to two groups (`corr/groups/g0.json`, `g1.json`) beside the 11 PC items (`g2.json`). One agent per
   group proposed corrections (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`): they
   rejected none and amended 2 (af02 p2's PC clear lines).
4. **Merge.** `corr/merge_xo.py` wrote 39 event corrections; `corr/dedupe.py` dropped 4 that repeated another group's
   fix (the af15 p1 and af22 p1 PCs, proposed by g0 and g2 alike), leaving 35 (`corr/dedupe_note.txt`).
   `corr/fixwas.py` found no `was` to repair.
5. **Cells.** Four, all piece counts: af04 p1 67 -> 65 (two phantom locks in a gap window), af29 p2 73 -> 71 (two
   phantom spawns during an online stall), af35 p1 82 -> 83 (a piece locked on the KO frame) and af29 p1 83 -> 78
   (the frame check removed one phantom lock in the same stall; the NEXT recount set the rest, below). The checkers
   also proposed `max_combo` and `max_b2b` cells; the chain recomputes them from the corrected events and already
   gives each one, so `dedupe.py` dropped them.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted all 74 player-games' spawns with `corr/tools/nextcount.py --game` (the 4-of-5-frame
template from `chain/sp`), and `corr/nc_compare.py` compared them with the table. af29 p1 read 78 cleanly (11 whole
bags, no unknown stretch, every spawn matched to a corrected lock event) against 82, and its cell was set to 78. After
that: 64 agree, 4 differ by one and 6 are lost reads (af10, af12, af13, af15, af17 and af20, all p2). No other piece
count was changed from it.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty).
