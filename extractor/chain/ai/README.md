# chain/ai: syakegohan vs ドラえもん, 15先 Part1-2 (uploaded 2025-06-28)

41 games, ids `ai00`–`ai40`, dataset `upload-2025-06-28`, two videos. This tree is a copy of `chain/sp`, run on the
two videos together and kept as it ran (its paths point at `/tmp/claude-0/ai/`, a cloud session's scratchpad). It
adds no frame image or video to the repo. Ids follow `chain/sp`'s two-letter scheme: this set is `ai`.

## Inputs

syakegohan is the LEFT board (p1) throughout; the opponent is ドラえもん.

| ids | video | WIN counters at the end (syakegohan first) |
|---|---|---|
| ai00–ai24 | `FQWOu2cQH10` (Part1) | 15-10 |
| ai25–ai40 | `75c1W0ZmJIs` (Part2) | 15-1 |

syakegohan 30-11 over the 41 games; both videos hold a whole set.

- The videos: リプレイVer 3.5, the layout the coordinates expect. Both were fetched at 720p and scaled to 854x480
  before the chain ran (no layout rescale).
- Games: `seg/` was run per video (`seg/v_<video>/`); `seg` never closes a video's last game, so `mkgames_ai.py`
  appends it and asserts each game moves one WIN counter by one.

## What differs from chain/sp


| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/ai/` |
| `mkgames_ai.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `ai` |
| `corr/merge_xo.py` | three groups (`range(3)`; g2 = the PC items) |
| `corr/dedupe.py` | as in `chain/ah`, with a missing `pc` read as 0 when two proposals are compared, and two g2 retypes at ai28 p1 dropped where g1 and g2 disagreed (below); applies the NEXT recount decision (`NC`) and drops cells the corrected events already give |
| `corr/dedupe_note.txt` | what `dedupe.py` dropped and decided |
| `apply/hand_edits_sp.py` | removed: the cell edits go straight to `analysis/ppt2-syakegohan/hand-edits.csv` |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 86 flags: 53 PERFECT CLEAR banner onsets, 12 gap windows, 8 banner/type
   disagreements, 8 winner KO pieces, 4 KO-tail score jumps and 1 T-spin with no banner. `check/score/` found 29
   score spots.
2. **PERFECT CLEARs.** 16 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 22 clusters
   (`corr/pcclusters.json`), checked with a lit-cell count of the board after each (`corr/litcount.txt`); those left
   in doubt went to a frame check as group g2. The set holds 25 PCs in all (syakegohan 20, ドラえもん 5).
3. **Frame checks.** `extractor/autosettle` settled 4 items as no change (`corr/out/auto.json`); the other items went
   to groups g0 (17 items) and g1 (19) beside the PC items (g2, 9). One agent per group proposed corrections
   (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`): they rejected none, amended six (the
   ai14 PC is a TRIPLE, the ai19 windows' bounds, two more ai28 p2 duplicates, ai28 p2 pieces 218) and added two
   missed items (an ai19 p1 false BREAK, ai40 p1 pieces 72).
   - `corr/out/v0.json` as written skipped one item and numbered the rest one short; the original is kept as
     `v0.orig.json`. The refs were renumbered (`ref_as_written` keeps what was written) and two verdicts were added by
     hand: keep e3 (ai14 913.87 a T-spin double, banner and a +3768 score step) and keep c6 (ai19 p1 max_combo 20, the
     same cell the refuter's own c5 covers).
4. **Merge.** `corr/merge_xo.py` wrote the event corrections and `corr/dedupe.py` dropped 7, leaving 33
   (`corr/dedupe_note.txt`): three repeated proposals, two g2 retypes inside g0's ai14 window, and two g2 retypes at
   ai28 p1 241.03/241.93. There g1 and g2 disagreed on which lock made the PERFECT CLEAR; the frames show the Z from
   hold making it at 241.90 with the I still in NEXT, which is g1's reading.
5. **Cells.** Eight, all piece counts: ai01 p1 119 -> 118, ai01 p2 109 -> 108, ai28 p1 231 -> 228, ai28 p2 225 -> 218,
   ai40 p1 81 -> 72, ai40 p2 76 -> 74 (KO-frame and phantom locks) and ai19 p1 169 -> 159, ai19 p2 163 -> 153 (the
   NEXT recount, below). The checkers also proposed seven `max_combo` cells; the chain recomputes REN from the
   corrected events and already gives each one, so `dedupe.py` dropped them.

## NEXT-queue recount

`corr/drive_nc.sh` re-counted all 82 player-games' spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/hand_edits.csv` is the cells without a header). ai19 p1 read
159 (23 whole bags, 161 shifts less the first hold and an unmatched last shift) and ai19 p2 153 (22 whole bags, 154
shifts less the first hold), and the corrected events number 159 and 153 with every shift matched and no event
unmatched, so both cells were set from the recount; the checkers' 166 and 162 had counted through the long REN
stretch the replace windows rebuilt. After that: 69 agree, 12 differ by one, 1 is a lost read. No other piece count
was changed from it.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty).
