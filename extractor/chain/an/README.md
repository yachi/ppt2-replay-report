# chain/an: syakegohan vs uyeshota, 15先 Part1-2 (uploaded 2025-06-29)

43 games, ids `an00`–`an42`, dataset `upload-2025-06-29` (the second set on that date, after `chain/ah`'s vs
ドラえもん), two videos. This tree is a copy of `chain/ai`, run on the two videos together and kept as it ran (its
paths point at `/tmp/claude-0/an/`, a cloud session's scratchpad). It adds no frame image or video to the repo.

## Inputs

syakegohan is the LEFT board (p1) throughout; the opponent is uyeshota.

| ids | video | WIN counters at the end (syakegohan first) |
|---|---|---|
| an00–an16 | `K4vvl7e2Ea4` (Part1) | 11-6 |
| an17–an42 | `kADGVeU2Miw` (Part2) | 15-11 |

syakegohan 26-17 over the 43 games.

- Part1 is NOT a whole set: the upload ends on the replay menu at マッチポイント with the counters at 11-6, so that
  set has no recorded finish. Part2 is a whole set, 15-11.
- The videos: リプレイVer 3.5, fetched at 720p and scaled to 854x480 before the chain ran (no layout rescale).
- Games: `seg/` was run per video (`seg/v_<video>/`); `seg` never closes a video's last game, so `mkgames_an.py`
  appends it and asserts each game moves one WIN counter by one.

## What differs from chain/ai

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/an/` |
| `mkgames_an.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `an` |
| `corr/dedupe.py` | as in `chain/am`, no NEXT recount decision (`NC = {}`) |
| `corr/dedupe_note.txt` | what `dedupe.py` dropped and decided |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 94 flags: 70 PERFECT CLEAR banner onsets, 8 winner KO pieces, 5 T-spins
   with no banner, 4 banner/type disagreements, 4 KO-tail score jumps, 2 gap windows over 4 s and 1 banner with no
   clear. `check/score/` found 39 score spots.
2. **PERFECT CLEARs.** 24 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 27 clusters
   (`corr/pcclusters.json`), checked with a lit-cell count of the board after each (`corr/litcount.txt`); 10 left
   in doubt went to a frame check. The set holds 34 PCs (syakegohan 19, uyeshota 15).
3. **Frame checks.** `extractor/autosettle` settled 3 items as no change (`corr/out/auto.json`); the other items went
   to groups g0 (15 items), g1 (12) and g2 (10). One agent per group proposed corrections (`corr/out/b*.json`) and
   another tried to refute each (`corr/out/v*.json`): they kept every one and amended two `was` values.
4. **Merge.** `corr/merge_xo.py` wrote the event corrections and `corr/dedupe.py` dropped 6 an30/an31 retypes that
   two groups had both proposed, leaving 36 (`corr/dedupe_note.txt`).
5. **Cells.** One: an04 p1 pieces 120 -> 121 (an L locked on the KO frame). A max_combo cell for an03 p1 was dropped
   because the chain recomputes REN from the corrected events and already gives it.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted all 86 player-games' spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/hand_edits.csv` is the cells without a header): 73 agree,
9 differ by one, 3 are lost reads and one reads 10 more: an19 p1, 158 against 148, where the corrected events also
number 148 and the frame check found the gaps were the player stalling. No piece count was changed from the recount.

## Known gaps

- Part1's set is unfinished in the upload (above).
- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty).
