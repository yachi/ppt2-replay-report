# chain/am: syakegohan vs いわしせいじん, 15先 Part1-2 (uploaded 2025-07-07)

45 games, ids `am00`–`am44`, dataset `upload-2025-07-07`, two videos. This tree is a copy of `chain/ai`, run on the
two videos together and kept as it ran (its paths point at `/tmp/claude-0/am/`, a cloud session's scratchpad). It
adds no frame image or video to the repo. Ids follow `chain/sp`'s two-letter scheme: this set is `am`.

## Inputs

syakegohan is the LEFT board (p1) throughout; the opponent is いわしせいじん.

| ids | video | WIN counters at the end (syakegohan first) |
|---|---|---|
| am00–am21 | `6qGeb6Kw7DQ` (Part1) | 15-7 |
| am22–am44 | `0E9wY0VUEHo` (Part2) | 15-8 |

syakegohan 30-15 over the 45 games.

- The videos: リプレイVer 3.5, the layout the coordinates expect. Both were fetched at 720p and scaled to 854x480
  before the chain ran (no layout rescale).
- Games: `seg/` was run per video (`seg/v_<video>/`); `seg` never closes a video's last game, so `mkgames_am.py`
  appends it and asserts each game moves one WIN counter by one.

## What differs from chain/ai

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/am/` |
| `mkgames_am.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `am` |
| `corr/dedupe.py` | as in `chain/al` (its two extra rules; the comments name the al games that needed them), no NEXT recount decision (`NC = {}`) |
| `corr/dedupe_note.txt` | what `dedupe.py` dropped and decided |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 87 flags: 51 PERFECT CLEAR banner onsets, 17 winner KO pieces, 5 T-spins
   with no banner, 5 KO-tail score jumps, 3 banners with no clear, 3 banner/type disagreements, 2 gap windows over
   4 s and 1 bad bag. `check/score/` found 34 score spots.
2. **PERFECT CLEARs.** 19 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 16 clusters
   (`corr/pcclusters.json`), checked with a lit-cell count of the board after each (`corr/litcount.txt`); those left
   in doubt went to a frame check as group g3 (8 items). The set holds 28 PCs (syakegohan 18, いわしせいじん 10).
3. **Frame checks.** `extractor/autosettle` settled 4 items as no change (`corr/out/auto.json`); the other items went
   to groups g0 (13 items), g1 (12) and g2 (13) beside the PC items (g3, 8). One agent per group proposed
   corrections (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`): they kept every one, and
   g1's added a cell its reader missed (am26 p2 pieces 191 -> 192).
4. **Merge.** `corr/merge_xo.py` wrote the event corrections and `corr/dedupe.py` dropped 2 am38 retypes that sat
   inside g3's window, leaving 27 (`corr/dedupe_note.txt`).
5. **Cells.** Five, all piece counts: am12 p1 92 -> 93 (a T locked just before the KO), am26 p2 191 -> 192, am27 p1
   77 -> 75 and am27 p2 70 -> 67 (phantom locks), and am40 p2 143 -> 140 (three phantom locks).

## NEXT-queue recount

`corr/drive_nc.sh` re-counted all 90 player-games' spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/hand_edits.csv` is the cells without a header): 79 agree,
6 differ by one, 4 are lost reads and one reads 2 fewer: am00 p2, 248 against 250, where the corrected events also
number 250. No piece count was changed from the recount.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty).
