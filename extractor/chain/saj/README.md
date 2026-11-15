# chain/saj: syakegohan vs あてん, 15先 Part1-2 (uploaded 2025-07-13)

35 games, ids `aj00`–`aj34`, dataset `upload-2025-07-13`, two videos. This tree is a copy of `chain/ai`, run on the
two videos together and kept as it ran (its paths point at `/tmp/claude-0/aj/`, a cloud session's scratchpad). It
adds no frame image or video to the repo. Ids follow `chain/sp`'s two-letter scheme: this set is `aj`. The tree is archived as `chain/saj` because `chain/aj` already holds
ゆうくん's stream of 2026-11-06 (ids `z000`–`z057`); the run itself used `aj` throughout.

## Inputs

syakegohan is the LEFT board (p1) throughout; the opponent is あてん.

| ids | video | WIN counters at the end (syakegohan first) |
|---|---|---|
| aj00–aj15 | `EVBb-RPvUf0` (Part1) | 15-1 |
| aj16–aj34 | `rfpPRlFVl24` (Part2) | 15-4 |

syakegohan 30-5 over the 35 games; both videos hold a whole set.

- The videos: リプレイVer 3.5, the layout the coordinates expect. Both were fetched at 720p and scaled to 854x480
  before the chain ran (no layout rescale).
- Games: `seg/` was run per video (`seg/v_<video>/`); `seg` never closes a video's last game, so `mkgames_aj.py`
  appends it and asserts each game moves one WIN counter by one.

## What differs from chain/ai

| file | change |
|---|---|
| all | paths rewritten to `/tmp/claude-0/aj/` |
| `mkgames_aj.py` | this run's games (above) |
| `drive_qh1.sh`, `check/score/scoresum.py` | point at `aj` |
| `corr/dedupe.py` | as in `chain/ai` with its ai-specific drops removed and no NEXT recount decision (`NC = {}`) |
| `corr/dedupe_note.txt` | what `dedupe.py` dropped and decided |
| `witnessed.json` | `[]`, beside `games.json` (not in `w/`) |

## Corrections

All event corrections and hand edits are in `analysis/ppt2-syakegohan/` (appended after the earlier datasets').

1. **Flags.** `apply/checks_xo.py` raised 60 flags: 38 PERFECT CLEAR banner onsets, 12 winner KO pieces, 3
   banner/type disagreements, 3 KO-tail score jumps, 2 bad bags, 1 APP outlier and 1 T-spin with no banner.
   `check/score/` found 18 score spots.
2. **PERFECT CLEARs.** 10 onsets carry `pcmap`'s "PC = clear at" (`corr/pcaccepted.json`); the rest make 17 clusters
   (`corr/pcclusters.json`), checked with a lit-cell count of the board after each (`corr/litcount.txt`); those left
   in doubt went to a frame check as group g2 (4 items). The set holds 14 PCs in all (syakegohan 12, あてん 2).
3. **Frame checks.** `extractor/autosettle` settled 8 items as no change (`corr/out/auto.json`); the other items went
   to groups g0 (6 items) and g1 (9) beside the PC items (g2, 4). One agent per group proposed corrections
   (`corr/out/b*.json`) and another tried to refute each (`corr/out/v*.json`): they rejected, amended and added
   nothing.
4. **Merge.** `corr/merge_xo.py` wrote the event corrections and `corr/dedupe.py` dropped 3, leaving 14
   (`corr/dedupe_note.txt`): g1 and g2 both retyped the aj20 p1 PERFECT CLEAR and the two duplicate clears after it.
   Every g2 fix has the same shape: the chain logged the clear but not as a PC, then logged one or two phantom
   clears on the empty board after it.
5. **Cells.** Three, all piece counts: aj09 p1 198 -> 200 (two opening locks the chain missed), aj18 p2 56 -> 53
   (three phantom locks under the TETRIS flash) and aj24 p1 135 -> 136 (a KO-frame lock).

## NEXT-queue recount

`corr/drive_nc.sh` re-counted all 70 player-games' spawns with `corr/tools/nextcount.py --game`, and
`corr/nc_compare.py` compared them with the table (`corr/hand_edits.csv` is the cells without a header): 47 agree,
5 differ by one and 18 are lost reads (bad bags or long unknown stretches). The lost reads sit mostly on あてん's side
in Part1, under heavy garbage, where attack effects cover the NEXT queue; they undercount. No piece count was changed
from the recount.

## Known gaps

- garbage-row counts (`gc`) inside rebuilt windows were read from the stack height, not counted row by row.
- No opener labels (the `opener` column is empty).
